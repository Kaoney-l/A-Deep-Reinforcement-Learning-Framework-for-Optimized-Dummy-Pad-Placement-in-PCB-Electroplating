# A-Deep-Reinforcement-Learning-Framework-for-Optimized-Dummy-Pad-Placement-in-PCB-Electroplating

This repository contains the relevant raw data and code for generating the dataset.

---

## Data Description

### Introduction to Raw Data

The raw data used in this project originate from actual PCB boards used in production.
This dataset is intended for PCB electroplating prediction and PCB dummy pad layout optimization.

Each sample contains the following three files:

* `cbm11856_020.tgz`: An ODB++ file. It serves as the source file for PCB design, including input, matrix, flows, steps, symbols, and other data. It can be directly used for simulation with COMSOL Multiphysics® software.
* `features`: A vector file. It contains the physical vector locations of plated-through holes, dummy pads, and virtual sub-board boundaries that require copper plating.
* `Untitled.txt`: A vector file. It contains electroplating copper data under various unknown conditions based on multiphysics simulation of the plating tank designed with COMSOL Multiphysics® software.

### Data Preprocessing

This project provides code to process the raw data into datasets suitable for model training and testing. The preprocessing workflow includes:

1. `Divide.py`: Divides the full PCB into multiple sub-boards.
2. `Pre_data.py`: Extracts the physical vector positions of dummy pads and plated-through holes and converts them to pixel coordinates.
3. `Pre_data2.py`: Extracts the physical vector positions of virtual sub-board boundaries and converts them to pixel coordinates.
4. `Create_dataset.py`: Organizes the processed results to generate datasets required for model training and testing.

## Sample Illustration of a Complete PCB Panel
![fd3e25c3890f151eac1ea1aa3dd122e](https://github.com/user-attachments/assets/805f2a57-bcea-4103-b1af-6961d5cdbd2b)


