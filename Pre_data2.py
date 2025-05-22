"""
边界的子板图像中画dummy pad和pad等元器件
"""
from PIL import Image, ImageDraw
import csv
import math
import os
from Utils import y_value

# 检查图片文件是否存在的函数
def load_image_if_exists(image_path):
    if os.path.exists(image_path):
        image = Image.open(image_path)
        return image
    else:
        return None

def read_coordinates(filename):
    extreme_coordinates = []

    with open(filename, 'r') as file:
        for line in file:
            # 从每一行中提取坐标信息
            values = line.strip().split()
            # 将字符串转换为浮点数并添加到坐标列表中
            max_x, max_y, min_x, min_y = map(float, values)
            extreme_coordinates.append((max_x, max_y, min_x, min_y))

    return extreme_coordinates


def point_in_range(point, range):
    x, y = point
    max_x, max_y, min_x, min_y = range
    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    return False


# 缩放坐标到图像尺寸
def scale_coord(x, y, m_in_sf):
    max_x, max_y, min_x, min_y = m_in_sf
    scaled_x = int((x - min_x) * width / (max_x - min_x))
    scaled_y = int((y - min_y) * height / (max_y - min_y))
    return scaled_x, scaled_y



for u in range(1,2):
    pad_file_path = r"C:\Users\LiYingGang\Desktop\data\data" + str(u) + r"\features"
    sc_set = []
    # 读取文件并提取以'A'开头的数据


    sliding_scale = 1000
    line_size = 4

    # 从coordinates.txt文件中读取坐标信息
    extreme_coordinates = read_coordinates('sfcoordinates.txt')


    #圆弧数据
    arc_in_sfs = [[] for _ in extreme_coordinates]
    sc_arc_in_sfs = [[] for _ in extreme_coordinates]

    #直线数据
    l_in_sfs = [[] for _ in extreme_coordinates]
    sc_l_in_sfs = [[] for _ in extreme_coordinates]

    #pad数据
    pad_in_sfs = [[] for _ in extreme_coordinates]
    sc_pad_in_sfs = [[] for _ in extreme_coordinates]



    arc_data = None
    #多边形起点
    start_point = None
    with open(pad_file_path, 'r') as file:
        for line in file:
            if line.startswith('A'):
                arc_data = line.split()[1:7]  # 提取数据
                arc_data = [float(x) for x in arc_data]  # 将数据转换为浮点数

                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range([arc_data[0], arc_data[1]], extreme_coordinate):
                        arc_in_sfs[i].append(arc_data)

                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)

                        x1, y1 = scale_coord(arc_data[0], arc_data[1], extreme_coordinate)
                        x2, y2 = scale_coord(arc_data[2], arc_data[3], extreme_coordinate)
                        x3, y3 = scale_coord(arc_data[4], arc_data[5], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        y3 = height - y3
                        sc_arc_in_sfs[i].append([x1, y1, x2, y2, x3, y3])

            if line.startswith('L'):
                # 提取直线的起始坐标
                coordinates = line.split()[1:5]  # 假设坐标是以空格分隔的，提取索引为1到4的元素
                # 转换坐标为浮点数
                coordinates = [float(coord) for coord in coordinates]

                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range([coordinates[0], coordinates[1]], extreme_coordinate):
                        l_in_sfs[i].append(coordinates)

                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)

                        x1, y1 = scale_coord(coordinates[0], coordinates[1], extreme_coordinate)
                        x2, y2 = scale_coord(coordinates[2], coordinates[3], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        sc_l_in_sfs[i].append([x1, y1, x2, y2])
                        # 检查行首字母是否为'P'


            if line.startswith('P'):
                # 提取圆的坐标
                coordinates = line.split()[1:3]  # 假设坐标是以空格分隔的，提取索引为1到2的元素
                # 转换坐标为浮点数
                coordinates = [float(coord) for coord in coordinates]
                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range([coordinates[0], coordinates[1]], extreme_coordinate):
                        pad_in_sfs[i].append(coordinates)
                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)
                        x1, y1 = scale_coord(coordinates[0], coordinates[1], extreme_coordinate)
                        y1 = height - y1
                        sc_pad_in_sfs[i].append([x1, y1])
                        # 检查行首字母是否为'P'



    with open(pad_file_path, 'r') as file:
        for line in file:
            tokens = line.strip().split()
            if line.startswith('OB'):
                # 多边形起点
                start_point = (float(tokens[1]), float(tokens[2]))
            elif line.startswith('OS'):
                # 线段
                end_point = (float(tokens[1]), float(tokens[2]))
                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range(start_point, extreme_coordinate):
                        l_in_sfs[i].append((start_point, end_point))

                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)
                        x1, y1 = scale_coord(start_point[0], start_point[1], extreme_coordinate)
                        x2, y2 = scale_coord(end_point[0], end_point[1], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        sc_l_in_sfs[i].append([x1, y1, x2, y2])


                start_point = end_point
            elif line.startswith('OC'):
                # 圆弧
                end_point = (float(tokens[1]), float(tokens[2]))
                center_point = (float(tokens[3]), float(tokens[4]))
                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range(start_point, extreme_coordinate):
                        arc_in_sfs[i].append([start_point[0], start_point[1], end_point[0], end_point[1], center_point[0], center_point[1]])


                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)

                        x1, y1 = scale_coord(start_point[0], start_point[1], extreme_coordinate)
                        x2, y2 = scale_coord(end_point[0], end_point[1], extreme_coordinate)
                        x3, y3 = scale_coord(center_point[0], center_point[1], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        y3 = height - y3
                        sc_arc_in_sfs[i].append([x1, y1, x2, y2, x3, y3])

                start_point = end_point

    # 打印结果
    em_datas = []
    for i, sc_arc_in_sf in enumerate(sc_arc_in_sfs):
        sc_l_in_sf = sc_l_in_sfs[i]
        sc_pad_in_sf = sc_pad_in_sfs[i]


        width = int((extreme_coordinates[i][0] - extreme_coordinates[i][2]) * sliding_scale)
        height = int((extreme_coordinates[i][1] - extreme_coordinates[i][3]) * sliding_scale)
        image = load_image_if_exists("data/image/data" + str(u) + "/output_" + str(i) +"x"+ ".png")
        if image is None:
            continue
        x = 0
        # if width == int(0.8199842519689984 * sliding_scale):
        if x == 0:
            # 创建一个绘图对象
            draw = ImageDraw.Draw(image)

            #画弧
            for sc_arc in sc_arc_in_sf:
                x1, y1, x2, y2, x3, y3 = sc_arc

                # Calculate center and radius of the circle
                cx = x3
                cy = y3
                radius = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
                # Calculate start and end angles
                start_angle = math.atan2(y1 - cy, x1 - cx)
                end_angle = math.atan2(y2 - cy, x2 - cx)
                # Convert angles to degrees
                start_angle = math.degrees(start_angle)
                end_angle = math.degrees(end_angle)
                # Ensure end angle is greater than start angle
                if start_angle > end_angle:
                    end_angle += 360

                # PIL's arc function requires angles in the format (start, end)
                # where 0 degrees is at the 3 o'clock position
                draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), start=start_angle, end=end_angle, fill="red",
                        width=line_size)


            for sc_line in sc_l_in_sf:
                x1, y1, x2, y2 = sc_line
                # 在图像上绘制直线
                draw.line([(x1, y1), (x2, y2)], fill="red", width=line_size)


            for sc_pad in sc_pad_in_sf:
                x, y = sc_pad
                # 计算圆的半径（这里假设半径为固定值）
                radius = 3  # 你可以根据需要调整半径的大小
                # 在图像上绘制圆
                draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], outline="green")

        image.save("data/image/data" + str(u) + "/output_" + str(i) +"x"+ ".png")


    # 定义保存到文本文件的文件名
    file_name = "em_data.txt"
    em_datas = []
    max_num = 0

    # 打开文件以写入模式
    for i, arc_in_sf in enumerate(arc_in_sfs):
        num = 0
        l_in_sf = l_in_sfs[i]
        pad_in_sf = pad_in_sfs[i]
        # if len(arc_in_sf) == 0 and len(l_in_sf) == 0 and len(pad_in_sf) == 0:
        #     continue
        width = int((extreme_coordinates[i][0] - extreme_coordinates[i][2]) * sliding_scale)
        height = int((extreme_coordinates[i][1] - extreme_coordinates[i][3]) * sliding_scale)
        if 159 == 159:
            em_data = []
            # for arc in arc_in_sf:
            #     num += 1
            #     print(arc)
            #     x1, y1, x2, y2, x3, y3 = arc
            #     em_data.append(x1)
            #     em_data.append(y1)
            #     break
            # if num==1:
            #     break
            # for line in l_in_sf:
            #     num += 1
            #     x1, y1, x2, y2 = line
            #     em_data.append(2)
            #     em_data.append(x1)
            #     em_data.append(y1)
            #     break
            # if num == 1:
            #     break
            for pad in pad_in_sf:
                num += 1
                x1, y1 = pad
                em_data.append(x1)
                em_data.append(y1)
                break
            em_datas.append(em_data)
            # if num < 60:
            #     for i in range(60-num):
            #         for j in range(7):
            #             em_data.append(0)


    with open('.\dataset\em_train_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(em_datas)
    # with open('result/Arc_sc.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['X1', 'Y1', 'X2', 'Y2','X3', 'Y3', 'X1-sc', 'Y1-sc', 'X2-sc', 'Y2-sc','X3-sc', 'Y3-sc'])  # 写入标题行
    #     for row in sc_set:
    #         writer.writerow(row)
