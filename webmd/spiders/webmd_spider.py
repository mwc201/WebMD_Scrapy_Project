from webmd.items import WebmdItem
from scrapy import Spider, Request
import re
import math


class WebmdSpider(Spider):
    name = 'webmd_spider'
    allowed_urls = ['https://www.webmd.com']
    start_urls = ['https://www.webmd.com/drugs/2/index']

    def parse(self, response):
        result_urls = response.xpath('//a[@class="common-result-review"]/@href').extract()
        #OVERRIDE THIS LATER!!!!!!!
        for partial_url in result_urls:
            #url = 'https://www.webmd.com' + partial_url + '&pageIndex=0&sortby=3&conditionFilter=-500 '
            url =  'https://www.webmd.com' + partial_url
            id_ = re.sub("[^0-9]", "", url)
            drug_id = id_[0:int((len(id_)/2))]


            yield Request(url = url, callback = self.parse_name,meta={'drug_id':drug_id})



    def parse_name(self,response):
        drug_id = response.meta.get('drug_id')
        header = response.xpath('//*[@id="header"]/div/h1/text()').extract()[0]
        name = header.split('-')[1].strip(' ').replace(' ','+')
        print(name,'                ','NAME      NAME     NAME')
        if 'amoxicillin' in name:
            url = 'https://www.webmd.com/drugs/drugreview-1531-amoxicillin+oral.aspx?drugid=1531&drugname=amoxicillin+oral&pageIndex=1&sortby=3&conditionFilter=-500'

        else:
            url = 'https://www.webmd.com/drugs/drugreview-' + drug_id + '-' + name + '.aspx?drugid=' + drug_id + '&drugname=' + name + '&pageIndex=1&sortby=3&conditionFilter=-500'

        yield Request(url = url, callback = self.parse_result_pages, meta={'url_nbs':url} )


    def parse_result_pages(self, response): 

        text = response.xpath('//*[@id="ratings_fmt"]/div[3]/div[2]/text()').extract_first()
        

        num_reviews = int(re.findall('\d+', text)[-1])  
        print(num_reviews)

        total_pages = math.ceil(num_reviews/5)

        url = response.meta.get('url_nbs')

        all_page_url = [url.replace('Index=1', 'Index=' + str(i)) for i in range(0, total_pages)]

        print(len(all_page_url))
        #OVERRIDE THIS LATER!!!!!!! COMMENT BELOW LINE OUT
        #all_page_url = [all_page_url[0]]
        #all_page_url = all_page_url[0:1] #first 5 pages of reviews, per drug

        for url in all_page_url:

            yield Request(url = url, callback = self.parse_review_pages)
            
    
    def parse_review_pages(self, response):          


        item = WebmdItem()

        drug = response.xpath('//div[@class="tb_main"]/h1/text()').extract()
        condition = [x.split(':')[1].strip(' ') for x in  response.xpath('//div[@class="conditionInfo"]/text()').extract()]
        effectiveness = [x.split(':')[1].strip(' ') for x in response.xpath('//*[@id="ratings_fmt"]/div/div[2]/div[1]/p[2]/span/text()').extract()] 
        ease_of_use = [x.split(':')[1].strip(' ') for x in response.xpath('//*[@id="ratings_fmt"]/div/div[2]/div[2]/p[2]/span/text()').extract()]
        satisfaction = [x.split(':')[1].strip(' ') for x in response.xpath('//*[@id="ratings_fmt"]/div/div[2]/div[3]/p[2]/span/text()').extract()]
        comment = response.xpath('//*[@id="ratings_fmt"]/div/p[3]/text()').extract()
        date = response.xpath('//div[@class="date"]/text()').extract()
        sex = [ 'Male' if 'Male' in sub_str else 'Female' if 'Female' in sub_str else 'Patient' for sub_str in response.xpath('//p[@class="reviewerInfo"]/text()').extract() ] 
        review = response.xpath('//p[@class="reviewerInfo"]/text()').extract()
        





        #for review_nb in range(len(response.xpath('//p[@class="reviewerInfo"]/text()')))


        for sub_item_nb in range(len(condition)):
            item['drug'] = drug
            item['condition'] = condition[sub_item_nb]
            item['effectiveness'] = effectiveness[sub_item_nb]
            item['ease_of_use'] = ease_of_use[sub_item_nb]
            item['satisfaction'] = satisfaction[sub_item_nb]
            try:
                item['comment'] = comment[sub_item_nb]
            except:
                item['comment'] = 'NO COMMENT'
            item['date'] = date[sub_item_nb]
            item['sex'] = sex[sub_item_nb]
            item['review'] = review[sub_item_nb]

            

            yield item

        

        

