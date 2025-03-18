import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from utils import save_offline_page

class OfflinePageDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Offline Page Downloader')
        self.setGeometry(100, 100, 400, 200)

        # Main layout
        layout = QVBoxLayout()

        # URL input
        self.url_entry = QLineEdit(self)
        self.url_entry.setPlaceholderText("Enter URL")
        layout.addWidget(self.url_entry)

        # Output filename input
        self.filename_entry = QLineEdit(self)
        self.filename_entry.setPlaceholderText("Enter output filename")
        layout.addWidget(self.filename_entry)

        # Download button
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.on_download_clicked)
        layout.addWidget(self.download_button)

        # Choose folder button
        self.folder_button = QPushButton('Choose Download Folder', self)
        self.folder_button.clicked.connect(self.on_folder_clicked)
        layout.addWidget(self.folder_button)

        # Show folder button
        self.show_folder_button = QPushButton('Show Download Folder', self)
        self.show_folder_button.clicked.connect(self.on_show_folder_clicked)
        layout.addWidget(self.show_folder_button)

        # Set layout
        self.setLayout(layout)

        # Default download folder
        self.download_folder = os.path.expanduser("~/Downloads")

    def on_download_clicked(self):
        url = self.url_entry.text()
        output_filename = self.filename_entry.text()

        if url and output_filename:
            output_path = os.path.join(self.download_folder, output_filename)
            save_offline_page(url, output_path)
            QMessageBox.information(self, 'Success', f'Page saved as {output_path}')
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both URL and output filename.')

    def on_folder_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Download Folder')
        if folder:
            self.download_folder = folder

    def on_show_folder_clicked(self):
        if os.path.exists(self.download_folder):
            os.system(f"xdg-open {self.download_folder}")
        else:
            QMessageBox.warning(self, 'Error', 'Download folder does not exist.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OfflinePageDownloader()
    window.show()
    sys.exit(app.exec_())