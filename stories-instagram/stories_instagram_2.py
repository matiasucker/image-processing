import cv2

import sys
from design import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

path =''


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.actionAbrir_imagem.triggered.connect(self.abrir_imagem)
        self.actionSalvar_imagem.triggered.connect(self.salvar_imagem)
        self.actionCinza.triggered.connect(self.cinza)

    def abrir_imagem(self):
        path, _ = QFileDialog.getOpenFileName(
            self.centralwidget,
            'Abrir imagem',
            ''
        )
        self.original_img = QPixmap(path)
        self.nova_imagem = self.original_img.scaledToWidth(640)
        self.labelImg.setPixmap(self.nova_imagem)

    def salvar_imagem(self):
        path, _ = QFileDialog.getSaveFileName(
            self.centralwidget,
            'Salvar imagem',
            ''
        )
        self.nova_imagem.save(path, 'PNG')

    def cinza(self):
        self.frameBlur.close()
        self.frameNegativo.close()
        self.img = cv2.cvtColor(path, cv2.COLOR_BGR2GRAY)
        print("até aqui")
        self.img = self.img.scaledToWidth(640)
        self.labelImg.repaint()



if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = App()
    app.show()
    qt.exec_()

