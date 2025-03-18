import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
import os
from utils import save_offline_page

class OfflinePageDownloader(Gtk.Window):
    def __init__(self):
        super().__init__(title="Offline Page Downloader")
        self.set_default_size(400, 200)

        # Main vertical box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.main_box)

        # URL entry
        self.url_entry = Gtk.Entry(placeholder_text="Enter URL")
        self.main_box.append(self.url_entry)

        # Output filename entry
        self.filename_entry = Gtk.Entry(placeholder_text="Enter output filename")
        self.main_box.append(self.filename_entry)

        # Download button
        self.download_button = Gtk.Button(label="Download")
        self.download_button.connect("clicked", self.on_download_clicked)
        self.main_box.append(self.download_button)

    def on_download_clicked(self, button):
        url = self.url_entry.get_text()
        output_filename = self.filename_entry.get_text()

        if url and output_filename:
            save_offline_page(url, output_filename)
            print(f"Downloaded: {output_filename}")
        else:
            print("Please enter both URL and output filename.")

# Run the application
app = Gtk.Application(application_id='org.example.OfflinePageDownloader')
app.connect('activate', lambda app: OfflinePageDownloader().show())
app.run(None)