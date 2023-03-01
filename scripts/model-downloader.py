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

def combine(cmd, url, content_type1, file_name):
    return gr.Textbox.update(cmd + url + content_type1 + file_name)

def out_filename(checkbox, file_name, cmd):
    r = gr.Textbox(file_name).update(value=" -o ", interactive=True)
    r1 = gr.Textbox(cmd).update(value="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M-o ")
    return r, r1
        
def run(command):
    out = getoutput(f"{command}")
    return out

def on_ui_tabs():     
    with gr.Blocks() as downloader:
        with gr.Group():
            with gr.Box():
                with gr.Row():
                    content_type = gr.Radio(label="1. Choose Content type", choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "Lora"])
                    content_type1 = gr.Textbox(visible=False)
                    content_type.change(fn=folder, inputs=content_type, outputs=content_type1)
                    download_btn = gr.Button("Start Download")
                with gr.Row():
                    url = gr.Textbox(label="2. Put Link Download Below", max_lines=1, placeholder="Type/Paste URL Here")
                    file_name = gr.Textbox(label="3. Type/Input Filename.extension Here(Required if Download URL from HuggingFace)", placeholder="don't delete( -o )when uncheck and appear", interactive=False)
                    cmd = gr.Textbox(value="aria2c --console-log-level=error --content-disposition-default-utf8 -c -x 16 -s 16 -k 1M -d ", visible=False)
                    checkbox = gr.Checkbox(label="Use the original Filename from the Source", value=True)
                    checkbox.change(fn=out_filename, inputs=[checkbox, file_name, cmd], outputs=[file_name, cmd])
                commands = gr.Textbox(label="Command", visible=True, interactive=False)
                content_type1.change(fn=combine, inputs=[cmd, url, content_type1, file_name], outputs=commands, queue=True)
                url.change(fn=combine, inputs=[cmd, url, content_type1, file_name], outputs=commands, queue=True)
                file_name.change(fn=combine, inputs=[cmd, url, content_type1, file_name], outputs=commands, queue=True)
                out_text = gr.Textbox(label="Result", placeholder="Result")
                download_btn.click(fn=run, inputs=commands, outputs=out_text)

    downloader.queue(concurrency_count=5)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
