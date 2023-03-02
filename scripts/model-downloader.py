import os
import gradio as gr
from modules import scripts, script_callbacks
from subprocess import getoutput

def folder(content_type):
    if content_type == "Checkpoint":
       return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Stable-diffusion -o ")
    elif content_type == "Hypernetwork":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/hypernetworks -o ")
    elif content_type == "TextualInversion/Embedding":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/embeddings -o ")
    elif content_type == "AestheticGradient":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings -o ")
    elif content_type == "VAE":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/VAE -o ")
    elif content_type == "Lora":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Lora -o ")

def combine(cmd, url, content_type1, filename):
    return gr.Textbox.update(cmd + url + content_type1 + filename)
    
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
                    filename = gr.Textbox(label="3. Create new Filename", placeholder="Type/Paste Filename.extension Here", interactive=True)
                    cmd = gr.Textbox(value="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M ", visible=False)
                commands = gr.Textbox(label="Information Command", visible=True, interactive=False)
                content_type1.change(fn=combine, inputs=[cmd, url, content_type1, filename], outputs=commands, queue=True)
                url.change(fn=combine, inputs=[cmd, url, content_type1, filename], outputs=commands, queue=True)
                filename.change(fn=combine, inputs=[cmd, url, content_type1, filename], outputs=commands, queue=True)
                out_text = gr.Textbox(label="Download Result", placeholder="Result")
                download_btn.click(fn=run, inputs=commands, outputs=out_text, queue=True)

    downloader.queue(concurrency_count=10)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
