import os
import sys

from PyQt5.Qt import QApplication

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from setTunnel import setTunnel

# https://blog.csdn.net/liuhao192/article/details/122810316

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = setTunnel()

    window.show()
    sys.exit(app.exec_())