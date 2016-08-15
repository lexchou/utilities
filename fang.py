#!/usr/bin/env python3.5
import re
import urllib.request
import gzip
import contextlib
from io import BytesIO

def loadData(url):
        req = urllib.request.Request(url)
        req.add_header('Accept-Encoding', '')
        with urllib.request.urlopen(req) as response:
          html = response.read()
          if response.info().get('Content-Encoding') == 'gzip':
              buf = BytesIO(html)
              f = gzip.GzipFile(fileobj = buf)
              html = f.read()
          return html.decode('gbk', 'replace')

def extract(s, reg, ret, key):
    g = re.search(reg, s, re.M | re.S)
    if g:
        ret[key] = g.group(1)
def get_detail(url):
    html = loadData(url)
    ret = {}
    extract(html, r"currNewcode = '(\d+)'", ret, 'id')
    if 'id' in ret:
        #extract(html, r'txt_minprice" value="(\d+)', ret, 'minprice')
        #extract(html, r'txt_maxprice" value="(\d+)', ret, 'maxprice')
        extract(html, r"projname = '(.*?)'", ret, 'name')

        extract(html, r'平均价格：</strong>&nbsp;<span class="prib cn_ff">(\d+)', ret, 'price')

        extract(html, r'txt_sale_rate" value="(.*?)"', ret, 'state')
        #extract(html, r'txt_sale_date" value="(.*?)"', ret, 'date')
        extract(html, r'txt_fix_status" value="(.*?)"', ret, 'decoration_status')
        if ret['decoration_status']:
                ret['decoration_status'] = ret['decoration_status'].replace(',', '/')
        extract(html, r'txt_address" value="(.*?)"', ret, 'address')
        extract(html, r'txt_developer" value="(.*?)"', ret, 'developer')
        detail_url = url + '/house/{}/housedetail.htm'.format(ret['id'])
        html = loadData(detail_url)
        extract(html, r'物 业 费 </strong>(.*?)[元<]', ret, 'wuyefei')
        extract(html, r'绿 化 率 </strong>(\d+)[%<]', ret, 'lvhualv')
        extract(html, r'容 积 率 </strong>(.*?)[&<]', ret, 'rongjilv')
        extract(html, r'交房时间 </strong>(.*?)[&<]', ret, 'date')
    else:

        extract(html, r'均价：<strong class="red">(\d+)<', ret, 'price')
        extract(html, r'总&ensp;户&ensp;数：</strong>(\d+)[户<]', ret, 'houses')
        extract(html, r'小区地址：</strong>(.*?)<', ret, 'address')
        extract(html, r"ask_title\('(.*?)'\)", ret, 'name')

        extract(html, r'开&ensp;发&ensp;商：</strong>(.*?)<', ret, 'developer')
        extract(html, r'物&ensp;业&ensp;费：</strong>(.*?)[元<]', ret, 'wuyefei')
        extract(html, r'绿&ensp;化&ensp;率：</strong>(.*?)<', ret, 'lvhualv')
        extract(html, r'容&ensp;积&ensp;率：</strong>(.*?)<', ret, 'rongjilv')
        extract(html, r'建筑年代：</strong>(.*?)[&<]', ret, 'date')
        detail_url = url + '/xiangqing/'



    return ret
    
def get_list():
    def get_from_url(url):
        html = loadData(url)
        g = re.findall(r'nlcd_name".*?href="(.*?)">\s+(.*?)\s+</a>', html, re.M | re.S)
        for (url, name) in g:
            print("Loading details for {} from {}".format(name, url))
            details = get_detail(url)
            details['name'] = name
            yield details
        g = re.findall(r'fl"><h4><a target="_blank" href="(.*?)">(.*?)</a>', html, re.M | re.S)
        for (url, name) in g:
            print("Loading details for {} from {}".format(name, url))
            details = get_detail(url)
            details['name'] = name
            yield details

        g = re.search(r'<a class="next"\s+href="(.*?)"', html, re.M | re.S)
        if g:
            next_url = "http://newhouse.wuhan.fang.com" + g.group(1)
            print("Found next page {}".format(next_url))
            yield from get_from_url(next_url)
        else:
            print("Cannot find next page")
    yield from get_from_url("http://newhouse.wuhan.fang.com/house/s/jianghan1/a77/")


def main():
    keys = "name,address,developer,date,wuyefei,lvhualv,rongjilv,decoration_status,price".split(',')
    result = open("result.csv", "w")
    result.write(", ".join(keys) + "\r\n")
    result.flush()
    for x in get_list():
        result.write(", ".join(map(lambda k : str(x.get(k)), keys)) + "\r\n")
        result.flush()
    result.close()


#print(get_detail("http://xinhuaximeilingongguan.fang.com"))
main()
