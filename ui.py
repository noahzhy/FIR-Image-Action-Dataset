from cv2 import *
from pandas import read_csv
from numpy import array, reshape
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 293)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

        self.path = QtCore.QDir.rootPath()
        self.pos = 0
        self.max_len = 0

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QLabel(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 320, 240))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 260, 321, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.valueChanged.connect(self.value_changed)
        self.horizontalSlider.sliderReleased.connect(self.slider_released)
        self.horizontalSlider.setDisabled(True)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(350, 10, 381, 241))
        self.groupBox.setObjectName("groupBox")
        self.fileModel = QtWidgets.QFileSystemModel()
        self.fileModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.listView = QtWidgets.QListView(self.groupBox)
        self.listView.setGeometry(QtCore.QRect(10, 20, 361, 211))
        self.listView.setModel(self.fileModel)
        self.listView.setObjectName("listView")
        self.listView.setRootIndex(self.fileModel.index(self.path))
        self.listView.clicked.connect(self.on_clicked)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(570, 260, 156, 23))
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Open
        )
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.select_path)
        self.buttonBox.rejected.connect(self.exit_win)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 262, 41, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(400, 260, 61, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("0")
        self.lineEdit.setDisabled(True)
        self.lineEdit.returnPressed.connect(self.choose_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Thermal Data View"))
        self.groupBox.setTitle(_translate("MainWindow", "Folder"))
        self.label.setText(_translate("MainWindow", "Frame"))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Close).setText("Exit")

    def select_path(self):
        self.path = QtWidgets.QFileDialog.getExistingDirectory()
        self.groupBox.setTitle(self.path)
        self.listView.setRootIndex(self.fileModel.setRootPath(self.path))

    def on_clicked(self, index):
        self.path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.show_frame(self.path, 0)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setMaximum(self.max_len)
        self.horizontalSlider.setDisabled(False)
        self.lineEdit.setDisabled(False)

    def show_frame(self, file_path, frame_pos):
        data = read_csv(file_path, index_col=None).iloc[:, 2:]
        self.max_len = len(data)-1
        data = data[frame_pos:frame_pos+1]
        data = array(data).reshape((24, 32))
        frame = self.data_to_frame(data)
        frame = resize(frame, (320, 240), interpolation=INTER_NEAREST)
        qimage = QtGui.QImage(frame, 320, 240, QtGui.QImage.Format_BGR888)
        self.frame.setPixmap(QtGui.QPixmap(qimage))

    @staticmethod
    def data_to_frame(data):
        out_data = None
        out_data = normalize(data, out_data, 0, 255, NORM_MINMAX)
        img_gray = (out_data).astype('uint8')
        heatmap_g = img_gray.astype('uint8')
        frame = applyColorMap(heatmap_g, COLORMAP_JET) # COLORMAP_JET
        return frame

    def value_changed(self):
        pos = self.horizontalSlider.value()
        self.lineEdit.setText(str(pos))

    def slider_released(self):
        pos = self.horizontalSlider.value()
        self.lineEdit.setText(str(pos))
        self.show_frame(self.path, pos)

    def choose_frame(self):
        pos = int(self.lineEdit.text())
        if pos > self.max_len:
            pos = self.max_len
            self.lineEdit.setText(str(pos))
        self.horizontalSlider.setValue(pos)
        self.show_frame(self.path, pos)

    def exit_win(self):
        QtCore.QCoreApplication.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
