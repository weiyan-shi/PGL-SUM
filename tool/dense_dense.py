import os
from PIL import Image

# 原始文件夹路径
source_folder = '/home/weiyan/Desktop/PGL-SUM/dense_dataset'
# 输出文件夹路径
output_folder = '/home/weiyan/Desktop/PGL-SUM/dense_dense_dataset'

# 如果输出文件夹不存在，则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历每个子文件夹
for subdir, _, files in os.walk(source_folder):
    # 提取当前子文件夹的名字
    current_folder_name = os.path.basename(subdir)
    
    segment_images = {}

    # 收集相同 segment 的所有图片
    for file in files:
        if file.endswith(".jpg") and "segment" in file:
            segment_number = file.split('_frame_')[0]  # 提取 segment 编号
            if segment_number not in segment_images:
                segment_images[segment_number] = []
            segment_images[segment_number].append(os.path.join(subdir, file))

    # 合并每个 segment 对应的图片
    for segment, image_paths in segment_images.items():
        images = [Image.open(img) for img in image_paths]
        
        # 假设所有图片大小相同
        width, height = images[0].size
        
        # 设置每行最多显示 5 张图片
        images_per_row = 5
        num_rows = (len(images) + images_per_row - 1) // images_per_row  # 计算需要多少行
        
        # 计算合并后的图片尺寸
        total_width = min(len(images), images_per_row) * width  # 根据图片数量调整总宽度
        total_height = num_rows * height  # 高度为行数乘以单张图片高度
        
        # 创建一个新的空白图像，用于拼接
        new_image = Image.new('RGB', (total_width, total_height))
        
        # 拼接图片
        x_offset = 0
        y_offset = 0
        for i, img in enumerate(images):
            new_image.paste(img, (x_offset, y_offset))
            x_offset += width
            
            # 每 5 张图片换一行
            if (i + 1) % images_per_row == 0:
                x_offset = 0
                y_offset += height
        
        # 输出图片的子文件夹，名字与当前子文件夹名字相同
        output_subdir = os.path.join(output_folder, current_folder_name)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        
        # 保存合并后的图片
        output_image_path = os.path.join(output_subdir, f'{segment}_combined.jpg')
        new_image.save(output_image_path)
        print(f'Saved {output_image_path}')