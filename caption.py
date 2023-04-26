import share
from transformers import BlipProcessor, BlipForConditionalGeneration
import PIL

def image_captioning(raw_image: PIL.Image.Image):
  inputs = share.shared_items.caption_processor(raw_image, return_tensors="pt")
  out = share.shared_items.caption_model.generate(**inputs, max_length=200)
  return share.shared_items.caption_processor.decode(out[0], skip_special_tokens=True, max_new_tokens=200)