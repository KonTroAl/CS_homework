# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.

val_1 = 'разработка'
val_2 = 'сокет'
val_3 = 'декоратор'

print(val_1, type(val_1))
print(val_2, type(val_2))
print(val_3, type(val_3))

val_1_unicode = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
val_2_unicode = '\u0441\u043e\u043a\u0435\u0442'
val_3_unicode = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

print(val_1_unicode, type(val_1_unicode))
print(val_2_unicode, type(val_2_unicode))
print(val_3_unicode, type(val_3_unicode))
