from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import cv2
import os

# video_path = 'dataset/PCIT-Session-r-euHPfAAiM.mp4'
# video_path = 'dataset/interaction.mp4'
video_path = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/videos/video_category_test_video.mp4'


summarization_pipeline = pipeline(Tasks.video_summarization, model='damo/cv_googlenet_pgl-video-summarization')
result = summarization_pipeline(video_path)
print(f'video summarization output: {result}.')

video_name = os.path.splitext(os.path.basename(video_path))[0]
output_folder = os.path.join('dataset', video_name)
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

for idx, segment in enumerate(result['output']):
    start_frame, end_frame = segment['frame']
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    for frame_num in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if not ret:
            break
        output_filename = os.path.join(output_folder, f'segment_{idx}_frame_{frame_num}.jpg')
        cv2.imwrite(output_filename, frame)

cap.release()

print(f"saved in {output_folder}")