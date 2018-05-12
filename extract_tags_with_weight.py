# /usr/local/boin/python3
# -*- coding: utf-8 -*-

'''
  使用jieba模块对职位信息进行分词处理，并提取其中词频权重较高的词
  存储在csv文件中
'''
import sys
import os
import csv
import codecs

import jieba
from jieba.analyse import extract_tags, set_stop_words
import jieba.posseg as pesg

# seg_list = jieba.cut('统计某招聘网站岗位职责要求关键字')
# print('all_key' + ','.join(seg_list))

class Data_Handle():
  # 获取csv文件所在当前路径，第二个参数可以自定义
  FILE_UTL = os.path.join(os.path.dirname(__file__), './job/job/spiders/__pycache__/移动开发.csv')
  
  # keyword转化
  TRANSFER_CONFIG = {
      # '英文': 'English',
      # '英语': 'English',
      # 'english': 'English'
  }

  # 二次数据加工，删除非预期数据
  DELETE_CONFIG = []
  
  def __init__(self):
    self.fileload(filename=self.FILE_UTL)
    self.participle()
    self.refine_keywords()
    self.savefile()
    
  # 获取绝对路径下的csv文件，并进行读取职位详情该列的每行数据
  def fileload(self, filename):
    csvfile = open(filename, encoding="utf-8")
    data = csv.reader(csvfile)
    dataset = []
    for line in data:
      dataset.append(line[7])
    csvfile.close()
    self.jb_details=dataset

  # jieba对职位详情数组中每条数据进行分词
  def participle(self):

    data_all_string = ''
    for index, item in enumerate(self.jb_details):
      data_all_string += item

    self.keywords = extract_tags(sentence=data_all_string, topK=100, withWeight=True, allowPOS=('eng', 'nz'))
  
  def refine_keywords(self):
    keywords_dict = {}

    # 进行keyword大小写统一化
    for keyword,weight in self.keywords:
      keyword_lower = keyword.lower()
      if keyword_lower in keywords_dict:
        keywords_dict[keyword_lower] += weight
        continue

      keywords_dict[keyword_lower] = weight

    # 进行keyword转化
    for keyword in keywords_dict:
      if keyword in self.TRANSFER_CONFIG:
        keywords_dict[self.TRANSFER_CONFIG[keyword]] += keywords_dict[keyword]
    
    # 删除缩写keyword
    for del_key in self.TRANSFER_CONFIG:
      del keywords_dict[del_key]

    for del_key in self.DELETE_CONFIG:
      del keywords_dict[del_key]

    self.keyword_list = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)
  

  def savefile(self):
      csvfile = codecs.open('list.csv', 'w', encoding='utf_8_sig')
      self.writer = csv.writer(csvfile)
      self.writer.writerow(['职位名称', '关键字', '频次'])

      for item in self.keyword_list:
        item = list(item)
        item.insert(0, '移动开发')
        self.writer.writerow(item)

a = Data_Handle()