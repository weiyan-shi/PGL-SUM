from moviepy.editor import VideoFileClip
import numpy as np

# 输入视频路径
video_path = '../dataset/Talk to Your Baby.mp4'

# 精华片段的时间段
segments = [
    {'start': '00:00:00.000', 'end': '00:00:03.083'},
    {'start': '00:00:36.875', 'end': '00:00:41.833'},
    {'start': '00:00:54.375', 'end': '00:00:55.583'},
    {'start': '00:00:58.125', 'end': '00:01:00.583'},
    {'start': '00:01:47.500', 'end': '00:01:50.583'},
    {'start': '00:01:56.250', 'end': '00:01:59.958'},
    {'start': '00:02:07.500', 'end': '00:02:09.958'},
    {'start': '00:02:20.000', 'end': '00:02:21.833'},
    {'start': '00:02:30.625', 'end': '00:02:31.833'},
    {'start': '00:02:48.125', 'end': '00:02:58.083'},
    {'start': '00:03:18.750', 'end': '00:03:21.833'},
    {'start': '00:03:32.500', 'end': '00:03:35.583'},
    {'start': '00:04:00.625', 'end': '00:04:01.208'},
    {'start': '00:04:21.250', 'end': '00:04:21.833'},
    {'start': '00:04:25.000', 'end': '00:04:25.583'},
    {'start': '00:04:34.375', 'end': '00:04:36.208'},
    {'start': '00:05:02.500', 'end': '00:05:03.083'},
    {'start': '00:05:09.375', 'end': '00:05:10.583'},
    {'start': '00:05:15.000', 'end': '00:05:16.000'}
]

# 加载原始视频
video = VideoFileClip(video_path)

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
            mask = np.full_like(frame, (255, 255, 0), dtype=np.uint8)
            return (frame * 0.5 + mask * 0.5).astype('uint8')
    return frame

# 对整个视频应用函数
highlighted_video = video.fl(lambda gf, t: add_highlight_mask(gf(t), t, segments))

# 输出视频
output_path = '../dataset/Talk to Your Baby/annotated_video.mp4'
highlighted_video.write_videofile(output_path, codec="libx264")

print(f"标注视频已保存至 {output_path}")
