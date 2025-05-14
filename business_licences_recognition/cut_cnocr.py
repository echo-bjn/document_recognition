import ast
import re

def extract_text(parsed_data):
    str_all = ''
    for n in range(len(parsed_data)):
        str_all = str_all + parsed_data[n][1][0]
    label = ["注册号","副本编号","副本号","统一社会信用代码","证照编号","编号",
             "名称","类型","主体类型","住所","法定代表人","注册资本","成立日期","营业期限",
             "经营范围","经营者","经营场所","组成形式","注册日期","营业场所","负责人","登记机关"]
    result = []
    labels = []
    str_all = str_all.replace(' ','')
    positions = []
    positions_ = []
    for text in label:
        if text in str_all:
            text_index = str_all.find(text)
            labels.append(text)
            positions_.append(text_index)
    zipped_pairs = list(zip(positions_,labels))
    zipped_pairs.sort()
    positions_sorted_, labels_sorted = zip(*zipped_pairs)
    positions_sorted_, labels_sorted = list(positions_sorted_),list(labels_sorted)
    
    for text in labels_sorted:
        text_index = str_all.find(text)
        str_all = str_all.replace(text, "", 1)
        positions.append(text_index)

    positions_sorted = positions
    
    def has_no_chinese(s):
        # 使用正则表达式检查字符串中是否有汉字
        # \u4e00-\u9fff 表示大部分常用汉字的Unicode编码范围
        pattern = re.compile(r'[\u4e00-\u9fff]')
        # 搜索字符串，如果找到匹配的汉字则返回True，否则返回False
        return not pattern.search(s)
        
    def find_first_chinese_index(s):
        # 正则表达式匹配汉字的Unicode编码范围
        pattern = re.compile(r'[\u4e00-\u9fff]')
        
        # 从字符串末尾开始向前搜索
        for index in range(len(s) - 1, -1, -1):
            # 如果当前字符是汉字
            if pattern.match(s[index]):
                return index + len(s[index])  # 返回汉字的索引
        return -1  # 如果没有找到汉字，返回-1
    
    def find_outside_parentheses_numbers(s):
        # 正则表达式匹配不在括号内的数字
        # 这个表达式使用了负向先行断言(?<!)和负向回顾后发断言(?!)来确保数字不在括号内
        pattern = r'(?<!\()[0-9]+(?!\))'
        matches = re.findall(pattern, s)
        
        # 将找到的数字转换为整数列表
        numbers = [int(num) for num in matches]
        return numbers
    def find_first_duplicate_index(lst):
        seen = set()
        for index, value in enumerate(lst):
            if value in seen:
                return index  # 返回第一个重复元素的索引
            seen.add(value)
        return -1  # 如果没有找到重复元素，返回-1
    

    if not (find_first_duplicate_index(positions_sorted) == -1):
        issame = find_first_duplicate_index(positions_sorted) - 1
        if labels_sorted[issame+1] == "统一社会信用代码":
            labels_sorted[issame], labels_sorted[issame+1] = labels_sorted[issame+1],labels_sorted[issame]
    for i in range(len(labels)):
        if labels_sorted[i] == "统一社会信用代码":
            if not has_no_chinese(str_all[positions_sorted[i]:positions_sorted[i+1]]):
                if has_no_chinese(str_all[positions_sorted[i] - 8 :positions_sorted[i]]):
                    index = find_outside_parentheses_numbers(str_all[:positions_sorted[i]])
                    for t in index :
                        if len(str(t)) > 6:
                            print(1)
                            result_str = t
                            break
                '''
                if index != -1:
                    result_str = str_all[index :positions_sorted[i]]
                else:
                    print("图片有误")'''
            else:
                result_str = str_all[positions_sorted[i]:positions_sorted[i+1]]
        else:
            if labels_sorted[i] == "登记机关":
                break
            if i < len(labels) - 1:
                result_str = str_all[positions_sorted[i]:positions_sorted[i+1]]
            else:
                result_str = str_all[positions_sorted[i]:]
            if "区市场" in result_str and (i == len(labels) - 1 or i == len(labels) - 2):
                result_str = result_str.replace("区市场", "", 1)
        result.append('{}：{}'.format(labels_sorted[i], result_str))
    
    return result