import cv2
import numpy as np

def determine(image):
    gray = image
    threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    border_thickness = 2
    height, width = threshold.shape
    
    threshold[0:border_thickness+45, :] = 0
    threshold[height-(border_thickness+45):height, :] = 0
    threshold[:, 0:border_thickness+45] = 0
    threshold[:, width-(border_thickness+45):width] = 0
    threshold[0:669, 0:205] = 0
    threshold[530:669, 0:350] = 0
    threshold[0:520,680:1084] = 0

    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
    dilation = cv2.dilate(threshold, element2, iterations = 1)
    erosion = cv2.erode(dilation, element1, iterations = 1)
    dilation2 = cv2.dilate(erosion, element2, iterations = 3)

    contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    resize_copy = gray.copy()
    res = cv2.drawContours(resize_copy, contours, -1, (255, 0, 0), 2)

    positions = []
    resize_copy = gray.copy()
    index = 0
    for contour in reversed(contours):
        epsilon = 0.002 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv2.boundingRect(approx)
        if h > 10 and x < 600 and y < 750 and x > 20 and y > 20 :
            res = cv2.rectangle(resize_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            positions.append((x, y, w, h))

    positions.sort(key=lambda p: p[1])
    index = 0
    while index < len(positions) - 1:
        if positions[index + 1][1] - positions[index][1] < 10:
            temp_list = [positions[index + 1], positions[index]]
            for i in range(index + 1, len(positions)):
                if positions[i + 1][1] - positions[i][1] < 10:
                    temp_list.append(positions[i + 1])
                else:
                    break
            temp_list.sort(key=lambda p: p[0])
            positions[index:(index + len(temp_list))] = temp_list
            index = index + len(temp_list) - 1
        else:
            index += 1

    print(positions)
    
    flag = 0
    for position in positions:
        x = position[0]
        y = position[1]
        w = position[2]
        h = position[3]
        sub_image = resize_copy[y:y+h, x+5:x+w-5]
        flag += 1
        output_filename = f'output\sub_image_{flag}.png'
                    
        cv2.imwrite(output_filename, sub_image)  
