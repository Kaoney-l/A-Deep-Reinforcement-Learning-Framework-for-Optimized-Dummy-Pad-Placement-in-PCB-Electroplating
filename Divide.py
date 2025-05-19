
# 用于保存坐标的列表
polygons = []
current_polygon = []  # 用于保存当前多边形的坐标

# 用于保存每个多边形的最大X坐标和最大Y坐标的列表
extreme_coordinates = []

pad_file_path = r'data/surface.txt'
thresholds = 0.03
min_xx = float("inf")
max_xx = float("-inf")
min_yy = float("inf")
max_yy = float("-inf")
# 打开txt文件进行读取
with open(pad_file_path, 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 如果以"SE"开头，则开始一个新的多边形
        if line.startswith("SE"):
            # 如果当前多边形不为空，则将其添加到多边形列表中
            if current_polygon:
                polygons.append(current_polygon)
                # 计算并保存最大X、Y坐标和最小X、Y坐标
                max_x = max(coord[0] for coord in current_polygon)
                max_y = max(coord[1] for coord in current_polygon)
                min_x = min(coord[0] for coord in current_polygon)
                min_y = min(coord[1] for coord in current_polygon)

                if min_xx > min_x:
                    min_xx = min_x
                if max_xx < max_x:
                    max_xx = max_x
                if min_yy > min_y:
                    min_yy = min_y
                if max_yy < max_y:
                    max_yy = max_y


                extreme_coordinates.append((max_x + thresholds, max_y + thresholds, min_x - thresholds, min_y - thresholds))
                current_polygon = []  # 重置当前多边形列表
        # 如果以"OS"或者"OB"开头，则提取后两位坐标并添加到当前多边形列表中
        elif line.startswith("OS") or line.startswith("OB"):
            parts = line.split()
            x = float(parts[1])
            y = float(parts[2])
            current_polygon.append((x, y))

    # 添加最后一个多边形到多边形列表中
if current_polygon:
    polygons.append(current_polygon)
    # 计算并保存最大X、Y坐标和最小X、Y坐标
    max_x = max(coord[0] for coord in current_polygon)
    max_y = max(coord[1] for coord in current_polygon)
    min_x = min(coord[0] for coord in current_polygon)
    min_y = min(coord[1] for coord in current_polygon)
    extreme_coordinates.append((max_x + thresholds, max_y + thresholds, min_x - thresholds, min_y - thresholds))

# 将最大和最小坐标保存到txt文档中
with open('sfcoordinates.txt', 'w') as outfile:
    for coords in extreme_coordinates:
        outfile.write(f"{coords[0]} {coords[1]} {coords[2]} {coords[3]}\n")

print("保存完成！")


