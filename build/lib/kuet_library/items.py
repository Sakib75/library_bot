# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose

def date_due_process(date_due):
    
    print(date_due)
    date_due_final = date_due
    return date_due_final

def clear_renew(remaining_renew):
    renew =  remaining_renew.replace('(','')
    renew =  renew.replace(')','').split()[0]   
    return renew

class KuetLibraryItem(scrapy.Item):
    title = scrapy.Field(output_processor = TakeFirst())
    author = scrapy.Field(output_processor = TakeFirst())
    date_due = scrapy.Field(output_processor = TakeFirst())
    renew_link = scrapy.Field(output_processor = TakeFirst())
    remaining_renew = scrapy.Field(output_processor = TakeFirst(),input_processor = MapCompose(clear_renew))
