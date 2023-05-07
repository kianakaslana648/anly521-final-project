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
  def __str__(self):
    rep = 'prompt: ' + self.prompt + '\t' + 'neg_prompt: ' + self.neg_prompt + '\t' + 'num_steps: ' + self.num_steps + '\t' + 'num_imgs: ' + self.num_imgs + '\t' + 'height: ' + self.height + '\t' + 'width: ' + self.width + '\t' + 'cfg_scale: ' + self.cfg_scale
    return rep
  def __repr__(self):
    rep =  'params(' + self.prompt + ', ' + self.neg_prompt + ', ' + self.num_steps + ', ' +self.num_imgs + ', ' + self.height + ', ' + self.width + ', ' + self.cfg_scale + ')'
    return rep

def generate_img(par: params):
  if share.shared_items.controlnet == None:
    return share.shared_items.sd_pipeline(prompt=par.prompt, 
    negative_prompt=par.neg_prompt, num_inference_steps=par.num_steps,
    height=par.height, width=par.width, guidance_scale=par.cfg_scale,
    num_images_per_prompt=par.num_imgs).images
  else:
    return share.shared_items.sd_pipeline(prompt=par.prompt, 
    negative_prompt=par.neg_prompt, num_inference_steps=par.num_steps,
    guidance_scale=par.cfg_scale, num_images_per_prompt=par.num_imgs, image=par.refer_image).images