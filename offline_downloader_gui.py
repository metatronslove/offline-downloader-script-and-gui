#!/usr/bin/env python3
import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QListWidget, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from utils import save_offline_page

class DownloadThread(QThread):
    progress_updated = pyqtSignal(int, int)  # row_index, percent
    status_updated = pyqtSignal(int, str)    # row_index, status
    finished = pyqtSignal(int)               # row_index

    def __init__(self, row_index, url, filename, folder):
        super().__init__()
        self.row_index = row_index
        self.url = url
        self.filename = filename
        self.folder = folder

    def run(self):
        try:
            output_path = os.path.join(self.folder, self.filename)

            def progress_handler(percent, msg):
                self.progress_updated.emit(self.row_index, percent)
                self.status_updated.emit(self.row_index, msg)

            save_offline_page(self.url, output_path, progress_handler)
            self.finished.emit(self.row_index)

        except Exception as e:
            self.status_updated.emit(self.row_index, f"Error: {str(e)}")
            self.progress_updated.emit(self.row_index, -1)

class OfflinePageDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.download_folder = os.path.expanduser("~/Downloads")
        self.download_threads = []

    def initUI(self):
        self.setWindowTitle('Offline Page Downloader')
        self.setGeometry(100, 100, 800, 400)

        # Main layout
        main_layout = QVBoxLayout()

        # URL and filename input
        input_layout = QHBoxLayout()
        self.url_entry = QLineEdit(self)
        self.url_entry.setPlaceholderText("Enter URL")
        input_layout.addWidget(self.url_entry)

        self.filename_entry = QLineEdit(self)
        self.filename_entry.setPlaceholderText("Enter output filename")
        input_layout.addWidget(self.filename_entry)

        self.add_button = QPushButton('Add to Queue', self)
        self.add_button.clicked.connect(self.add_to_queue)
        input_layout.addWidget(self.add_button)

        main_layout.addLayout(input_layout)

        # Table for download queue
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["URL", "Filename", "Progress", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        self.folder_button = QPushButton('Choose Download Folder', self)
        self.folder_button.clicked.connect(self.on_folder_clicked)
        button_layout.addWidget(self.folder_button)

        self.show_folder_button = QPushButton('Show Download Folder', self)
        self.show_folder_button.clicked.connect(self.on_show_folder_clicked)
        button_layout.addWidget(self.show_folder_button)

        main_layout.addLayout(button_layout)

        # Set layout
        self.setLayout(main_layout)

    def add_to_queue(self):
        url = self.url_entry.text()
        output_filename = self.filename_entry.text()

        if url and output_filename:
            row_index = self.table.rowCount()
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(url))
            self.table.setItem(row_index, 1, QTableWidgetItem(output_filename))

            progress_bar = QProgressBar(self)
            progress_bar.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row_index, 2, progress_bar)

            self.table.setItem(row_index, 3, QTableWidgetItem("Pending"))

            # Start download thread
            thread = DownloadThread(row_index, url, output_filename, self.download_folder)
            thread.progress_updated.connect(self.update_progress)
            thread.status_updated.connect(self.update_status)
            thread.finished.connect(self.download_finished)
            thread.start()

            self.download_threads.append(thread)
            self.url_entry.clear()
            self.filename_entry.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both URL and output filename.')

    def update_progress(self, row_index, progress):
        progress_bar = self.table.cellWidget(row_index, 2)
        progress_bar.setValue(progress)

    def update_status(self, row_index, status):
        self.table.setItem(row_index, 3, QTableWidgetItem(status))

    def download_finished(self, row_index):
        self.table.item(row_index, 3).setText("Completed")
        self.show_folder_button.setEnabled(True)

    def on_folder_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Download Folder')
        if folder:
            self.download_folder = folder

    def on_show_folder_clicked(self):
        if os.path.exists(self.download_folder):
            subprocess.run(['xdg-open', self.download_folder])
        else:
            QMessageBox.warning(self, 'Error', 'Download folder does not exist.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OfflinePageDownloader()
    window.show()
    sys.exit(app.exec_())