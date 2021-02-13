import cv2
from pandas import read_csv
from numpy import array, reshape, where, mean
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(760, 293)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

        self.path = QtCore.QDir.rootPath()
        self.pos = 0
        self.max_len = 0
        # 1.047 it's a best split value by many times testing
        self.divide = 47

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QLabel(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 320, 240))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(340, 10, 22, 240))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setValue(self.divide)
        self.verticalSlider.valueChanged.connect(self.divide_value_changed)
        
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 260, 321, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.valueChanged.connect(self.value_changed)
        self.horizontalSlider.sliderReleased.connect(self.slider_released)
        self.horizontalSlider.setDisabled(True)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(370, 10, 381, 241))
        self.groupBox.setObjectName("groupBox")
        self.fileModel = QtWidgets.QFileSystemModel()
        self.fileModel.setFilter(
            QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.listView = QtWidgets.QListView(self.groupBox)
        self.listView.setGeometry(QtCore.QRect(10, 20, 361, 211))
        self.listView.setModel(self.fileModel)
        self.listView.setObjectName("listView")
        self.listView.setRootIndex(self.fileModel.index(self.path))
        self.listView.clicked.connect(self.on_clicked)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(596, 260, 156, 23))
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Open
        )
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.select_path)
        self.buttonBox.rejected.connect(self.exit_win)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 262, 41, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(420, 260, 61, 20))
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
        qimage = QtGui.QImage(frame, 320, 240, QtGui.QImage.Format_BGR888)
        self.frame.setPixmap(QtGui.QPixmap(qimage))

    def divide_value_changed(self):
        self.divide = self.verticalSlider.value()
        print("current divide:", self.divide)
        pos = self.horizontalSlider.value()
        self.show_frame(self.path, pos)

    def data_to_frame(self, data):
        def center_point(x, y, w, h):
            x0 = x + w/2
            y0 = y + h/2
            xl = x0 - 8
            yl = y0 - 8
            return int(xl)*10, int(yl)*10, 16*10, 16*10

        _mean = mean(data)
        data_mean = where(data > _mean*(1+0.001*self.divide), data, 0)

        frame = (data_mean).astype('uint8')
        cnts, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)  # COLORMAP_JET

        out_data = None
        out_data = cv2.normalize(data, out_data, 0, 255, cv2.NORM_MINMAX)
        color_frame = (out_data).astype('uint8')
        color_frame = cv2.applyColorMap(color_frame, cv2.COLORMAP_JET)  # COLORMAP_JET
        color_frame = cv2.resize(color_frame, (320, 240), interpolation=cv2.INTER_NEAREST)

        cnt = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        print(cv2.contourArea(cnt))
        if cv2.contourArea(cnt) >= 3:
            x, y, w, h = center_point(x, y, w, h)
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

        return color_frame

    def value_changed(self):
        pos = self.horizontalSlider.value()
        self.lineEdit.setText(str(pos))
        self.show_frame(self.path, pos)

    def slider_released(self):
        pos = self.horizontalSlider.value()
        # self.lineEdit.setText(str(pos))
        # self.show_frame(self.path, pos)

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
