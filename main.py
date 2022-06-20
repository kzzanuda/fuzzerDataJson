import json
import requests
import re

url = "#"
cookies = {"sid ": "#"}
headers = {"#""}
json={"data": {"isHidden": "true", "productId": "123"}, "meta": {"channel": "mobile"}}



# Тут пихаем словарь, !Надо переписать на открытие файла *.txt!
#first_re = requests.post(url,cookies=cookies,headers=headers,json=json1)
#print(first_re.request,first_re.text )
with open("sqli.txt","r",encoding="UTF-8") as file:
    wordlist = file.read().splitlines()



# some JSON:
#x = '{"data": {"patronymicIsVisible": False}, "meta": {"channel": "mobile"}}'
# parse x:
# y = json.loads(x)


# Основная функция с рекурсией
def replace_word(ls, new_word, parent_json):
    for i in ls:
        if isinstance(ls[i], dict):  # Если словарь, то углубляемся
            #print('i am dict', i) # - Отладка
            replace_word(ls[i], new_word, parent_json)
        elif isinstance(ls[i], list):  # Если лист, то там числовые индексы, углубление просто в сам элемент j
            #print('i am list', i) # - Отладка
            for j in ls[i]: # Для всех элементов листа надо еще цикл
                replace_word(j, new_word, parent_json)
        else:
            #print('im not dict --', i, '-- and value:', ls[i], 'and type', type(ls[i])) # - Отладка
            old_w = ls[i] # Временная переменая, чтобы потом вернуть замененное значение
            ls[i] = new_word # Замена "найденного" в глубине значения
            d = json.dumps(parent_json) # "Парсим"
            try:
                r = requests.post(url, headers=headers, cookies=cookies, json=d,timeout=10)
                print('успех')
                print(r.text)
                text_response = r.text
                status_code_response = r.status_code
                #print(type(status_code_response))
                ls[i] = old_w  # Возвращаем прежднее значение
                r_body = str(r.request.body.decode("UTF-8"))
                r_body = r_body.replace('"\"','')
                if (re.search(r"Sql injection detected",str(text_response)) == None) or \
                        (re.search(r'["status":"error"]',str(text_response)) == None and status_code_response == 200):
                    print(status_code_response,text_response)
                    with open("results.txt", "a",encoding="UTF-8") as report:
                        report.write(" Тело запроса: " +'\n\n' + url +'\n' + str(cookies) +'\n' + str(headers) +'\n' + str(r_body.replace('"\"','')) +'\n\n' + " ОТВЕТ: " + '\n\n' + str(r.status_code) +'\n\n' + str(text_response) +'\n\n')

            except requests.exceptions.RequestException as e:
                print(e)
                print('неудача')
             # - ВОТ ТУТ ПИХАЕМ САМ ЗАПРОС, т.е. d пихаем в 'data' в requests, к примеру

# Вызов цикла по нашему словарю:
for i in wordlist:
    replace_word(json, i, json)


#requests.post(url, headers=headers, cookies=cookies, json=d)
