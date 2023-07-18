import sys

from PyQt5.QtWidgets import QApplication

from ui.mainWindow import mainWindow


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())


if "__main__" == __name__:
    # url = 'https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe'
    # file_name = 'BaiduNetdisk_7.2.8.9.exe'
    # # 开始下载文件
    # download(url, file_name)

    main()
