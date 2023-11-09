# _*_ coding : utf-8 _*_
# @Time : 2023/11/6 17:04
# @Author : Black
# @File : face_swap_utils
# @Project : face_fusion_damo

import cv2
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import moviepy.editor as mp
import torch
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
import natsort


# 将视频video_path分割成图片和音频文件，保存到save_path文件夹中
def video2mp3_img(video_path, save_path):
    def _video2img(video_path, save_path):
        cap = cv2.VideoCapture(video_path)
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))  # 获取视频帧率
        i = 0
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(save_path + '/' + str(i) + '.jpg', frame)
                i += 1
            else:
                break
        cap.release()
        print(f"Video frame rate: {frame_rate}")
        return frame_rate

    def _video2mp3(video_path, save_path):
        # 提取音频并保存为临时文件（默认是WAV格式）
        audio_temp_file = os.path.join(save_path, 'audio.wav')
        ffmpeg_extract_audio(video_path, audio_temp_file)

        # 将音频转换为MP3格式
        audio_clip = mp.AudioFileClip(audio_temp_file)
        audio_temp_file = os.path.join(save_path, 'audio.mp3')
        audio_clip.write_audiofile(audio_temp_file)
        # 删除临时音频文件
        audio_clip.close()

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 视频分割
    frame_rate = _video2img(video_path, save_path)
    print("split picture finished!")
    # 视频提取音频
    _video2mp3(video_path, save_path)
    print("extract audio finished!")

    return frame_rate


# 将图片文件夹中的图片进行人脸替换，保存到save_dir文件夹中
def replace_all_img(template_dir, user_path, save_dir):
    # image_face_fusion = pipeline(Tasks.image_face_fusion, model='damo/cv_unet-image-face-fusion_damo')
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                template_path = os.path.join(root, file)
                replace_single_img(template_path=template_path, user_path=user_path,
                                   save_dir=save_dir)


# 将单张图片进行人脸替换，保存到save_dir文件夹中
def replace_single_img(template_path, user_path, save_dir):
    image_face_fusion = pipeline(Tasks.image_face_fusion, model='damo/cv_unet-image-face-fusion_damo')
    filename = os.path.basename(template_path)
    print(f"{filename} start face swapping!")
    # filename = os.path.splitext(os.path.basename(template_path))[0]

    # 替换面部依赖: template为原图,即视频拆分图; user为用户要替换脸的图
    result = image_face_fusion(dict(template=template_path, user=user_path))
    filepath = os.path.join(save_dir, filename)
    cv2.imwrite(filepath, result[OutputKeys.OUTPUT_IMG])

    # 释放CUDA内存
    # 只是删除了该内部函数作用域中的变量引用，而不会影响外部函数的变量
    del image_face_fusion
    torch.cuda.empty_cache()
    print(f"{filename} finished!")
    return filepath


# 将图片文件夹中的图片合成视频，保存到output_dir文件夹中
def img2mp4(save_name, output_dir, img_folder, mp3_folder, fps=25):
    images = []
    for root, dirs, files in os.walk(img_folder):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                images.append(file_path)
    # 将图片按照文件名进行自然排序
    images = natsort.natsorted(images)

    clips = [ImageSequenceClip(images, fps=fps)]
    video_clip = clips[0]
    audio_path = os.path.join(mp3_folder, 'audio.wav')
    audio_clip = AudioFileClip(audio_path)

    # 如果音频和视频时长不匹配，可以选择截取或重复音频以使其匹配视频长度
    if audio_clip.duration > video_clip.duration:
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    else:
        video_clip = video_clip.subclip(0, audio_clip.duration)

    video_clip = video_clip.set_audio(audio_clip)

    save_name = save_name + '.mp4'
    video_clip.write_videofile(os.path.join(output_dir, save_name), codec="libx264")
    return os.path.join(output_dir, save_name)


# 整个视频的替换人脸
def replace_video(video_path, user_path):
    # .py文件所在路径
    BASE = os.path.dirname(__file__)
    template_dir = os.path.join(BASE, 'video_split')
    save_dir = os.path.join(BASE, 'video_split_swap')
    output_dir = os.path.join(BASE, 'output')

    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将视频分割成图片和音频
    fps = video2mp3_img(video_path=video_path, save_path=template_dir)
    replace_all_img(template_dir=template_dir, user_path=user_path, save_dir=save_dir)
    save_path = img2mp4(save_name='swapped_video', output_dir=output_dir, img_folder=save_dir, mp3_folder=template_dir,
                        fps=fps)
    return save_path


# if __name__ == '__main__':
#     # .py文件所在路径
#     BASE = os.path.dirname(__file__)
#     # .ipynb文件所在路径
#     # BASE = os.getcwd()
#     # 设置工作路径为当前脚本所在的路径
#     os.chdir(BASE)
#
#     user_path = r'./input/Trump.jpg'
#     template_dir = r'./middle'
#     save_dir = r'./middle_after_swap'
#     output_dir = r'./output'
#     video_path = r'./input/zhan.mp4'
#
#     # 将视频分割成图片和音频
#     fps = video2mp3_img(video_path=video_path, save_path=template_dir)
#     replace_all_img(template_dir=template_dir, user_path=user_path, save_dir=save_dir)
#     img2mp4(save_name='Zhan_Trump', output_dir=output_dir, img_folder=save_dir, mp3_folder=template_dir, fps=fps)
