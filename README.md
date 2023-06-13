# sd-model-downloader
SD Web UI Extension to Download Model from URL
  
# This Extension Work on AUTO1111 SD Webui

To install it, clone the repo into the `extensions` directory and run terminal:<br>
`git clone https://github.com/Iyashinouta/sd-model-downloader /content/stable-diffusion-webui/extensions/sd-model-downloader`

or Install from SD Webui:<br>
install from URL, and Paste Link https://github.com/Iyashinouta/sd-model-downloader

# Instructions

<details><summary>tap to see image</summary>
  
  ![preview](https://raw.githubusercontent.com/Iyashinouta/sd-model-downloader/main/images/instructions.png)
  
</details>

# Update fix/features

<details><summary>
  See Releases for more details
  </summary>

  - June 14, 2023<br>
    - bug fix = fix `NoneType` variables from <a href=https://github.com/Iyashinouta/sd-model-downloader/issues/8#issue-1751439968>YKefasu<br>
    - rollback features = Filename features finally back again<br>
  - May 30, 2023<br>
    - bug fix : path fix<br>
    - bug fix : downloading `card-no-preview.png` if not exist
  - May 28, 2023<br>
    - adding features : save to <a href=https://github.com/kohya-ss/sd-webui-additional-networks>AddNet Extension</a><br>
    - optimizing fix : more stable, though in latest version on webui<br>
  - May 26, 2023<br>
    - optimizing fix : fix performance when reading information<br>
  - May 22, 2023<br>
    - bug fix : getting error while downloading Huggingface<br>
  
  - May 21, 2023<br>
    - adding feature : show image preview model and save to thumbnail<br>
    - fix : re-organize ui<br>

  - May 12, 2023<br>
    - adding features : submit url/filename<br>
    - bug fix : path fix<br>
  
</details>
