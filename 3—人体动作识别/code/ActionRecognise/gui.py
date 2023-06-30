import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer,QFile
import cv2
import keyboard
from de import Ui_MainWindow
import time
import sys
import GetAcitionData
import ModelTest
import TrainModel
import PoseDetector


def open_video_stream(video_path):
    # 打开视频流
    cap = cv2.VideoCapture(video_path)
    return cap



class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,OpenVideo,train,Test,video_path="D:/1_user/videos/test6.mp4"):
        super().__init__()
        self.flag = False
        self.window = None
        self.cap = open_video_stream(video_path)
        self.setupUi(self)
        self.filename = video_path
        self.OpenVideo = OpenVideo
        self.train = train
        self.Test = Test
        self.open_button.clicked.connect(self.open_button_clicked)
        self.start_button.clicked.connect(self.start_button_clicked)
        self.last_ret = False



    def open_button_clicked(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi);;所有文件 (*)",
                                                  options=options)
        if fileName:
            print("选择的文件路径：", fileName)
            self.label_process.setText("选择的文件路径："+fileName)
            self.label_process.show()

            self.filename = fileName
            self.set_video(self.filename,1)

        else:
            print("打开失败")

    def start_button_clicked(self):
        if self.filename is None:
            print("未选择视频")
            self.label_process.setText("未选择视频")
            self.label_process.show()
        else:
            self.label_process.setText("正在处理请稍等")
            self.label_process.show()
            QApplication.processEvents()
            self.cap.release()
            self.main_back()

    def main_back(self):

        self.OpenVideo.ActionRecognition(open_video_stream(self.filename), self)
        self.label_process.setText("处理完成")
        self.label_process.show()

    def con_set(self,frame):
        self.timer.timeout.connect(self.set_img)

    def update_frame(self):
        ret, frame = self.cap.read()
        if self.last_ret != ret:
            print(ret)
            self.last_ret = ret

        if ret:
            # 转换视频帧为Qt图像格式
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = rgb_image.shape
            qimage = QImage(rgb_image.data, w, h, QImage.Format_RGB888)

            # 将Qt图像设置为QLabel的背景图像
            pixmap = QPixmap.fromImage(qimage)
            pixmap = pixmap.scaled(self.label_show.size(), Qt.KeepAspectRatio)
            self.label_show.setPixmap(pixmap)



    def set_img(self,frame):
        # 转换视频帧为Qt图像格式
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb_image.shape
        qimage = QImage(rgb_image.data, w, h, QImage.Format_RGB888)

        # 将Qt图像设置为QLabel的背景图像
        pixmap = QPixmap.fromImage(qimage)
        pixmap = pixmap.scaled(self.label_show.size(), Qt.KeepAspectRatio)
        self.label_show.setPixmap(pixmap)

    def set_video(self,cap,flag=0):
        if flag == 1 :
            self.cap = open_video_stream(cap)
        elif flag ==0 :
            # 创建定时器用于更新视频帧
            self.cap = cap

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 设置定时器间隔为30ms，约30fps的显示速度


if __name__=="__main__":
    app = QApplication(sys.argv)
    # 创建主窗口并显示
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



