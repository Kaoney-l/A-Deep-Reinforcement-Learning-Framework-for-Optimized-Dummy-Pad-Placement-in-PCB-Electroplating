"""
创建数据集
"""

import os
from PIL import Image
import numpy as np
from pre_data_2 import y_value
import csv
import cv2
import re

import csv

# 假设你的文件名为 data.csv
file_name = 'dataset/index_data.csv'

# 读取文件并保存为列表
index_data = []
with open(file_name, mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        index_data.append(row)






# 创建一个空列表，用于存储所有图像的一维矩阵
with open(r'.\dataset\test_data.csv', 'w', newline='', encoding='utf-8') as file:
    for u in range(1, 2):
        y_data = y_value(r"C:\Users\LiYingGang\Desktop\data\data" + str(u) + r"\Untitled.txt")
        # 遍历文件夹中的图像文件
        image_data = []
        nums = []
        folder_path = r"D:\电镀CODE\Predata\data\image\data" + str(u)  # 替换为你的图像文件夹路径
        for i, filename in enumerate(os.listdir(folder_path)):
            if filename.endswith(".jpg") or filename.endswith(".png"):  # 只处理jpg和png格式的图像
                match = re.search(r'(\d+)', filename)
                number = int(match.group(1))
                nums.append(number)
                # 构建完整的图像文件路径
                image_path = os.path.join(folder_path, filename)
                # 读取图像
                image = Image.open(image_path)

                # 将图像转换为灰度图像
                image_gray = image.convert('L')

                # 将图像转换为NumPy数组
                image_array = np.array(image_gray)
                image_array = 255 - image_array
                # 将二维矩阵转换为一维矩阵
                image_flat = image_array.flatten()

                image_flat = image_flat.tolist()
                image_flat.append(index_data[i][0])
                image_flat.append(index_data[i][1])
                image_flat.append(y_data[number])
                #
                # 将一维矩阵添加到列表中
                image_data.append(image_flat)
        writer = csv.writer(file)
        writer.writerows(image_data)
    # 将列表保存到 txt 文件
    with open('numbers.txt', 'w') as f:
        for num in nums:
            f.write(f"{num}\n")

    print("数字已保存到 numbers.txt")
