import os
import cv2
import numpy as np
from ultralytics import YOLO
#import torch

def main():
    # use_gpu = True

    # if use_gpu:
    #     torch.set_default_device('cuda')

    # load the best weigths into the model
    model = YOLO(os.path.join('run', 'best.pt')) 

    images_dir = os.path.join('test', 'images')
    actual_mask_dir = os.path.join('test', 'masks_actual')
    output_dir = os.path.join('test', 'masks_model')

    os.makedirs(output_dir, exist_ok=True)

    for image_file in os.listdir(images_dir):
        image_path = os.path.join(images_dir, image_file)

        image = cv2.imread(image_path)

        results = model.predict(image)

        masks = results[0].masks   
            
        masks = results[0].masks.data.cpu().numpy() 
        classes = results[0].boxes.cls.cpu().numpy()  

        mask_glasses = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        mask_lenses = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            
        for mask, cls in zip(masks, classes):
            mask_uint8 = (mask * 255).astype(np.uint8)
            if cls == 0:  
                mask_glasses = np.maximum(mask_glasses, mask_uint8)
            elif cls == 1:  
                mask_lenses = np.maximum(mask_lenses, mask_uint8)
            
        # Get the eyeglass frame (desired binary image)
        result_mask = mask_glasses - mask_lenses
            
        result_mask = cv2.cvtColor(result_mask, cv2.COLOR_GRAY2BGR)


        mask_output_path = os.path.join(output_dir, f"{image_file}_mask.png")

        actual_mask_path = os.path.join(actual_mask_dir, f'{image_file[:8]}mask.png')
        actual_mask = cv2.imread(actual_mask_path)

        actual_mask = cv2.resize(actual_mask, (512, 512))
        
        # Concat image/actual_mask/result_mask into one image for convenience
        result_image = np.concatenate((image, actual_mask, result_mask), axis = 1)

        cv2.imwrite(mask_output_path, result_image)


if __name__ == '__main__':
    main()