import numpy as np
import matplotlib.pyplot as plt
import csv


def scale_coord(x, y, m_in_sf):
    max_x, max_y, min_x, min_y = m_in_sf
    scaled_x = int((x - min_x) * width / (max_x - min_x))
    scaled_y = int((y - min_y) * height / (max_y - min_y))
    return scaled_x, scaled_y


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

# 创建空的 X、Y 坐标和厚度值列表
x_coords = []
y_coords = []
thickness_values = []
data_path = 'data\CBM11856_020-T.txt'
# 从coordinates.txt文件中读取坐标信息
extreme_coordinates = read_coordinates('sfcoordinates.txt')

y_in_range = [[] for _ in range(len(extreme_coordinates))]
sc_y_in_range = [[] for _ in range(len(extreme_coordinates))]

min_x = float("inf")
max_x = float("-inf")
min_y = float("inf")
max_y = float("-inf")

# 打开文件
with open(data_path, 'r', encoding='UTF-8') as file:
    # 跳过前8行
    for _ in range(8):
        next(file)

    # 从第九行开始逐行读取数据
    for line in file:
        arc_data = line.split()[1:7]  # 提取数据
        # 按空格分割每行数据
        data = line.split()
        # 如果该行不包含4个数值则跳过
        if len(data) != 4:
            continue
        # 提取X、Y坐标和厚度值
        x = float(data[0])/25
        y = float(data[1])/25
        thickness = float(data[3])
        if min_x > x:
            min_x = x
        if max_x < x:
            max_x = x
        if min_y > y:
            min_y = y
        if max_y < y:
            max_y = y

        for i, extreme_coordinate in enumerate(extreme_coordinates):
            if point_in_range([x, y], extreme_coordinate):
                y_in_range.append([x, y, thickness])

                width = int((extreme_coordinate[0] - extreme_coordinate[2]) * 1000)
                height = int((extreme_coordinate[1] - extreme_coordinate[3]) * 1000)

                x1, y1 = scale_coord(x, y, extreme_coordinate)
                y1 = height - y1
                sc_y_in_range[i].append([x1, y1, thickness])



        # 将提取的数据添加到列表中
        x_coords.append(x)
        y_coords.append(y)
        thickness_values.append(thickness)

# 将列表转换为 NumPy 数组
x_coords = np.array(x_coords)
y_coords = np.array(y_coords)
thickness_values = np.array(thickness_values)

# 创建二维数组来存储厚度值
grid_size = 128  # 定义热力图的网格大小
heatmap = np.zeros((grid_size, grid_size))

x_min = x_coords.min()
x_max = x_coords.max()
y_min = y_coords.min()
y_max = y_coords.max()

counter = np.zeros((grid_size, grid_size), dtype=int)
heatmap_max = np.zeros((grid_size, grid_size))

avg_data = []
max_data = []
counter_data = []

forces = []
forces_data = []

counter_zeros = []
# 将坐标映射到网格上，并计算每个网格内的厚度值平均值和最大值
for x, y, thickness in zip(x_coords, y_coords, thickness_values):
    grid_x = int((x - x_coords.min()) / (x_coords.max() - x_coords.min()) * (grid_size-1))
    grid_y = int((y - y_coords.min()) / (y_coords.max() - y_coords.min()) * (grid_size-1))
    heatmap[grid_x, grid_y] += thickness
    if thickness > heatmap_max[grid_x, grid_y]:
        heatmap_max[grid_x, grid_y] = thickness
    counter[grid_x, grid_y] += 1

for i in range(grid_size):
    for j in range(grid_size):
        if counter[i, j] > 0:
            heatmap[i, j] = heatmap[i, j]/counter[i, j]
            avg_data.append((i, j, heatmap[i, j]))
            max_data.append((i, j, heatmap_max[i, j]))
        counter_data.append((i, j, counter[i, j]))


for i in range(grid_size):
    for j in range(grid_size):
        if counter[i, j] > 100:
            forces.append((i,j))
            print(i, j)
            break

for i, j in forces:
    for x, y, thickness in zip(x_coords, y_coords, thickness_values):
        grid_x = int((x - x_coords.min()) / (x_coords.max() - x_coords.min()) * (grid_size - 1))
        grid_y = int((y - y_coords.min()) / (y_coords.max() - y_coords.min()) * (grid_size - 1))
        if grid_x == i and grid_y == j:
            forces_data.append((x, y, thickness))




















# for i in range(grid_size):
#     for j in range(grid_size):
#         if counter[i, j] == 0:
#             counter_zeros.append((i, j, 100))
#
# with open('result/counter_zeros.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['X', 'Y', 'Value'])  # 写入标题行
#     for row in counter_zeros:
#         writer.writerow(row)


# with open('result/forces_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['X', 'Y', 'Value'])  # 写入标题行
#     for row in forces_data:
#         writer.writerow(row)
#
#
#
#
#
# # 将数据写入CSV文件
# with open('result/avg_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['X', 'Y', 'Value'])  # 写入标题行
#     for row in avg_data:
#         writer.writerow(row)
#
# with open('result/max_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['X', 'Y', 'Value'])  # 写入标题行
#     for row in max_data:
#         writer.writerow(row)
#
# with open('result/counter_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['X', 'Y', 'Value'])  # 写入标题行
#     for row in counter_data:
#         writer.writerow(row)

# # 创建一个1x3的布局
# fig, axs = plt.subplots(1, 3, figsize=(18, 6))
#
# # 在第一个subplot中绘制厚度热力图
# im1 = axs[0].imshow(counter, cmap='YlGnBu', interpolation='nearest')
# axs[0].set_title('Count')
# fig.colorbar(im1, ax=axs[0], label='Thickness')
# axs[0].set_xlabel('X')
# axs[0].set_ylabel('Y')
# axs[0].set_aspect('equal')
#
# # 在第二个subplot中绘制计数热力图
# im2 = axs[1].imshow(heatmap, cmap='YlGnBu', interpolation='nearest')
# axs[1].set_title('avg')
# fig.colorbar(im2, ax=axs[1], label='Thickness')
# axs[1].set_xlabel('X')
# axs[1].set_ylabel('Y')
# axs[1].set_aspect('equal')
#
# # 在第三个subplot中绘制计数热力图
# im3 = axs[2].imshow(heatmap_max, cmap='YlGnBu', interpolation='nearest')
# axs[2].set_title('max')
# fig.colorbar(im3, ax=axs[2], label='Thickness')
# axs[2].set_xlabel('X')
# axs[2].set_ylabel('Y')
# axs[2].set_aspect('equal')
#
# # 调整布局以防止重叠
# plt.tight_layout()
#
# # 保存图像
# plt.savefig('heatmaps.png')
#
# # 显示图像
# plt.show()