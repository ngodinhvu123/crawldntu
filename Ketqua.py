
from scrapy.crawler import CrawlerProcess
import scrapy
from scrapy import signals
from scrapy.http import Request
from scrapy.signalmanager import dispatcher

def xuly(path):
    if path==None:
        return "Trong"
    else:
        return path
        
class DmozSpider(scrapy.Spider):  
    name = "login"
    start_urls = ['https://sv.dntu.edu.vn/login/dang-nhap.htm']
        
    def parse(self, response):
        data={
            '__VIEWSTATE':'/wEPDwUJMTUzNDQ4NzQwD2QWAgIHDxYCHgZhY3Rpb24FAS9kGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ5fY3RsMTg6aW5wU2F2ZemWtiC2wDnYmiTAJyTf0GMW8KTthtGAvnYEZGxdp9FG',
            '__VIEWSTATEGENERATOR':'CA0B0334',
            '__EVENTVALIDATION':'/wEdAAU+hiO9LaV7x4uLL6BiQWsv3BAFmS2fMMyaWfpn0jQc+G+Le09EEWifT02JSL7EgufJzwi5uORJRDUBKIO2iIB5nj93cunMabbkmyBy8GzZdwcqNGqmFXfDFnrD/K3jCn0VaPX9P3AaufezoKc12fX+',
            '_ctl18:inpUserName': self.mssv, 
            '_ctl18:inpPassword': self.mk,
            '_ctl18:butLogin':'%C4%90%C4%83ng+nh%E1%BA%ADp'}
        return scrapy.FormRequest.from_response(
            response,
            formdata=data,
            callback=self.after_login
        )
    def after_login(self, response):
        _setcookies=(response.headers.getlist('Set-Cookie'))[3]
        vnkweb=str(_setcookies)
        temp=''
        for i in range(9,vnkweb.find(';')):
            temp=temp+vnkweb[i]
        return Request(url="https://sv.dntu.edu.vn/timestable/calendarcl/thoi-khoa-bieu.htm",
                               cookies={'vnkweb': temp},
                               callback=self.thoikhoabieu)
    def thoikhoabieu(self,response):        
        complete=[]
        req=response.xpath('//*[@class="k-table"]//tr')       
        for row in req:         
            tkb={
                'stt':xuly(row.xpath('./td[1]/text()').extract_first()),
                'Thu':xuly(row.xpath('./td[2]/text()').extract_first()),
                'Ngay':xuly(row.xpath('./td[3]/text()').extract_first()),
                'Sang':xuly(row.xpath('./td[4]/span/text()').extract()),
                'Chieu':xuly(row.xpath('./td[5]/span/text()').extract()),
                'Toi':xuly(row.xpath('./td[6]/text()').extract_first()),
                'GhiChu':xuly(row.xpath('./td[7]/text()').extract_first())
            }
            complete.append(tkb)    
        return(complete)

