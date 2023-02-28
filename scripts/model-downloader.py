import os
import gradio as gr
from modules import scripts, script_callbacks
from subprocess import getoutput

def downloading (content_type, url):
  if content_type == "Checkpoint":
        return output + url + " -d /content/stable-diffusion-webui/models/Stable-diffusion" 
  elif content_type == "Hypernetwork":
        return output + url + " -d /content/stable-diffusion-webui/models/hypernetworks"
  elif content_type == "TextualInversion":
        return output + url + " -d /content/stable-diffusion-webui/embeddings" 
  elif content_type == "AestheticGradient":
        return output + url + " -d /content/stable-diffusion-webui/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings"
  elif content_type == "VAE":
        return output + url + " -d /content/stable-diffusion-webui/models/VAE"
  elif content_type == "Lora":
        return output + url + " -d /content/stable-diffusion-webui/models/Lora"
    
def run(command):
    out = getoutput(f"{command}")
    return out

def on_ui_tabs():     
    with gr.Blocks() as downloader:
        with gr.Group():
            with gr.Box():
                content_type = gr.Radio(label='Content type:', choices=["Checkpoint","Hypernetwork","TextualInversion","AestheticGradient", "VAE", "Lora"], value="Checkpoint", type="value")
                url = gr.Textbox(label="Link Download", max_lines=1, placeholder="Type/Paste URL Here")
                output = gr.Textbox(label="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M ", visible=True, interactive=False)
                comand = gr.Textbox(downloading, visible=True, interactive=False)
                btn_run = gr.Button("Start Download")
                btn_run.click(fn=downloading, inputs=command, outputs=out_text)
                out_text + gr.Text
    return (downloader, "Model Downloader", "downloader"),
script_callbacks.on_ui_tabs(on_ui_tabs)
