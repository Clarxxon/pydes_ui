import os
import sys
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTextEdit, QAction, QMainWindow, QLabel, QVBoxLayout, \
    QHBoxLayout, QButtonGroup, QRadioButton, QFormLayout, QLineEdit, QPushButton

from transliterate import translit, get_available_language_codes
from des import encrypt,decrypt

os.environ['QT_MAC_WANTS_LAYER'] = '1'


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Шифратор DES'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        encrypted_text_label = QLabel()
        encrypted_text_label.setText("Закодированый текст")
        encrypted_text_label.adjustSize()

        decrypted_text_label = QLabel()
        decrypted_text_label.setText("Оригинальный текст")
        decrypted_text_label.adjustSize()

        self.encodetTextEdit = QTextEdit()
        self.encodetTextEdit.adjustSize()

        self.decodetTextEdit = QTextEdit()
        self.decodetTextEdit.adjustSize()

        layout = QVBoxLayout()

        #  ----------- generator type + alg type ----------
        row1 = QHBoxLayout()

        #  ----------- generator params ---------
        self.config = QFormLayout()
        self.config.addWidget(QLabel("Параметры"))
        self.key = QLineEdit("133457799BBCDFF1")
        self.isRussian = QRadioButton('Русский текст', self)
        self.isRussian.setChecked(True)
        self.config.addRow("key ", self.key)
        self.config.addRow(self.isRussian)

        self.encodeButton = QPushButton("Закодировать")
        self.encodeButton.clicked.connect(self.encode)
        self.decodeButton = QPushButton("Заскодировать")
        self.decodeButton.clicked.connect(self.decode)

        layout.addLayout(self.config)

        layout.addWidget(self.encodeButton)
        layout.addWidget(self.decodeButton)

        layout.addWidget(encrypted_text_label)
        layout.addWidget(self.encodetTextEdit)

        layout.addWidget(decrypted_text_label)
        layout.addWidget(self.decodetTextEdit)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.statusBar()
        self.show()

    def showDialog(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                print(data)
                self.decodetTextEdit.setText(data)

    def encode(self):
        text = self.decodetTextEdit.toPlainText()

        if self.isRussian.isChecked():
            text = translit(text, 'ru', reversed=True)

        res = encrypt(mess=text,KEY=self.key.text())
        self.encodetTextEdit.document().setPlainText(res)
        # from des2 import des
        #
        # key = "secret_k"
        # text = translit(self.decodetTextEdit.toPlainText(),'ru', reversed=True)
        # d = des()
        # res = d.encrypt(key, text, padding=True)  # Or just True in third arg
        # self.encodetTextEdit.document().setPlainText(res)



    def decode(self):
        res = decrypt(mess=self.encodetTextEdit.toPlainText(),KEY=self.key.text())

        if self.isRussian.isChecked():
            res = translit(res, 'ru')

        self.decodetTextEdit.document().setPlainText(res)
        # from des2 import des
        #
        # key = "secret_k"
        # text = self.encodetTextEdit.toPlainText()
        # d = des()
        # res = d.decrypt(key, text, padding=True)  # Or just True in third arg
        # res = translit(res,'ru')
        # self.decodetTextEdit.document().setPlainText(res)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
