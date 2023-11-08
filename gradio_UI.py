# _*_ coding : utf-8 _*_
# @Time : 2023/11/7 21:42
# @Author : Black
# @File : gradio_UI
# @Project : face_fusion_damo

import gradio as gr
import os
from face_swap_utils import *


def face_swap(src_picture=None, src_video=None,
              target_picture=os.path.join(os.path.dirname(__file__), 'example/Trump.jpg')):
    save_dir = os.path.join(os.path.dirname(__file__), 'output')
    # 检查是否存在临时文件夹，如果不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if src_picture is not None:
        print(src_picture)
        result = replace_single_img(src_picture, target_picture, save_dir)
        return result, None
    elif src_video is not None:
        print(src_video)
        result = replace_video(src_video, target_picture)
        return None, result


demo = gr.Interface(fn=face_swap,
                    inputs=[gr.Image(type='filepath'), gr.Video(), gr.Image(type='filepath')],
                    outputs=[gr.Image(type='filepath', label='swapped_image'),
                             gr.Video(label='swapped_video')],
                    title="🎭 Painted Skin 🎭",
                    description="# Face Swap Tool\n"
                                "Welcome to the 🎭 Painted Skin 🎭! Get ready to have some fun with faces. 😄\n"
                                "## How it Works\n"
                                "This tool allows you to perform a face swap. Simply follow these steps:\n"
                                "1. **Upload Source:**\n"
                                "   - Choose between `src_picture` and `src_video` for the face you want to swap.\n"
                                "   - Note: You can only upload one source at a time, and the tool processes one task at a time.\n"
                                "2. **Upload Target:**\n"
                                "   - Upload `target_picture`, and our model will swap the face onto the source image or video.\n"
                                "3. **Submit and Wait:**\n"
                                "   - Click the submit button and patiently wait for the process to complete.\n"
                                "   - Keep in mind that face swapping in videos might take some time, so be patient! 😅\n"
                                "## Important Note\n"
                                "- Ensure that `target_picture` is uploaded for the face swap to work effectively.\n"
                                "Enjoy swapping faces and have a good laugh! 😆\n",

                    # css="body {background-color: red;}",
                    # article="Attention is all you need!",
                    examples=[[os.path.join(os.path.dirname(__file__), 'example/Trump.jpg'),
                               None,
                               os.path.join(os.path.dirname(__file__), 'example/Obama.jpg')],
                              [os.path.join(os.path.dirname(__file__), 'example/CXK.jpg'),
                               None,
                               os.path.join(os.path.dirname(__file__), 'example/James.jpg')]
                              ],
                    # allow_flagging="never",
                    # cache_examples=True
                    )

if __name__ == "__main__":
    demo.launch(share=True)
