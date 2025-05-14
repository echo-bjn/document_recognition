import os
import shutil

# 指定源文件夹和目标文件夹路径
src_folder = 'VOCdevkit\VOC2007\JPEGImages'
dst_folder = 'VOCdevkit\VOC2007\\temp'

# 获取源文件夹中的所有文件
files = os.listdir(src_folder)

# 复制文件到目标文件夹
for index, file in enumerate(files):
    src_file = os.path.join(src_folder, file)
    dst_file = os.path.join(dst_folder, str(index+13*9).zfill(3) +".jpg")
    shutil.copy(src_file, dst_file)
    print(f"已将 {file} 复制到目标文件夹。")

print("文件复制完成。")