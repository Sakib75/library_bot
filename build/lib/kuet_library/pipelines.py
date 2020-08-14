# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class KuetLibraryPipeline:
    def process_item(self, item, spider):
        item.setdefault('remaining_renew','0')
        item.setdefault('renew_link','N/A')
        
        return item
