import os
import shutil

# 定义主文件夹路径和目标文件夹路径
main_folder = 'dataset'  # 主文件夹路径
output_folder = 'dense_dataset'  # 目标文件夹路径
os.makedirs(output_folder, exist_ok=True)

# 遍历主文件夹下的所有子文件夹
for subdir in os.listdir(main_folder):
    subdir_path = os.path.join(main_folder, subdir)

    # 确保只处理文件夹
    if os.path.isdir(subdir_path):
        # 获取子文件夹中的所有图片文件，并按名称排序
        images = sorted([f for f in os.listdir(subdir_path) if f.endswith(('.jpg', '.png'))])
        
        # 创建目标文件夹中的子文件夹
        output_subdir = os.path.join(output_folder, subdir)
        os.makedirs(output_subdir, exist_ok=True)
        
        # 每隔 8 张图片选择一张保存到目标文件夹
        for i in range(0, len(images), 8):
            image_path = os.path.join(subdir_path, images[i])
            new_image_path = os.path.join(output_subdir, images[i])
            
            # 复制文件到新文件夹
            shutil.copy(image_path, new_image_path)
            
print(f"图片已成功保存到 {output_folder}")
