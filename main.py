import time
from threading import Thread
from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtTest
# PySide6-uic demo.ui -o ui_demo.py
# from ui_demo import Ui_Demo
#from task import add
from GUI import Ui_MainWindow
from task import nick_name

#from Signal import my_signal


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # UI类的实例化()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint )
        self.ui.setupUi(self)
        self.band()

    def band(self):
        # self.ui.___ACTION___.triggered.connect(___FUNCTION___)
        # self.ui.___BUTTON___.clicked.connect(___FUNCTION___)
        # self.ui.___COMBO_BOX___.currentIndexChanged.connect(___FUNCTION___)
        # self.ui.___SPIN_BOX___.valueChanged.connect(___FUNCTION___)
        # 自定义信号.属性名.connect(___FUNCTION___)

        self.ui.runButton.clicked.connect(self.handle_click)
        self.ui.ontopButton.clicked.connect(self.ontop)
        self.ui.nickname_input.returnPressed.connect(self.onReturnPressed2)
        self.ui.folder_dir_input.returnPressed.connect(self.onReturnPressed1)
        self.ui.folder_dir_input.setFocus()
    def handle_click(self):
        def innerFunc():
            self.ui.runButton.setEnabled(False)
            input1 = self.ui.folder_dir_input.text()
            input2 = self.ui.nickname_input.text()
            if self.ui.delete_name_button.isChecked():
                option = 1
            else:
                option = 0
            self.ui.result.setStyleSheet("QLabel { color : black; }")
            self.ui.result.setText("please wait")

            result = nick_name(input1, input2, option)
            QtTest.QTest.qWait(500)
            self.ui.runButton.setEnabled(True)
            if result:
                self.ui.result.setText("Done")
                self.ui.result.setStyleSheet("QLabel { color : green; }")
            else:
                self.ui.result.setText("Error")
                self.ui.result.setStyleSheet("QLabel { color : red; }")


        task = Thread(target=innerFunc)
        task.start()
    def ontop(self):
        if self.ui.ontopButton.isChecked():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.Widget)
            self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            self.show()
            # self.setWindowFlags(QtWidgets)
            # self.show()

    def onReturnPressed1(self):
        # show()
        self.ui.nickname_input.setFocus()
    def onReturnPressed2(self):
        self.handle_click()
        self.ui.folder_dir_input.setFocus()


if __name__ == '__main__':
    app = QApplication([])  # 启动一个应用
    window = MainWindow()  # 实例化主窗口
    window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出
