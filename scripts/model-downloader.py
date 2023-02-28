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

def split(downloader_type, url, in_text):
  return gr.Textbox.update(downloader_type + url + in_text)

def run(command):
    out = getoutput(f"{command}")
    return out

def on_ui_tabs():     
    with gr.Blocks() as downloader:
        with gr.Group():
            with gr.Box():
                content_type = gr.Radio(label='Content type:', choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "Lora"])
                in_text = gr.Textbox(visible=False)
                content_type.change(fn=folder, inputs=content_type, outputs=in_text)
                url = gr.Textbox(label="Link Download", max_lines=1, placeholder="Type/Paste URL Here")
                downloader_type = gr.Textbox(value="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M ", visible=False, interactive=False)
                commands = gr.Textbox(visible=False)
                url.change(fn=split, inputs=[downloader_type, url, in_text], outputs=commands)
                out_text = gr.Textbox(label="Result", placeholder="Result")
                gr.Button("Start Download").click(fn=run, inputs=commands, outputs=out_text)
    return (downloader, "Model Downloader", "downloader"),
script_callbacks.on_ui_tabs(on_ui_tabs)
