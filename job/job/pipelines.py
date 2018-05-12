# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import MySQLdb

# from scrapy.utils.project import get_project_settings

# 连接mysql数据库,将数据存储在mysql中
# class JobPipeline(object):
#
#     # setting mysql connection
#     db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="job", port=3306, charset="utf8")
#     cursor = db.cursor()
#
#     def process_item(self, item, spider):
#         # 该表名称
#         add_item = ('INSERT INTO jobs(job_name, company_name, salary_min, salary_max,'
#                     ' url, object_url, jb_description, company_type, company_people_min, company_people_max,'
#                     ' company_work)'
#                     'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
#
#         self.cursor.execute(add_item, (item['job_name'], item['company_name'], item['salary_min'],
#                                        item['salary_max'], item['url'], item['object_url'], item['jb_description'],
#                                        item['company_type'], item['company_people_min'], item['company_people_max'],
#                                        item['company_work']))
#         self.db.commit()
#         return item

# 将数据保存在csv文件中
import codecs
import csv


class CSVPipeline(object):

  def __init__(self):
    file = codecs.open('51job.csv', 'w', encoding='utf_8_sig')
    self.writer = csv.writer(file)
    self.writer.writerow(['职位名称', '公司名称', '经验要求', '学历','工作地点', '最低薪水', '最高薪水', '职位描述', '公司类型', '最低员工人数',
                          '最高员工人数', '主营业务'])
    pass

  def process_item(self, item, spider):
    """
    :param item:
    :param spider:
    :return:
    """
    self.writer.writerow([item['job_name'], item['company_name'], item['experience'], item['Education'],
                          item['workplace'], item['salary_min'],item['salary_max'],item['jb_description'],
                          item['company_type'], item['company_people_min'],item['company_people_max'],
                          item['company_work']])
    return item

