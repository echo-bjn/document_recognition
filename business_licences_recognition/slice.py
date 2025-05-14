import cv2
import numpy as np

# 模板匹配
def find_template(image, flag_path, threshold=0.5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(flag_path, 0)
    h, w = template.shape
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED) # 在图像中进行模板匹配
    loc = np.where(res >= threshold) # 找到匹配度最高的位置
    # 返回匹配区域的左上角和右下角坐标
    if len(loc[0]) > 0 and len(loc[1]) > 0:
        x1, y1 = loc[1][0], loc[0][0]
        x2, y2 = x1 + w, y1 + h
        return [x1, y1, x2, y2]
    else:
        return False

# 切分竖版图像(竖版图像1400x1000)
def slice_vertical_image(img):
    img_resize = cv2.resize(img, (1000, 1400))
    flag_v_path = "flag/flag_v.jpg"
    result = find_template(img_resize, flag_v_path)
    if result == False:
        flag_v2_path = "flag/flag_v2.jpg"
        result = find_template(img_resize, flag_v2_path)
        if result == False:
            print("please input the correct image!")
    if result[0]>result[1]:
        temp = result[0]
        result[0] = result[1]
        result[1] = temp
    if result[2]>result[3]:
        temp = result[2]
        result[2] = result[3]
        result[3] = temp
    print(result)
    left = result[1]-280
    right = result[3]+320
    up = result[2]+190
    up2 = result[2]
    bottom = up+600
    img_slice = img_resize[up:bottom, left:right]
    img_slice2 = img_resize[up2:bottom, left:right]

    return img_slice, img_slice2

# 切分横版图像(横板图像800x1150)
def slice_horizontal_image(img):
    img_resize = cv2.resize(img, (1150, 800))
    flag_h_path = "flag/flag_h.jpg"
    result = find_template(img_resize, flag_h_path)
    print(result)
    if result == False:
        print("please input the correct image!")
    if result[0]>result[1]:
        temp = result[0]
        result[0] = result[1]
        result[1] = temp
    if result[2]>result[3]:
        temp = result[2]
        result[2] = result[3]
        result[3] = temp
    left = result[1]-420
    right = result[3]+420
    up = result[2]+130
    bottom = up+400
    up2 = result[2]
    img_slice = img_resize[up:bottom, left:right]
    img_slice_2 = img_resize[up2:bottom, left:right]

    return img_slice, img_slice_2

# 切分图像
def slice_image(img_path):
    img = cv2.imread(img_path)
    x = img.shape[0]
    y = img.shape[1]
    if x > y:
        print("识别竖版营业执照")
        s = "vertical"
        img_slice, img_slice_2 = slice_vertical_image(img)
    else:
        print("识别横版营业执照")
        s = "horizontal"
        img_slice, img_slice_2 = slice_horizontal_image(img)
    
    return s, img_slice, img_slice_2

if __name__ == "__main__":
    img_path = "business_licences/6.jpg"
    # img_path = "yyzz/kdyc/27.jpg"
    # out_path = "test/test.jpg"
    # img = cv2.imread(img_path)
    # print(img.shape)
    # img_resize = cv2.resize(img, (1150, 800))
    # cv2.imwrite(out_path, img_resize)
    # result = slice_image(img_path)
    # print(result)

    # img = cv2.imread(img_path)
    # img = cv2.resize(img, (1000, 1400))
    # img[result[0]-5:result[0]+5, result[1]-5:result[1]+5] = (0, 0, 255)
    # img[result[2]-5:result[2]+5, result[3]-5:result[3]+5] = (0, 0, 255)
    _, img, img2 = slice_image(img_path)
    cv2.imwrite("test/test.jpg", img)
    cv2.imwrite("test/test2.jpg", img2)
    # cv2.imshow('Modified Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()