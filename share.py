from typing import Union, List, Any
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, StableDiffusionPipeline
import dataclasses

@dataclasses.dataclass
class shared:
  sd_pipeline: Union[StableDiffusionControlNetPipeline, StableDiffusionPipeline, None] = None
  detector: Any = None
  controlnet: Union[str, None] = None
  caption_model: Any = None
  caption_processor: Any = None
shared_items = shared()