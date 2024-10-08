import json
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

# 加载原始视频
video_path = "/home/weiyan/Desktop/MCGaze/MCGaze_demo/output_video.mp4"
video = VideoFileClip(video_path)

# 加载外部音频
audio_path = "/home/weiyan/Desktop/PGL-SUM/dataset/Parent_Child_Interaction_Therapy_PCIT_Effective_Treatment_Effective/Parent_Child_Interaction_Therapy_PCIT_Effective_Treatment_Effective.wav"
audio = AudioFileClip(audio_path)

# 从 key-event.json 读取片段信息
with open('/home/weiyan/Desktop/PGL-SUM/dataset/Parent_Child_Interaction_Therapy_PCIT_Effective_Treatment_Effective/key-event.json', 'r') as f:
    segments = json.load(f)

# 将时间戳转换为秒，方便处理
def time_to_seconds(time_str):
    return sum([float(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(":")))])

# 创建透明蒙版（50%透明度的黄色）
def add_highlight_mask(frame, t, segments):
    for segment in segments:
        start_time = time_to_seconds(segment['start'])
        end_time = time_to_seconds(segment['end'])
        if start_time <= t <= end_time:
            # 添加透明黄色蒙版
            mask = np.full_like(frame, (255, 255, 0), dtype=np.uint8)  # 黄色蒙版
            return (frame * 0.7 + mask * 0.3).astype('uint8')  # 50%透明度
    return frame

# 创建标题叠加函数
def add_title_clip(clip, segments):
    # 创建标题视频层
    clips = [clip]  # 保留原始视频的所有部分
    for segment in segments:
        start_time = time_to_seconds(segment['start'])
        end_time = time_to_seconds(segment['end'])
        
        # 创建黑色字体的标题文本
        title_text = TextClip(segment['title'], fontsize=20, color='black', bg_color='yellow', method='caption').set_position('top').set_duration(end_time - start_time)
        
        # 创建只有在这个时间段才出现的子视频
        title_subclip = title_text.set_start(start_time).set_end(end_time)
        
        # 将标题层加入列表
        clips.append(title_subclip)
    
    return CompositeVideoClip(clips, size=clip.size)

# 对整个视频应用高亮蒙版，保留音频
highlighted_video = video.fl(lambda gf, t: add_highlight_mask(gf(t), t, segments))

# 添加标题叠加效果
annotated_video = add_title_clip(highlighted_video, segments)

# 将外部音频与视频结合
final_video = annotated_video.set_audio(audio)

# 输出视频，确保音频保留
output_path = '/home/weiyan/Desktop/PGL-SUM/dataset/Parent_Child_Interaction_Therapy_PCIT_Effective_Treatment_Effective/Parent_Child_Interaction_Therapy_PCIT_Effective_Treatment_Effective-annotated_eye.mp4'
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

print(f"标注视频已保存至 {output_path}")
