import os
import cv2

path = 'JPGImages/'
output_path='JPGImages_re/'
file_list=os.listdir(path)
print(file_list)
n=0
for item in file_list:
    file_name=path+item
    output_name=output_path+str("{:03d}".format(n))+'.jpg'
    
    with open(file_name,'rb') as fp1:
        b1=fp1.read()
        
    with open(output_name,'wb') as fp2:
        fp2.write(b1)
    
    n+=1