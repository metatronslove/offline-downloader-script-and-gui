import os
import requests
from bs4 import BeautifulSoup
import base64
from urllib.parse import urljoin, urlparse

def download_and_convert_to_base64(url, base_url):
    try:
        # Handle protocol-relative URLs (e.g., "//example.com/file.png")
        if url.startswith("//"):
            url = f"{urlparse(base_url).scheme}:{url}"
        # Handle root-relative and parent-relative URLs
        elif not url.startswith(("http://", "https://")):
            url = urljoin(base_url, url)

        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def process_css(soup, base_url):
    for style in soup.find_all('link', rel='stylesheet'):
        css_url = style['href']
        base64_css = download_and_convert_to_base64(css_url, base_url)
        if base64_css:
            style_tag = soup.new_tag('style', id=f"{os.path.splitext(os.path.basename(css_url))[0]}_css")
            style_tag.string = base64_css
            style.replace_with(style_tag)

def process_js(soup, base_url):
    for script in soup.find_all('script', src=True):
        js_url = script['src']
        base64_js = download_and_convert_to_base64(js_url, base_url)
        if base64_js:
            script_tag = soup.new_tag('script', id=f"{os.path.splitext(os.path.basename(js_url))[0]}_js")
            script_tag.string = base64_js
            script.replace_with(script_tag)

def process_images(soup, base_url):
    for img in soup.find_all('img', src=True):
        img_url = img['src']
        base64_img = download_and_convert_to_base64(img_url, base_url)
        if base64_img:
            img['src'] = f"data:image/{os.path.splitext(img_url)[1][1:]};base64,{base64_img}"

def process_media(soup, base_url):
    for media in soup.find_all(['audio', 'video'], src=True):
        media_url = media['src']
        base64_media = download_and_convert_to_base64(media_url, base_url)
        if base64_media:
            media['src'] = f"data:{media.name}/{os.path.splitext(media_url)[1][1:]};base64,{base64_media}"

def process_svg(soup, base_url):
    for svg in soup.find_all('img', src=True):
        if svg['src'].endswith('.svg'):
            svg_url = svg['src']
            base64_svg = download_and_convert_to_base64(svg_url, base_url)
            if base64_svg:
                svg['src'] = f"data:image/svg+xml;base64,{base64_svg}"

def save_offline_page(url, output_filename):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Calculate base_url including the path
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        if not base_url.endswith('/'):
            base_url = os.path.dirname(base_url) + '/'

        # Process CSS, JS, images, media, and SVG
        process_css(soup, base_url)
        process_js(soup, base_url)
        process_images(soup, base_url)
        process_media(soup, base_url)
        process_svg(soup, base_url)

        # Save the HTML content
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Page saved as {output_filename}")
    except Exception as e:
        print(f"Error: {e}")