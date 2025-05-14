import cv2
import cv2.img_hash
import numpy as np
import os
from slice import *

# def show_img(img):
#     cv2.imshow('img',img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def cal_num(line):
    num=0
    for i in range(len(line)-1):
        #print(line)
        if line[i]<128:
            num+=0
        else:
            num+=1
    return num

def image_divide(img):
    #show_img(img)
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # show_img(img_gray)
    img_result=img_gray.copy()
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    img_gray=cv2.GaussianBlur(img_gray,(3,3),0,0)
    img_gray=cv2.morphologyEx(img_gray,cv2.MORPH_BLACKHAT,kernel)
    img_gray=cv2.medianBlur(img_gray,11)
    height,width=img_gray.shape
    print(type(img_gray))
    
    img_sobel1=cv2.Sobel(img_gray,cv2.CV_64F,dx=1,dy=0,ksize=11)
    img_sobel1=cv2.Sobel(img_gray,cv2.CV_64F,dx=1,dy=0,ksize=11)
    sobelx = cv2.convertScaleAbs(img_sobel1)
    sobelx=cv2.morphologyEx(sobelx,cv2.MORPH_CLOSE,kernel,iterations=4)
    sobelx=cv2.morphologyEx(sobelx,cv2.MORPH_OPEN,kernel,iterations=2)
    retval,sobelx=cv2.threshold(sobelx,128,maxval=255,type=cv2.THRESH_BINARY)
    # show_img(sobelx)
    
    is_script=[]
    for w in range(width):
        cal=cal_num(sobelx[:,w])
        is_script.append(cal)

    print(is_script)
    
    save_path='results/'
    remove_list=os.listdir(save_path)
    if remove_list!=[]:
        for item in remove_list:
            file=save_path+item
            os.remove(file)
    
    index_list=np.where(is_script==np.min(is_script,axis=0))
    index_list=index_list[0].tolist()
    
    left=int(width*0.4)
    right=int(width*0.6)
    index_list=[i if (i<right and i>left) else None for i in index_list]
    index_list=set(index_list)
    index_list=list(index_list)
    if None in index_list:
        index_list.remove(None)
    divide=int((index_list[0]+index_list[-1])/2)
    print(index_list)
    
    cv2.imwrite(save_path+'left.jpg',img[:,0:divide])
    cv2.imwrite(save_path+'right.jpg',img[:,divide:])
    return divide
            
# if __name__ == '__main__':
#     #img=slice_image("train/24.jpg")
#     _,img,img2=slice_image("train/75.jpg")
#     #show_img(img2)
#     print(img.shape)
#     divide=image_divide(img=img)
#     cv2.imwrite('left_1.jpg',img2[:,:divide])
#     cv2.imwrite('right_1.jpg',img2[:,divide:])