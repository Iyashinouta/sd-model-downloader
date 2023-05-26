import os
import requests
import gradio as gr
from urllib.parse import urlparse
from modules import script_callbacks

sd_path = os.getcwd()
no_prev = f"{sd_path}/html/card-no-preview.png"
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
    global downloadpath
    global namepath
    global modelname
    downloadpath = None
    namepath = None
    modelname = None
    if content_type == "Checkpoint":
       downloadpath = checkpoint_path
       return downloadpath
    elif content_type == "Hypernetwork":
         downloadpath = hypernetwork_path
         return downloadpath
    elif content_type == "TextualInversion/Embedding":
         downloadpath = embedding_path
         return downloadpath
    elif content_type == "AestheticGradient":
         downloadpath = aestheticembedding_path
         return downloadpath
    elif content_type == "VAE":
         downloadpath = vae_path
         return downloadpath
    elif content_type == "LoRA":
         downloadpath = lora_path
         return downloadpath
    elif content_type == "LyCORIS(LoCon/LoHA)":
         downloadpath = lycoris_path
         return downloadpath

def get_data_from_url(url, name, image, download_btn, out_text):
    global namepath
    global modelurl
    global modelname
    global imgurl
    global imgname
    namepath = None
    modelname = None
    try:
        if url.find("https://civitai.com/")!=-1:
           convert = "" + url.replace("download/models", "v1/model-versions")
           req = requests.get(convert, stream=True)
           metadata1 = req.json()['files'][0]['name']
           metadata1.replace(" ", "_")
           metadata2 = req.json()['images'][0]['url']
           modelname = metadata1
           namepath = os.path.splitext(metadata1)[0]
           imgurl = metadata2
           imgname = f"{namepath}.preview.png"
           return gr.Textbox(name).update(value=modelname), gr.Image(image).update(value=imgurl), gr.Button(download_btn).update(visible=True, variant="primary"), gr.Textbox(out_text).update(value= "Ready", visible=True)
        else:
             parse = urlparse(url).path
             metadata1 = parse[parse.rfind('/') + 1:]
             metadata1.replace(" ", "_")
             modelname = metadata1
             namepath = os.path.splitext(metadata1)[0]
             imgurl = no_prev
             imgname = f"{namepath}.preview.png"
             return gr.Textbox(name).update(value=modelname), gr.Image(image).update(value=imgurl), gr.Button(download_btn).update(visible=True, variant="primary"), gr.Textbox(out_text).update(value= "Ready", visible=True)
    except:
           imgurl = no_prev
           return gr.Image(image).update(value=imgurl)

def info_update(url, content_type):
    modelurl = "" + url
    return gr.Markdown.update(f"<font size=2><p><b>Model Information :</b><br><b>URL</b>:  {modelurl} <br> <b>Folder Path</b>:  {downloadpath}/{namepath} <br> <b>File Name</b>:  {modelname} <br> <b>Preview Model</b>:</p>")

def show_filename(filename1):
    if filename1 == "Use original Filename from the Source(Recomended)":
       return gr.Textbox.update(visible=False)
    elif filename1 == "Create New Filename":
         return gr.Textbox.update(visible=True)

def start_downloading(download_btn, url, name):
    modelurl = "" + url
    command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --input-file model.txt -d {sd_path}{downloadpath}/{namepath}"
    complete1 = f"SUCCESS: Download Completed, Saved to\n[{sd_path}{downloadpath}/{namepath}]"
    complete2 = f"ERROR: File Already Exist in\n[{sd_path}{downloadpath}/{namepath}]"
    with open("model.txt", "w") as w:
         if not modelurl.find("https://civitai.com/")!=-1:
            w.write(f"{modelurl}\n out={modelname}")
         else:
              w.write(f"{modelurl}\n out={modelname}\n{imgurl}\n out={imgname}")
    if not os.path.exists(f"{sd_path}{downloadpath}/{namepath}"):
       line1 = os.popen(command)
       for l in line1:
           l = l.rstrip()
           yield complete1
       print(complete1)
    else:
         yield complete2
         print(complete2)

def back(download_btn):
    return gr.Button.update(visible=True, variant="secondary")

def on_ui_tabs():
    with gr.Blocks() as downloader:    
         with gr.Row():
              with gr.Column(scale=2):
                   content_type = gr.Radio(label="1. Choose Content type", choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "LoRA", "LyCORIS(LoCon/LoHA)"])
         with gr.Row():
              url = gr.Textbox(label="2. Put Link Download Below", max_lines=1, placeholder="Type/Paste URL Here")
              url.style(show_copy_button=True)
         with gr.Row(visible=False):
              filename1 = gr.Radio(label="Setting Filename(please choose original, we're getting bug on 'Create New Filename')", choices=["Use original Filename from the Source(Recomended)", "Create New Filename"], type="value", value="Use original Filename from the Source(Recomended)")
              name = gr.Textbox(label="3. Create new Filename", placeholder="Type/Paste Filename.extension Here", visible=False, interactive=False)
         with gr.Row():
              download_btn = gr.Button("Start Download", visible=False, variant="secondary")
              out_text = gr.Textbox(label="Download Result", placeholder="Result", visible=False, show_progress=True)
         with gr.Row():
              with gr.Column():
                   info = gr.Markdown(value="<font size=2><p><b>Model Information :</b><br><b>URL</b>: <br> <b>Folder Path</b>: <br> <b>File Name</b>:<br> <b>Preview Model</b>:</p>", label="Information")
              with gr.Column():
                   image = gr.Image(value=no_prev, show_label=False)
                   image.style(width=256, height=384)
         with gr.Row():
              github = gr.Markdown(
               """
               <center><font size=2>Having Issue? | <a href=https://github.com/Iyashinouta/sd-model-downloader/issues>Report Here</a>
               """
              )

              filename1.change(show_filename, filename1, name)
              content_type.change(folder, content_type)
              url.change(get_data_from_url, url, [name, image, download_btn, out_text])
              content_type.change(info_update, content_type, info)
              url.change(info_update, [url, name], info)
              download_btn.click(start_downloading, [download_btn, url, name], out_text)
              url.submit(start_downloading, [download_btn, url, name], out_text)
              download_btn.click(back, download_btn, download_btn)
              url.submit(back, url, download_btn)

    downloader.queue(concurrency_count=5)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
