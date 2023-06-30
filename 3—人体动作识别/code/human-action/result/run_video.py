import argparse
import logging
import time
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage
from pyqt5_plugins.examplebuttonplugin import QtGui
import pose
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import scripts.label_image as label_img

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

def cvimg_to_qtimg(cvimg):

    height, width, depth = cvimg.shape
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)

    return cvimg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--video', type=str, default="D:/1_user/videos/pb1.mp4")

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()

    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    logger.debug('read video+')
    cam = cv2.VideoCapture(args.video)
    ret_val, image = cam.read()
    logger.info('video image=%dx%d' % (image.shape[1], image.shape[0]))

    # 定义视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    # 创建 VideoWriter 对象
    out = cv2.VideoWriter('./result/output3.mp4', fourcc, 20.0, (image.shape[1], image.shape[0]))

    # count = 0
    while True:

        logger.debug('+image processing+')
        ret_val, image = cam.read()
        if not ret_val:
            break

        logger.debug('+postprocessing+')
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        img = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        logger.debug('+classification+')
        # Getting only the skeletal structure (with white background) of the actual image
        image = np.zeros(image.shape, dtype=np.uint8)
        image.fill(255)
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        # Classification
        pose_class = label_img.classify(image)

        logger.debug('+displaying+')
        cv2.putText(img,
                    "Current predicted pose is : %s" % (pose_class),
                    (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', img)
        pose.pose_img = img

        # 将处理后的帧写入视频文件
        out.write(img)

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        logger.debug('+finished+')

        # For gathering training data
        # title = 'img'+str(count)+'.jpeg'
        # path = <enter any path you want>
        # cv2.imwrite(os.path.join(path , title), image)
        # count += 1

    cam.release()
    out.release()
    cv2.destroyAllWindows()