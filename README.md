# A-Deep-Reinforcement-Learning-Framework-for-Optimized-Dummy-Pad-Placement-in-PCB-Electroplating

This repository contains the relevant raw data and code for generating the dataset.

## Data Description

### Introduction to Raw Data

本项目所使用的原始数据来源于自行采集的实验数据。  
该数据集用于PCB电镀（Electroplating）预测及PCB虚拟焊盘（Dummy Pad）布局优化。

每个样本包含以下三个文件：  
- `cbm11856_020.tgz`：PCB设计的源文件。  
- `features`：矢量文件，包含需要电镀铜的通孔、Dummy pad及Virtual Sub-Board Boundary的物理矢量位置。  
- `Untitled.txt`：基于COMSOL Multiphysics®软件设计的电镀槽多物理场仿真结果，包含不同未知条件下的电镀铜数据。  

### Data Preprocessing

本项目提供了将原始数据处理为模型训练和测试数据集的代码，处理流程包括：  
1. `Divide.py`：将整版PCB分解为多个子板。  
2. `Pre_data.py`：提取Dummy pad和通孔的物理矢量位置，转换为像素坐标。  
3. `Pre_data2.py`：提取Virtual Sub-Board Boundary的物理矢量位置，转换为像素坐标。  
4. `Create_dataset.py`：整理处理结果，生成模型训练和测试所需的数据集。  

## Sample Illustration of a Complete PCB Panel
![bb626b2cdc51cdd161dac967ce5fa0a](https://github.com/user-attachments/assets/44b24963-9b60-45c8-ad30-e0b5d387effb)

