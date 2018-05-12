# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader.processors import TakeFirst, Compose


# 获取薪资最小值
def get_min(value):
    matrix = 1
    if '千' in value[0]:
        matrix=1000
    elif '万' in value[0]:
        matrix=10000

    if isinstance(value, str):
        value = value
    elif isinstance(value, list):
        value = value[0]
    value = re.findall('\d+\.{0,1}\d*', value)
    value = list(map(lambda x: float(x), value))
    return str(int(min(value) * matrix))


# 获取薪资最大值
def get_max(value):
    matrix = 1
    if '千' in value[0]:
        matrix = 1000
    elif '万' in value[0]:
        matrix = 10000

    if isinstance(value, str):
        value = value
    elif isinstance(value, list):
        value = value[0]
    value = re.findall('\d+\.{0,1}\d*', value)
    value = list(map(lambda x: float(x), value))
    return str(int(max(value) * matrix))


def filter_educate(value):
    if '人' in value[0]:
        return ''
    return value


def filter_company_type(value):
    a = re.findall('[^\s\|]+', value[0])
    return a[0]


def filter_company_scale(value):
    a = re.findall('[^\s\|]+', value[0])
    return a[1]


def filter_company_work(value):
    a = re.findall('[^\s\|]+', value[0])
    return a[2]


def filter_job_msg(value):
    value = re.sub('\s*\<\/{0,1}.*?\>\s*', '', value[0])
    return re.sub('职能类别.*', '', value)



class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    company_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    experience = scrapy.Field(
        output_processor=TakeFirst()
    )
    Education = scrapy.Field(
        input_processor=filter_educate,
        output_processor=TakeFirst()
    )
    workplace = scrapy.Field(
        output_processor=TakeFirst()
    )
    salary_min = scrapy.Field(
        input_processor=get_min,
        output_processor=TakeFirst()
    )
    salary_max = scrapy.Field(
        input_processor=get_max,
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    object_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    jb_description = scrapy.Field(
        input_processor=filter_job_msg,
        output_processor=TakeFirst()
    )
    company_type = scrapy.Field(
        input_processor=filter_company_type,
        output_processor=TakeFirst()
    )

    company_people_min = scrapy.Field(
        input_processor=Compose(filter_company_scale, get_min),
        output_processor=TakeFirst()
    )
    company_people_max = scrapy.Field(
        input_processor=Compose(filter_company_scale, get_max),
        output_processor=TakeFirst()
    )

    company_work = scrapy.Field(
        input_processor=filter_company_work,
        output_processor=TakeFirst()
    )
