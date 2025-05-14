import json
import base64

now=0

for i in range(now+1,now+300):
    file_name='JPGImages/'+str(now)+'.json'
    with open(file_name,'r',encoding='utf8') as file:
        data=json.load(file)
    
    file_path='JPGImages/'+str(i)+'.jpg'
    data["imagePath"]=file_path
    #data["imageData"]=""
    print(data["imagePath"])
    
    with open(file_path,'rb') as image_file:
        image_data=image_file.read()
    base64_image=base64.b64encode(image_data).decode('utf-8')
    #print(base64_image)
    data["imageData"]=base64_image
    
    file_new='JPGImages/'+str(i)+'.json'
    with open(file_new,'w',encoding='utf8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)