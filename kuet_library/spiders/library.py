import scrapy
from scrapy.http import FormRequest
import datetime
from scrapy.loader import ItemLoader 
from ..items import KuetLibraryItem
from ..cred import userid,password

now = datetime.date.today()


class LibrarySpider(scrapy.Spider):
    name = 'library'

    start_urls = ['http://library.kuet.ac.bd:8000/']

    def date_parser(self,due):
   
        date = due.split(" ")[0]
    
        date = date.split("/")
 
        date = datetime.date(int(date[2]),int(date[1]),int(date[0]))
        return date 

    def renew_decision(self,due):
        due_date =  self.date_parser(due)
        remaining = due_date - now
        binod = datetime.timedelta(days=1)
        if(remaining >
         binod):
            return False
        else:
            return True

    def parse(self, response):
        yield FormRequest.from_response(response=response,formxpath="//form[@id='auth']",formdata={
            'userid':userid,
            'password': password
        },callback=self.after_login)



    def after_login(self,response):
        book_table = response.xpath("//table[@id='checkoutst']/tbody/tr")    
        for book in book_table:
            loader = ItemLoader(item=KuetLibraryItem(),selector=book)
            loader.add_xpath('title',".//td[@class='title']/a/text()")
            loader.add_xpath('author',".//td[@class='author']/text()")
            loader.add_xpath('date_due',".//td[contains(@class,'date_due')]/span/@title")
            loader.add_xpath('renew_link',".//td[@class='renew']/a/@href")
            loader.add_xpath('remaining_renew',".//span[@class='renewals']/text()")



            
            global date_due
            date_due = book.xpath(".//td[contains(@class,'date_due')]/span/text()").getall()[-1].strip()
            if date_due:
                decision = self.renew_decision(date_due)
                try: 
                    renew_url = book.xpath(".//td[@class='renew']/a/@href").get()
                except:
                    print('No renew url')
                print("Decision : " + str(decision))

                if decision == True and renew_url != None:
                    renew_url = 'http://library.kuet.ac.bd:8000/' + renew_url
                    yield scrapy.Request(url=renew_url,callback=self.parse_renew)

            yield loader.load_item()

    def parse_renew(self,response):
        new_date_due = response.xpath(".//td[contains(@class,'date_due')]/span/text()").getall()[-1].strip()
        if new_date_due != date_due:
            print("Successfully Renewed")
        else:
            print("Couldn't renew")