const url = 'http://127.0.0.1:8000/'
cur_sdmodel = 'None'
cur_controlnet = 'None'
cur_scheduler = 'None'


document.getElementById('controlnet-part').style.display = 'none'


/// sleep function
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/// get buttons
refresh_button = document.getElementById('model-selection-refresh')
model_selection_submit = document.getElementById('model-selection-submit')
image_processing_submit = document.getElementById('image-preprocessing-submit')
image_generation_submit = document.getElementById('img-params-submit')
chatgpt_help_submit = document.getElementById('gpt-prompt-submit-img')
blip_help_submit = document.getElementById('image-captioning-submit')
post_prompt_submit = document.getElementById('post-prompt-submit')
post_submit = document.getElementById('post-submit')
/// pause button
function pause(){
    refresh_button.disabled = true

    model_selection_submit.disabled = true
    model_selection_submit.innerHTML = 'Processing...'

    image_processing_submit.disabled = true
    image_processing_submit.innerHTML = 'Processing...'

    image_generation_submit.disabled = true
    image_generation_submit.innerHTML = 'Processing...'

    chatgpt_help_submit.disabled = true
    chatgpt_help_submit.innerHTML = 'Processing...'

    blip_help_submit.disabled = true
    blip_help_submit.innerHTML = 'Processing...'

    post_prompt_submit.disabled = true
    post_prompt_submit.innerHTML = 'Processing...'

    post_submit.disabled = true
    post_submit.innerHTML = 'Processing...'
}
/// resume button
function resume(){
    refresh_button.disabled = false

    model_selection_submit.disabled = false
    model_selection_submit.innerHTML = 'submit & load models'

    image_processing_submit.disabled = false
    image_processing_submit.innerHTML = 'submit image to be preprocessed'

    image_generation_submit.disabled = false
    image_generation_submit.innerHTML = 'submit & generating images'

    chatgpt_help_submit.disabled = false
    chatgpt_help_submit.innerHTML = 'submit'

    blip_help_submit.disabled = false
    blip_help_submit.innerHTML = 'submit'

    post_prompt_submit.disabled = false
    post_prompt_submit.innerHTML = 'submit'

    post_submit.disabled = false
    post_submit.innerHTML = 'post instagram'
}

/// model-selection
    document.getElementById('model-selection-submit').addEventListener('click', async function (event) {
        // get model names
        cur_sdmodel = document.getElementById('stable-diffusion-models').value
        cur_controlnet = document.getElementById('controlnet-models').value
        cur_scheduler = document.getElementById('scheduler-models').value

        // disable buttons
        pause()

        // send to backend
        let resp = await fetch(
            url + 'model_selection/',
            {
                method: 'POST',
                body: JSON.stringify({
                    'sdmodel': cur_sdmodel,
                    'controlnet': cur_controlnet,
                    'scheduler': cur_scheduler
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
        // wait for processing and check for state
        while(true){
            await sleep(2000)
            let state = await fetch(
                url + 'state/',
                {
                    method: 'GET'
                }
            )
            let state_json = await state.json()
            if (state_json['is_processing'] == 'False'){
                break
            }
        }
        // enable buttons
        resume()
        /// check if controlnet is None
         if(cur_controlnet == 'None'){
            document.getElementById('controlnet-part').style.display = 'none';
        }else{
            document.getElementById('controlnet-part').style.display = 'block';
        }
    })

/// image-preprocessing
    document.getElementById('image-preprocessing-submit').addEventListener('click', async function (event) {
        // check file
        if( document.getElementById("image-preprocessing").files.length == 0 ){
            alert('please load an image to be processed')
        }else{
            // get file

            let file = document.getElementById('image-preprocessing').files[0];
            // send to backend as multipart
            let formData = new FormData();
            formData.append('refer_img', file);
            // disable buttons
            pause()
        
            let resp = await fetch(
                url + 'image_preprocessing/',
                {
                    method: 'POST',
                    body: formData,
                }
            )
            /// wait for processing and check for state
            while(true){
                await sleep(2000)
                let state = await fetch(
                    url + 'state/',
                    {
                        method: 'GET'
                    }
                )
                let state_json = await state.json()
                if (state_json['is_processing'] == 'False'){
                    break
                }
            }

            /// download image
            let returned = await fetch(
                url + 'generated/annotated_image/',
                {
                    method: 'GET',
                }
            )

            let returned_json = await returned.json()
            let returned_image_url = returned_json['returned_image_url']

            // download image
            let a = document.createElement('a')
            a.href = returned_image_url
            a.download = 'returned_image.png'
            a.click()

            // let image = document.createElement('img')
            document.getElementById('imageContainer-preprocessed').firstChild.src = url + returned_image_url.slice(1)
            // image.style.height = '200px'
            // document.getElementById('image-preprocessing-container').appendChild(image)

            // recover buttons
            resume()
        }
})

/// image generation
document.getElementById('img-params-submit').addEventListener('click', async function (event) {
    // check file
    if( cur_sdmodel == 'None' ){
        alert('please load a sd model')
    }else if(cur_controlnet != 'None' && document.getElementById("image-preprocessed").files.length == 0){
        alert('please load a reference/processed image')
    }else{
        // get file
        if(cur_controlnet == 'None'){
            let prompt = document.getElementById('prompt-img').value
            let neg_prompt = document.getElementById('neg-prompt-img').value
            let cfg_scale = document.getElementById('cfg-range').value
            let inference_steps = document.getElementById('step-range').value
            let num_samples = document.getElementById('num-range').value
            let width = document.getElementById('width-range').value
            let height = document.getElementById('height-range').value
            // check prompt
            if(prompt.trim() == ''){
                alert('please input a prompt')
                return
            }else{
            // disable buttons
                pause()
                let resp = await fetch(
                    url + 'image_generation/no_controlnet/',
                    {
                        method: 'POST',
                        body: JSON.stringify({
                            'prompt': prompt,
                            'neg_prompt': neg_prompt,
                            'cfg_scale': cfg_scale,
                            'inference_steps': inference_steps,
                            'num_samples': num_samples,
                            'width': width,
                            'height': height
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                )
            }
        }else{
            let prompt = document.getElementById('prompt-img').value
            let neg_prompt = document.getElementById('neg-prompt-img').value
            let cfg_scale = document.getElementById('cfg-range').value
            let inference_steps = document.getElementById('step-range').value
            let num_samples = document.getElementById('num-range').value
            let width = document.getElementById('width-range').value
            let height = document.getElementById('height-range').value
            let file = document.getElementById('image-preprocessed').files[0];
            // check prompt
            if(prompt.trim() == ''){
                alert('please input a prompt')
                return
            }else{
                // send to backend as multipart
                let formData = new FormData();
                formData.append('refer_img', file);
                formData.append('prompt', prompt);
                formData.append('neg_prompt', neg_prompt);
                formData.append('cfg_scale', cfg_scale);
                formData.append('inference_steps', inference_steps);
                formData.append('num_samples', num_samples);
                formData.append('width', width);
                formData.append('height', height);
                // disable buttons
                pause()
            
                let resp = await fetch(
                    url + 'image_generation/use_controlnet/',
                    {
                        method: 'POST',
                        body: formData,
                    }
                )
            }
        }
        /// wait for processing and check for state
        while(true){
            await sleep(2000)
            let state = await fetch(
                url + 'state/',
                {
                    method: 'GET'
                }
            )
            let state_json = await state.json()
            if (state_json['is_processing'] == 'False'){
                break
            }
        }

        /// download image
        let returned = await fetch(
            url + 'generated/result_image/',
            {
                method: 'GET',
            }
        )

        let returned_json = await returned.json()
        let returned_image_url = returned_json['returned_image_url']

        // download image
        let a = document.createElement('a')
        a.href = returned_image_url
        a.download = 'returned_image.png'
        a.click()

        // let image = document.createElement('img')
        document.getElementById('resultImageContainer').firstChild.src = url + returned_image_url.slice(1)
        // image.style.height = '200px'
        // document.getElementById('image-preprocessing-container').appendChild(image)

        // recover buttons
        resume()
    }
})

///// chatgpt prompt help
document
  .getElementById("gpt-prompt-submit-img")
  .addEventListener("click", async function () {
    var prompt = document.getElementById("gpt-prompt-img").value;

    if(prompt.trim() == ''){
        alert('Please enter a prompt')
    }else{
      var returned = document.getElementById("gpt-prompt-returned");

      const data = { 'prompt': prompt };
      pause()

    let response = await fetch(url + 'gpthelp/', {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    /// wait for processing and check for state
    while(true){
        await sleep(2000)
        let state = await fetch(
            url + 'state/',
            {
                method: 'GET'
            }
        )
        let state_json = await state.json()
        if (state_json['is_processing'] == 'False'){
            break
        }
    }
    /// fetch returned text
    let result = await fetch(
        url + 'gpthelp/result',
        {
            method: 'GET',
        }
    )

    let returned_json = await result.json()
    let returned_text = await returned_json['returned_text']
    document.getElementById('gpt-prompt-returned').value = await returned_text
    resume()
    }
  });

///// text generation
document
  .getElementById("post-prompt-submit")
  .addEventListener("click", async function () {
    var prompt = document.getElementById("post-prompt").value;

    if(prompt.trim() == ''){
        alert('Please enter a prompt')
    }else{

      const data = { 'prompt': prompt };
      pause()

    let response = await fetch(url + 'text_generation/', {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    /// wait for processing and check for state
    while(true){
        await sleep(2000)
        let state = await fetch(
            url + 'state/',
            {
                method: 'GET'
            }
        )
        let state_json = await state.json()
        if (state_json['is_processing'] == 'False'){
            break
        }
    }
    /// fetch returned text
    let result = await fetch(
        url + 'text_generation/result',
        {
            method: 'GET',
        }
    )

    let returned_json = await result.json()
    let returned_text = await returned_json['returned_text']
    document.getElementById('post-text').value = await returned_text
    resume()
    }
  });


  /// captioning
  document.getElementById('image-captioning-submit').addEventListener('click', async function (event) {
    // check file
    if( document.getElementById("image-captioning").files.length == 0 ){
        alert('please load an image to be captioned')
    }else{
        // get file
        let file = document.getElementById('image-captioning').files[0];
        // send to backend as multipart
        let formData = new FormData();
        formData.append('refer_img', file);
        // disable buttons
        pause()
    
        let resp = await fetch(
            url + 'captioning/',
            {
                method: 'POST',
                body: formData,
            }
        )
        /// wait for processing and check for state
        while(true){
            await sleep(2000)
            let state = await fetch(
                url + 'state/',
                {
                    method: 'GET'
                }
            )
            let state_json = await state.json()
            if (state_json['is_processing'] == 'False'){
                break
            }
        }

        /// fetch returned text
        let result = await fetch(
            url + 'captioning/result',
            {
                method: 'GET',
            }
        )

        let returned_json = await result.json()
        let returned_text = await returned_json['returned_text']
        document.getElementById('returned-captions').value = await returned_text
        resume()
    }
})