# -*- coding: utf-8 -*-
# 开发团队   ：CSSC_linyuanlab
# 开发人员   ：yyc
# 开发时间   ：2019/7/28  13:43 
# 文件名称   ：main.py
# 开发工具   ：PyCharm
import time
from scrapy.cmdline import execute
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "wanfang"])