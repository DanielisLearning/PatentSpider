# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from urllib import parse
from PatentSpider.items import wanfangPatentItem, PatentItemLoader
from PatentSpider.utils.common import get_md5


# 大类+小类：

small_class_list = ['A01', 'A21', 'A22', 'A23', 'A24', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47', 'A61', 'A62',
'A63', 'A99',
'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B21', 'B22', 'B23', 'B24', 'B25',
'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'B41', 'B42', 'B43', 'B44', 'B60', 'B61', 'B62',
'B63', 'B64', 'B65', 'B66', 'B67', 'B68', 'B81', 'B82', 'B99',
'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14',
'C21', 'C22', 'C23', 'C25', 'C30', 'C40', 'C99',
'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D21', 'D99',
'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E21', 'E99',
'F01', 'F02', 'F03', 'F04', 'F15', 'F16', 'F17', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27',
'F28', 'F41', 'F42', 'F99',
'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G21', 'G99',
'H01', 'H02', 'H03', 'H04', 'H05', 'H99']

# 国家列表（13个）：
ctry_list = ['CN', 'JP', 'US', 'EP', 'WO', 'DE', 'RU', 'KR', 'FR', 'AU', 'CA', 'GB', 'CH']
ctry_Label_list = ['中国', '日本', '美国', '欧洲专利局', '世界知识产权组织', '德国', '俄罗斯', '韩国', '法国', '澳大利亚', '加拿大', '英国', '瑞士']

page_num = 1
start_page_num = 1
test_code = 'D02'
# third_domain_url_list = ['http://www.wanfangdata.com.cn/search/searchList.do?searchType=patent&searchWord=分类号:{0}' \
#                          '&facetField=$pub_org_code:{1}' \
#                          '&showType=detail&pageSize=50&page={2}' \
#                          '&facetName={3}' \
#                          ':$pub_org_code&isHit=&isHitUnit=&navSearchType=patent&firstAuthor=false&rangeParame='
#                          .format(test_code, ctry_list[ctry_num], start_page_num, ctry_Label_list[ctry_num]) for ctry_num in range(13)]

third_domain_url_list = ['http://www.wanfangdata.com.cn/search/searchList.do?searchType=patent&searchWord=分类号:{0}' \
                         '&facetField=$pub_org_code:{1}' \
                         '&showType=detail&pageSize=50&page={2}' \
                         '&facetName={3}' \
                         ':$pub_org_code&isHit=&isHitUnit=&navSearchType=patent&firstAuthor=false&rangeParame='
                         .format(test_code, ctry_list[ctry_num], start_page_num, ctry_Label_list[ctry_num]) for ctry_num in range(1)]

class WanfangSpider(scrapy.Spider):
    name = 'wanfang'
    allowed_domains = ['c.wanfangdata.com.cn/patent', 'www.wanfangdata.com.cn']
    start_urls = third_domain_url_list

    def parse(self, response):
        global page_num

        """
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        """
        # 解析列表页中的所有专利url并交给scrapy下载后并进行解析

        patent_number = response.css(".author span:nth-child(3)::text").extract()
        post_urls = ['http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id='+item for item in patent_number]

        for post_url in post_urls:
            yield scrapy.http.Request(url=post_url, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        total_page = int(response.css('.searchPageWrap_all::text').extract_first(""))
        curr_page = int(response.css('.searchPageWrap_cur::text').extract_first(""))
        if curr_page < total_page:
            page_num += 1
            next_url = response.url.replace('&page={0}'.format(page_num - 1), '&page={0}'.format(page_num))
            yield Request(url=next_url, callback=self.parse)
        else:
            page_num = 1


    def parse_detail(self, response):
        global test_code

        patent_item = wanfangPatentItem()

        item_loader = PatentItemLoader(item=wanfangPatentItem(), response=response)

        info_list = response.css(".info_right.author::text").extract()
        info_list = [item.strip() for item in info_list]
        first_info_label = response.css(".info_left::text").extract_first('')

        # 中国专利以专利分类作为第一项
        if first_info_label == '申请/专利号：':
            pos = 0
        else:
            pos = 1

        # 专利名称
        item_loader.add_css("patent_name", '.title::text')
        # IPC编号
        item_loader.add_value("IPC", test_code)
        # 专利号
        item_loader.add_value("patent_number", info_list[pos])
        # 申请日期
        item_loader.add_value("filling_date", info_list[pos+1])
        # 公告号
        item_loader.add_value("announcement_number", info_list[pos+2])
        # 公告日
        item_loader.add_value("announcement_date", info_list[pos+3])
        # 主分类号
        item_loader.add_value("main_classification", info_list[pos+4])
        # 分类号
        item_loader.add_value("classification", info_list[pos+5])
        # 专利权人
        item_loader.add_css('patentee', ".info_right.info_right_newline a::text")
        # 发明人
        item_loader.add_css('designer', ".info_right .info_right_name::text")
        # 详情页的URL
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))


        patent_item = item_loader.load_item()
        # time.sleep(0.1)

        yield patent_item