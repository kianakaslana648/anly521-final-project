import share
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, StableDiffusionPipeline
from diffusers import DDIMScheduler, DDPMScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler, KarrasVeScheduler, UniPCMultistepScheduler
import os
import torch
from controlnet_aux import OpenposeDetector, HEDdetector, MidasDetector, LineartDetector, LineartAnimeDetector
from segment_anything import sam_model_registry
from transformers import BlipProcessor, BlipForConditionalGeneration
import gc

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
  'scribble': 'sd-controlnet-scribble',
  'lineartanime': 'sd-controlnet-lineartanime'
}
valid_scheduler_dict = {
  'DDIMScheduler': DDIMScheduler,
  'DDPMScheduler': DDPMScheduler,
  'EulerDiscreteScheduler': EulerDiscreteScheduler,
  'DPMSolverMultistepScheduler': DPMSolverMultistepScheduler,
  'KarrasVeScheduler': KarrasVeScheduler,
  'UniPCMultistepScheduler': UniPCMultistepScheduler
}
def check_controlnets():
  return list(valid_controlnet_dict.keys())
def check_schedulers():
  return list(valid_scheduler_dict.keys())

def load_sd_pipeline(sd_model: str, scheduler: str):
  assert sd_model in valid_models
  assert scheduler in valid_scheduler_dict.keys()
  if share.shared_items.sd_pipeline != None:
    del share.shared_items.sd_pipeline
  if share.shared_items.detector != None:
    del share.shared_items.detector
  sd_model_path = os.path.join(sd15_model_path, sd_model)
  share.shared_items.sd_pipeline = StableDiffusionPipeline.from_pretrained(sd_model_path, torch_dtype=torch.float16)
  share.shared_items.sd_pipeline.scheduler = valid_scheduler_dict[scheduler].from_config(share.shared_items.sd_pipeline.scheduler.config)
  share.shared_items.sd_pipeline.to("cuda")
  gc.collect()
  share.shared_items.sd_pipeline.enable_xformers_memory_efficient_attention()


def load_controlnet_sd_pipeline(sd_model: str, controlnet: str, scheduler: str):
  assert sd_model in valid_models
  assert scheduler in valid_scheduler_dict.keys()
  assert controlnet in valid_controlnet_dict.keys()
  if share.shared_items.sd_pipeline != None:
    del share.shared_items.sd_pipeline
  if share.shared_items.detector != None:
    del share.shared_items.detector
  share.shared_items.controlnet = controlnet
  sd_model_path = os.path.join(sd15_model_path, sd_model)
  sd_controlnet_path = os.path.join(controlnet_path, valid_controlnet_dict[controlnet])
  share.shared_items.sd_pipeline = StableDiffusionControlNetPipeline.from_pretrained(sd_model_path, controlnet=ControlNetModel.from_pretrained(sd_controlnet_path, torch_dtype=torch.float16), torch_dtype=torch.float16)
  share.shared_items.sd_pipeline.scheduler = valid_scheduler_dict[scheduler].from_config(share.shared_items.sd_pipeline.scheduler.config)
  share.shared_items.sd_pipeline.to('cuda')
  # share.shared_items.sd_pipeline.enable_model_cpu_offload()
  share.shared_items.sd_pipeline.enable_xformers_memory_efficient_attention()
  gc.collect()

def load_annotator(controlnet: str):
  assert controlnet in valid_controlnet_dict.keys()
  if controlnet == 'canny':
    pass
  elif controlnet == 'openpose':
    share.shared_items.detector = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
  elif controlnet == 'depth':
    share.shared_items.detector = MidasDetector.from_pretrained("lllyasviel/ControlNet")
  elif controlnet == 'seg':
    pass
    # sam_checkpoint = "/content/drive/MyDrive/ANLY521/annotator/sam_vit_h_4b8939.pth"
    # model_type = "vit_h"
    # device = "cuda"
    # share.shared_items.detector = sam_model_registry[model_type](checkpoint=sam_checkpoint)
  elif controlnet == 'lineart':
    share.shared_items.detector = LineartDetector.from_pretrained("lllyasviel/Annotators")
  elif controlnet == 'scribble':
    share.shared_items.detector = HEDdetector.from_pretrained('lllyasviel/Annotators')
  elif controlnet == 'lineartanime':
    share.shared_items.detector = LineartAnimeDetector.from_pretrained('lllyasviel/Annotators')
  else:
    pass
  if controlnet == 'seg':
    share.shared_items.detector.to('cuda')
  gc.collect()

def load_caption_model():
  share.shared_items.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
  share.shared_items.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
  gc.collect()