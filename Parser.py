from bs4 import BeautifulSoup
from lxml import etree
import json


class Parser:
    def xPath(self, html, data):
        html_string = str(html)
        tree = etree.HTML(html_string)
        xpath_expression = f"//div[@class='col'][h2[contains(text(), '{data}')]]"
        result = tree.xpath(xpath_expression)
        return BeautifulSoup(etree.tostring(result[0]), 'html.parser')

    def get_info(self, html, num):
        #try:
            list = []
            html = html.find('div', class_="wrapper")
            list.append(self.get_info_normal(self.xPath(html, "Общая информация")))
            list.append(self.get_info_normal(self.xPath(html, "Информация о заказчике")))
            list.append(self.get_info_normal(self.xPath(html, "Общие данные")))
            list.append(self.get_info_table(self.xPath(html, "Информация о поставщиках")))
            print(list)
            with open(f"./in/{num}.json", "w", encoding="UTF-8") as outfile:
                for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(list):
                    outfile.write(chunk)
        #except:
            #print("NO")

    def clean(self, line):
        line = line.strip()
        line = line.replace("\n", " ")
        line = line.replace('\"', " ")
        line = ' '.join(line.split())
        return line

    def get_info_table(self, html):
        head = html.find('h2').text
        print(head)
        html = html.find('table')
        print(html.prettify())
        info = f'{{"{head}" : {{}}}}'
        info = json.loads(info)
        thead = html.find('thead')
        tbody = html.find('tbody')
        list = []
        for th in thead.find_all('th'):
            name = th.text
            if name != '':
                list.append(name)
                info[head][name] = []

        info[head]["ИНН"] = []
        info[head]["КПП"] = []
        i = 0
        flag = 0
        for td in tbody.find_all('td'):
            if "tableBlock__col_last" in td.get('class'):
                continue
            if "tableBlock__col_first" in td.get('class'):
                for sec in td.find_all('section'):
                    if flag == 0:
                        info[head]["ИНН"].append(sec.select_one(":nth-child(2)").text)
                        flag = 1
                    else:
                        info[head]["КПП"].append(sec.select_one(":nth-child(2)").text)
            text = td.text
            text = self.clean(text)
            info[head][list[i]].append(text)
            i = i + 1
        return info

    def get_info_normal(self, html):
        head = html.find('h2').text
        print(head)
        html = html.find('div')
        print(html.prettify())
        if html.find('div', class_="mb-32px"):
            html = html.find('div', class_="mb-32px")
        info = f'{{"{head}" : {{}}}}'
        info = json.loads(info)
        for i in html.find_all('section'):
            name = i.find('span', class_="section__title").text
            name = self.clean(name)
            data = i.find('span', class_="section__info").text
            data = self.clean(data)
            print(name, data)
            info[head][name] = data
        print(info)
        return info
