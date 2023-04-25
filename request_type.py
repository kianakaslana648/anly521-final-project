from pydantic import BaseModel
from fastapi import UploadFile, File, Form
from typing import Annotated, Union, Optional

class gpthelp_request(BaseModel):
    prompt: str

class modelselection_request(BaseModel):
    sdmodel: str
    controlnet: str
    scheduler: str

class imagegeneration_nocontrol_request(BaseModel):
    prompt: str
    neg_prompt: str
    cfg_scale: float
    inference_steps: int
    num_samples: int
    width: int
    height: int

# class imagegeneration_usecontrol_request(BaseModel):
#     prompt: Optional[str] = None
#     neg_prompt: Optional[str] = None
#     cfg_scale: float = Form(...)
#     inference_steps: int = Form(...)
#     num_samples: int = Form(...)
#     width: int = Form(...)
#     height: int = Form(...)
#     refer_img: UploadFile = File(...)