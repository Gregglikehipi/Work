from bot import bot
import time
import os.path
from logic import download_file
import json


@bot.message_handler(commands=["start"])
def handle_role_selection(message):
    bot.send_message(message.chat.id, 'Есть 9 команд:\n'
                                      '/start получить список команд\n'
                                      '/load добавить контракт в базу\n'
                                      '/getText получить получить краткую информацию контракта по номеру\n'
                                      '/getFile получить получить полную информацию контракта по номеру\n'
)


@bot.message_handler(commands=["load"])
def get_text_command(message):
    bot.send_message(message.chat.id, 'Введите номер контракта')
    bot.register_next_step_handler(message, load_text)


def load_text(message):
    if download_file(int(message.text)) == 1:
        bot.send_message(message.chat.id, 'Вы выгрузили контракт. Повторите запрос, чтобы получить данные')
    else:
        bot.send_message(message.chat.id, 'Контракт не получилось выгрузить')


@bot.message_handler(commands=["getText"])
def get_text_command(message):
    bot.send_message(message.chat.id, 'Введите номер контракта')
    bot.register_next_step_handler(message, send_text)


def send_text(message):
    path = f'./in/{int(message.text)}.json'
    check_file = os.path.isfile(path)
    if check_file:
        with open(path) as json_file:
            data = json.load(json_file)
            price = ''
            worker = ''
            if "Организация" in data["Информация о поставщиках"]:
                for i in data["Информация о поставщиках"]["Организация"]:
                    worker = worker + i + "\n"
            if "Максимальное значение цены контракта" in data["Общие данные"]:
                price = data["Общие данные"]["Максимальное значение цены контракта"]
            if "Цена контракта" in data["Общие данные"]:
                price = data["Общие данные"]["Цена контракта"]

            bot.send_message(message.chat.id, f'Контракт:\n'
                                              f'Номер контракта: {data["Общая информация"]["Реестровый номер контракта"]}\n'
                                              f'Статус: {data["Общая информация"]["Статус контракта"]}\n'
                                              f'Цена: {price}\n'
                                              f'Заказчик: {data["Информация о заказчике"]["Полное наименование заказчика"]}\n'
                                              f'Поставщик: {worker}'
                             )
    else:
        if download_file(int(message.text)) == 1:
            with open(path) as json_file:
                data = json.load(json_file)
                price = ''
                worker = ''
                if "Организация" in data["Информация о поставщиках"]:
                    for i in data["Информация о поставщиках"]["Организация"]:
                        worker = worker + i + "\n"
                if "Максимальное значение цены контракта" in data["Общие данные"]:
                    price = data["Общие данные"]["Максимальное значение цены контракта"]
                if "Цена контракта" in data["Общие данные"]:
                    price = data["Общие данные"]["Цена контракта"]

                bot.send_message(message.chat.id, f'Контракт:\n'
                                                  f'Номер контракта: {data["Общая информация"]["Реестровый номер контракта"]}\n'
                                                  f'Статус: {data["Общая информация"]["Статус контракта"]}\n'
                                                  f'Цена: {price}\n'
                                                  f'Заказчик: {data["Информация о заказчике"]["Полное наименование заказчика"]}\n'
                                                  f'Поставщик: {worker}'
                                 )
        else:
            bot.send_message(message.chat.id, 'Контракт не получилось выгрузить')


@bot.message_handler(commands=["getFile"])
def get_file_command(message):
    bot.send_message(message.chat.id, 'Введите номер контракта')
    bot.register_next_step_handler(message, send_file)


def send_file(message):
    path = f'./in/{int(message.text)}.json'
    check_file = os.path.isfile(path)
    print(path)
    if check_file:
        with open(path, 'rb') as file:
            bot.send_document(chat_id=message.chat.id, document=file)
    else:
        if download_file(int(message.text)) == 1:
            with open(path, 'rb') as file:
                bot.send_document(chat_id=message.chat.id, document=file)
        else:
            bot.send_message(message.chat.id, 'Контракт не получилось выгрузить')


while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)
