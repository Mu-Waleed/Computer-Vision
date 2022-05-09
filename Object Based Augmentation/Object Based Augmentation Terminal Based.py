import argparse
import albumentations as A
import os
from PIL import Image
import cv2 as cv
import cv2
import matplotlib.pyplot as plt
import numpy
parser = argparse.ArgumentParser()

parser.add_argument('--images_path', type=str, required=True, help="Enter Path of image folder")
parser.add_argument('--labels_path', type=str, required=True, help="Enter Path of label folder")
parser.add_argument('--save_path', type=str, required=True, help="Enter Path to save augmented images and labels")
parser.add_argument('--instance_no', type=int, required=True, help="Enter the instance class value like in text file i.e 0 or 1 or 2 etc")
parser.add_argument('--no_aug', type=str, required=True, help="Enter the number of Augmenation Performed. 0 to for all the images")
args = parser.parse_args()

# This cell can be used to apply bounding box level augmentation to dataset for YOLO.

# Each instance represented by a number
cup, bottle, glass, tin_can, gym_bottle = 0, 1, 2, 3, 4


# Method to read single file in the provided path
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        Lines = f.readlines()
        return Lines


# Method to found the given instance in the file.
def match_object(lines, object):
    found = 0
    for each_line in lines:
        if each_line[0] == str(object):
            found = found + 1
        else:
            found = 0
            return found
    return found


# Method to draw the bounding box to verify augmentation result
def draw(img, bboxes, mode):
    h, w, _ = img.shape
    for each_line in bboxes:
        x11 = int(float(each_line.split(' ')[1]) * w)
        y11 = int(float(each_line.split(' ')[2]) * h)
        xw1 = int(float(each_line.split(' ')[3]) * w / 2)
        yw1 = int(float(each_line.split(' ')[4]) * h / 2)

        start_point1 = (x11 - xw1, y11 - yw1)

        end_point1 = (x11 + xw1, y11 + yw1)
        if mode == 1:
            ccc = cv2.rectangle(img, start_point1, end_point1, (2550, 0, 0), 3)
        else:
            ccc = cv2.rectangle(img, start_point1, end_point1, (0, 0, 255), 3)
    plt.imshow(img)
    plt.show()


# This method convert yolo format to pascal inorder to find intersection over union (iou) for overlapping bounding box.
def yolo_to_pascal_voc(x_center, y_center, w, h, image_w, image_h):
    w = w * image_w
    h = h * image_h
    x1 = ((2 * x_center * image_w) - w) / 2
    y1 = ((2 * y_center * image_h) - h) / 2
    x2 = x1 + w
    y2 = y1 + h
    return [x1, y1, x2, y2]


# This method calculates intersection over union (iou) for all the bounding boxes in a single image.
def bb_intersection_over_union(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou


# This method is used to apply the augmentation to the provided data
def augment(path, path_image, result_path, obj, obj_name, instance, write, iter):
    global max_aug
    max_aug = 0
    for file in os.listdir(path):
        if max_aug >= instance:
            break

        elif file.endswith(".txt"):
            lines = read_text_file(path + "/" + file)
            found = match_object(lines, obj)
            if found >= 1:
                path1 = file
                path1 = path1.replace(".txt", ".jpg")
                image2 = cv2.imread(path_image + "/" + path1)
                class_labels = []
                bboxes = []
                pascal = []
                for i in lines:
                    int(i[0])
                    result = i.split(" ")
                    class_labels.append(result[0])
                    l = []
                    l.append(float(result[1]))
                    l.append(float(result[2]))
                    l.append(float(result[3]))
                    l.append(float(result[4]))
                    bboxes.append(l)

                try:
                    transformed = transform(image=image2, bboxes=bboxes, class_labels=class_labels)

                    transformed_image = transformed['image']
                    transformed_bboxes = transformed['bboxes']
                    transformed_class_labels = transformed['class_labels']

                    if write == False:
                        draw(image2, lines, 1)

                    count = 0
                    h, w, _ = transformed_image.shape
                    trans_lines = []
                    result_bboxes = []
                    overlapped, show = overlap_check(transformed_bboxes, transformed_image)
                    for each_line in transformed_bboxes:
                        result_bboxes.append(list(each_line))
                        s = ""
                        s = s + str(class_labels[count]) + " "
                        count += 1
                        for i in each_line:
                            s = s + str(i) + " "

                        position = len(s) - 1
                        new_character = '\n'
                        s = s[:position] + new_character + s[position + 1:]

                        if write == True and overlapped == False:
                            f = open(result_path + "/" + "labels" + "/" + iter + file, "a")
                            f.write(s)
                            f.close()
                        trans_lines.append(s)
                    if write == False:
                        print(show)
                        max_aug += found
                        draw(transformed_image, trans_lines, 0)
                    elif overlapped == False and write == True:
                        max_aug += found
                        cv2.imwrite(result_path + "/" + "images" + "/" + iter + path1, transformed_image)

                except:
                    pass

    return max_aug


# Third method check all the images one by one if their bounding boxes overlap or not.
def overlap_check(transformed_bbox, img):
    greater = False
    over = ""
    to_pascal = []
    for i in transformed_bbox:
        to_pascal.append(yolo_to_pascal_voc(i[0], i[1], i[2], i[3], img.shape[1], img.shape[0]))

    if len(to_pascal) > 1:
        for i in to_pascal:
            to_pascal.remove(i)
            for j in to_pascal:
                iou = bb_intersection_over_union(boxA=i, boxB=j)
                if iou > 0.12:
                    over = "Overlapping Bounding Box. Augmentation Rejected!"
                    greater = True
    return greater, over

prob = 0.5
brightness = 0.2
contrast_limit = 0.2
blur_x, blur_y = 7,7
transform = A.Compose([
                       A.GaussianBlur(blur_limit=(blur_x, blur_y), p=prob, always_apply= True),
                       A.ShiftScaleRotate(rotate_limit=(25,35), p=1),
                       A.RandomBrightnessContrast(brightness_limit=brightness, contrast_limit=contrast_limit, p=prob),
], bbox_params=A.BboxParams(format='yolo', min_area=1024, min_visibility=0.3, label_fields=['class_labels']))


path_images = args.images_path
path_label = args.labels_path
path_save = args.save_path
instance_class_value = int(args.instance_no)
no_aug = int(args.no_aug)
write = True
if no_aug == 0:
    no_aug = 9999999
try:
    os.mkdir(path_save + "/images")
    os.mkdir(path_save + "/labels")
except:
    pass

augment(path_label, path_images, path_save, instance_class_value , "", no_aug, write= write, iter="")