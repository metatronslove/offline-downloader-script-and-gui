import os
import re
import requests
from bs4 import BeautifulSoup
import base64
from urllib.parse import urljoin, urlparse
from tqdm import tqdm  # Terminal progress bar için

# Regex for CSS url() patterns
CSS_URL_PATTERN = re.compile(r'url\(\s*[\'"]?(.*?)[\'"]?\s*\)', re.IGNORECASE)

def download_resource(url, base_url):
	"""Download resource and return (content, mime_type)"""
	try:
		if url.startswith("//"):
			url = f"{urlparse(base_url).scheme}:{url}"
		elif not url.startswith(("http://", "https://")):
			url = urljoin(base_url, url)

		response = requests.get(url, stream=True)
		response.raise_for_status()

		# MIME Type ve Content-Length
		mime_type = response.headers.get('Content-Type', '').split(';')[0].strip()
		total_size = int(response.headers.get('content-length', 0))

		content = bytearray()
		for data in response.iter_content(chunk_size=1024):
			content.extend(data)

		return bytes(content), mime_type
	except Exception as e:
		print(f"Error downloading {url}: {e}")
		return None, None
def replace_css_urls(css_text, base_url):
	"""Replace all url() references in CSS with Base64 data URIs"""
	def replace_url(match):
		resource_url = match.group(1).strip()
		content, mime_type = download_resource(resource_url, base_url)

		if content and mime_type:
			b64 = base64.b64encode(content).decode('utf-8')
			return f"url(data:{mime_type};base64,{b64})"
		return match.group(0)

	return CSS_URL_PATTERN.sub(replace_url, css_text)

def process_css(soup, base_url):
	# Process external CSS files
	for style in soup.find_all('link', rel='stylesheet'):
		css_url = style['href']
		css_content, _ = download_resource(css_url, base_url)

		if css_content:
			# Get CSS base URL
			parsed_css_url = urlparse(css_url)
			css_base = f"{parsed_css_url.scheme}://{parsed_css_url.netloc}{os.path.dirname(parsed_css_url.path)}/"

			# Decode CSS content and replace URLs
			css_text = css_content.decode('utf-8')
			updated_css = replace_css_urls(css_text, css_base)

			# Replace original CSS link
			style_tag = soup.new_tag('style', id=f"{os.path.splitext(os.path.basename(css_url))[0]}_css")
			style_tag.string = updated_css
			style.replace_with(style_tag)

	# Process inline <style> tags
	for style in soup.find_all('style'):
		if style.string:
			updated_css = replace_css_urls(style.string, base_url)
			style.string = updated_css

def process_js(soup, base_url):
	for script in soup.find_all('script', src=True):
		js_url = script['src']
		js_content, _ = download_resource(js_url, base_url)

		if js_content:
			script_tag = soup.new_tag('script', id=f"{os.path.splitext(os.path.basename(js_url))[0]}_js")
			script_tag.string = js_content.decode('utf-8')
			script.replace_with(script_tag)

def process_images(soup, base_url):
	for img in soup.find_all('img', src=True):
		img_url = img['src']
		content, mime_type = download_resource(img_url, base_url)

		if content:
			if mime_type == 'image/svg+xml':
				# Replace <img> with inline SVG
				svg_content = content.decode('utf-8')
				svg_soup = BeautifulSoup(svg_content, 'html.parser')
				img.replace_with(svg_soup.svg)
			else:
				# Convert other images to Base64
				b64 = base64.b64encode(content).decode('utf-8')
				img['src'] = f"data:{mime_type};base64,{b64}"

def process_media(soup, base_url):
	for media in soup.find_all(['audio', 'video', 'source'], src=True):
		media_url = media['src']
		content, mime_type = download_resource(media_url, base_url)

		if content and mime_type:
			b64 = base64.b64encode(content).decode('utf-8')
			media['src'] = f"data:{mime_type};base64,{b64}"

def process_assets(soup, base_url, progress_callback=None):
	total_steps = 5  # HTML, CSS, JS, Images, Media
	current_step = 0

	# CSS Processing
	if progress_callback:
		progress_callback(int(current_step/total_steps*100), "Processing CSS...")
	process_css(soup, base_url)

	# JS Processing
	current_step += 1
	if progress_callback:
		progress_callback(int(current_step/total_steps*100), "Processing JS...")
	process_js(soup, base_url)

	# Images Processing
	current_step += 1
	if progress_callback:
		progress_callback(int(current_step/total_steps*100), "Processing Images...")
	process_images(soup, base_url)

	# Media Processing
	current_step += 1
	if progress_callback:
		progress_callback(int(current_step/total_steps*100), "Processing Media...")
	process_media(soup, base_url)

def save_offline_page(url, output_filename, progress_callback=None):
	try:
		# Terminal progress bar
		terminal_progress = tqdm(
			total=100,
			desc=f"Processing {os.path.basename(output_filename)}",
			unit="%",
			ncols=75
		)

		def combined_progress(percent, msg=None):
			terminal_progress.update(percent - terminal_progress.n)
			if progress_callback:
				progress_callback(percent, msg)
			if msg:
				terminal_progress.set_postfix_str(msg)

		# Ana işlemler
		combined_progress(0, "Downloading HTML...")
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')

		combined_progress(20, "Processing assets...")
		process_assets(soup, url, lambda p, msg: combined_progress(20 + int(p*0.6), msg))

		combined_progress(90, "Saving file...")
		with open(output_filename, 'w', encoding='utf-8') as f:
			f.write(str(soup))

		combined_progress(100, "Completed!")
		terminal_progress.close()

	except Exception as e:
		print(f"\nError: {e}")
		if progress_callback:
			progress_callback(-1, f"Error: {e}")  # Hata durumu