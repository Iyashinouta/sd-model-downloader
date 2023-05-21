# sd-model-downloader
SD Web UI Extension to Download Model from URL

<details><summary><b>
  <h1>Update fix/features</h>
  </b></summary>
  
  - May 21, 2023<br>
    - adding features : show image preview model and save to thumbnail<br>
      > image will show below information<br>
    - fix : re-organize ui<br>
      > `Start Download` button and `Outputs` textbox is hidden until `Information` fully appear<br>
      > move `Start Download` button next to `Information`<br>
      > fix `outputs` textbox to be simple and accurate<br>
    
  - May 12, 2023<br>
    - adding features : submit url/filename<br>
      > when you click enter on url/filename textbox, it will start downloading<br>
    - bug fix : path fix<br>
      > from `"/path"` (manual) change to `os.getcwd()` to automatic search sd-webui path<br>
  
</details>
  
# This Extension Work on AUTO1111 SD Webui

To install it, clone the repo into the `extensions` directory and run colab:<br>
`!git clone https://github.com/Iyashinouta/sd-model-downloader /content/stable-diffusion-webui/extensions/sd-model-downloader`<br>
or Install from SD Webui:<br>
install from URL, and Paste Link `https://github.com/Iyashinouta/sd-model-downloader`
