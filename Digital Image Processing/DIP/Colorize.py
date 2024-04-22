import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QSize, Qt
import cv2
import numpy as np

class ImageColorizationGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Colorization")
        self.setGeometry(100, 100, 600, 400)

        self.image_label = QLabel(self)
        self.image_label.setText("No Image Selected")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_image)

        self.colorize_button = QPushButton("Colorize", self)
        self.colorize_button.clicked.connect(self.colorize_image)
        
        self.download_button = QPushButton("Download Colorized", self)
        self.download_button.clicked.connect(self.download_colorized_image)
        self.download_button.setEnabled(False)

        self.close_button = QPushButton("Close Colorized Image", self)
        self.close_button.clicked.connect(self.close_colorized_window)
        self.close_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.browse_button)
        button_layout.addWidget(self.colorize_button)
        button_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.close_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.colorized_image = None

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
            self.colorize_button.setEnabled(True)
    def colorize_image(self):
        Prototxt = "/Users/hunaragrawal/Documents/Image Colorization Project/colorization_deploy_v2.prototxt"
        Points = "/Users/hunaragrawal/Documents/Image Colorization Project/pts_in_hull.npy"
        Model = "/Users/hunaragrawal/Documents/Image Colorization Project/colorization_release_v2.caffemodel"

        net = cv2.dnn.readNetFromCaffe(Prototxt, Model)
        pts = np.load(Points)

        class8 = net.getLayerId("class8_ab")
        conv8 = net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)

        net.getLayer(class8).blobs = [pts.astype("float32")]
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

        image = cv2.imread(self.image_path)
        if image is None:
            print("Error: Failed to load image.")
            return

        scaled = image.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

        L = cv2.split(lab)[0]
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized, 0, 1)
        colorized = (255 * colorized).astype("uint8")

        if colorized.size == 0:
            print("Error: Colorization failed.")
            return

        cv2.imshow("Colorized", colorized)
        self.close_button.setEnabled(True)
        self.download_button.setEnabled(True)

        self.colorized_image = colorized

    def close_colorized_window(self):
        cv2.destroyAllWindows()
        self.close_button.setEnabled(False)
        self.download_button.setEnabled(False)
    
    def download_colorized_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Colorized Image", "", "Image Files (*.jpg)")
        if file_path:
            cv2.imwrite(file_path, self.colorized_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageColorizationGUI()
    window.show()
    sys.exit(app.exec_())
