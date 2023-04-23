import share
from typing import Union
import PIL
import dataclasses

@dataclasses.dataclass
class params:
  prompt: str
  neg_prompt: Union[str, None]
  num_steps: int
  num_imgs: int
  height: int
  width: int
  cfg_scale: float
  refer_image: Union[PIL.Image.Image, None]

def generate_img(par: params):
  if shared_items.controlnet == None:
    return shared_items.sd_pipeline(prompt=par.prompt, 
    negative_prompt=par.neg_prompt, num_inference_steps=par.num_steps,
    height=par.height, width=par.width, guidance_scale=par.cfg_scale,
    num_images_per_prompt=par.num_imgs).images
  else:
    return shared_items.sd_pipeline(prompt=par.prompt, 
    negative_prompt=par.neg_prompt, num_inference_steps=par.num_steps,
    height=par.height, width=par.width, guidance_scale=par.cfg_scale,
    num_images_per_prompt=par.num_imgs, image=par.refer_image).images