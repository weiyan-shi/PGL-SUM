import cv2
import os
import numpy as np

# 源文件夹路径（包含子文件夹）
source_folder = 'dataset'
# 目标文件夹路径（用于存放拼接后的图片）
target_folder = 'dense_dense_dataset'

# 创建拼接图片的函数
def combine_images(images, per_row=4):
    rows = []
    for i in range(0, len(images), per_row):
        row_images = images[i:i + per_row]
        # 如果图像数量不足，补齐空白图像
        while len(row_images) < per_row:
            row_images.append(np.zeros_like(row_images[0]))  # 添加空白图像填充
        # 水平拼接每行图片
        rows.append(np.hstack(row_images))
    # 纵向拼接所有行
    return np.vstack(rows)

# 遍历源文件夹下的所有子文件夹
for subfolder in os.listdir(source_folder):
    subfolder_path = os.path.join(source_folder, subfolder)

    # 检查是否是子文件夹
    if os.path.isdir(subfolder_path):
        # 创建在目标文件夹中的同名子文件夹
        target_subfolder = os.path.join(target_folder, subfolder)
        os.makedirs(target_subfolder, exist_ok=True)

        # 读取子文件夹中的所有图片
        all_images = sorted([img for img in os.listdir(subfolder_path) if img.endswith('.jpg')])

        # 根据 segment_{idx} 分组图片
        segment_images = {}
        for img_file in all_images:
            # 假设文件名格式为 segment_{idx}_frame_{frame_num}.jpg
            segment_idx = int(img_file.split('_')[1])
            if segment_idx not in segment_images:
                segment_images[segment_idx] = []
            segment_images[segment_idx].append(img_file)

        # 遍历每个 segment，并选取每隔 8 张图片进行拼接
        for idx, images in segment_images.items():
            selected_images = images[::8]  # 每隔 8 张选一张

            images_to_combine = []
            for img_file in selected_images:
                img_path = os.path.join(subfolder_path, img_file)
                img = cv2.imread(img_path)
                images_to_combine.append(img)

            # 拼接选中的图片，每行 4 张
            combined_image = combine_images(images_to_combine, per_row=4)

            # 保存拼接后的图片到目标文件夹中的同名子文件夹
            output_filename = os.path.join(target_subfolder, f'segment_{idx}_combined.jpg')
            cv2.imwrite(output_filename, combined_image)

print(f"所有拼接的图片已保存至文件夹 {target_folder}")
