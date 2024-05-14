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
        try:
            info = {}
            html = html.find('div', class_="wrapper")
            info.update(self.get_info_normal(self.xPath(html, "Общая информация")))
            info.update(self.get_info_normal(self.xPath(html, "Информация о заказчике")))
            info.update(self.get_info_normal(self.xPath(html, "Общие данные")))
            info.update(self.get_info_table(self.xPath(html, "Информация о поставщиках")))
            print(info)
            with open(f"./in/{num}.json", "w", encoding="UTF-8") as outfile:
                for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(info):
                    outfile.write(chunk)
            return 1
        except:
            return 0

    def delete_after_inn(self, text):
        index = text.find("ИНН")  # Find the index of the first occurrence of "HIJ"
        if index != -1:  # If "HIJ" is found
            return text[:index]  # Return the substring from the start of the string to the index of "HIJ"
        else:
            return text  # If "HIJ" is not found, return the original string

    def clean(self, line):
        line = line.strip()
        line = line.replace("\n", " ")
        line = line.replace('\"', " ")
        line = line.replace('Загрузка ...', " ")
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
        list = []
        for th in thead.find_all('th'):
            name = th.text
            if name != '':
                list.append(name)
                info[head][name] = []

        info[head]["ИНН"] = []
        info[head]["КПП"] = []
        for tbody in html.find_all('tbody'):
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
                text = self.delete_after_inn(text)
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
            try:
                name = i.find('span', class_="section__title").text
                name = self.clean(name)
                data = i.find('span', class_="section__info").text
                data = self.clean(data)
                print(name, data)
                info[head][name] = data
            except:
                print("oof")
        print(info)
        return info
