from moviepy.editor import VideoFileClip, concatenate_videoclips


# 输入视频路径
video_path = 'dataset/Talk to Your Baby.mp4'

# 根据提供的时间戳，定义需要保留的片段
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

# 加载视频
video = VideoFileClip(video_path)

# 将时间戳转换为秒，并剪辑视频
clips = []
for segment in segments:
    start_time = sum([float(x) * 60 ** i for i, x in enumerate(reversed(segment['start'].split(":")))])
    end_time = sum([float(x) * 60 ** i for i, x in enumerate(reversed(segment['end'].split(":")))])
    clip = video.subclip(start_time, end_time)
    clips.append(clip)

# 将所有片段合并为一个视频
final_clip = concatenate_videoclips(clips)

# 保存精华版视频
output_path = 'dataset/Talk to Your Baby/highlight_video.mp4'
final_clip.write_videofile(output_path, codec="libx264")

print(f"精华版视频已保存至 {output_path}")
