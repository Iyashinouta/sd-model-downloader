import os
import gradio as gr
from modules import scripts, script_callbacks
from subprocess import getoutput

def folder(content_type):
    if content_type == "Checkpoint":
       return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Stable-diffusion")
    elif content_type == "Hypernetwork":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/hypernetworks")
    elif content_type == "TextualInversion/Embedding":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/embeddings")
    elif content_type == "AestheticGradient":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings")
    elif content_type == "VAE":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/VAE")
    elif content_type == "Lora":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Lora")

def combine(downloader_type, url, content_type1, file_name):
    return gr.Textbox.update(downloader_type + url + content_type1 + file_name)

def combine1(downloader_type, url, content_type1, file_name1, file_name):
    return gr.Textbox.update(downloader_type + url + content_type1 + file_name1 + file_name)

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
                    file_name = gr.Textbox(label="3. Set File Name(Required if Download URL from HuggingFace)", placeholder="Type/Input Filename.extension Here", interactive=True)
                    file_name1 = gr.Textbox(value=" -o ", visible=False)
                downloader_type = gr.Textbox(value="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M ", visible=False, interactive=False)
                commands = gr.Textbox(label="Command", visible=True, interaactive=False, show_progress=True)
                url.change(fn=combine, inputs=[downloader_type, url, content_type1, file_name], outputs=commands)
                file_name.change(fn=combine1, inputs=[downloader_type, url, content_type1, file_name1, file_name], outputs=commands)
                content_type1.change(fn=combine, inputs=[downloader_type, url, content_type1, file_name], outputs=commands)
                out_text = gr.Textbox(label="Result", placeholder="Result", scroll_to_output=True)
                download_btn.click(fn=run, inputs=commands, outputs=out_text)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
