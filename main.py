from Crawler import Crawler
from Parser import Parser
#from bot import bot
#import time

print("hi")
num = 2352502347623000268
crawler = Crawler()
parser = Parser()
link = f'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber={num}'
print(link)
flag = parser.get_info(crawler.get_html(link), num)


