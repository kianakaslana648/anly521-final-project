from controlnet_aux import OpenposeDetector, HEDdetector, MidasDetector, LineartDetector
import cv2
import PIL
from PIL import Image
import numpy as np
from typing import List
import share
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import supervision as sv

### canny
def canny_detect(imgs: List[PIL.Image.Image], low_thres=100, high_thres=200):
  canny_imgs = []
  for image in imgs:
    image = np.array(image)
    image = cv2.Canny(image, low_thres, high_thres)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    canny_imgs.append(Image.fromarray(image))
  return canny_imgs

### openpose
def openpose_detect(imgs: List[PIL.Image.Image]):
  return [shared_items.detector(img) for img in imgs]

### depth
def depth_detect(imgs: List[PIL.Image.Image]):
  return [shared_items.detector(img) for img in imgs]

### seg
def seg_detect(imgs: List[PIL.Image.Image]):
  mask_generator = SamAutomaticMaskGenerator(shared_items.detector)
  mask_annotator = sv.MaskAnnotator()
  seg_imgs = []
  for image in imgs:
    masks = mask_generator.generate(image)
    detections = sv.Detections.from_sam(masks)
    annotated_image = mask_annotator.annotate(image, detections)
    seg_imgs.append(Image.fromarray(annotated_image))
  return seg_imgs

### lineart
def lineart_detect(imgs: List[PIL.Image.Image]):
  return [shared_items.detector(img) for img in imgs]

### scribble
def scribble_detect(imgs: List[PIL.Image.Image]):
  return [shared_items.detector(img, scribble=True) for img in imgs]


