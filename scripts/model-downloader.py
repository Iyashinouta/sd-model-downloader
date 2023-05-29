import os
import requests
import argparse
import gradio as gr
from urllib.parse import urlparse
from modules import script_callbacks

sd_path = os.getcwd()
ext = "/extensions"
no_prev = None
addnet_path = None

try:
    from modules.paths_internal import data_path, models_path, extensions_dir
except ImportError:
       from modules.paths import data_path, models_path
       extensions_dir = os.path.join(data_path, 'extensions')

parser = argparse.ArgumentParser()
parser.add_argument("--ckpt-dir", type=str, default=os.path.join(models_path, 'Stable-diffusion'))
parser.add_argument("--vae-dir", type=str, default=os.path.join(models_path, 'VAE'))
parser.add_argument("--embeddings-dir", type=str, default=os.path.join(data_path, 'embeddings'))
parser.add_argument("--hypernetwork-dir", type=str, default=os.path.join(models_path, 'hypernetworks'))
parser.add_argument("--lora-dir", type=str, default=os.path.join(models_path, 'Lora'))
parser.add_argument("--lycoris-dir", type=str, default=os.path.join(models_path, 'LyCORIS'))
args, _ = parser.parse_known_args()

if not os.path.exists(f"{sd_path}/html/card-no-preview.png"):
   try:
       os.system(f"wget -P {data_path}/html https://github.com/AUTOMATIC1111/stable-diffusion-webui/raw/master/html/card-no-preview.png  >/dev/null 2>&1")
   except:
          pass
   no_prev = f"{data_path}/html/card-no-preview.png"
else:
     no_prev = f"{sd_path}/html/card-no-preview.png"
if not os.path.exists(f"{sd_path}{ext}/sd-webui-additional-networks"):
   addnet_path = f"{extensions_dir}/sd-webui-additional-networks"
else:
     addnet_path = f"{sd_path}{ext}/sd-webui-additional-networks"

checkpoint_path = args.ckpt_dir
vae_path = args.vae_dir
embedding_path = args.embeddings_dir
hypernetwork_path = args.hypernetwork_dir
lora_path = args.lora_dir
lycoris_path = args.lycoris_dir

print(f"Model Downloader v1.0.5")
print("Checking Directories...")
if not os.path.exists(checkpoint_path):
   os.makedirs(checkpoint_path)
   print ("Creating Checkpoint Folder")
if not os.path.exists(hypernetwork_path):
   os.makedirs(hypernetwork_path)
   print ("Creating Hypernetwork Folder")
if not os.path.exists(embedding_path):
   os.makedirs(embedding_path)
   print ("Creating TextualInversion/Embeddings Folder")
if not os.path.exists(vae_path):
   os.makedirs(vae_path)
   print ("Creating VAE Folder")
if not os.path.exists(lora_path):
   os.makedirs(lora_path)
   print ("Creating LoRA Folder")
if not os.path.exists(lycoris_path):
   os.makedirs(lycoris_path)
   print ("Creating LyCORIS Folder")
else:
     pass
print("all Directories already Created.")

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
    elif content_type == "VAE":
         downloadpath = vae_path
         return downloadpath
    elif content_type == "LoRA":
         downloadpath = lora_path
         return downloadpath
    elif content_type == "LyCORIS(LoCon/LoHA)":
         downloadpath = lycoris_path
         return downloadpath

def get_data_from_url(url, image, download_btn, out_text, info):
    global downloadpath
    global namepath
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
           imgurl = req.json()['images'][0]['url']
           modelname = metadata1.replace(" ", "_")
           namepath = os.path.splitext(metadata1)[0]
           imgname = f"{namepath}.preview.png"
           markdown2 = f"""
                       <font size=2><p>
                       <b>Model Information :</b><br>
                       <b>URL :</b>   {url}<br>
                       <b>Folder Path :</b>   {downloadpath}/{namepath}<br>
                       <b>File Name :</b>   {modelname}
                       </p>
                       """
           return gr.Image(image).update(value=imgurl), gr.Button(download_btn).update(visible=True, variant="primary"), gr.Textbox(out_text).update("Ready", visible=True), gr.Markdown(info).update(markdown2)
        else:
             parse = urlparse(url).path
             metadata1 = parse[parse.rfind('/') + 1:]
             modelname = metadata1.replace(" ", "_")
             namepath = os.path.splitext(metadata1)[0]
             imgurl = no_prev
             imgname = f"{namepath}.preview.png"
             markdown2 = f"""
                         <font size=2><p>
                         <b>Model Information :</b><br>
                         <b>URL :</b>   {url}<br>
                         <b>Folder Path :</b>   {downloadpath}/{namepath}<br>
                         <b>File Name :</b>   {modelname}
                         </p>
                         """
             return gr.Image(image).update(value=imgurl), gr.Button(download_btn).update(visible=True, variant="primary"), gr.Textbox(out_text).update("Ready", visible=True), gr.Markdown(info).update(markdown2)
    except:
           markdown2 = f"""
                       <font size=2><p>
                       <b>Model Information :</b><br>
                       <b>URL :</b>   {url}<br>
                       <b>Folder Path :</b>   {downloadpath}/{namepath}<br>
                       <b>File Name :</b>   {modelname}
                       </p>
                       """
           imgurl = no_prev
           return gr.Image(image).update(value=imgurl), gr.Button(download_btn).update(visible=True, variant="primary"), gr.Textbox(out_text).update("Ready", visible=True), gr.Markdown(info).update(markdown2)

def start_downloading(download_btn, url, addnet):
    complete1 = f"SUCCESS: Download Completed, Saved to\n"
    complete2 = f"ERROR: File Already Exist in\n"
    target1 = f"{downloadpath}/{namepath}"
    target2 = f"{addnet_path}/models/lora/{namepath}"
    final_target = None
    if addnet:
       final_target = target2
    else:
         final_target = target1
    command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --input-file model.txt -d {final_target}"
    with open("model.txt", "w") as w:
         if not url.find("https://civitai.com/")!=-1:
            w.write(f"{url}\n out={modelname}")
         else:
              w.write(f"{url}\n out={modelname}\n{imgurl}\n out={imgname}")
    if not os.path.exists(final_target):
       line1 = os.popen(command)
       for l in line1:
           l = l.rstrip()
           yield f"{complete1}{final_target}"
       print(f"{complete1}{final_target}")
    else:
         yield f"{complete2}{final_target}"
         print(f"{complete2}{final_target}")

def back(download_btn):
    return gr.Button.update(visible=True, variant="secondary")

def on_ui_tabs():
    with gr.Blocks() as downloader:
         with gr.Row():
              with gr.Column():
                   content_type = gr.Radio(
                                           label="1. Choose Content type",
                                           choices=["Checkpoint",
                                                    "Hypernetwork",
                                                    "TextualInversion/Embedding",
                                                    "VAE", 
                                                    "LoRA", 
                                                    "LyCORIS(LoCon/LoHA)"
                                                    ]
                                           )
                   addnet = None
                   if os.path.exists(addnet_path):
                      addnet = gr.Checkbox(label="save to Additional Networks", value=False, visible=True)
                      print("Model Downloader detects Additional Networks, creating checkbox for AddNet.")
                   else:
                        addnet = gr.Checkbox(value=False, visible=False)
         with gr.Row():
              url = gr.Textbox(
                               label="2. Put Link Download Below",
                               max_lines=1, placeholder="Type/Paste URL Here"
                               )
              url.style(show_copy_button=True)
         with gr.Row():
              download_btn = gr.Button(
                                       "Start Download",
                                       visible=False,
                                       variant="secondary"
                                       )
              out_text = gr.Textbox(
                                    label="Download Result",
                                    placeholder="Result",
                                    visible=False,
                                    show_progress=True
                                    )
         with gr.Row():
              with gr.Column():
                   markdown1 = """
                               <font size=2><p>
                               <b>Model Information :</b><br>
                               <b>URL :</b><br>
                               <b>Folder Path :</b><br>
                               <b>File Name :</b>
                               </p>
                               """
                   info = gr.Markdown(markdown1)
              with gr.Column():
                   preview = gr.Markdown("""<font size=2><b>Preview Model :</b>""")
                   image = gr.Image(value=no_prev, show_label=False)
                   image.style(width=256, height=384)
         with gr.Row():
              github = gr.Markdown(
                                   """
                                   <center><font size=2>Having Issue? |
                                   <a href=https://github.com/Iyashinouta/sd-model-downloader/issues>
                                   Report Here</a><br>
                                   <center><font size=1>Model Downloader v1.0.5
                                   """
                                   )
              content_type.change(folder, content_type)
              url.change(get_data_from_url, url, [image, download_btn, out_text, info])
              download_btn.click(start_downloading, [download_btn, url, addnet], out_text)
              url.submit(start_downloading, [download_btn, url, addnet], out_text)
              download_btn.click(back, download_btn, download_btn)
              url.submit(back, url, download_btn)
    return (downloader, "Model Downloader", "downloader"),

script_callbacks.on_ui_tabs(on_ui_tabs)
