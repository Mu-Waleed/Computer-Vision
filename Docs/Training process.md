<h1> Training process for yolov5 v4 </h1>
  
This will guide you how to train the model using yolov5 especially version 4.
 
Go and read the Setting up [Environment.md](https://github.com/Mu-Waleed/Computer-Vision/blob/main/Docs/Setting%20up%20Environment.md) in order to set up the environment, add yolov5 repository and install requirements .


<h2> Train On Custom Data </h2>

<h3> Create dataset.yaml </h3>

dataset.yaml, shown below, is the dataset configuration file that you should create (if not present) according to your dataset in your yolov5 directory that defines 1) an optional download command/URL for auto-downloading, 2) a path to a directory of training images (or path to a *.txt file with a list of training images), 3) the same for our validation images, 4) the number of classes, 5) a list of class names:
train represents the training images path.
val represents the validation images path.

```
# train and val data as 1) directory: path/images/, 2) file: path/images.txt, or 3) list: [path1/images/, path2/images/]
train: ../dataset/images/
val: ../dataset/images/

# number of classes
nc: 80

# class names
names: ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
        'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 
        'teddy bear', 'hair drier', 'toothbrush']
```

**Note:** Your train/val images labels should be in separated folder named labels along with images folder.
YOLOv5 locates labels automatically for each image by replacing the last instance of /images/ in each image path with /labels/. For example:
```
dataset/images/im0.jpg  # image
dataset/labels/im0.txt  # label
```

<h3> Select a Model </h3>
Select a pretrained model to start training from. Larger models like YOLOv5x and YOLOv5x6 will produce better results in nearly all cases, but have more parameters, require more CUDA memory to train, and are slower to run. For mobile deployments we recommend YOLOv5s/m, for cloud deployments we recommend YOLOv5l/x. See our README table for a full comparison of all models.
<h3> Train </h3>

Train a YOLOv5s model on your dataset by specifying dataset, batch-size, image size and either pretrained --weights yolov5s.pt (recommended), or randomly initialized --weights '' --cfg yolov5s.yaml (not recommended). Pretrained weights are auto-downloaded from the latest YOLOv5 release.

**Note:** If do not want to do mulit-class training you can simply add --single-cls parameter below too for force single class training.
**Note:** You can use any pretrained weight according to your need.
```
$ python train.py --img 640 --batch 16 --epochs 5 --data dataset.yaml --weights yolov5s.pt
```

<h3> More about parameters </h3>

**Epochs.** It represents the number of epochs. Start with 300 epochs. If this overfits early then you can reduce epochs. If overfitting does not occur after 300 epochs, train longer, i.e. 600, 1200 etc epochs.</br></br>
**Image size.** It represents resolution of image. COCO trains at native resolution of --img 640, though due to the high amount of small objects in the dataset it can benefit from training at higher resolutions such as --img 1280. If there are many small objects then custom datasets will benefit from training at native or higher resolution. Best inference results are obtained at the same --img as the training was run at, i.e. if you train at --img 1280 you should also test and detect at --img 1280.</br></br>
**Batch size.** It represenst the number of epochs. Use the largest --batch-size that your hardware allows for. Small batch sizes produce poor batchnorm statistics and should be avoided.</br>

<h3> Local Logging </h3>

All results are logged by default to runs/train, with a new experiment directory created for each new training as runs/train/exp2, runs/train/exp3, etc. View train and test jpgs to see mosaics, labels, predictions and augmentation effects.
