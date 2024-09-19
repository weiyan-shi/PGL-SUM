from moviepy.editor import VideoFileClip 
import numpy as np

# 输入视频路径
video_path = '../dataset/Talk to Your Baby.mp4'

# 精华片段的时间段（替换后的关键事件时间段）
segments = [
  {
    "title": "Checking if the child is done",
    "start": "00:00:00",
    "end": "00:00:03",
    "description": "Mom: [Benjamin, are you all done?]\nMom asks if the child has finished a task, initiating interaction.\nChild: [Yeah.]\nChild responds to confirm completion."
  },
  {
    "title": "Guiding polite expression",
    "start": "00:00:03",
    "end": "00:00:14",
    "description": "Mom: [Can you say may?]\nMom tries to guide the child to say 'may'.\nMom: [Please.]\nContinues to guide the child to learn polite expressions.\nChild: [Bye, Mom.]\nThe child tries to respond, learning the polite expression 'bye'."
  },
  {
    "title": "Asking about breakfast choice",
    "start": "00:00:55",
    "end": "00:00:59",
    "description": "Mom: [Benjamin, would you like some scrambled eggs this morning?]\nMom asks about the child's breakfast preference, guiding participation in the conversation.\nChild: [Mm-hmm.]\nChild responds, showing interest in scrambled eggs."
  },
  {
    "title": "Guiding participation in cooking",
    "start": "00:01:03",
    "end": "00:01:47",
    "description": "Mom: [You wanna watch mama while I make them?]\nMom asks if the child wants to watch the cooking process.\nChild: [Yeah.]\nChild responds, willing to participate.\nMom: [Can you stir that for Mama?]\nMom invites the child to stir the scrambled eggs, interactive teaching.\nChild: No verbal response, but may participate through action."
  },
  {
    "title": "Auditory perception interaction",
    "start": "00:01:10",
    "end": "00:01:27",
    "description": "Mom: [Do you hear that sound? Do you hear the cracking noise?]\nMom asks questions to draw the child's attention to the sound, helping them perceive the environment.\nMom: [Can you say crack?]\nMom continues to guide the child to try saying 'crack'.\nChild: No clear response but may be learning the new word through observation."
  },
  {
    "title": "Fruit interaction and vocabulary learning",
    "start": "00:01:56",
    "end": "00:02:09",
    "description": "Mom: [Benjamin, would you like some berries while Mama makes your eggs?]\nMom asks if the child wants to eat berries, initiating a new interaction.\nMom: [Berries?]\nConfirms again, guiding the child to respond.\nChild: No response, but Mom continues reinforcing vocabulary through repetition.\nMom: [Can you say berry?]\nEncourages the child to say 'berry'.\nMom: [Do you like strawberries?]\nExpands vocabulary further by introducing 'strawberries'."
  },
  {
    "title": "Cooling scrambled eggs interaction",
    "start": "00:02:36",
    "end": "00:02:44",
    "description": "Mom: [Can you blow them with me?]\nMom invites the child to blow on the food together, teaching a practical life skill interactively.\nChild: No verbal response but may participate through action."
  },
  {
    "title": "Sharing and refusal interaction",
    "start": "00:02:59",
    "end": "00:03:08",
    "description": "Mom: [Can mama have a bite of your eggs?]\nMom asks to share food, initiating interaction.\nChild: [No.]\nChild clearly refuses, expressing their preference.\nMom: [Oh, mama's gonna eat some too.]\nMom humorously responds to the child's refusal, continuing the interaction."
  },
  {
    "title": "Playful interaction",
    "start": "00:03:08",
    "end": "00:03:18",
    "description": "Mom: [Can mama have a bite of your hand?]\nMom playfully interacts with the child, adding fun to the conversation.\nChild: [No.]\nChild refuses again, expressing their will.\nMom: [I'm going to eat you up.]\nMom continues the playful language to maintain engagement."
  },
  {
    "title": "Finger counting interaction",
    "start": "00:03:34",
    "end": "00:03:56",
    "description": "Mom: [Can you count your fingers with me while we wipe?]\nMom guides the child in counting fingers as part of a learning game.\nMom: [1, 2, 3... 9 and 10!]\nMom progressively leads the child through counting from 1 to 10, completing the interactive teaching.\nChild: May participate through action or verbal responses."
  }
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
