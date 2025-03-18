import os
import re
import requests
from bs4 import BeautifulSoup
import base64
from urllib.parse import urljoin, urlparse

# Regex for CSS url() patterns
CSS_URL_PATTERN = re.compile(r'url\(\s*[\'"]?(.*?)[\'"]?\s*\)', re.IGNORECASE)

def download_resource(url, base_url):
    """Download resource and return (content, mime_type)"""
    try:
        # Handle URL resolution
        if url.startswith("//"):
            url = f"{urlparse(base_url).scheme}:{url}"
        elif not url.startswith(("http://", "https://")):
            url = urljoin(base_url, url)

        response = requests.get(url)
        response.raise_for_status()
        mime_type = response.headers.get('Content-Type', '').split(';')[0].strip()
        return response.content, mime_type
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

def save_offline_page(url, output_filename):
    try:
        # Fetch main HTML
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        # Calculate base URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        if not base_url.endswith('/'):
            base_url = os.path.dirname(base_url) + '/'

        # Process all resources
        process_css(soup, base_url)
        process_js(soup, base_url)
        process_images(soup, base_url)
        process_media(soup, base_url)

        # Save final HTML
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"Successfully saved: {output_filename}")

    except Exception as e:
        print(f"Fatal error: {e}")

# Kullanım örneği
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        save_offline_page(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 offline_downloader.py <URL> <output.html>")