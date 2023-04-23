import share
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, StableDiffusionPipeline
from diffusers import DDIMScheduler, DDPMScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler, KarrasVeScheduler, UniPCMultistepScheduler
import os
import torch
from controlnet_aux import OpenposeDetector, HEDdetector, MidasDetector, LineartDetector
from segment_anything import sam_model_registry
from transformers import BlipProcessor, BlipForConditionalGeneration

annotator_path = '/content/drive/MyDrive/ANLY521/annotator'
controlnet_path = '/content/drive/MyDrive/ANLY521/controlnet'
sd15_model_path = '/content/drive/MyDrive/ANLY521/sd15-models'


def check_sd_models():
  return os.listdir(sd15_model_path)

valid_models = check_sd_models()
valid_controlnet_dict = {
  'canny': 'sd-controlnet-canny',
  'openpose': 'sd-controlnet-openpose',
  'depth': 'sd-controlnet-depth',
  'seg': 'sd-controlnet-seg',
  'lineart': 'sd-controlnet-lineart',
  'scribble': 'sd-controlnet-scribble'
}
valid_scheduler_dict = {
  'DDIMScheduler': DDIMScheduler,
  'DDPMScheduler': DDPMScheduler,
  'EulerDiscreteScheduler': EulerDiscreteScheduler,
  'DPMSolverMultistepScheduler': DPMSolverMultistepScheduler,
  'KarrasVeScheduler': KarrasVeScheduler,
  'UniPCMultistepScheduler': UniPCMultistepScheduler
}

def load_sd_pipeline(sd_model: str, scheduler: str):
  assert sd_model in valid_models
  assert scheduler in valid_scheduler_dict.keys()
  sd_model_path = os.path.join(sd15_model_path, sd_model)
  shared_items.sd_pipeline = StableDiffusionPipeline.from_pretrained(sd_model_path, torch_dtype=torch.float16)
  shared_items.sd_pipeline.scheduler = valid_scheduler_dict[scheduler].from_config(shared_items.sd_pipeline.scheduler.config)
  shared_items.sd_pipeline.enable_model_cpu_offload()
  shared_items.sd_pipeline.enable_xformers_memory_efficient_attention()


def load_controlnet_sd_pipeline(sd_model: str, controlnet: str, scheduler: str):
  assert sd_model in valid_models
  assert scheduler in valid_scheduler_dict.keys()
  assert controlnet in valid_controlnet_dict.keys()
  sd_model_path = os.path.join(sd15_model_path, sd_model)
  sd_controlnet_path = os.path.join(controlnet_path, valid_controlnet_dict[controlnet])
  shared_items.sd_pipeline = StableDiffusionControlNetPipeline.from_pretrained(sd_model_path, controlnet=ControlNetModel.from_pretrained(sd_controlnet_path, torch_dtype=torch.float16), torch_dtype=torch.float16)
  shared_items.sd_pipeline.scheduler = valid_scheduler_dict[scheduler].from_config(shared_items.sd_pipeline.scheduler.config)
  shared_items.sd_pipeline.enable_model_cpu_offload()
  shared_items.sd_pipeline.enable_xformers_memory_efficient_attention()

def load_annotator(controlnet: str):
  assert controlnet in valid_controlnet_dict.keys()
  if controlnet == 'canny':
    pass
  elif controlnet == 'openpose':
    shared_items.detector = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
  elif controlnet == 'depth':
    shared_items.detector = MidasDetector.from_pretrained("lllyasviel/ControlNet")
  elif controlnet == 'seg':
    sam_checkpoint = "/content/drive/MyDrive/ANLY521/annotator/sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    device = "cuda"
    shared_items.detector = sam_model_registry[model_type](checkpoint=sam_checkpoint)
  elif controlnet == 'lineart':
    shared_items.detector = LineartDetector.from_pretrained("lllyasviel/Annotators")
  elif controlnet == 'scribble':
    shared_items.detector = HEDdetector.from_pretrained('lllyasviel/Annotators')
  else:
    pass

def load_caption_model():
  shared_items.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
  shared_items.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")