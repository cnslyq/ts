# -*- coding:utf-8 -*-

"""
新闻事件数据接口 
Created on 2015/02/07
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""

from tushare.stock import cons as ct
from tushare.stock import news_vars as nv
import pandas as pd
from datetime import datetime
import lxml.html
from lxml import etree
import re
import json
import time
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request



def get_latest_news(top=None, show_content=False, retry_count=10, pause=0.01):
    """
        获取即时财经新闻
    
    Parameters
    --------
        top:数值，显示最新消息的条数，默认为80条
        show_content:是否显示新闻内容，默认False
    
    Return
    --------
        DataFrame
            classify :新闻类别
            title :新闻标题
            time :发布时间
            url :新闻链接
            content:新闻内容（在show_content为True的情况下出现）
    """
    for _ in range(retry_count):
        time.sleep(pause)
        top = ct.PAGE_NUM[2] if top is None else top
        try:
            request = Request(nv.LATEST_URL % (ct.P_TYPE['http'], ct.DOMAINS['sina'],
                                                       ct.PAGES['lnews'], top,
                                                       _random()))
            data_str = urlopen(request, timeout=10).read()
            data_str = data_str.decode('GBK')
            data_str = data_str.split('=')[1][:-1]
            data_str = eval(data_str, type('Dummy', (dict,), 
                                           dict(__getitem__ = lambda s, n:n))())
            data_str = json.dumps(data_str)
            data_str = json.loads(data_str)
            data_str = data_str['list']
            data = []
            for r in data_str:
                rt = datetime.fromtimestamp(r['time'])
                rtstr = datetime.strftime(rt, "%m-%d %H:%M")
                arow = [r['channel']['title'], r['title'], rtstr, r['url']]
                if show_content:
                    arow.append(latest_content(r['url']))
                data.append(arow)
            df = pd.DataFrame(data, columns=nv.LATEST_COLS_C if show_content else nv.LATEST_COLS)
            return df
        except Exception as er:
            print('get_latest_news error : ' + str(er))
    raise IOError(ct.NETWORK_URL_ERROR_MSG)

def latest_content(url, retry_count=10, pause=0.01):
    '''
        获取即时财经新闻内容
    Parameter
    --------
        url:新闻链接
    
    Return
    --------
        string:返回新闻的文字内容
    '''
    from pandas.io.common import urlopen
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            # html = lxml.html.parse(url)
            with urlopen(url) as resp:
                lines = resp.read().decode('utf8')
            html = lxml.html.document_fromstring(lines)
            res = html.xpath('//div[@id=\"artibody\"]/p')
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr).replace('&#12288;', '').replace('&#160;', '').replace('&#183;', '').replace('&#252;', '')#.replace('\n\n', '\n').
            html_content = lxml.html.fromstring(sarr)
            content = html_content.text_content()
            return content
        except Exception as er:
            # print url
            # print(str(er))
            pass
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def get_notices(code=None, date=None, show_content=False, retry_count=10, pause=0.01):
    '''
    个股信息地雷
    Parameters
    --------
        code:股票代码
        date:信息公布日期
    
    Return
    --------
        DataFrame，属性列表：
        title:信息标题
        type:信息类型
        date:公告日期
        url:信息内容URL
    '''
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            if code is None:
                return None
            symbol = 'sh' + code if code[:1] == '6' else 'sz' + code
            url = nv.NOTICE_INFO_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                      ct.PAGES['ntinfo'], symbol)
            url = url if date is None else '%s&gg_date=%s'%(url, date)
            html = lxml.html.parse(url)
            res = html.xpath('//table[@class=\"body_table\"]/tbody/tr')
            data = []
            for td in res:
                if len(td.xpath('th/a/text()')) != 0:
                    # title = td.xpath('th/a/text()')[0]
                    # type = td.xpath('td[1]/text()')[0]
                    title = td.xpath('th/a/text()')[0].encode('utf8')
                    type = td.xpath('td[1]/text()')[0].encode('utf8')
                    date = td.xpath('td[2]/text()')[0]
                    url = '%s%s%s'%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], td.xpath('th/a/@href')[0])
                    content = ''
                    if show_content:
                        content = notice_content(url)
                        if content is not None:
                            content = content.encode('utf8')
                    data.append([title, type, date, url, content])
            if len(data) == 0:
                return None
            df = pd.DataFrame(data, columns=nv.NOTICE_INFO_CLS)
            return df
        except Exception as er:
            print er
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def notice_content(url):
    '''
        获取信息地雷内容
    Parameter
    --------
        url:内容链接
    
    Return
    --------
        string:信息内容
    '''
    try:
        html = lxml.html.parse(url)
        res = html.xpath('//div[@id=\"content\"]/pre/text()')[0]
        return res.strip()
    except Exception as er:
        print(str(er))  


def guba_sina(show_content=False):
    """
       获取sina财经股吧首页的重点消息
    Parameter
    --------
        show_content:是否显示内容，默认False
    
    Return
    --------
    DataFrame
        title, 消息标题
        content, 消息内容（show_content=True的情况下）
        ptime, 发布时间
        rcounts,阅读次数
    """
    
    from pandas.io.common import urlopen
    try:
        with urlopen(nv.GUBA_SINA_URL%(ct.P_TYPE['http'],
                                       ct.DOMAINS['sina'])) as resp:
            lines = resp.read()
        html = lxml.html.document_fromstring(lines)
        res = html.xpath('//ul[@class=\"list_05\"]/li')
        heads = html.xpath('//div[@class=\"tit_04\"]')
        data = []
        for head in heads[:1]:
            # title = head.xpath('a/text()')[0]
            title = unicode(head.xpath('a/text()')[0])
            url = head.xpath('a/@href')[0]
            if 'live' in url:
                continue
            ds = [title, url]
            ds.extend(_guba_content(url))
            data.append(ds)
        for row in res:
            # title = row.xpath('a[2]/text()')[0]
            if len(row.xpath('a[2]/text()')) == 0:
                continue
            title = unicode(row.xpath('a[2]/text()')[0])
            url = row.xpath('a[2]/@href')[0]
            if 'live' in url:
                continue
            ds = [title, url]
            ds.extend(_guba_content(url))
            data.append(ds)
        df = pd.DataFrame(data, columns=nv.GUBA_SINA_COLS)
        df['rcounts'] = df['rcounts'].astype(float)
        return df if show_content is True else df.drop('content', axis=1)
    except Exception as er:
        print url
        print(str(er))  
    
    
def _guba_content(url):
    from pandas.io.common import urlopen
    try:
        # html = lxml.html.parse(url)
        with urlopen(url) as resp:
            lines = resp.read().decode('GBK')
        html = lxml.html.fromstring(lines)
        res = html.xpath('//div[@class=\"ilt_p\"]/p')
        if len(res) is 0:
            return ['', '', '0']
        if ct.PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr).replace('&#12288;', '').replace('&#160;', '').replace('&#183;', '').replace('&#252;', '')#.replace('\n\n', '\n').
        html_content = lxml.html.fromstring(sarr)
        content = html_content.text_content()
        ptime = html.xpath('//div[@class=\"fl_left iltp_time\"]/span/text()')[0]
        rcounts = html.xpath('//div[@class=\"fl_right iltp_span\"]/span[2]/text()')[0]
        reg = re.compile(r'\((.*?)\)') 
        rcounts = reg.findall(rcounts)[0]
        return [unicode(content), unicode(ptime), rcounts]
    except Exception, e:
        print url
        print e
        return ['', '', '0']


def _random(n=16):
    from random import randint
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(randint(start, end))

