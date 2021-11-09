import sys
import re
import json
import argparse
from tqdm import tqdm
from typing import List

class Information:
    email: str
    height: str
    snils: str
    passport_series: str
    occupation: str
    age: str
    academic_degree: str
    worldview: str
    address: str

    def __init__(self, dic: dict):
        self.cur_dict = dic
        self.email = dic['email']
        self.height = dic['height']
        self.snils = dic['snils']
        self.passport_series = dic['passport_series']
        self.occupation = dic['occupation']
        self.age = dic['age']
        self.academic_degree = dic['academic_degree']
        self.worldview = dic['worldview']
        self.address = dic['address']


class Validator:

    notes: List[Information]

    def __init__(self, notes: List[Information]):
        self.notes = []
        for i in notes:
            self.notes.append(Information(i))

    def parse_note(self, notes: Information) -> List[str]:
        incorrect_keys = []
        if (self.check_email(notes.email) == 0):
            incorrect_keys.append('email')
        elif (self.check_snils(notes.snils) == 0):
            incorrect_keys.append('snils')
        elif (self.check_passport(notes.passport_series) == 0):
            incorrect_keys.append('passport_series')
        elif (self.check_height(notes.height) == 0):
            incorrect_keys.append('height')
        elif (self.check_age(notes.age) == 0):
            incorrect_keys.append('age')
        elif (self.check_address(notes.address) == 0):
            incorrect_keys.append('address')
        elif (self.check_occupation(notes.occupation) == 0):
            incorrect_keys.append('occupation')
        elif (self.check_degree(notes.academic_degree) == 0):
            incorrect_keys.append('academic_degree')
        elif (self.check_worldview(notes.worldview) == 0):
            incorrect_keys.append('worldview')

        return incorrect_keys

    def parse(self) -> (List[List[str]], List[Information]):
        incorrect_n = []
        correct_n = []
        for i in self.notes:
            incorrect_keys = self.parse_note(i)
            if len(incorrect_keys) != 0:
                incorrect_n.append(incorrect_keys)
            else:
                correct_n.append(i)
        return (incorrect_n, correct_n)

    def check_email(self, email: str) -> bool:
        pattern = "^[^\\s@]+@([^\\s@.,]+\\.)+[^\\s@.,]{2,}$"
        if re.match(pattern, email):
            return True
        return False

    def check_snils(self, inn: str) -> bool:
        pattern = '^\\d{11}$'
        if re.match(pattern, inn):
            return True
        return False

    def check_passport(self, passport: str) -> bool:
        pattern = '^\\d{2} \\d{2}$'
        if re.match(pattern, passport):
            return True
        return False

    def check_height(self, height: str) -> bool:
        try:
            height_1 = float(height)
        except ValueError:
            return False
        return 1.1 < height_1 < 3

    def check_age(self, age: str) -> bool:
        try:
            age_1 = int(age)
        except ValueError:
            return False
        return 18 <= age_1 < 110

    def check_address(self, address: str) -> bool:
        pattern = '^[\\wа-яА-Я\\s\\.\\d-]* \\d+$'
        if re.match(pattern, address):
            return True
        return False

    def check_occupation(self, occupation: str) -> bool:
        pattern = '^[a-zA-Zа-яА-Я -]+$'
        if re.match(pattern, occupation):
            return True
        return False

    def check_degree(self, degree: str) -> bool:
        pattern = "Бакалавр|Кандидат наук|Специалист|Магистр|Доктор наук|"
        if re.match(pattern, degree):
            return True
        return False

    def check_worldview(self, worldview: str) -> bool:
        pattern = "^.+(?:изм|анство)$"
        if re.match(pattern, worldview):
            return True
        return False


def summary(result: List[List[str]], filename: str = ''):
    all_errors_count = 0
    errors_count = {
        "email": 0,
        "height": 0,
        "snils": 0,
        "passport_series": 0,
        "occupation": 0,
        "age": 0,
        "academic_degree": 0,
        "worldview": 0,
        "address": 0,
    }
    for i in result:
        all_errors_count += 1
        for j in i:
            errors_count[j] += 1

    if filename == '':
        print('\n Ошибок в файле %d\n' % all_errors_count)
        print('Ошибки по типам: ')
        for key in errors_count.keys():
            print(key, errors_count[key], sep=' ')

    else:
        with open(filename, 'w') as file:
            file.write('Ошибок в файле  %d\n' % all_errors_count)
            for key in errors_count.keys():
                file.write(key + '\t' + str(errors_count[key]) + '\n')

def save_in_json(data: List[Information], filename: str):

    f = open(filename, 'w')
    count = 0
    for i in data:
        f.write("Запись № %s\n" % str(count+1))
        f.write(f'''
                 {{
                   "email": "{i.email}",
                   "height": {i.height},
                   "snils": "{i.snils}",
                   "passport_series": "{i.passport_series}",
                   "occupation": "{i.occupation}",
                   "age": {i.age},
                   "academic_degree": "{i.academic_degree}",
                   "worldview": "{i.worldview}",
                   "address": "{i.address}",
                 }},''')
        f.write('\n')
        count += 1
    f.close()


if len(sys.argv) != 1:
    parser = argparse.ArgumentParser(description='Make users\' valid information.')
    parser.add_argument('-input_file', nargs=1, type=str, help='input file name')
    parser.add_argument('-output_file', nargs=1, type=str, help='output file name')
    args = parser.parse_args()

    input_file = args.input_file[0]
    output_file = args.output_file[0]
else:
    input_file = '19.txt'
    output_file = 'result.txt'


validator = Validator([])

with tqdm(range(100), colour='green', ncols=100) as progressbar:
    data = json.load(open(input_file, encoding='windows-1251'))
    progressbar.update(20)
    validator = Validator(data)
    progressbar.update(30)
    res = validator.parse()
    progressbar.update(50)
    summary(res[0], output_file)
    save_in_json(res[1], 'correct_data.txt')




































