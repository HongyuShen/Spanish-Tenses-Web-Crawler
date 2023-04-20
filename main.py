import csv

import requests as requests
from bs4 import BeautifulSoup

import pandas as pd
import xlsxwriter

reader = csv.DictReader(open('Verb List.csv', newline='', encoding='utf-8'))

word_count = 0

verb_list = None
data_frame = None

headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})

def search_all_verbs():
    global word_count

    global verb_list
    global data_frame

    verb_list = []

    for row in reader:
        find_all_tenses_for_one_verb(row['Español'])
        word_count += 1

        # if word_count > 2:
        #     break

    print(word_count)

    data_frame = pd.DataFrame(verb_list, columns=['0'] * 84)

    writer = pd.ExcelWriter('Tiempos En Español.xlsx', engine='xlsxwriter')
    data_frame.to_excel(writer, sheet_name='Tiempos En Español', index=False)

    writer._save()


def find_all_tenses_for_one_verb(verb):
    url = "https://conjugator.reverso.net/conjugation-spanish-verb-" + verb + ".html"

    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

    termination_index = 0

    global word_count

    global verb_list

    print_all_verbs = False

    current_verb_list = []

    for div_element in soup.find_all("div", {"class": "blue-box-wrap"}):
        termination_index += 1

        item_count = 0

        long_version = False
        masculine = ""

        if termination_index > 7:
            break

        for tense_item in div_element.find_all("li"):
            content = ""

            for tense_subElement in tense_item.find_all():
                tense_item_string = str(tense_subElement.text)

                if item_count == 0 and tense_item_string == "me ":
                    tense_item_string = "yo "
                elif item_count == 1 and tense_item_string == "te ":
                    tense_item_string = "tú "
                elif item_count == 2 and tense_item_string == "se ":
                    tense_item_string = "él/ella/Ud. "
                elif item_count == 3 and tense_item_string == "nos ":
                    tense_item_string = "nosotros "
                elif item_count == 4 and tense_item_string == "os ":
                    tense_item_string = "vosotros "
                elif item_count == 5 and tense_item_string == "se ":
                    tense_item_string = "ellos/ellas/Uds. "

                content += tense_item_string

            item_count += 1

            # print(content)

            current_verb_list.append(content)
            current_verb_list.append(",")

            # if print_all_verbs:
            #     print(content)

    verb_list.append(current_verb_list)


search_all_verbs()