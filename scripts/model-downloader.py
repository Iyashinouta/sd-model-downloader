import os
import requests
import argparse
import subprocess
import gradio as gr
from urllib.parse import urlparse
from modules import scripts, script_callbacks
try:
    from modules.paths_internal import data_path, models_path, extensions_dir
except ImportError:
       from modules.paths import data_path, models_path
       extensions_dir = os.path.join(data_path, 'extensions')

sd_path = os.getcwd()
ext = '/extensions'
no_prev = None
addnet_path = None
md_path = scripts.basedir()

parser = argparse.ArgumentParser()
parser.add_argument('--ckpt-dir', type=str, default=os.path.join(models_path, 'Stable-diffusion'))
parser.add_argument('--vae-dir', type=str, default=os.path.join(models_path, 'VAE'))
parser.add_argument('--embeddings-dir', type=str, default=os.path.join(data_path, 'embeddings'))
parser.add_argument('--hypernetwork-dir', type=str, default=os.path.join(models_path, 'hypernetworks'))
parser.add_argument('--lora-dir', type=str, default=os.path.join(models_path, 'Lora'))
parser.add_argument('--lyco-dir', type=str, default=os.path.join(models_path, 'LyCORIS'))
args, _ = parser.parse_known_args()

if not os.path.exists(os.path.join(sd_path, 'html', 'card-no-preview.png')):
   try:
       no_prev = os.path.join(md_path, 'images', 'card-no-prev.png')
   except:
          pass
else:
     no_prev = os.path.join(sd_path, 'html', 'card-no-preview.png')
if not os.path.exists(os.path.join(sd_path, ext, 'sd-webui-additional-networks')):
   addnet_path = os.path.join(extensions_dir, 'sd-webui-additional-networks')
else:
     addnet_path = os.path.join(sd_path, ext, 'sd-webui-additional-networks')

checkpoint_path = args.ckpt_dir
vae_path = args.vae_dir
embedding_path = args.embeddings_dir
hypernetwork_path = args.hypernetwork_dir
lora_path = args.lora_dir
lycoris_path = args.lyco_dir
controlnet_path = os.path.join(extensions_dir, 'sd-webui-controlnet')
controlnet_model_path = os.path.join(controlnet_path, 'models')

print(f'Model Downloader v1.0.8')
print('Checking Directories...')
if not os.path.exists(checkpoint_path):
   os.makedirs(checkpoint_path)
   print ('Creating Checkpoint Folder')
if not os.path.exists(hypernetwork_path):
   os.makedirs(hypernetwork_path)
   print ('Creating Hypernetwork Folder')
if not os.path.exists(embedding_path):
   os.makedirs(embedding_path)
   print ('Creating TextualInversion/Embeddings Folder')
if not os.path.exists(vae_path):
   os.makedirs(vae_path)
   print ('Creating VAE Folder')
if not os.path.exists(lora_path):
   os.makedirs(lora_path)
   print ('Creating LoRA Folder')
if not os.path.exists(lycoris_path):
   os.makedirs(lycoris_path)
   print ('Creating LyCORIS Folder')
else:
     pass
print('all Directories already Created.')

def folder(content_type):
    if content_type == 'Checkpoint':
       downloadpath = checkpoint_path
    elif content_type == 'Hypernetwork':
         downloadpath = hypernetwork_path
    elif content_type == 'TextualInversion/Embedding':
         downloadpath = embedding_path
    elif content_type == 'VAE':
         downloadpath = vae_path
    elif content_type == 'LoRA':
         downloadpath = lora_path
    elif content_type == 'LyCORIS(LoCon/LoHA)':
         downloadpath = lycoris_path
    elif content_type == 'ControlNet Model':
         downloadpath = controlnet_model_path
    else:
         downloadpath = 'Unset, Please Choose your Content Type'
    return downloadpath

def get_filename_from_url(url):
    if url.find('https://civitai.com/')!=-1:
       convert = '' + url.replace('download/models', 'v1/model-versions')
       req = requests.get(convert, stream=True)
       basename, extension = os.path.splitext(req.json()['files'][0]['name'].replace(' ', '_'))
    else:
         parse = urlparse(url).path
         req = parse[parse.rfind('/') + 1:].replace(' ', '_')
         basename, extension = os.path.splitext(req)
    return basename, extension

def get_image_from_url(url):
    if url.find('https://civitai.com/')!=-1:
       convert = '' + url.replace('download/models', 'v1/model-versions')
       req = requests.get(convert, stream=True)
       imgurl = req.json()['images'][0]['url']
    else:
         imgurl = no_prev
    return imgurl

def change_name(changename):
    if changename:
       filename = gr.Textbox.update(visible=True)
    else:
         filename = gr.Textbox.update(visible=False)
    return filename

def custom_download_path(custompath):
    if custompath:
       downloadpath = gr.Textbox.update(visible=True)
    else:
         downloadpath = gr.Textbox.update(visible=False)
    return downloadpath

def get_data_from_url(url, downloadpath):
    try:
        imgurl = get_image_from_url(url)
        basename, extension = get_filename_from_url(url)
        markdown2 = f'''
                     <font size=2>
                     <center><b>Model Information</b><br></center>
                     <b>URL :</b> {url}<br>
                     <b>Folder Path :</b> {downloadpath}<br>
                     <b>File Name :</b> {basename}{extension}<br>
                     '''
    except:
           imgurl = no_prev
           markdown2 = f'''
                        <font size=2>
                        <center><b>Model Information</b><br></center>
                        <b>URL :</b> {url}<br>
                        <b>Folder Path :</b> {downloadpath}<br>
                        <b>File Name :</b> ???
                        '''
    filename = gr.Textbox.update(basename)
    image = gr.Image.update(imgurl)
    download_btn =  gr.Button.update(visible=True, variant='primary')
    out_text = gr.Textbox.update('Ready', visible=True)
    info = gr.Markdown.update(markdown2)
    return filename, image, download_btn, out_text, info

def start_downloading(downloader_type, download_btn, url, downloadpath, filename, addnet, logging, new_folder, preview):
    complete1 = f'SUCCESS: Download Completed, Saved to\n'
    complete2 = f'ERROR: File Already Exist in\n'
    complete3 = 'ERROR: Something went wrong, please try again later'
    path, extension = get_filename_from_url(url)
    imgname = f'{filename}.preview.png'
    if new_folder:
       target1 = os.path.join(downloadpath, filename)
       target2 = os.path.join(addnet_path, 'models', 'lora', filename)
    else:
         target1 = os.path.join(downloadpath)
         target2 = os.path.join(addnet_path, 'models', 'lora')
    final_target = None
    if addnet:
       final_target = target2
    else:
         final_target = target1
    back(download_btn)
    if not os.path.exists(os.path.join(final_target, f'{filename}{extension}')):
       try:
           if downloader_type == 'aria2':
              command = f'aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --input-file model.txt -d {final_target}'
              with open('model.txt', 'w') as w:
                   if not url.find('https://civitai.com/')!=-1:
                      w.write(f'{url}\n out={filename}{extension}')
                   else:
                        if preview:
                           imgurl = get_image_from_url(url)
                           w.write(f'{url}\n out={filename}{extension}\n{imgurl}\n out={imgname}')
                        else:
                             w.write(f'{url}\n out={filename}{extension}')
              if logging:
                 command.replace(' --console-log-level=error', ' ')
                 line = subprocess.getoutput(command)
                 yield line
                 print(line)
              else:
                   line = os.popen(command)
                   for l in line:
                       l = l.rstrip()
                       yield f'{complete1}{final_target}'
                   print(f'{complete1}{final_target}')
           elif downloader_type == 'requests':
                if new_folder:
                   os.makedirs(final_target, exist_ok=True)
                else:
                     pass
                download = requests.get(url, allow_redirects=True)
                if not url.find('https://civitai.com/')!=-1:
                   with open(os.path.join(final_target, f'{filename}{extension}'), 'wb') as f:
                        f.write(download.content)
                else:
                     if preview:
                        imgurl = get_image_from_url(url)
                        img_download = requests.get(str(imgurl), allow_redirects=True)
                        with open(os.path.join(final_target, f'{filename}{extension}'), 'wb') as f:
                             f.write(download.content)
                        with open(os.path.join(final_target, imgname), 'wb') as img:
                             img.write(img_download.content)
                     else:
                          with open(os.path.join(final_target, f'{filename}{extension}'), 'wb') as f:
                               f.write(download.content)
                yield f'{complete1}{final_target}'
                print(f'{complete1}{final_target}')
       except Exception as e:
               yield f'{e}\n{complete3}'
               print(f'{e}\n{complete3}')
    else:
         yield f'{complete2}{final_target}'
         print(f'{complete2}{final_target}')

def back(download_btn):
    return gr.Button.update(visible=True, variant='secondary')

def on_ui_tabs():
    with gr.Blocks() as downloader:
         with gr.Row():
              with gr.Column():
                   downloader_type = gr.Radio(
                                              label='Downloader Type',
                                              choices=[
                                                       'aria2',
                                                       'requests'
                                                       ],
                                              value='aria2',
                                              type='value'
                                              )
                   with gr.Row():
                        content_type = gr.Radio(
                                                label='1. Choose Content Type',
                                                choices=[
                                                         'Checkpoint',
                                                         'Hypernetwork',
                                                         'TextualInversion/Embedding',
                                                         'VAE',
                                                         'LoRA',
                                                         'LyCORIS(LoCon/LoHA)',
                                                         'ControlNet Model'
                                                         ]
                                                )
                   addnet = None
                   if os.path.exists(addnet_path):
                      addnet = gr.Checkbox(label='save to Additional Networks', value=False, visible=True)
                      print('Model Downloader detects Additional Networks, creating checkbox for AddNet.')
                   else:
                        addnet = gr.Checkbox(value=False, visible=False)
         with gr.Row():
              with gr.Column():
                   url = gr.Textbox(
                                    label='2. Put Link Download Below',
                                    max_lines=1, placeholder='Type/Paste URL Here'
                                    )
                   downloadpath = gr.Textbox(
                                             value='Unset, Please Choose your Content Type',
                                             label='Custom Download Path',
                                             placeholder='Paste Folder Path Here',
                                             visible=False
                                             )
                   filename = gr.Textbox(
                                         label='Change Filename',
                                         placeholder='Filename',
                                         visible=False
                                         )
              with gr.Row():
                   logging = gr.Checkbox(label='turn on log', value=False)
                   changename = gr.Checkbox(label='Change Filename', value=False)
                   custompath = gr.Checkbox(label='Custom Download Path', value=False)
                   preview = gr.Checkbox(label='Download Preview', value=True)
                   new_folder = gr.Checkbox(label='Create New Folder', value=False)
         with gr.Row():
              with gr.Column():
                   download_btn = gr.Button(
                                            'Start Download',
                                            visible=False,
                                            variant='secondary'
                                            )
                   out_text = gr.Textbox(
                                         label='Download Result',
                                         placeholder='Result',
                                         visible=False,
                                         )
              with gr.Row():
                   with gr.Column():
                        info = gr.Markdown(
                                           '''
                                           <font size=2>
                                           <center><b>Model Information</b><br></center>
                                           <b>URL :</b><br>
                                           <b>Folder Path :</b><br>
                                           <b>File Name :</b>
                                           '''
                                           )
                   with gr.Column():
                        prev_markdown = gr.Markdown('''<font size=2><b>Preview Model :</b>''')
                        image = gr.Image(value=no_prev, show_label=False)
                        image.style(width=156, height=234)
         with gr.Row():
              github = gr.Markdown(
                                   '''
                                   <center><font size=2>Having Issue? |
                                   <a href=https://github.com/Iyashinouta/sd-model-downloader/issues>
                                   Report Here</a><br>
                                   <center><font size=1>Model Downloader v1.0.8
                                   '''
                                   )
         content_type.change(folder, content_type, downloadpath)
         changename.change(change_name, changename, filename)
         custompath.change(custom_download_path, custompath, downloadpath)
         url.change(
                    get_data_from_url,
                    [
                     url,
                     downloadpath
                     ],
                    [
                     filename,
                     image,
                     download_btn,
                     out_text,
                     info
                     ]
                    )
         download_btn.click(
                            start_downloading,
                            [
                             downloader_type,
                             download_btn,
                             url,
                             downloadpath,
                             filename,
                             addnet,
                             logging,
                             new_folder,
                             preview
                             ],
                             out_text
                            )
         url.submit(
                    start_downloading,
                    [
                     downloader_type,
                     download_btn,
                     url,
                     downloadpath,
                     filename,
                     addnet,
                     logging,
                     new_folder,
                     preview
                     ],
                     out_text
                    )
         download_btn.click(back, download_btn, download_btn)
         url.submit(back, url, download_btn)
    return (downloader, 'Model Downloader', 'downloader'),

script_callbacks.on_ui_tabs(on_ui_tabs)
