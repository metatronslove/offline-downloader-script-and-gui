import sys
from utils import save_offline_page

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python3 offline_downloader.py <URL> <output_filename>")
		sys.exit(1)

	url = sys.argv[1]
	output_filename = sys.argv[2]
	save_offline_page(url, output_filename)