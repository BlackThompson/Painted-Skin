# 🎭 Painted Skin 🎭

> Welcome to the 🎭 Painted Skin 🎭! Get ready to have some fun with faces. 😄

 ![License](https://img.shields.io/badge/license-Apache2.0-blue)

## 🐾 Preview

![image-20231108160501352](https://black-thompson.oss-cn-beijing.aliyuncs.com/img/image-20231108160501352.png)



## 🪄 How to use

1. **Clone the Repository:**
   
    ```bash
    git clone https://github.com/BlackThompson/Painted-Skin.git
    ```
    
2. **Create a New Environment and Install Dependencies:**
   
    - Note: Python version should be >=3.8
    - Note: The versions of `torch`, `torchvision`, and `torchaudio` should align with your CUDA version.
    
    ```bash
    conda create --name painted_skin python=3.8
    conda activate painted_skin
    pip install -r requirements.txt 
    ```
    
3. **Run `gradio_UI.py`:**
    ```bash
    gradio gradio_UI.py
    ```

4. **Click the Local URL**

## 🦾 How it Works

This tool allows you to perform a face swap. Simply follow these steps:

1. **Upload Source:**
   - Choose between `src_picture` and `src_video` for the face you want to swap.
   - Note: You can only upload one source at a time, and the tool processes one task at a time.
2. **Upload Target:**
   - Upload `target_picture`, and our model will swap the face onto the source image or video.
3. **Submit and Wait:**
   - Click the submit button and patiently wait for the process to complete.
   - Keep in mind that face swapping in videos might take some time, so be patient! 😅

## ❗ Important Note
- If you are able to load `src_picture` but encounter issues with loading `src_video`, please ensure that you have downloaded  [FFmpeg](https://ffmpeg.org/download.html) and correctly added its `bin` directory to your system path.
- Ensure that `target_picture` is uploaded for the face swap to work effectively.

Enjoy swapping faces and have a good laugh! 😆

## 💌 Acknowledgements

This repository borrows heavily from [facefusion-damo](https://www.modelscope.cn/models/damo/cv_unet-image-face-fusion_damo/summary) and [face-change](https://github.com/Quietbe/mv_face_change/blob/main/video_cut_cv_h.py). Thanks to the authors for sharing their code and models.
