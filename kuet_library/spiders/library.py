import scrapy
from scrapy.http import FormRequest
import datetime
from scrapy.loader import ItemLoader 
from ..items import KuetLibraryItem

from ..online import get_all_cred

now = datetime.date.today()


class LibrarySpider(scrapy.Spider):
    name = 'library'

    start_urls = ['http://library.kuet.ac.bd:8000/']

    all_cred = get_all_cred()

    def date_parser(self,due):
   
        date = due.split(" ")[0]
    
        date = date.split("/")
 
        date = datetime.date(int(date[2]),int(date[1]),int(date[0]))
        return date 

    def renew_decision(self,due):
        due_date =  self.date_parser(due)
        remaining = due_date - now
        print(remaining)
        binod = datetime.timedelta(days=2)
        if(remaining >
         binod):
            return [False,remaining]
        else:
            return [True,remaining]

    def parse(self, response):
        try:
            for value in self.all_cred.values():
                global userid
                userid = value.get('username')
                password = value.get('password')

                print('Scaning for ' + userid)


                yield FormRequest.from_response(response=response,formxpath="//form[@id='auth']",formdata={
                    'userid':userid,
                    'password': password
                },callback=self.after_login,meta={'userid':userid,'password':password})
        except:
            print('No account Listed')


    def after_login(self,response):
        username = response.xpath("//span[@class='loggedinusername']/text()").get()
        book_table = response.xpath("//table[@id='checkoutst']/tbody/tr")    
        if book_table == [] :
            loader = ItemLoader(item=KuetLibraryItem(),response=response)
            loader.add_value('username','empty')
            loader.add_value('userid',response.meta['userid'])
            loader.add_value('title','empty')
            loader.add_value('author','empty')
            loader.add_value('date_due','empty')
            loader.add_value('renew_link','empty')
            loader.add_value('remaining_renew','empty')
            loader.add_value('remaining_days','empty')
            print('-------Couldn\'t enter into '+ response.meta['userid'] + '\'s account')
            yield loader.load_item()
            
       
        for book in book_table:
        
            loader = ItemLoader(item=KuetLibraryItem(),selector=book,response=response)
            loader.add_value('username' , username)
            myid = response.meta['userid']
            print('----------------' + myid + '----------------')
            loader.add_value('userid',myid)
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

                if decision[0] == True and renew_url != None:
                    renew_url = 'http://library.kuet.ac.bd:8000/' + renew_url
                    yield scrapy.Request(url=renew_url,callback=self.parse_renew)
            loader.add_value('remaining_days',str(decision[1]).split(',')[0].split(' ')[0])
            yield loader.load_item()

            

    def parse_renew(self,response):
        new_date_due = response.xpath(".//td[contains(@class,'date_due')]/span/text()").getall()[-1].strip()
        if new_date_due != date_due:
            print("Successfully Renewed")
        else:
            print("Couldn't renew")