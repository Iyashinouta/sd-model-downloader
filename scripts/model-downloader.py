import os
import gradio as gr
from modules import scripts, script_callbacks
from subprocess import getoutput

def folder(content_type):
    if content_type == "Checkpoint":
       return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Stable-diffusion ")
    elif content_type == "Hypernetwork":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/hypernetworks ")
    elif content_type == "TextualInversion/Embedding":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/embeddings ")
    elif content_type == "AestheticGradient":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings ")
    elif content_type == "VAE":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/VAE ")
    elif content_type == "Lora":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Lora ")

def update(file_name, checkbox):
    if checkbox == "Use the original Filename from the Source":
       return gr.Textbox(file_name).update(interactive=False)
    elif checkbox == "Create new Filename(Recomended)":
         return gr.Textbox(file_name).update(interactive=True)

def rename(checkbox, file_name, cmd, cmd1):
    return gr.Textbox.update(cmd1 + file_name)

def combine(cmd, url, content_type1, opt):
    return gr.Textbox.update(cmd + url + content_type1 + opt)
    
def run(command):
  with os.popen(command) as pipe:
    for line in pipe:
      line = line.rstrip()
      print(line)
      yield line

def on_ui_tabs():     
    with gr.Blocks() as downloader:
        with gr.Group():
            with gr.Box():
                with gr.Row():
                    content_type = gr.Radio(label="1. Choose Content type", choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "Lora"])
                    content_type1 = gr.Textbox(visible=False)
                    content_type.change(fn=folder, inputs=content_type, outputs=content_type1, queue=True)
                    download_btn = gr.Button("Start Download")
                with gr.Row():
                    url = gr.Textbox(label="2. Put Link Download Below", max_lines=1, placeholder="Type/Paste URL Here")
                    file_name = gr.Textbox(label="3. Create new Filename", placeholder="Type/Paste Filename.extension Here", interactive=False)
                    cmd = gr.Textbox(value="aria2c --console-log-level=error --content-disposition-default-utf8 -c -x 16 -s 16 -k 1M ", visible=False)
                    cmd1 = gr.Textbox(value=" -o ", visible=False)
                    checkbox = gr.Radio(label="File Name", choices=["Use the original Filename from the Source","Create new Filename(Recomended)"], type="value", value="Use the original Filename from the Source")
                    checkbox.change(fn=update, inputs=checkbox, outputs=file_name, queue=True)
                    opt = gr.Textbox(visible=False)
                commands = gr.Textbox(label="Command", visible=True, interactive=False)
                content_type1.change(fn=combine, inputs=[cmd, url, content_type1, opt], outputs=commands, queue=True)
                url.change(fn=combine, inputs=[cmd, url, content_type1, opt], outputs=commands, queue=True)
                file_name.change(fn=rename, inputs=[cmd1, file_name], outputs=opt, queue=True)
                out_text = gr.Textbox(label="Result", placeholder="Result")
                download_btn.click(fn=run, inputs=commands, outputs=out_text, queue=True)

    downloader.queue(concurrency_count=10)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
