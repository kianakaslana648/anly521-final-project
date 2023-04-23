import share
from transformers import BlipProcessor, BlipForConditionalGeneration
import PIL

def image_captioning(raw_image: PIL.Image.Image):
  inputs = shared_items.caption_processor(raw_image, return_tensors="pt")
  out = shared_items.caption_model.generate(**inputs)
  return processor.decode(out[0], skip_special_tokens=True)