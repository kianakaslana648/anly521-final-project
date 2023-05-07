from pydantic import BaseModel
from fastapi import UploadFile, File, Form
from typing import Annotated, Union, Optional

class gpthelp_request(BaseModel):
    prompt: str
    def __str__(self):
        rep = 'prompt: ' + self.prompt
        return rep
    def __repr__(self):
        rep = 'gpthelp_request(' + self.prompt + ')'
        return rep

class modelselection_request(BaseModel):
    sdmodel: str
    controlnet: str
    scheduler: str
    def __str__(self):
        rep = 'sdmodel: ' + self.sdmodel + '\t' + 'controlnet: ' + self.controlnet + '\t' + 'scheduler' + self.scheduler + '\t'
        return rep
    def __repr__(self):
        rep = 'modelselection_request(' + self.sdmodel + ', ' + self.controlnet + ', ' + self.scheduler + ')'
        return rep

class imagegeneration_nocontrol_request(BaseModel):
    prompt: str
    neg_prompt: str
    cfg_scale: float
    inference_steps: int
    num_samples: int
    width: int
    height: int
    def __str__(self):
        rep = 'prompt: ' + self.prompt + '\t' + 'neg_prompt: ' + self.neg_prompt + '\t' + 'cfg_scale: ' + self.cfg_scale + '\t' + 'inference_steps: ' + self.inference_steps + '\t' + 'num_samples: ' + self.num_samples + '\t' + 'width: ' + self.width + '\t' + 'height: ' + self.height
        return rep
    def __repr__(self):
        rep = 'imagegeneration_nocontrol_request(' + self.prompt + ', ' + self.neg_prompt + ', ' + self.cfg_scale + ', ' + self.inference_steps + ', ' + self.num_samples + ', ' + self.width + ', ' + self.height + ')'
        return rep
# class imagegeneration_usecontrol_request(BaseModel):
#     prompt: Optional[str] = None
#     neg_prompt: Optional[str] = None
#     cfg_scale: float = Form(...)
#     inference_steps: int = Form(...)
#     num_samples: int = Form(...)
#     width: int = Form(...)
#     height: int = Form(...)
#     refer_img: UploadFile = File(...)