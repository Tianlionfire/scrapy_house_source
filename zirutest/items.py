# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZirutestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 房源链接
    house_url = scrapy.Field()
    # 房源标题
    house_title = scrapy.Field()
    # 房源编号1
    house_number1 = scrapy.Field()
    # 房源编号2
    house_number2 = scrapy.Field()
    # 行政区
    house_area1 = scrapy.Field()
    # 商圈
    # business_district = scrapy.Field()
    # 小区
    # house_area2 = scrapy.Field()
    # 月付价,页面代码里面没有
    price_month = scrapy.Field()
    # 季付价,页面代码里面没有
    price_season = scrapy.Field()
    # 面积
    house_space = scrapy.Field()
    # 朝向
    house_chaoxiang = scrapy.Field()
    # 户型
    house_model = scrapy.Field()
    # 楼层
    house_floor = scrapy.Field()
    # 出租类型
    house_renting_type = scrapy.Field()
    # 是否阳台
    is_balcony = scrapy.Field()
    # 装修风格
    house_style = scrapy.Field()
    # 是否近地铁
    is_close_metro = scrapy.Field()
    # 交通信息
    traffic_info = scrapy.Field()
    # 经纬度
    house_position = scrapy.Field()
    # 出租状态 #招租的房间号，准备以json保存
    renting_status = scrapy.Field()
    # 租客信息（姓别，星座，职业，入住时间，到期时间） 租客信息，准备以list存储,如果没有，就是空list
    renter_info = scrapy.Field()
    # 房屋配置,string保存，','分开
    house_config = scrapy.Field()
    # 房屋所在城市
    city = scrapy.Field()
    pass
