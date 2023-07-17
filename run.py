import sys

from PyQt5.QtWidgets import QApplication

from ui.mainWindow import mainWindow

from services.download_services import download


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())


if "__main__" == __name__:
    # # url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/packages/0d/ea/f936c14b6e886221e53354e1992d0c4e0eb9566fcc70201047bb664ce777/tensorflow-2.3.1-cp37-cp37m-macosx_10_9_x86_64.whl#sha256=1f72edee9d2e8861edbb9e082608fd21de7113580b3fdaa4e194b472c2e196d0'
    # url = 'https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe'
    # file_name = 'BaiduNetdisk_7.2.8.9.exe'
    # # 开始下载文件
    # download(url, file_name)

    main()
