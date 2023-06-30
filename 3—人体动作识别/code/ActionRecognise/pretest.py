import sys

from PyQt5.QtWidgets import QApplication

import gui

if __name__ == "__main__":
    video_path = "D:/1_user/videos/5_8/test4.mp4"
    app = QApplication(sys.argv)
    # 创建主窗口并显示
    window = gui.MainWindow(video_path)
    window.show()
    sys.exit(app.exec_())
