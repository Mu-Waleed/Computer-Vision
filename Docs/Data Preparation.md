# Data Preparation

We provide some tips for yolov5 data preparation in this file.

## Notes on Data Format

The following file formats are currently supported for yolov5:
</br></br>
&emsp;&emsp;**Images:** bmp, jpg, jpeg, png, tif, tiff, dng, webp, mpo
</br>
&emsp;&emsp;**Videos:** mov, avi, mp4, mpg, mpeg, m4v, wmv, mkv

## Organize Directories

Organize your train and val images and labels according to the example below. In this example we assume /coco128 is next to the /yolov5 directory. YOLOv5 locates labels automatically for each image by replacing the last instance of /images/ in each image path with /labels/. For example:

```
dataset/images/im0.jpg  # image
dataset/labels/im0.txt  # label
```

<img src="https://user-images.githubusercontent.com/26833433/112467887-e18a0980-8d67-11eb-93af-6505620ff8aa.png" width="500" height="600">

## Dataset

* **Images per class.** ≥1.5k images per class.</br>
* **Instances per class.** ≥10k instances (labeled objects) per class total.</br>
* **Image variety.** Must be representative of deployed environment. For real-world use cases we recommend images from different times of day, different seasons, different weather, different lighting, different angles, different sources (scraped online, collected locally, different cameras) etc.</br>
* **Label consistency.** All instances of all classes in all images must be labelled. Partial labelling will not work.</br>
* **Label accuracy.** Labels must closely enclose each object. No space should exist between an object and it's bounding box. No objects should be missing a label.</br>
* **Background images.** Background images are images with no objects that are added to a dataset to reduce False Positives (FP). We recommend about 0-10% background images to help reduce FPs (COCO has 1000 background images for reference, 1% of the total).</br>

## Labels

After using a tool like roboflow, CVAT, makesense.ai or Labelbox to label your images, export your labels to YOLO format, with one *.txt file per image (if no objects in image, no *.txt file is required). The *.txt file specifications are:

* One row per object
* Each row is class x_center, y_center, width and height format.
* Box coordinates must be in normalized xywh format (from 0 - 1). If your boxes are in pixels, divide x_center and width by image width, and y_center and height by image height.
* Class numbers are zero-indexed (start from 0).

<img src="https://user-images.githubusercontent.com/26833433/91506361-c7965000-e886-11ea-8291-c72b98c25eec.jpg" width="600" height="500">


The label file corresponding to the above image contains 2 persons (class 0) and a tie (class 27):

<img src="https://user-images.githubusercontent.com/26833433/112467037-d2568c00-8d66-11eb-8796-55402ac0d62f.png" width="400" height="200">

## Dataset Sources:

Online data sources can be used if the data is not sufficient. Some of the Image Datasets for Computer Vision Training are given below:

* [**Labelme:**](http://labelme.csail.mit.edu/Release3.0/browserTools/php/dataset.php?ref=hackernoon.com) A large dataset created by the MIT Computer Science and Artificial Intelligence Laboratory (CSAIL) containing 187,240 images, 62,197 annotated images, and 658,992 labeled objects.

* [**Lego Bricks:**](https://www.kaggle.com/datasets/joosthazelzet/lego-brick-images?ref=hackernoon.com) Approximately 12,700 images of 16 different Lego bricks classified by folders and computer rendered using Blender.

* [**ImageNet:**](http://image-net.org/?ref=hackernoon.com) The de-facto image dataset for new algorithms. Is organized according to the WordNet hierarchy, in which each node of the hierarchy is depicted by hundreds and thousands of images.

* [**MS COCO:**](https://cocodataset.org/) COCO is a large-scale object detection, segmentation, and captioning dataset containing over 200,000 labeled images. It can be used for object segmentation, recognition in context, and many other use cases.

* [**Columbia University Image Library**:](https://www1.cs.columbia.edu/CAVE/software/softlib/coil-100.php?ref=hackernoon.com) COIL100 is a dataset featuring 100 different objects imaged at every angle in a 360 rotation.

* [**Visual Genome:**](http://visualgenome.org/?ref=hackernoon.com) Visual Genome is a dataset and knowledge base created in an effort to connect structured image concepts to language. The database features detailed visual knowledge base with captioning of 108,077 images.

* [**Google’s Open Images:**](https://ai.googleblog.com/2016/09/introducing-open-images-dataset.html?ref=hackernoon.com) A collection of 9 million URLs to images “that have been annotated with labels spanning over 6,000 categories” under Creative Commons.

**Note:** Data Augmentation can be useful if data is imbalance.
