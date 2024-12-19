import os
import csv
from tabulate import tabulate


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        files = os.listdir(file_path)
        prices = []
        for file in files:
            if 'price' in file.lower(): # учитывает название файлов в которых есть 'price'
                prices.append(file)
                with open(file=file, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=',')
                    headers = reader.fieldnames
                    for row in reader:
                        name_column, price_column, weight_column = None, None, None
                        for header in headers:
                            if header.lower() in ['название', 'продукт', 'товар', 'наименование']:
                                name_column = header
                            elif header.lower() in ['цена', 'розница']:
                                price_column = header
                            elif header.lower() in ['фасовка', 'масса', 'вес']:
                                weight_column = header
                        columns = [name_column, price_column, weight_column]
                        product_name = row.get(columns[0])
                        price = row.get(columns[1])
                        weight = row.get(columns[2])
                        price_per_kg = float(price) / float(weight)
                        self.data.append([product_name, price, weight, file.name, round(price_per_kg, 2)])

    def export_to_html(self, file_name='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Вес</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write(result)
            self.data = sorted(self.data, key=lambda x: x[0]) # сортировка названий по алфавиту
            table = tabulate(self.data, headers=['Название', 'Цена', 'Вес', 'Файл', 'Цена за кг.'], tablefmt='html')
            file.write(table)
            file.write(result)

    def find_text(self, text):
        filtered_data = []
        for row in self.data:
            if text.lower() in row[0].lower():
                filtered_data.append(row)
        sorted_data = sorted(filtered_data, key=lambda x: x[4]) # сортировка по цене
        table = []
        for i, row in enumerate(sorted_data):
            step = [i + 1]
            for item in row:
                step.append(item)
            table.append(step)
        self.result = tabulate(table, headers=["№", "Название", "Цена", "Вес", "Файл", "Цена за кг."], tablefmt="plain")
        print(self.result)


pm = PriceMachine()
pm.load_prices('./')
'''
    Логика работы программы
'''
while True:
    user_input = input('Введите название товара для поиска (или "exit" для завершения): ')
    if user_input.lower() in ['exit']:
        print('the end')
        break
    pm.find_text(user_input)
    pm.export_to_html()
