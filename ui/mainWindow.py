import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QInputDialog, QAction, QMainWindow, qApp, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton

from services.download_services import download


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # ---------------状态栏--------------------
        statusBar = self.statusBar()
        # ---------------设置菜单-------------------------
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&文件")
        settingMenu = menuBar.addMenu("&设置")
        helpMenu = menuBar.addMenu("&关于")

        extAction = QAction(QIcon("./images/exit.png"), "&退出", self)
        extAction.setStatusTip("退出程序")
        extAction.triggered.connect(qApp.exit)

        newTaskAction = QAction(QIcon("./images/newtask.png"), "&新建任务", self)
        newTaskAction.setStatusTip("新建下载任务")
        newTaskAction.triggered.connect(self.showNewTaskDialog)

        fileMenu.addAction(newTaskAction)
        fileMenu.addAction(extAction)
        # self.setMenuBar(menuBar)

        # ----------------工具栏----------------------------
        toolbar = self.addToolBar("新建下载任务")
        new = QAction(QIcon("./images/new.png"), "新建下载任务", self)
        toolbar.addAction(new)
        start = QAction(QIcon("./images/start.png"), "开始下载", self)
        toolbar.addAction(start)
        pause = QAction(QIcon("./images/pause.png"), "暂停下载", self)
        toolbar.addAction(pause)
        ext = QAction(QIcon("./images/exit.png"), "退出", self)
        toolbar.addAction(ext)
        # --------------主窗口布局-----------------------------

        btn1 = QPushButton("111")
        btn2 = QPushButton("222")
        hbox = QHBoxLayout()

        hbox.addWidget(btn1)
        hbox.addWidget(btn2)

        # ----下面3行代码解决在QMainWindow中布局问题
        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

        self.setGeometry(300, 300, 800, 500)
        self.center()
        self.setWindowTitle("IWD下载器")
        # self.show()

    def showNewTaskDialog(self):
        url, ok = QInputDialog.getText(self, "新建下载任务", "输入下载地址")
        if ok:
            print(url)
            print(os.path.basename(url))
            download(url, os.path.basename(url))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    mw = mainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
