from typing import Union, List, Any
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, StableDiffusionPipeline

class shared:
  sd_pipeline: Union[StableDiffusionControlNetPipeline, StableDiffusionPipeline, None]
  detector: Any
  sampler: Any

shared_items = shared()