# -*- coding:utf-8 -*-
############################################################################
# 程序：通用程序处理
# 功能：抽取常用功能封装为函数
# 创建时间：2016/11/26
# 更新时间：2016/11/26
# 使用库：requests、BeautifulSoup4、MySQLdb
# 作者：yuzhucu
#############################################################################
import requests
from bs4 import BeautifulSoup
import time

def getCurrentTime():
    return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

def getURL(url,tries_num=5,sleep_time=1,time_out=10):
    headers = {'content-type': 'application/json',  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    sleep_time_p=sleep_time
    time_out_p=time_out
    tries_num_p=tries_num
    try:
          res=requests.get(url,headers=headers,timeout=time_out)
          res.raise_for_status()    # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
          sleep_time_p=sleep_time_p+1
          time_out_p=time_out_p+5
          tries_num_p=tries_num_p-1
          print getCurrentTime(),url, 'URL Connection Error: 第',tries_num-tries_num_p,u'次 Retry Connection' , e
          #print getCurrentTime(),url, 'URL Connection Error: 第',10-tries_num+1,u'次 Retry Connection' , e.message
          #设置重试次数，最大timeout 时间和 最长休眠时间
          if tries_num_p>0 and sleep_time_p<300 and time_out_p<600:
            time.sleep(sleep_time_p)
            res=getURL(url,tries_num_p,sleep_time_p,time_out_p)
            return res
            print getCurrentTime(),url,'URL Connection Success: 共尝试',tries_num-tries_num_p,u'次',',sleep_time:',sleep_time_p,',time_out:',time_out_p
            #print getCurrentTime(),url, 'URL Connection Sucess:', e
    return  res

if __name__=="__main__":
   print getCurrentTime(),'Main Scrapy Starting'
   url='http://sh.lianjia.com/ershoufang'
   print getURL(url).text