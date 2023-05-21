import os
import json
import requests
import werkzeug
import gradio as gr
from urllib.parse import urlparse
from modules import script_callbacks

sd_path = os.getcwd()
default = "Set as Default"
checkpoint_path = "/models/Stable-diffusion"
hypernetwork_path = "/models/hypernetworks"
embedding_path = "/embeddings"
aestheticembedding_path = "/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings"
vae_path = "/models/VAE"
lora_path = "/models/Lora"
lycoris_path = "/models/LyCORIS"

print("Model Downloader: Checking Directories...")
if not os.path.exists(f"{sd_path}{checkpoint_path}"):
   os.makedirs(f"{sd_path}{checkpoint_path}")
   print ("Model Downloader: Creating Checkpoint Folder")
if not os.path.exists(f"{sd_path}{hypernetwork_path}"):
   os.makedirs(f"{sd_path}{hypernetwork_path}")
   print ("Model Downloader: Creating Hypernetwork Folder")
if not os.path.exists(f"{sd_path}{embedding_path}"):
   os.makedirs(f"{sd_path}{embedding_path}")
   print ("Model Downloader: Creating TextualInversion/Embeddings Folder")
if not os.path.exists(f"{sd_path}{aestheticembedding_path}"):
   os.makedirs(f"{sd_path}{aestheticembedding_path}")
   print ("Model Downloader: Creating AestheticGradient Folder")
if not os.path.exists(f"{sd_path}{vae_path}"):
   os.makedirs(f"{sd_path}{vae_path}")
   print ("Model Downloader: Creating VAE Folder")
if not os.path.exists(f"{sd_path}{lora_path}"):
   os.makedirs(f"{sd_path}{lora_path}")
   print ("Model Downloader: Creating LoRA Folder")
if not os.path.exists(f"{sd_path}{lycoris_path}"):
   os.makedirs(f"{sd_path}{lycoris_path}")
   print ("Model Downloader: Creating LyCORIS Folder")
else:
     pass 
print("Model Downloader: all Directories already Created.")

def folder(content_type):
    if content_type == "Checkpoint":
       return gr.Textbox.update(value=checkpoint_path)
    elif content_type == "Hypernetwork":
         return gr.Textbox.update(value=hypernetwork_path)
    elif content_type == "TextualInversion/Embedding":
         return gr.Textbox.update(value=embedding_path)
    elif content_type == "AestheticGradient":
         return gr.Textbox.update(value=aestheticembedding_path)
    elif content_type == "VAE":
         return gr.Textbox.update(value=vae_path)
    elif content_type == "LoRA":
         return gr.Textbox.update(value=lora_path)
    elif content_type == "LyCORIS(LoCon/LoHA)":
         return gr.Textbox.update(value=lycoris_path)

def get_filename_from_url(url=None):
    if url is None:
       return None
    else:
         try:
             with requests.get(url, stream=True) as req:
                  if content_disposition := req.headers.get("Content-Disposition"):
                     param, options = werkzeug.http.parse_options_header(content_disposition)
                     if param == 'attachment' and (filename := options.get('filename')):
                        f = filename.replace(" ", "_")
                        return f
                  path = urlparse(req.url).path
                  n = path[path.rfind('/') + 1:]
                  name = n.replace(" ", "_")
                  return name
         except:
                return default

def change_filename(filename1, filename):
    if filename1 == "Use original Filename from the Source":
       return gr.Textbox(filename).update(visible=False)
    elif filename1 == "Create New Filename(Recomended)":
         return gr.Textbox(filename).update(visible=True)

def combine(url, content_type1, filename):
    global pathname
    pathname = os.path.splitext(filename)[0]
    return gr.Textbox.update(value=f"aria2c -c -x 16 -s 16 -k 1M {url} -d {sd_path}{content_type1}/{pathname} -o {filename}")

def info_update(url, content_type1, filename, info):
    return gr.Markdown.update(f"<p><b>URL</b>:  {url} <br> <b>Folder Path</b>:  {content_type1} <br> <b>File Name</b>:  {filename} <br> <b>Preview Model</b>:</p>")

def get_image_from_url(url):
    convert = url.replace("download/models", "v1/model-versions")
    civitai = "https://image.civitai.com/"
    try:
        with requests.get(convert) as req:
             j = req.json()
             r = json.dumps(j)
             start = r.find(civitai) + len(civitai)
             end = r.find('"', start)
             global img_url
             img_url = f'{civitai}{r[start:end]}'
             return gr.Image.update(value=img_url)
    except:
           return gr.Image.update(value=f'{sd_path}/html/card-no-preview.png')

def show_download(filename):
    return gr.Button.update(visible=True), gr.Textbox.update(value= "Ready", visible=True)

success = "Download Completed, Saved in:"
exist = "File Already Exist in:"

def run(command, content_type1, filename):
    if not os.path.exists(f"{sd_path}{content_type1}/{pathname}/{filename}"):
       os.popen(command)
       return success
    else:
         return exist

def run_image(image_url, content_type1, filename):
    imgname = f"{pathname}.preview.png"
    if not os.path.exists(f"{sd_path}{content_type1}/{pathname}/{imgname}"):
       os.popen(f"aria2c {img_url} -d {sd_path}{content_type1}/{pathname} -o {imgname}")
       print(f"{success} {sd_path}{content_type1}/{pathname}")
       return f"{success} {sd_path}{content_type1}/{pathname}"
    else:
         print(f"{exist} {sd_path}{content_type1}/{pathname}")
         return f"{exist} {sd_path}{content_type1}/{pathname}"

def on_ui_tabs():
    with gr.Blocks() as downloader:    
         with gr.Row():
              with gr.Column(scale=2):
                   content_type = gr.Radio(label="1. Choose Content type", choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "LoRA", "LyCORIS(LoCon/LoHA)"])
                   content_type1 = gr.Textbox(visible=False)
                   content_type.change(folder, content_type, content_type1)
         with gr.Row():
              url = gr.Textbox(label="2. Put Link Download Below", max_lines=1, placeholder="Type/Paste URL Here")
              url.style(show_copy_button=True)
         with gr.Row():
              filename1 = gr.Radio(label="Setting Filename", choices=["Use original Filename from the Source", "Create New Filename(Recomended)"], type="value", value="Use original Filename from the Source")
         with gr.Row():
              filename = gr.Textbox(label="3. Create new Filename", placeholder="Type/Paste Filename.extension Here", visible=False, interactive=True)
              filename1.change(change_filename, [filename1, filename], filename)
              commands = gr.Textbox(value=f"aria2c -c -x 16 -s 16 -k 1M", label="Information Command", visible=False, interactive=False)
         with gr.Row():
              with gr.Column():
                   info = gr.Markdown(value="<p><b>URL</b>: <br> <b>Folder Path</b>: <br> <b>File Name</b>:<br> <b>Preview Model</b>:</p>", label="Information")
                   image = gr.Image(value=f"{sd_path}/html/card-no-preview.png", show_label=False)
                   image.style(width=256, height=384)
              content_type1.change(combine, [url, content_type1, filename], commands)
              url.change(combine, [url, content_type1, filename], commands)
              url.change(get_filename_from_url, url, filename)
              url.change(get_image_from_url, url, image)
              filename.change(combine, [url, content_type1, filename], commands)
              content_type1.change(info_update, [url, content_type1, filename], info)
              url.change(info_update, [url, content_type1, filename], info)
              filename.change(info_update, [url, content_type1, filename], info)
              with gr.Column():
                   download_btn = gr.Button("Start Download", visible=False, variant="primary")
                   out_text = gr.Textbox(label="Download Result", placeholder="Result", visible=False, show_progress=True)
                   filename.change(show_download, filename, [download_btn, out_text])
                   download_btn.click(run, commands, out_text)
                   download_btn.click(run_image, [url, content_type1, filename], out_text)
                   url.submit(run, commands, out_text)
                   url.submit(run_image, [url, content_type1, filename], out_text)
                   filename.submit(run, commands, out_text)
                   filename.submit(run_image, [url, content_type1, filename], out_text)

    downloader.queue(concurrency_count=5)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
