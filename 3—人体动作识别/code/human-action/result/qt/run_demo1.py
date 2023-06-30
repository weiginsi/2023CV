import sys
from subprocess import Popen, PIPE
import pose

from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget


class RunCodeThread(QThread):
    def __init__(self, video_path):
        super(RunCodeThread, self).__init__()
        self.video_path = video_path

    def run(self):
        command = ['python', 'run_video.py', '--video', self.video_path]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()


# 定义一个类，这个类从QMainWindow里面继承
class CenterForm(QMainWindow):

    # 初始化
    def __init__(self,parent=None):
        super(CenterForm,self).__init__(parent)

        # 设置主窗口的标题
        self.setWindowTitle('pose')

        # 设置窗口的尺寸
        self.resize(400,300)

        # 添加center方法，作用就是让窗口居中
        def center(self):
            # 创建实例，获得屏幕对象,得到屏幕的坐标系
            screen = QDesktopWidget().screenGeometry()

            # 得到窗口的坐标系
            size = self.geometry()

            # 获取屏幕的宽度、高度
            # 窗口左边缘的坐标等于(屏幕的宽度-窗口的宽度)/2
            newLeft = (screen.width()-size.width()) / 2

            # 屏幕上边缘的坐标等于(屏幕的高度-窗口的高度) / 2
            newTop = (screen.height() - size.height()) / 2

            # 移动窗口
            self.move(newLeft,newTop)



if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    mainWindow = CenterForm()
    # 创建ui，引用pose文件中的Ui_MainWindow类
    ui = pose.Ui_Form()
    # 调用Ui_MainWindow类的setupUi，创建初始组件
    ui.setupUi(mainWindow)
    # 创建窗口
    mainWindow.show()
    # def show_vi():
    #     cv2.putText(run_video.img,
    #                 "Current predicted pose is : %s" % (run_video.pose_class),
    #                 (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                 (0, 255, 0), 2)
    #     cv2.imshow('tf-pose-estimation result', run_video.img)




    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())



