from fastapi import FastAPI, Response, UploadFile, File, Form, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated, Union, Optional
import shutil
import PIL
from PIL import Image
import io
import os
import time
from request_type import modelselection_request, gpthelp_request, imagegeneration_nocontrol_request#, imagegeneration_usecontrol_request
import openai
from fastapi.staticfiles import StaticFiles
from load import check_sd_models, check_controlnets, check_schedulers
from load import load_sd_pipeline, load_controlnet_sd_pipeline, load_annotator, load_caption_model
from img_generate import generate_img, params
from reference_generate import generate_reference
from caption import image_captioning

organization = 'org-Xt3o1oIa9ke1kVNz87ZylhBw'
keys =  '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'
openai.organization = organization
openai.api_key = keys

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.global_is_processing = 'False'
app.global_gpthelp_result = ''
app.global_textgeneration_result = ''
app.global_captioning_result = ''
app.current_sdmodel = 'None'
app.current_controlnet = 'None'
app.current_scheduler = 'None'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/model_selection/')
async def root(modelselection: modelselection_request, background_tasks: BackgroundTasks):
    app.global_is_processing = 'True'
    background_tasks.add_task(async_load_model, modelselection)
    return {'msg': 'model_selection is processing'}

@app.post('/gpthelp/')
async def root(prompt: gpthelp_request, background_tasks: BackgroundTasks):
    app.global_is_processing = 'True'
    background_tasks.add_task(asycn_gpthelp, prompt)
    return {'msg': 'gpthelp is processing'}

@app.post('/image_preprocessing/')
async def root(refer_img: Annotated[UploadFile, File()], background_tasks: BackgroundTasks):
    refer_img_content= refer_img.file.read()
    img = Image.open(io.BytesIO(refer_img_content))
    app.global_is_processing = 'True'
    background_tasks.add_task(async_preprocess_image, img)
    return {'msg': 'image_preprocessing is processing'}

@app.post('/image_generation/no_controlnet/')
async def root(request: imagegeneration_nocontrol_request, background_tasks: BackgroundTasks):
    # refer_img_content= refer_img.file.read()
    # img = Image.open(io.BytesIO(refer_img_content))
    app.global_is_processing = 'True'
    background_tasks.add_task(async_generate_image_nocontrol, request)
    return {'msg': 'image_generation is processing'}

@app.post('/image_generation/use_controlnet/')
async def root(refer_img: Annotated[UploadFile, File()], prompt: Annotated[str, Form()], neg_prompt: Annotated[str, Form()], 
                cfg_scale: Annotated[float, Form()], inference_steps: Annotated[int, Form()], num_samples: Annotated[int, Form()],
                width: Annotated[int, Form()], height: Annotated[int, Form()], 
                background_tasks: BackgroundTasks= BackgroundTasks()):
    print('### fastapi')
    print(prompt)
    print(neg_prompt)
    refer_img_content= refer_img.file.read()
    img = Image.open(io.BytesIO(refer_img_content))
    app.global_is_processing = 'True'
    background_tasks.add_task(async_generate_image_usecontrol, img, prompt, neg_prompt, cfg_scale,
                                inference_steps, num_samples, width, height)
    return {'msg': 'image_generation is processing'}

@app.post('/captioning/')
async def root(refer_img: Annotated[UploadFile, File()], background_tasks: BackgroundTasks):
    refer_img_content= refer_img.file.read()
    # print(refer_img_content)
    img = Image.open(io.BytesIO(refer_img_content))
    app.global_is_processing = 'True'
    background_tasks.add_task(async_captioning, img)
    return {'msg': 'captioning is processing'}

@app.post('/text_generation/')
async def root(prompt: gpthelp_request, background_tasks: BackgroundTasks):
    app.global_is_processing = 'True'
    background_tasks.add_task(async_generate_text, prompt)
    return {'msg': 'text_generation is processing'}

@app.get('/generated/result_image/')
async def root():
    filenames = os.listdir('/tmp/')
    q = {}
    for i, filename in enumerate(filenames):
      url_key = 'sample_' + str(i) + '.png'
      url_value = os.path.join('/tmp', filename)
      q[url_key] = url_value
    return q

@app.get('/generated/annotated_image/')
async def root():
    return {'returned_image_url': '/imgs/no-image.jpg'}

@app.get('/tmp/{filename}')
async def _(filename):
    with open('./tmp/'+filename, 'rb') as f:
        image_bytes = f.read()
        headers = {'Content-Disposition': 'attachment; filename="hiahia.png"'}

        return Response(content=image_bytes, media_type="image/png", headers=headers)

@app.get('/state/')
async def root():
    return {'is_processing': app.global_is_processing}


@app.get('/gpthelp/result')
async def root():
    return {'returned_text': app.global_gpthelp_result}

@app.get('/text_generation/result')
async def root():
    return {'returned_text': app.global_textgeneration_result}


@app.get('/captioning/result')
async def root():
    return {'returned_text': app.global_captioning_result}

@app.get('/refresh/')
async def root():
    return {'sdmodel': app.current_sdmodel, 'controlnet': app.current_controlnet, 'scheduler': app.current_scheduler}

def async_preprocess_image(raw_image: PIL.Image.Image):
    refer_img = generate_reference(raw_image)
    refer_img.save('./tmp/annotated_image.png')
    app.global_is_processing = 'False'
    return 

def asycn_gpthelp(prompt: gpthelp_request):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': prompt.prompt}
        ]
    )
    app.global_gpthelp_result = response['choices'][0].message.content
    print(app.global_gpthelp_result)
    app.global_is_processing = 'False'
    return

def async_generate_text(prompt: gpthelp_request):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': prompt.prompt}
        ]
    )
    app.global_textgeneration_result = response['choices'][0].message.content

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': 'Please give me hashtags of the following paragraphs:\n' + app.global_textgeneration_result}
        ]
    )
    hashtags = response['choices'][0].message.content
    app.global_textgeneration_result = app.global_textgeneration_result + '\n' + hashtags
    print(app.global_textgeneration_result)
    app.global_is_processing = 'False'
    return

def async_load_model(options: modelselection_request):
    if options.controlnet == 'None':
        app.current_sdmodel = options.sdmodel
        app.current_controlnet = 'None'
        app.current_scheduler = options.scheduler
        load_sd_pipeline(options.sdmodel, options.scheduler)
    else:
        app.current_sdmodel = options.sdmodel
        app.current_controlnet = options.controlnet
        app.current_scheduler = options.scheduler
        load_controlnet_sd_pipeline(options.sdmodel, options.controlnet, options.scheduler)
        load_annotator(options.controlnet)
    load_caption_model()
    app.global_is_processing = 'False'
    return 

def async_generate_image_nocontrol(request: imagegeneration_nocontrol_request):
    one_row = params(prompt=request.prompt, neg_prompt=request.neg_prompt, num_steps=request.inference_steps,
    num_imgs=request.num_samples, height=request.height,  width=request.width, 
    cfg_scale=request.cfg_scale, refer_image=None)
    imgs = generate_img(one_row)
    for i in range(len(imgs)):
        imgs[i].save('./tmp/sample_' + str(i) + '.png')
    app.global_is_processing = 'False'
    return

def async_generate_image_usecontrol(refer_img: PIL.Image.Image, prompt: str, neg_prompt: str, 
                cfg_scale: float, inference_steps: int, num_samples: int,
                width: int, height: int):
    print('###async')
    print(prompt)
    print(neg_prompt)
    one_row = params(prompt=prompt, neg_prompt=neg_prompt, num_steps=inference_steps,
    num_imgs=num_samples, height=height,  width=width, 
    cfg_scale=cfg_scale, refer_image=refer_img)
    imgs = generate_img(one_row)
    for i in range(len(imgs)):
        imgs[i].save('./tmp/sample_' + str(i) + '.png')
    app.global_is_processing = 'False'
    return

def async_captioning(raw_image: PIL.Image.Image):
    app.global_captioning_result = image_captioning(raw_image)
    app.global_is_processing = 'False'
    return