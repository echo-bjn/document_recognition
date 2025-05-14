import cv2
from yolov5.predict import predict
from determine import determine
from recognition import extract_text

# 将图像转换为灰度图像
def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 调整图像大小，调整后的图像尺寸默认为(1084, 669)
def resize_image(image, size=(1084, 669)):
    return cv2.resize(image, size)

# 预处理
def preprocess_image(img, points, size=(1084, 669)):

    top = points[0]
    bottom = points[1]
    left = points[2]
    right = points[3]

    img = img[top:bottom, left:right]

    transformed_image = resize_image(img, size) # 固定shape
   
    gray_image = convert_to_gray(transformed_image)  # 转换为灰度图像

    return gray_image, transformed_image


# if __name__ == "__main__":
#     img = cv2.imread("hello.jpg")
#     top, bottom, left, right = predict("hello.jpg")
#     points = [top, bottom, left, right]
#     g, t = preprocess_image(img, points)
#     determine(g)
#     text = extract_text()
#     print(text)