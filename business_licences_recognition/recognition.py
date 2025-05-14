# -*- coding:utf-8 -*-

import math
import numpy as np 
from paddleocr import PaddleOCR, draw_ocr

def euclidean_distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def greater(pt1, pt2, pt3, pt4):
    width = euclidean_distance(pt1, pt2)
    height = euclidean_distance(pt1, pt4)
    
    return height > width

def divide_into_blocks(text_region, num_blocks):
    pt1, pt2, pt3, pt4 = text_region
    block_height = round((pt4[1] - pt1[1]) / num_blocks, 1)
    blocks = []
    
    for i in range(num_blocks):
        new_pt1 = [pt1[0], pt1[1] + i * block_height]
        new_pt2 = [pt2[0], pt1[1] + i * block_height]
        new_pt3 = [pt2[0], pt1[1] + (i + 1) * block_height]
        new_pt4 = [pt1[0], pt1[1] + (i + 1) * block_height]
        blocks.append([new_pt1, new_pt2, new_pt3, new_pt4])
    
    return blocks

def deleteword(data):   
    filtered_data = [item for item in data if item[1][0] != '营业执']
    filtered_data = [item for item in filtered_data if item[1][0] != '营业']
    filtered_data = [item for item in filtered_data if item[1][0] != '营']
    filtered_data = [item for item in filtered_data if item[1][0] != '营业执照']
    filtered_data = [item for item in filtered_data if item[1][0] != '（副本']
    filtered_data = [item for item in filtered_data if item[1][0] != '（副']
    filtered_data = [item for item in filtered_data if item[1][0] != '（副本）']
    filtered_data = [item for item in filtered_data if item[1][0] != '(副本)']
    filtered_data = [item for item in filtered_data if item[1][0] != '(副本']
    filtered_data = [item for item in filtered_data if item[1][0] != '(副']
    filtered_data = [item for item in filtered_data if item[1][0] != '(副本）']
    return filtered_data


def characters(img_path):
    ocr = PaddleOCR(use_angle_cls=True,use_gpu=False)
    result = ocr.ocr(img_path, cls=True)
    new_result = []
    for text_regions in result:
        for text_region_item in text_regions:
            text_region = text_region_item[0]
            recognized_text = text_region_item[1][0]
            confidence = text_region_item[1][1]

            pt1, pt2, pt3, pt4 = text_region
            
            if greater(pt1, pt2, pt3, pt4):
                num_blocks = len(recognized_text)
                blocks = divide_into_blocks(text_region, num_blocks)
                
                for i in range(num_blocks):
                    char = recognized_text[i]
                    new_result.append([blocks[i], (char, confidence)])
            else:
                new_result.append([text_region, (recognized_text, confidence)])

    positions = [(entry[0][0][0], entry[0][0][1], entry) for entry in new_result]
    positions.sort(key=lambda p: p[1])
    index = 0
    while index < len(positions) - 1:
        if positions[index + 1][1] - positions[index][1] < 15:
            temp_list = [positions[index]]
            for i in range(index + 1, len(positions)):
                if positions[i][1] - positions[index][1] < 15:
                    temp_list.append(positions[i])
                else:
                    break
            temp_list.sort(key=lambda p: p[0])
            positions[index:(index + len(temp_list))] = temp_list
            index = index + len(temp_list)
        else:
            index += 1

    sorted_data = [entry[2] for entry in positions]

    target_text = '名'
    target_x_coords = []

    for item in sorted_data:
        text_region, (recognized_text, confidence) = item
        if target_text in recognized_text:
            top_left_x = text_region[0][0]
            target_x_coords.append(top_left_x)

    filtered_data = sorted_data

    if target_x_coords:
        x = min(target_x_coords)
        threshold = x - 70 
        filtered_data = [item for item in sorted_data if item[0][0][0] >= threshold]

    sorted_data = sorted(filtered_data, key=lambda x: len(x[1][0]), reverse=True)
    y = sorted_data[0][0][1][0]
    print(y)
    threshold = y + 50 
    filtered_data = [item for item in filtered_data if item[0][0][0] <= threshold]

    filtered_data = deleteword(filtered_data)

    return filtered_data


# img_path = '222.jpg'
# filtered_data = wenzi(img_path)
# for item in filtered_data:
#     print(item)
# # print(filtered_data)