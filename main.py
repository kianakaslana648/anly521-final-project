from fastapi import FastAPI, Response, UploadFile, File, Form, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated, Union, Optional
import shutil
import PIL
from PIL import Image
import io
import time
from request_type import modelselection_request, gpthelp_request, imagegeneration_nocontrol_request#, imagegeneration_usecontrol_request
import openai

organization = 'xxxxxxxxx'
keys =  'xxxxxxxx'
openai.organization = organization
openai.api_key = keys

app = FastAPI()

app.global_is_processing = 'False'
app.global_gpthelp_result = ''
app.global_textgeneration_result = ''
app.global_captioning_result = 'abc'

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
async def root(refer_img: UploadFile = File(...), prompt: Optional[str] = None, neg_prompt: Optional[str] = None, 
                cfg_scale: float = Form(...), inference_steps: int = Form(...), num_samples: int = Form(...),
                width: int = Form(...), height: int = Form(...), 
                background_tasks: BackgroundTasks= BackgroundTasks()):
# async def root(request: imagegeneration_usecontrol_request, background_tasks: BackgroundTasks):
    # refer_img_content= refer_img.file.read()
    # img = Image.open(io.BytesIO(refer_img_content))
    app.global_is_processing = 'True'
    background_tasks.add_task(async_generate_image_usecontrol, refer_img, prompt, neg_prompt, cfg_scale,
                                inference_steps, num_samples, width, height)
    return {'msg': 'image_generation is processing'}

@app.post('/captioning/')
async def root(refer_img: Annotated[UploadFile, File()], background_tasks: BackgroundTasks):
    refer_img_content= refer_img.file.read()
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
    return {'returned_image_url': '/imgs/no-image.jpg'}

@app.get('/generated/annotated_image/')
async def root():
    return {'returned_image_url': '/imgs/no-image.jpg'}

@app.get('/imgs/{filename}')
async def _(filename):
    with open('./imgs/'+filename, 'rb') as f:
        image_bytes = f.read()
        return Response(content=image_bytes, media_type="image/png")

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

def async_preprocess_image(raw_image: PIL.Image.Image):
    time.sleep(10)
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
    app.global_is_processing = 'False'
    return

def async_load_model(options: modelselection_request):
    time.sleep(10)
    app.global_is_processing = 'False'
    return 

def async_generate_image_nocontrol(request: imagegeneration_nocontrol_request):
    time.sleep(10)
    app.global_is_processing = 'False'
    return

def async_generate_image_usecontrol(refer_img: UploadFile = File(...), prompt: Optional[str] = None, neg_prompt: Optional[str] = None, 
                cfg_scale: float = Form(...), inference_steps: int = Form(...), num_samples: int = Form(...),
                width: int = Form(...), height: int = Form(...)):
    time.sleep(10)
    app.global_is_processing = 'False'
    return

def async_captioning(raw_image: PIL.Image):
    time.sleep(10)
    app.global_is_processing = 'False'
    return