import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QSize, Qt
import cv2
import numpy as np

class BgRemmoveGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Background Remove")
        self.setGeometry(100, 100, 600, 400)

        self.image_label = QLabel(self)
        self.image_label.setText("No Image Selected")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_image)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.BgRemoved_image)
        
        self.download_button = QPushButton("Download Image", self)
        self.download_button.clicked.connect(self.download_BgRemoved_image)
        self.download_button.setEnabled(False)

        self.close_button = QPushButton("Close Image", self)
        self.close_button.clicked.connect(self.close_BgRemoved_window)
        self.close_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.browse_button)
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.close_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.BgRemoved_image = None

        # Set maximum and minimum sizes to initial size
        self.setMaximumSize(self.size())
        self.setMinimumSize(self.size())

    def browse_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.png)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.convert_button.setEnabled(True)

    def BgRemoved_image(self):
        from rembg import remove
        from PIL import Image

        image = Image.open(self.image_path)
        outputImage = remove(image)
        outputImage = np.array(outputImage)  # Convert PIL image to NumPy array

        cv2.imshow("Bg Removed", outputImage)
        self.BgRemoved_image = outputImage
        self.close_button.setEnabled(True)
        self.download_button.setEnabled(True)

    def close_BgRemoved_window(self):
        cv2.destroyAllWindows()
        self.close_button.setEnabled(False)
        self.download_button.setEnabled(False)
    
    def download_BgRemoved_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "Image Files (*.jpg)")
        if file_path:
            cv2.imwrite(file_path, self.BgRemoved_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BgRemmoveGUI()
    window.show()
    sys.exit(app.exec_())
