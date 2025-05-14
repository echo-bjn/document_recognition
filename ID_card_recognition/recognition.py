from cnocr import CnOcr
import time
import re
import os

def extract_text():
    def get_image_files_in_folder(folder_path):
        image_files = []
        for file in os.listdir(folder_path):
            if file.endswith('.JPG') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp') or file.endswith('.jpg') or file.endswith('.PNG') or file.endswith('.JPEG') or file.endswith('.BMP'):
                image_files.append(os.path.join(folder_path, file))
    
        # 按照文件名中的数字部分进行排序
        image_files.sort(key=lambda f: int(re.search(r'(\d+)', os.path.basename(f)).group()))
        return image_files
    start_time = time.time() 
    folder_path = 'output'            
    image_files = get_image_files_in_folder(folder_path)
    ocr = CnOcr(name='densenet-s')
    ocr_ = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
    length = len(image_files)
    address_flag = 0
    address_result = ''
    count = -1
    result = []
    label_minzu = [
    "汉", "蒙古", "回", "藏", "维吾尔", "苗", "彝", "壮", "布依",
    "朝鲜", "满", "瑶", "白", "土家", "哈尼", "哈萨克", "傣", "黎",
    "傈僳", "佤", "畲", "高山", "拉祜", "水", "东乡", "纳西", "景颇",
    "柯尔克孜", "土", "达斡尔", "仫佬", "羌", "布朗", "撒拉", "毛南",
    "仡佬", "锡伯", "阿昌", "普米", "塔吉克", "怒", "乌孜别克", "俄罗斯",
    "鄂温克", "德昂", "保安", "裕固", "京", "塔塔尔", "独龙", "鄂伦春",
    "赫哲", "门巴", "珞巴", "基诺"
]
    for file_path in image_files:
        count = count + 1
        if count == len(image_files) - 1:
            ocr_data = ocr_.ocr(file_path)
            ocr_result = ocr_data[0]['text']
        else:
            ocr_data = ocr.ocr_for_single_line(file_path)
            ocr_result = ''.join([ocr_data['text']]).replace(' ', '')
        pattern = re.compile(r'[^\u4e00-\u9fff-\d]') # 使用re.sub替换掉这些字符为空字符串
        ocr_result = re.sub(pattern, '', ocr_result)
        label = ['姓名', '性别', '民族', '出生', '住址','公民身份号码']
        sex = ['男','女']
        #按照顺序判断姓名，性别，民族，出生
        if count < 3:
            ocr_result = re.sub(r'[^\u4e00-\u9fa5\d]', '', ocr_result)
            if count == 0:
                result.append('{}：{}'.format(label[count], ocr_result))
                continue
            if count == 1:
                for s in sex:
                    if s in ocr_result:
                        result.append('{}：{}'.format(label[count], s))
                        break
                continue
            if count == 2:
                for s in label_minzu:
                    if s in ocr_result:
                        result.append('{}：{}'.format(label[count], s))
                        break
                continue
        if count == 3:
            ocr_result = re.sub(r'[^0-9年月日]+', '', ocr_result)
            result.append('{}：{}'.format(label[count], ocr_result))
            continue
        #先判断是不是住址区域，对住址数据进行操作
        if count == 4 :
            if len(image_files) == 5:
                result.append('{}：{}'.format(label[count], ocr_result))
                continue
            else:
                address_result = ocr_result
                continue
        if count < len(image_files) - 1:
            address_result = address_result + ocr_result
        if count == len(image_files) - 2:
            result.append('{}：{}'.format(label[-2], address_result))
            continue
        if len(ocr_result) == 17:
             ocr_result = ocr_result + 'X'
        result.append('{}：{}'.format(label[-1], ocr_result))
    return result