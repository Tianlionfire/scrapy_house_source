# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from openpyxl import Workbook
import pymysql


# class ZirutestPipeline(object):
#
#     def __init__(self):
#         self.wb = Workbook()
#         self.ws = self.wb.active
#         self.ws.append(
#             ['城市', '房源链接', '房源标题', '房源编号1', '房源编号2', '行政区', '月付价', '季付价', '面积', '朝向', '户型', '楼层', '出租类型', '是否阳台', '装修风格',
#              '是否近地铁', '交通信息', '经纬度', '出租状态', '租客信息', '房屋配置'])  # 设置表头
#
#     def process_item(self, item, spider):
#         line = [item['city'], item['house_url'], item['house_title'], item['house_number1'], item['house_number2'],
#                 str(item['house_area1']), item['price_month'], item['price_season'], item['house_space'],
#                 item['house_chaoxiang'], item['house_model'],
#                 item['house_floor'], item['house_renting_type'], item['is_balcony'], item['house_style'],
#                 item['is_close_metro'], item['traffic_info'], item['house_position'], str(item['renting_status']),
#                 str(item['renter_info']), item['house_config']]  # 把数据中每一项整理出来
#         self.ws.append(line)  # 将数据以行的形式添加到xlsx中
#         return item
#
#     def close_spider(self, spider):
#         file_name = 'shanghaiziroom.xlsx'
#         self.wb.save(file_name)  # 保存xlsx文件

class ZirutestPipeline(object):
    def __init__(self, dbparams):
        self.connect = pymysql.connect(
            host=dbparams['host'],
            port=dbparams['port'],
            db=dbparams['db'],
            user=dbparams['user'],
            passwd=dbparams['passwd'],
            charset=dbparams['charset'],
            use_unicode=dbparams['use_unicode']
        )
        # 创建一个句柄
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        # 读取settings中的配置
        dbparams = dict(
            host=crawler.settings.get('MYSQL_HOST'),
            db=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            passwd=crawler.settings.get('MYSQL_PASSWD'),
            port=crawler.settings.get('MYSQL_POR'),
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode=False,
        )
        return cls(dbparams)

    def process_item(self, item, spider):
        if spider.name == 'ziroom':
            sql = 'insert into ziroom_data(city,house_url,house_title,house_number1,house_number2,house_area1,price_mouth,price_season,house_space,house_chaoxiang,house_model,house_floor,house_renting_type,is_balcony,house_style,is_close_metro,traffic_info,house_position,renting_status,renter_info,house_config) values (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)'
            self.cursor.execute(sql, (item['city'], item['house_url'], item['house_title'], item['house_number1'], item['house_number2'],str(item['house_area1']), item['price_month'], item['price_season'], item['house_space'],item['house_chaoxiang'], item['house_model'],item['house_floor'], item['house_renting_type'], item['is_balcony'], item['house_style'],item['is_close_metro'], item['traffic_info'], item['house_position'], str(item['renting_status']),str(item['renter_info']), item['house_config']))
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()
