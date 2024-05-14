from Crawler import Crawler
from Parser import Parser


def download_file(num):
    crawler = Crawler()
    parser = Parser()
    link = f'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber={num}'
    print(link)
    flag = parser.get_info(crawler.get_html(link), num)
    return flag
