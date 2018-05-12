# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.loader import ItemLoader
from scrapy.http import Request


from job.items import JobItem


class LagouSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['https://jobs.51job.com', 'https://search.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,大数据,2,1.html']

    def parse(self, response):
        url_list = response.css('#resultList .el .t1 span a::attr(href)').extract()
        for url in url_list:
            yield Request(url=url, callback=self.parse_detail, dont_filter=True)

        next_url = response.css('.dw_page li:last-child a::attr(href)').extract_first()

        if next_url:
            yield Request(url=str(next_url), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        jobs = ItemLoader(JobItem(), response=response)
        url_md5 = hashlib.md5()
        url_md5.update(response.url.encode(encoding='utf-8'))
        jobs.add_css('job_name', '.tHjob .cn h1::attr(title)')
        jobs.add_css('company_name', '.tHjob .cname a::attr(title)')
        jobs.add_css('experience', '.tBorderTop_box .jtag .t1 span:nth-child(1)::text')
        jobs.add_css('Education', '.tBorderTop_box .jtag .t1 span:nth-child(2)::text')
        jobs.add_css('workplace', '.tHeader .lname::text')
        jobs.add_css('salary_min', '.tHjob .cn strong::text')
        jobs.add_css('salary_max', '.tHjob .cn strong::text')
        jobs.add_value('url', response.url)
        jobs.add_value('object_url', url_md5.hexdigest())
        jobs.add_css('jb_description', '.tCompany_main div[class=tBorderTop_box] .job_msg')
        jobs.add_css('company_type',  '.tHjob .in .cn .ltype::text')
        jobs.add_css('company_people_min',  '.tHjob .in .cn .ltype::text')
        jobs.add_css('company_people_max', '.tHjob .in .cn .ltype::text')
        jobs.add_css('company_work',  '.tHjob .in .cn .ltype::text')
        return jobs.load_item()
