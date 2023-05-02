# Social Media AI-Assistance
Team Member: Minglei Cai, Zezhen Liu, Jamie Zhang, Shihong Zhou

Report Website: https://kianakaslana648.github.io/anly521-final-project/

## Project Goals
Social media has become an important part of campus life at Georgetown University, which not only connects the school with students, faculty, and alumni but promotes campus events, programs, and initiatives. These social media accounts, ranging from offices to student organizations, often post festival information, announcements, and updates. However, managing these accounts can be challenging. The content needs to be both informative and fun while keeping up with the high volume of daily posts. Sometimes topics can often be similar, but it still requires creativity to keep the audience engaged.

While different kinds of deep-learning-based generative models emerge, we aim at incorporating generative models in domains of NLP (Natural Language Processing) and CV (Computer Vision) to help with content composition of social media posts.

## Main Parts
### NLP
We use state-of-the-art text-generation model ChatGPT (GPT-3.5-turbo) as our text content generator, hashtag summarizer and stable diffusion prompt helper.

### CV
We compose stable diffusion pipelines using **Huggingface** APIs (pipelines with controlnet or without controlnets) and use these sd pipelines as our image generator.

We download our stable diffusion models from the open-source website https://civitai.com/. We download our controlnets and corresponding annotators from https://huggingface.co/lllyasviel/ControlNet.

### Deploy
As students without high-RAM GPUs, we use **Google Colab Pro** as our deploy space, **Google One** for model storing.

## Usage
* Upload **521_project.ipynb** 
* Download .safetensors .ckpt models from https://civitai.com/.
* Download controlnet models from https://huggingface.co/lllyasviel/ControlNet
* Transform safetensors/ckpt models into **Huggingface Diffusers** (Tutorial notebook **sd_transform_test.ipynb**); save diffusers and controlnets
* Configure your stable diffusion model path and controlnet path in **load.py**
* Configure your **OpenAI** API in **main.py**
* Run **521_project.ipynb** in **Google Colab Pro**
* Go to the address given by
```
  from google.colab.output import eval_js
  print(eval_js("google.colab.kernel.proxyPort(8000)"))
```
(which is the address of FastAPI backend)
```
+ '/static/index.html'
```

(which is a local frontend)

Then you are at the front webpage.

### Thanks
* SD part largely inspired by the great project https://github.com/AUTOMATIC1111/stable-diffusion-webui. 
* Thanks to all the researchers and model-trainers, we could complete our course project and make some contributions to our university.
