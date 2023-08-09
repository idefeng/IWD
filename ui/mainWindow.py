import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QInputDialog, QAction, QMainWindow, qApp, QWidget, \
    QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QHBoxLayout, QTreeWidget, QTreeWidgetItem, QTableWidget

from services.download_service2 import download
from services.common_services import verify_file_type


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.tableInfo = None
        self.initUI()

        self.info = dict()

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

        # ----------------工具栏----------------------------
        toolbar = self.addToolBar("新建下载任务")
        new = QAction(QIcon("./images/new.png"), "新建下载任务", self)
        new.triggered.connect(self.showNewTaskDialog)
        toolbar.addAction(new)
        start = QAction(QIcon("./images/start.png"), "开始下载", self)
        toolbar.addAction(start)
        pause = QAction(QIcon("./images/pause.png"), "暂停下载", self)
        toolbar.addAction(pause)
        setting = QAction(QIcon("./images/setting.png"), "配置", self)
        toolbar.addAction(setting)
        ext = QAction(QIcon("./images/exit.png"), "退出", self)
        ext.triggered.connect(qApp.quit)

        toolbar.addAction(ext)
        # --------------主窗口布局-----------------------------
        hbox = QHBoxLayout()

        self.typeTree = QTreeWidget()
        self.typeTree.setHeaderLabels(["类型", "数量"])
        root = QTreeWidgetItem(self.typeTree)
        root.setText(0, "全部任务")
        root.setIcon(0, QIcon("./images/folder.png"))

        child1 = QTreeWidgetItem(root)
        child1.setText(0, "压缩文件")
        child1.setText(1, "0")
        child1.setIcon(0, QIcon("./images/zip.png"))

        child2 = QTreeWidgetItem(root)
        child2.setText(0, "文档")
        child2.setText(1, "0")
        child2.setIcon(0, QIcon("./images/doc.png"))

        child3 = QTreeWidgetItem(root)
        child3.setText(0, "音乐")
        child3.setText(1, "0")
        child3.setIcon(0, QIcon("./images/music.png"))

        child4 = QTreeWidgetItem(root)
        child4.setText(0, "视频")
        child4.setText(1, "0")
        child4.setIcon(0, QIcon("./images/video.png"))

        child5 = QTreeWidgetItem(root)
        child5.setText(0, "程序")
        child5.setText(1, "0")
        child5.setIcon(0, QIcon("./images/exe.png"))

        child6 = QTreeWidgetItem(root)
        child6.setText(0, "未知类型")
        child6.setText(1, "0")
        child6.setIcon(0, QIcon("./images/other.png"))

        self.typeTree.expandAll()
        hbox.addWidget(self.typeTree)

        self.tableInfo = QTableWidget()
        self.tableInfo.setRowCount(20)
        self.tableInfo.setColumnCount(7)
        self.tableInfo.setHorizontalHeaderLabels(
            ["文件名", "大小", "状态", "剩余时间", "传输速度", "最后连接", "下载链接"])
        self.tableInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格自适应窗口
        self.tableInfo.horizontalHeader().setStretchLastSection(True)  # 设置最后一列自动填充窗口

        hbox.addWidget(self.tableInfo, 2)

        # ----下面3行代码解决在QMainWindow中布局问题
        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

        self.setGeometry(300, 300, 1000, 600)
        self.center()
        self.setWindowTitle("IWD下载器")
        self.setWindowIcon(QIcon("./images/download.png"))
        # self.show()

    def showNewTaskDialog(self):
        url, ok = QInputDialog.getText(self, "新建下载任务", "输入下载地址")
        if ok:
            print(url)
            print(os.path.basename(url))
            # self.get_download_info_signal.emit(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }
            self.info = download(url, "e:\\dev\\iwd\\aaa.exe", headers)
            print(self.info)
            self.tableInfo.setItem(0, 0, QTableWidgetItem(str(self.info['file_name'])))
            self.tableInfo.setItem(0, 1, QTableWidgetItem(str(self.info['content_size_formated'])))
            if self.info['exit']:
                self.tableInfo.setItem(0, 2, QTableWidgetItem(str("完成")))
            else:
                self.tableInfo.setItem(0, 2, QTableWidgetItem(str("未完成")))
            self.tableInfo.setItem(0, 4, QTableWidgetItem(str(self.info['speed']) + '/S'))
            self.tableInfo.setItem(0, 3, QTableWidgetItem(str(self.info['data_bytes_formated'])))
            self.tableInfo.setItem(0, 5, QTableWidgetItem(str(self.info['data_bytes'])))
            self.tableInfo.setItem(0, 6, QTableWidgetItem(str(self.info['download_url'])))

            if verify_file_type(self.info['file_name']) == 1:
                pass

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
