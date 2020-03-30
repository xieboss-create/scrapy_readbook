# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings


class ReadbookPipeline(object):
    class ReadbookPipeline(object):
        def open_spider(self, spider):
            self.fp = open('book.json', 'w', encoding='utf-8')

        def process_item(self, item, spider):
            self.fp.write(str(item))
            return item

        def close_spider(self, spider):
            self.fp.close()


# pymysql的使用步骤
#   1 conn   连接
#   2 cursor 游标
#   3 cursor.execute(sql)
#
#   4 conn.commit()
#   5 cursor.close()
#   6 conn.close()
import pymysql


class SaveDataPipeline(object):
    def open_spider(self, spider):
        # 导入settings.py文件中的配置
        # 会把settings中的所有的等号左边的值当作key  等号右边的值当作value
        settings = get_project_settings()
        db_host = settings['DB_HOST']
        db_port = settings['DB_PORT']
        db_user = settings['DB_USER']
        db_password = settings['DB_PASSWORD']
        db_name = settings['DB_NAME']
        db_charset = settings['DB_CHARSET']

        self.conn = pymysql.Connect(host=db_host,
                                    user=db_user,
                                    password=db_password,
                                    database=db_name,
                                    # 端口号必须是整型
                                    port=db_port,
                                    # 字符集不允许加-
                                    charset=db_charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # {}的外面必须要加 “”
        sql = 'insert into `read` values ("{}","{}")'.format(item['src'], item['name'])
        self.cursor.execute(sql)
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
