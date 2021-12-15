import sys, os, cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QCheckBox, QSpinBox, QDoubleSpinBox, QSlider, QFrame, QFileDialog,
                             QMessageBox, QHBoxLayout, QVBoxLayout, QAction)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

style_sheet = """
QLabel#ImageLabel{
color: darkgrey;
border: 2px solid #000000;
qproperty-alignment: AlignCenter
}"""


class StoriesInstagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()


    def initializeUI(self):
        self.setMinimumSize(900, 600)
        self.setWindowTitle('Stories Instagram')
        self.contrast_adjusted = False
        self.brightness_adjusted = False
        self.image_smoothing_checked = False
        self.edge_detection_checked = False
        self.points_checked = False
        self.setupWindow()
        self.setupMenu()
        self.show()


    def setupWindow(self):
        self.image_label = QLabel()
        self.image_label.setObjectName("ImageLabel")

        contrast_label = QLabel("Contrast [Range: 0.0:4.0]")
        self.contrast_spinbox = QDoubleSpinBox()
        self.contrast_spinbox.setMinimumWidth(100)
        self.contrast_spinbox.setRange(0.0, 4.0)
        self.contrast_spinbox.setValue(1.0)
        self.contrast_spinbox.setSingleStep(.10)
        self.contrast_spinbox.valueChanged.connect(self.adjustContrast)

        brightness_label = QLabel("Brightness [Range: -127:127]")
        self.brightness_spinbox = QSpinBox()
        self.brightness_spinbox.setMinimumWidth(100)
        self.brightness_spinbox.setRange(-127, 127)
        self.brightness_spinbox.setValue(0)
        self.brightness_spinbox.setSingleStep(1)
        self.brightness_spinbox.valueChanged.connect(self.adjustBrightness)

        smoothing_label = QLabel("Image Smoothing Filters")
        self.smoothing_spinbox = QSpinBox()
        self.smoothing_spinbox.setMinimumWidth(100)
        self.smoothing_spinbox.setRange(3, 21)
        self.smoothing_spinbox.setValue(3)
        self.smoothing_spinbox.setSingleStep(2)
        self.filter_2D_cb = QCheckBox("Blur")
        self.filter_2D_cb.stateChanged.connect(self.imageSmoothingFilter)

        edges_label = QLabel("Detect Edges")
        self.edges_slider = QSlider()
        self.edges_slider.setGeometry((QtCore.QRect(370, 340, 160, 19)))
        self.edges_slider.setMinimumWidth(100)
        self.edges_slider.setRange(10, 300)
        self.edges_slider.setValue(10)
        self.edges_slider.setSingleStep(10)
        self.edges_slider.setOrientation(QtCore.Qt.Horizontal)
        self.canny_cb = QCheckBox("Canny Edge Detector")
        self.canny_cb.stateChanged.connect(self.edgeDetection)

        points_label = QLabel("Points")
        self.points_cb = QCheckBox("Enable Points")
        self.points_cb.stateChanged.connect(self.makePoints)

        self.apply_process_button = QPushButton("Apply Processes")
        self.apply_process_button.setEnabled(False)
        self.apply_process_button.clicked.connect(self.applyImageProcessing)

        reset_button = QPushButton("Reset Image Settings")
        reset_button.clicked.connect(self.resetImageAndSettings)

        side_panel_v_box = QVBoxLayout()
        side_panel_v_box.setAlignment(Qt.AlignTop)

        side_panel_v_box.addWidget(contrast_label)
        side_panel_v_box.addWidget(self.contrast_spinbox)

        side_panel_v_box.addWidget(brightness_label)
        side_panel_v_box.addWidget(self.brightness_spinbox)

        side_panel_v_box.addSpacing(15)

        side_panel_v_box.addWidget(smoothing_label)
        side_panel_v_box.addWidget(self.smoothing_spinbox)
        side_panel_v_box.addWidget(self.filter_2D_cb)

        side_panel_v_box.addWidget(edges_label)
        side_panel_v_box.addWidget(self.edges_slider)
        side_panel_v_box.addWidget(self.canny_cb)

        side_panel_v_box.addWidget(points_label)
        side_panel_v_box.addWidget(self.points_cb)

        side_panel_v_box.addWidget(self.apply_process_button)

        side_panel_v_box.addStretch(1)

        side_panel_v_box.addWidget(reset_button)

        side_panel_frame = QFrame()
        side_panel_frame.setMinimumWidth(200)
        side_panel_frame.setFrameStyle(QFrame.WinPanel)
        side_panel_frame.setLayout(side_panel_v_box)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.image_label, 1)
        main_h_box.addWidget(side_panel_frame)

        container = QWidget()
        container.setLayout(main_h_box)
        self.setCentralWidget(container)


    def setupMenu(self):
        open_act = QAction('Abrir', self)
        open_act.setShortcut('Ctrl+O')
        open_act.triggered.connect(self.openImageFile)
        save_act = QAction('Salvar', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(self.saveImageFile)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)


    def adjustContrast(self):
        if self.image_label.pixmap() != None:
            self.contrast_adjusted = True


    def adjustBrightness(self):
        if self.image_label.pixmap() != None:
            self.brightness_adjusted = True


    def imageSmoothingFilter(self, state):
        if state == Qt.Checked and self.image_label.pixmap() != None:
            self.image_smoothing_checked = True
        elif state != Qt.Checked and self.image_label.pixmap() != None:
            self.image_smoothing_checked = False


    def edgeDetection(self, state):
        if state == Qt.Checked and self.image_label.pixmap() != None:
            self.edge_detection_checked = True
        elif state != Qt.Checked and self.image_label.pixmap() != None:
            self.edge_detection_checked = False


    def makePoints(self, state):
        if state == Qt.Checked and self.image_label.pixmap() != None:
            self.points_checked = True
        elif state != Qt.Checked and self.image_label.pixmap() != None:
            self.points_checked = False


    def applyImageProcessing(self):

        if self.contrast_adjusted == True or self.brightness_adjusted == True:
            contrast = self.contrast_spinbox.value()
            brightness = self.brightness_spinbox.value()
            self.cv_image = cv2.convertScaleAbs(self.cv_image, self.processed_cv_image, contrast, brightness)

        if self.image_smoothing_checked == True:
            blur = self.smoothing_spinbox.value()
            self.cv_image = cv2.GaussianBlur(self.cv_image, (blur, blur), 0)

        if self.edge_detection_checked == True:
            slider = self.edges_slider.value()
            self.cv_image = cv2.Canny(self.cv_image, slider, 3 * slider)

        if self.points_checked == True:
            xrange = np.arange(0, self.cv_image.shape[0] - 5, 5) + 5 // 2
            yrange = np.arange(0, self.cv_image.shape[1] - 5, 5) + 5 // 2

            points = np.zeros(self.cv_image.shape, dtype=np.uint8)

            np.random.shuffle(xrange)
            for i in xrange:
                np.random.shuffle(yrange)
                for j in yrange:
                    x = i + np.random.randint((2 * 3) - 3 + 1)
                    y = j + np.random.randint((2 * 3) - 3 + 1)
                    color = self.cv_image[x, y]
                    cv2.circle(points, (y, x), 3, (int(color[0]), int(color[1]), int(color[2])), -1, cv2.LINE_AA)
            self.cv_image = points.copy()

        self.convertCVToQImage(self.cv_image)
        self.image_label.repaint()


    def resetImageAndSettings(self):
        answer = QMessageBox.information(self, "Reset Image",
                                         "Are you sure you want to reset the image settings?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.No:
            pass
        elif answer == QMessageBox.Yes and self.image_label.pixmap() != None:
            self.resetWidgetValues()
            self.cv_image = self.copy_cv_image
            self.convertCVToQImage(self.copy_cv_image)

    def resetWidgetValues(self):
        self.contrast_spinbox.setValue(1.0)
        self.brightness_spinbox.setValue(0)
        self.filter_2D_cb.setChecked(False)
        self.canny_cb.setChecked(False)
        self.points_cb.setChecked(False)

    def openImageFile(self):
        image_file, _ = QFileDialog.getOpenFileName(self, "Abrir imagem",
                                                    os.getenv('HOME'), "Images (*.png *.jpeg *.jpg *.bmp)")
        if image_file:
            self.resetWidgetValues()
            self.apply_process_button.setEnabled(True)
            self.cv_image = cv2.imread(image_file)
            self.copy_cv_image = self.cv_image

            self.processed_cv_image = np.zeros(self.cv_image.shape, self.cv_image.dtype)
            self.convertCVToQImage(self.cv_image)
        else:
            QMessageBox.information(self, "Erro", "Nenhuma imagem foi carregada.", QMessageBox.Ok)


    def saveImageFile(self):
        image_file, _ = QFileDialog.getSaveFileName(self, "Salvar imagem",
                                                    os.getenv('HOME'),
                                                    "JPEG (*.jpeg);;JPG (*.jpg);;PNG (*.png);;Bitmap (*.bmp)")
        if image_file and self.image_label.pixmap() != None:
            cv2.imwrite(image_file, self.cv_image)
        else:
            QMessageBox.information(self, "Erro",
                                    "Não é possível salvar a imagem.", QMessageBox.Ok)


    def convertCVToQImage(self, image):
        cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = cv_image.shape
        bytes_per_line = width * channels
        converted_Qt_image = QImage(cv_image, width, height, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(converted_Qt_image).scaled(
            self.image_label.width(), self.image_label.height(),
            Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = StoriesInstagram()
    sys.exit(app.exec_())
