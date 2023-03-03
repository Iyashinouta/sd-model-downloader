import os
import gradio as gr
from modules import scripts, script_callbacks

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

def cfn(filename1, filename, opt):
    if filename1 == "Use original Filename from the Source":
       return gr.Textbox(opt).update(value=" "),  gr.Textbox(filename).update(value=" ", visible=False)
    elif filename1 == "Create New Filename(Recomended)":
         return gr.Textbox(opt).update(value=" -o "), gr.Textbox(filename).update(value=" ", visible=True)

def dwn(content_type1, url, download_btn):
    return gr.Button(download_btn).update(visible=True)
    
def combine(cmd, url, content_type1, opt, filename):
    return gr.Textbox.update(cmd + url + content_type1 + opt + filename)

def inf(url, content_type1, filename, info):
    return gr.Textbox(info).update(value="[URL]:  " + url + "     [Folder Path]: " + content_type1 + "     [File Name]:  " + filename)
    
def run(command):
  with os.popen(command) as pipe:
    for line in pipe:
      line = line.rstrip()
      print(line)
      yield line
    
def on_ui_tabs():
    with gr.Blocks() as downloader:    
        with gr.Row():
            with gr.Column(scale=2):
                content_type = gr.Radio(label="1. Choose Content type", choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "Lora"])
                content_type1 = gr.Textbox(visible=False)
                content_type.change(fn=folder, inputs=content_type, outputs=content_type1, queue=True)
        with gr.Row():
            url = gr.Textbox(label="2. Put Link Download Below", max_lines=1, placeholder="Type/Paste URL Here")
            opt = gr.Textbox(value=" ", visible=False)
        with gr.Row():
            with gr.Column(scale=2):
                filename1 = gr.Radio(label="Setting Filename", choices=["Use original Filename from the Source", "Create New Filename(Recomended)"], type="value", value="Use original Filename from the Source")
        with gr.Row():
            filename = gr.Textbox(label="3. Create new Filename", placeholder="Type/Paste Filename.extension Here", visible=False, interactive=True)
            filename1.change(fn=cfn, inputs=[filename1, opt, filename], outputs=[opt, filename], queue=True)
        with gr.Row():
            cmd = gr.Textbox(value="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M ", visible=False)
            commands = gr.Textbox(label="Information Command", visible=False, interactive=False)
            info = gr.Textbox(label="Information", placeholder="Make sure to Check properly whether everything is Correct", interactive=False)
        with gr.Row():
            download_btn = gr.Button("Start Download", visible=False)
        with gr.Row():
            content_type1.change(fn=combine, inputs=[cmd, url, content_type1, opt, filename], outputs=commands, queue=True)
            url.change(fn=dwn, inputs=[url, content_type1, download_btn], outputs=download_btn, queue=True)
            url.change(fn=combine, inputs=[cmd, url, content_type1, opt, filename], outputs=commands, queue=True)
            filename.change(fn=combine, inputs=[cmd, url, content_type1, opt, filename], outputs=commands, queue=True)
            content_type1.change(fn=inf, inputs=[url, content_type1, filename], outputs=info, queue=True)
            url.change(fn=inf, inputs=[url, content_type1, filename], outputs=info, queue=True)
            filename.change(fn=inf, inputs=[url, content_type1, filename], outputs=info, queue=True)
        with gr.Row():
            out_text = gr.Textbox(label="Download Result", placeholder="Result")
            download_btn.click(fn=run, inputs=commands, outputs=out_text, queue=True)

    downloader.queue(concurrency_count=15)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
