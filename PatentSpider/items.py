# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join



# 针对不愿extract_first()，实行覆盖
def return_value(value):
    return value


def date_convert(value):

    try:
        # value = value.split(' ')[0]
        try:
            create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            # create_date = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            create_date = datetime.datetime.strptime(value, "%Y/%m/%d %H").date()
            # create_date = datetime.datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def remove_writer_tags(value):
    #去掉writer中“作者：”
    if "作者: " in value:
        return value.split(':')[1].strip()
    else:
        return value


def remove_whitespace_line_breaks_tabs(value):
    #去除空白符、制表符、换行符，并整理成列表
    value = value.replace('\r', '').replace('\n', '').replace('\t', '').replace(u'\xa0',u' ').split(' ')
    return value


def remove_whitespace_line_breaks_tabs_not_split(value):
    #去除空白符、制表符、换行符，并整理成列表
    value = value.replace('\r', '').replace('\n', '').replace('\t', '').replace(u'\xa0',u' ')
    return value

class PatentItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class PatentspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class wanfangPatentItem(scrapy.Item):
    patent_name = scrapy.Field(
        input_processor=MapCompose(remove_whitespace_line_breaks_tabs_not_split),
    )
    IPC = scrapy.Field()
    patent_number = scrapy.Field()
    announcement_number = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    classification = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    designer = scrapy.Field(
        output_processor=MapCompose(return_value)
    )

    filling_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    announcement_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )


    main_classification = scrapy.Field(
        input_processor=MapCompose(remove_whitespace_line_breaks_tabs),
    )
    patentee = scrapy.Field(
        input_processor=MapCompose(remove_whitespace_line_breaks_tabs),
    )


