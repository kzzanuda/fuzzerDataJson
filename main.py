import json

# Тут пихаем словарь, !Надо переписать на открытие файла *.txt!
wordlist = ["some", 'word', 'and', 'list']

# some JSON:
x = '{"data":{"inputs": [{"name": "ID1", "value": "1234"}, {"name": "ID2", "value": "check"}],' \
    '"stage": "confirm"},"meta": {"channel": "test"}} '
# parse x:
y = json.loads(x)


# Основная функция с рекурсией
def replace_word(ls, new_word):
    for i in ls:
        if isinstance(ls[i], dict):  # Если словарь, то углубляемся
            #print('i am dict', i) # - Отладка
            replace_word(ls[i], new_word)
        elif isinstance(ls[i], list):  # Если лист, то там числовые индексы, углубление просто в сам элемент j
            #print('i am list', i) # - Отладка
            for j in ls[i]: # Для всех элементов листа надо еще цикл
                replace_word(j, new_word)
        else:
            #print('im not dict --', i, '-- and value:', ls[i], 'and type', type(ls[i])) # - Отладка
            old_w = ls[i] # Временная переменая, чтобы потом вернуть замененное значение
            ls[i] = new_word # Замена "найденного" в глубине значения
            d = json.dumps(y) # "Парсим"
            print(d) # - ВОТ ТУТ ПИХАЕМ САМ ЗАПРОС, т.е. d пихаем в 'data' в requests, к примеру
            ls[i] = old_w # Возвращаем прежднее значение


# Вызов цикла по нашему словарю:
for i in wordlist:
    replace_word(y, i)
