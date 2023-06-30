# Human Action Classification说明文档

人体姿态估计和检测我们使用OpenPose实现https://github.com/ildoonet/tf-pose-estimation与Tensorflow最低限度地实现。对于姿势的二分类，(坐着或直立)，最初在ImageNet大型视觉识别挑战数据集上训练的CNN)在大约1500张姿势图像的数据集上重新训练(最后一层)。为了对所考虑的人周围的场景进行分类，我们组测试了部分数据集重新训练Inception-v3架构，该数据集包含多种不同的日常活动。

姿态分类准确率为94.56%，场景识别率为92.3%。
 
### Testing Ouputs for a Single Image

![alt text](_show.png)

![alt text](_show1.png)


以下是必须的库：

- Python3
- tensorflow-gpu 1.13.0 (works with CPU version as well but with a much higher inference time)
- opencv3
- slim
- slidingwindow - (https://github.com/adamrehn/slidingwindow)



单幅图像的姿态估计和动作分类需要：

```
$ python3 run_image.py --image=1.jpg
```

基于摄像头的姿态估计与动作分类：

```
$ python3 run_webcam.py
```

自定义数据集训练：

在这个项目中有两个分类任务。一个是姿态，另一个是场景分类。两者都遵循类似的训练策略，都需要一个训练目录结构，如下所示:

```
training
│   README.md   
│
└───Action-1
│   │   file011.jpg
│   │   file012.jpg
│ 
└───Action-2
    │   file021.jpg
    │   file022.jpg
```
动作-(n)文件夹将包含想要分类的不同姿势和场景

收集完数据集后，我们通过在终端(从克隆目录)发出以下命令开始训练:

```
python3 scripts/retrain.py --model_dir=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --image_dir=training/
```
接下来测试训练数据，我们组可以通过gui界面输入测试图片和视频，基于姿态估计和检测分类输出实验结果，包括检测出的人体骨科连接点及站坐概率模型，统一标注在界面中。

而且还可以直接运行run_image.py或run_video.py或run_webcam.py进行代码运行

我们组代码文件里总共有
数据集img_data
输入数据res
输出结果result
run_image.py
run_video.py
run_webcam.py
gui.py等主要文件
