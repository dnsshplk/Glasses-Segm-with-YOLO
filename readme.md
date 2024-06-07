Task 1 - DL - Eyeglasses Segmentation Model

# Solution Desription
For this task, the yolov8n-seg from Ultralytics is used.


# Data preparation

## Convert binary masks to polygons
First, we need to prepare the data. Specifically, convert it into the YOLO format, where istead of binary masks, the model accepts .txt files containing polygons of each object. The problem is that it considers all pixels whithin some polygon to be part of an object and that is not true in our case. Most of the time we need to segment eyeglasses frames without lenses. That is why we need to segment lenses separately from eyeglasses and in the end deduct lenses mask from the eyeglasses.

Other that that, data covnertion is pretty straitforward:
For to conver binary mask to yolo-polygons we need:
1. find contours in the mask
2. Convert countours into polygons. External countours append to the 'glasses' class, internal - to the 'lens' class.
3. Write polygons into .txt files

## Rearange data folder and create dataset.yaml file
Second we need to rearange the data so yolo can accept it (we can do it manually):
```
data/
├── train/
│   ├── images/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── labels/
│       ├── img1.txt
│       ├── img2.txt
│       └── ...
├── val/
│   ├── images/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── labels/
│       ├── img1.txt
│       ├── img2.txt
│       └── ...
```
Then, create a dataset.yaml file:
```
names:
- glasses
- lens
nc: 2
path: /kaggle/input/glasses-segm/data
train: images/train
val: images/val
```

Now we can train our model


# Model Training
Model training has been done on kaggle
Train the model for 50 epochs with a batch size 32 (+- 30 min on GPU P100)
Here we can see losses and scores during traning:
