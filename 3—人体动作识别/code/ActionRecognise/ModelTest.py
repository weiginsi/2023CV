from tensorflow.keras.models import load_model
import numpy as np
import cv2
import pickle
import time
import PoseDetector
import gui

#创建类
class ModelTest():
    # # 指定使用的GPU设备
    # physical_devices = tf.config.list_physical_devices('GPU')
    # tf.config.set_visible_devices(physical_devices[0], 'GPU')
    #
    # # 验证可见的GPU设备
    # tf.config.get_visible_devices()

    #打开视频
    def OpenVideo(self,Path):
        cap=cv2.VideoCapture(Path)
        return cap

    #打开摄像头
    def OpenCamera(self):
        cap=cv2.VideoCapture(0)
        return cap



    #判断动作
    def ActionRecognition(self,cap,window):

        # 模型和标签名
        MODEL_NAME = "ActionModel.h5"
        LABEL_NAME = "ActionLabels.dat"

        fps = 30
        size = (1024, 720)
        video = cv2.VideoWriter("D:/my_data/ActionRecognize--main/ActionData/result/output.avi",cv2.VideoWriter_fourcc("I",'4','2','0'),fps,size)
        # 加载标签
        with open(LABEL_NAME, "rb") as f:
            lb = pickle.load(f)

        # 加载神经网络
        model = load_model(MODEL_NAME)

        while (True):

            ret, frame = cap.read()
            if frame is None:
                break
            frame = cv2.flip(frame, 3)
            frame = cv2.resize(frame, (1024, 720))

            if ret == True:
                roi = frame
                roi1 = roi
                roi1 = cv2.resize(roi, (100, 100))
                roi1 = np.expand_dims(roi1, axis=0)
                roi1 = roi1 / 255.
                prediction = model.predict(roi1)
                detector = PoseDetector.poseDetector()
                detector.FindPose(roi)
                # 判断动作并打印在屏幕上
                Action_Probability = prediction[0][np.argmax(prediction[0])]
                Action = lb.inverse_transform(prediction)[0]
                cv2.putText(roi, Action, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                cv2.putText(roi, ('%.2f' % (Action_Probability * 100)) + '%', (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 1)

                frame = cv2.resize(frame, (1024, 720))
                video.write(frame)
                window.set_img(frame)
            #cv2.imshow('Action_Recognition', frame)

        video.release()
        window.set_video("output.avi",1)
