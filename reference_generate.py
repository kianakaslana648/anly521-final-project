from detect import canny_detect, openpose_detect, depth_detect, seg_detect, lineart_detect, scribble_detect, lineartanime_detect
import share
import PIL

def generate_reference(img: PIL.Image.Image):
  if share.shared_items.controlnet == 'canny':
    return canny_detect([img])[0]
  elif share.shared_items.controlnet == 'openpose':
    return openpose_detect([img])[0]
  elif share.shared_items.controlnet == 'depth':
    return depth_detect([img])[0]
  elif share.shared_items.controlnet == 'seg':
    return seg_detect([img])[0]
  elif share.shared_items.controlnet == 'lineart':
    return lineart_detect([img])[0]
  elif share.shared_items.controlnet == 'scribble':
    return scribble_detect([img])[0]
  elif share.shared_items.controlnet == 'lineartanime':
    return lineartanime_detect([img])[0]
  else:
    pass
