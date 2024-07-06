# Solution Description
For this task, the yolov8n-seg from Ultralytics is used.

# Data preparation

## Convert binary masks to polygons
First, we need to prepare the data. Specifically, convert it into the YOLO format, where instead of binary masks, the model accepts .txt files containing polygons of each object. The problem is that the model considers all pixels whithin some polygon to be part of an object and that is not true in our case. Most of the time we need to segment eyeglasses frames without lenses. That is why we need to segment lenses separately from eyeglasses and in the end deduct lenses masks from the eyeglasses masks.

Other that that, data covnertion is straitforward:
To convert binary mask to yolo-polygons we need:
1. find contours in the mask
2. Convert countours into polygons. External countours append to the 'glasses' class, internal - to the 'lens' class.
3. Write polygons into .txt files

## Rearrange data folder and create dataset.yaml file
Now we need to rearrange the data so yolo can accept it (we can do it manually):
```
data
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
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/run/results.png)

Validation Batches:
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/run/val_batch1_labels.jpg)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/run/val_batch2_labels.jpg)


# Overall Result

## CPU VS GPU
On average it takes 140ms for CPU to inference one image. And 8ms for GPU (GPU P100)

## Here can we se the actual perfomace of the model on the test data:
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58080_3_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58162_2_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58196_0_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58208_1_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58212_0_generated_1_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58219_1_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58223_0_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58234_0_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58258_0_generated_0_00001_.png_mask.png)
![alt text](https://github.com/dnsshplk/Task1_int/blob/main/test/masks_model/58277_1_generated_0_00001_.png_mask.png)
