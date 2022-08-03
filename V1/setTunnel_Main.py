from PyQt5.Qt import *
import sys
from setTunnel import setTunnel

# https://blog.csdn.net/liuhao192/article/details/122810316

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = setTunnel()

    window.show()
    sys.exit(app.exec_())