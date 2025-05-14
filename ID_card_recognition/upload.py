# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta
from preprocess import preprocess_image
from yolov5.predict import predict
from determine import determine
from recognition import extract_text
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp']) # 设置允许的文件格式
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1) # 设置静态文件缓存过期时间
 
@app.route('/', methods=['POST', 'GET']) # 添加路由
def upload():
   if request.method == 'POST':
       # 删除/static/images里面的所有图像
      target_path = 'static\images'
      for filename in os.listdir(target_path):
         file_path = os.path.join(target_path, filename)
         os.remove(file_path)

      target_path2 = 'output'
      for filename in os.listdir(target_path2):
         file_path = os.path.join(target_path2, filename)
         os.remove(file_path)

      f = request.files['file']

      if not (f and allowed_file(f.filename)):
         return jsonify({"error": 1001, "msg": "请检查上传的图片类型, 仅限于png、PNG、jpg、JPG、bmp"})
 
      user_input = request.form.get("name")
 
      basepath = os.path.dirname(__file__) # 当前文件所在源路径
 
      upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename)) # 另存路径:static/image/{filename}
      f.save(upload_path)

      top, bottom, left, right = predict(upload_path)
      points = [top, bottom, left, right]

      img = cv2.imread(upload_path) # 处理的图像
      gray_img, img = preprocess_image(img, points) # preprocess

      size = img.shape
      img = cv2.resize(img, (int(size[1]/2), int(size[0]/2)), interpolation=cv2.INTER_AREA) 
      cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

      determine(gray_img)
      text = extract_text()

      # 上传文字
      products = text
      return render_template('upload_ok.html', userinput=user_input, val1=time.time(), products = products)
 
   return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8987, debug=True)