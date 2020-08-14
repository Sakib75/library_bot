# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
import datetime

def renew_decision(self,due):
    due_date =  self.date_parser(due)
    remaining = due_date - datetime.datetime.now()
    return str(remaining)
    



def clear_renew(remaining_renew):
    renew =  remaining_renew.replace('(','')
    renew =  renew.replace(')','').split()[0]   
    return renew

class KuetLibraryItem(scrapy.Item):
    username = scrapy.Field(output_processor = TakeFirst())
    remaining_days = scrapy.Field(output_processor = TakeFirst())
    userid = scrapy.Field(output_processor = TakeFirst())
    title = scrapy.Field(output_processor = TakeFirst())
    author = scrapy.Field(output_processor = TakeFirst())
    date_due = scrapy.Field(output_processor = TakeFirst())
    renew_link = scrapy.Field(output_processor = TakeFirst())
    remaining_renew = scrapy.Field(output_processor = TakeFirst(),input_processor = MapCompose(clear_renew))
