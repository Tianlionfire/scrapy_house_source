# -*- coding: utf-8 -*-
import scrapy
import json
from zirutest.items import ZirutestItem


# from scrapy_splash import SplashRequest


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = []
    start_urls = ['http://sh.ziroom.com/z/nl/z3.html']
    # start_urls = ['http://sh.ziroom.com/z/nl/z3.html', 'http://www.ziroom.com/z/nl/z3.html', 'http://sz.ziroom.com/z/nl/z3.html', 'http://hz.ziroom.com/z/nl/z3.html']

    def parse(self, response):
        """
        urls里面保存了所有的区域地址的链接，已经去除了"全部"的链接
        """
        # url = 'http://sh.ziroom.com/z/vr/60696339.html'
        # yield scrapy.Request(url, callback=self.parse_item)
        urls = []
        url_list = response.xpath('//dl[@class="clearfix zIndex6"]/dd/ul/li/div/span')
        for url1 in url_list:
            if url1.xpath('./a/text()').extract()[0] != '全部':
                urls.append('http:' + url1.xpath('./a/@href').extract()[0])
        for url2 in urls:
            yield scrapy.Request(url2, callback=self.parse_url_list)
            # yield SplashRequest(url=url2, callback=self.parse_url_list, args={'wait': 1})
        # # print(len(urls))

    def parse_url_list(self, response):
        """
        循环处理各地区的url,扒出house_list里的url,然后循环用另外的函数处理.如果有下一页,递归自己
        """
        house_list_url = response.xpath('//ul[@id="houseList"]/li/div[@class="txt"]/h3/a/@href').extract()
        # house_list_url2就是每一页上面的房子的链接
        house_list_url2 = []
        for url1 in house_list_url:
            house_list_url2.append('http:' + url1)
        for url2 in house_list_url2:
            # 去详情页面处理数据抓取item
            yield scrapy.Request(url2, callback=self.parse_item)
            # yield SplashRequest(url=url2, callback=self.parse_item, args={'wait': 1})
        if response.xpath('//div[@id="page"]/a[@class="next"]/@href').extract():
            new_url = 'http:' + response.xpath('//div[@id="page"]/a[@class="next"]/@href').extract()[0]
            yield scrapy.Request(new_url, callback=self.parse_url_list)
            # yield SplashRequest(url=new_url, callback=self.parse_url_list, args={'wait': 1})

    def parse_item(self, response):
        """
        处理item
        """
        item = ZirutestItem()
        item['house_url'] = response.url
        # 判断房子所在的城市
        item['city'] = '北京'
        if item['house_url'].find('sh') != -1:
            item['city'] = '上海'
        if item['house_url'].find('sz') != -1:
            item['city'] = '深圳'
        if item['house_url'].find('hz') != -1:
            item['city'] = '杭州'
        if item['house_url'].find('nj') != -1:
            item['city'] = '南京'
        if item['house_url'].find('cd') != -1:
            item['city'] = '成都'
        if item['house_url'].find('wh') != -1:
            item['city'] = '武汉'
        if item['house_url'].find('gz') != -1:
            item['city'] = '广州'
        if item['house_url'].find('tj') != -1:
            item['city'] = '天津'
        item['house_title'] = response.xpath('//div[@class="room_name"]/h2/text()').extract()[0].strip()
        item['house_number1'] = response.xpath('//h3[@class="fb"]/text()').extract()[1].strip()
        item['house_number2'] = response.xpath('//h3[@class="fb"]/text()').extract()[1].strip().split('_')[0]
        item['house_area1'] = response.xpath('//div[@class="room_name"]/p/span[@class="ellipsis"]/text()').extract()[
            0].strip()
        detail_room = response.xpath('//ul[@class="detail_room"]/li/text()').extract()
        item['house_space'] = ''
        item['house_chaoxiang'] = ''
        item['house_model'] = ''
        item['house_floor'] = ''
        for detail in detail_room:
            if detail.strip().replace(" ", "").replace("\n", "").find('面积') == 0:
                item['house_space'] = detail.strip().replace(" ", "").replace("\n", "").split('：')[1]
            if detail.strip().replace(" ", "").replace("\n", "").find('朝向') == 0:
                item['house_chaoxiang'] = detail.strip().replace(" ", "").replace("\n", "").split('：')[1]
            if detail.strip().replace(" ", "").replace("\n", "").find('户型') == 0:
                item['house_model'] = detail.strip().replace(" ", "").replace("\n", "").split('：')[1]
            if detail.strip().replace(" ", "").replace("\n", "").find('楼层') == 0:
                item['house_floor'] = detail.strip().replace(" ", "").replace("\n", "").split('：')[1]

        # 租房方式
        item['house_renting_type'] = \
            response.xpath('//ul[@class="detail_room"]/li/span[@class="icons"]/text()').extract()[0]
        # 是否靠近地铁
        if len(response.xpath('//span[@class="subway"]/text()').extract()) > 0:
            item['is_close_metro'] = response.xpath('//span[@class="subway"]/text()').extract()[0]
        else:
            item['is_close_metro'] = ''
        # 是否有阳台
        if len(response.xpath('//span[@class="balcony"]/text()').extract()) > 0:
            item['is_balcony'] = response.xpath('//span[@class="balcony"]/text()').extract()[0]
        else:
            item['is_balcony'] = ''
        # 装修风格
        if len(response.xpath('//span[@class="style"]/text()').extract()) > 0:
            item['house_style'] = response.xpath('//span[@class="style"]/text()').extract()[0]
        else:
            item['house_style'] = ''
        # 交通信息
        item['traffic_info'] = response.xpath('//div[@class="aboutRoom gray-6"]/p/text()').extract()[1]
        # 经纬度
        house_position_dict = dict()
        house_position_dict['lng'] = response.xpath('//input[@id="mapsearchText"]/@data-lng').extract()[0]
        house_position_dict['lat'] = response.xpath('//input[@id="mapsearchText"]/@data-lat').extract()[0]
        item['house_position'] = json.dumps(house_position_dict)
        # 出租状态,就是招租的房间号，准备以list保存
        item['renting_status'] = []
        # 如果是空的,表示没有招租信息,也没有室友信息
        if len(response.xpath('//div[@class="greatRoommate"]').extract()) > 0:
            if len(response.xpath('//div[@class="greatRoommate"]/ul/li[@class="current "]').extract()) > 0:
                item['renting_status'] = response.xpath(
                    '//div[@class="greatRoommate"]/ul/li[@class="current "]//div[@class = "user_top clearfix"]/p/ text()').extract()
        else:
            item['renting_status'] = []

        # 租客信息（姓别，星座，职业，入住时间，到期时间） 租客信息，准备以list存储,如果没有，就是空list,list里面存储的是json
        item['renter_info'] = []
        if len(response.xpath('//div[@class="greatRoommate"]').extract()) > 0:
            if len(response.xpath('//div[@class="greatRoommate"]/ul/li[@class="man "]').extract()) > 0:
                # 如果有男室友
                for man in response.xpath('//div[@class="greatRoommate"]/ul/li[@class="man "]'):
                    renter_info_dict = dict()
                    renter_info_dict['room_number'] = man.xpath('//div[@class="user_top clearfix"]/p/text()').extract()[0]
                    renter_info_dict['sex'] = 'man'
                    # 如果填写了星座
                    if man.xpath('//div[@class="user_center"]/p[@class="sign"]/text()').extract():
                        renter_info_dict['sign'] = man.xpath('//div[@class="user_center"]/p[@class="sign"]/text()').extract()[0]
                    else:
                        renter_info_dict['sign'] = ''
                    # 如果填写了职业
                    if man.xpath(
                            '//div[@class="user_center"]/p[@class="jobs"]/span[@class="ellipsis"]/text()').extract():
                        renter_info_dict['job'] = man.xpath(
                            '//div[@class="user_center"]/p[@class="jobs"]/span[@class="ellipsis"]/text()').extract()[0]
                    else:
                        renter_info_dict['job'] = ''
                    # 如果写了居住时间
                    if man.xpath('//div[@class="user_bottom"]/p/text()').extract():
                        renter_info_dict['rent_time'] = man.xpath('//div[@class="user_bottom"]/p/text()').extract()[
                            0].strip()
                    else:
                        renter_info_dict['rent_time'] = ''
                    item['renter_info'].append(str(renter_info_dict))
            if len(response.xpath('//div[@class="greatRoommate"]/ul/li[@class="woman "]').extract()) > 0:
                # 如果有女室友
                for woman in response.xpath('//div[@class="greatRoommate"]/ul/li[@class="woman "]'):
                    renter_info_dict = dict()
                    renter_info_dict['room_number'] = \
                        woman.xpath('//div[@class="user_top clearfix"]/p/text()').extract()[0]
                    renter_info_dict['sex'] = 'woman'
                    # 如果填写了星座
                    if woman.xpath('//div[@class="user_center"]/p[@class="sign"]/text()').extract():
                        renter_info_dict['sign'] = \
                            woman.xpath('//div[@class="user_center"]/p[@class="sign"]/text()').extract()[0]
                    else:
                        renter_info_dict['sign'] = ''
                    # 如果填写了职业
                    if woman.xpath(
                            '//div[@class="user_center"]/p[@class="jobs"]/span[@class="ellipsis"]/text()').extract():
                        renter_info_dict['job'] = woman.xpath(
                            '//div[@class="user_center"]/p[@class="jobs"]/span[@class="ellipsis"]/text()').extract()[0]
                    else:
                        renter_info_dict['job'] = ''
                    # 如果写了居住时间
                    if woman.xpath('//div[@class="user_bottom"]/p/text()').extract():
                        renter_info_dict['rent_time'] = woman.xpath('//div[@class="user_bottom"]/p/text()').extract()[
                            0].strip()
                    else:
                        renter_info_dict['rent_time'] = ''
                    item['renter_info'].append(str(renter_info_dict))
        else:
            item['renter_info'] = []
        # 动态信息,需要用scrapy-splash来获取
        item['price_month'] = ''
        item['price_season'] = ''
        # 房屋配置,string保存，'-'分开,动态信息
        # item['house_config'] =  response.xpath('//li[@class="have"]/text()').extract()
        item['house_config'] = ''
        yield item
