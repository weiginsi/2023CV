import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel
from PyQt5.QtCore import QThread
from subprocess import Popen, PIPE


class RunCodeThread(QThread):
    def __init__(self, video_path):
        super(RunCodeThread, self).__init__()
        self.video_path = video_path

    def run(self):
        command = ['python', 'run_video.py', '--video', self.video_path]
        print(command)
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Video Pose Estimation'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 200

        self.video_path = ""
        self.label = QLabel(self)
        self.label.resize(300, 20)
        self.label.move(70, 40)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        select_video_button = QPushButton('Select Video', self)
        select_video_button.setToolTip('Select Video')
        select_video_button.move(100, 80)
        select_video_button.clicked.connect(self.select_video)

        run_code_button = QPushButton('Run Code', self)
        run_code_button.setToolTip('Run Code')
        run_code_button.move(300, 80)
        run_code_button.clicked.connect(self.run_code)

        self.show()

    def select_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "",
                                                         "MP4 Files (*.mp4);;All Files (*)", options=options)
        if self.video_path:
            self.label.setText(f"Selected Video: {os.path.basename(self.video_path)}")

    def run_code(self):
        if self.video_path:
            self.run_thread = RunCodeThread(self.video_path)
            self.run_thread.start()


def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()