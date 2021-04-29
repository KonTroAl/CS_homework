# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.

val_1 = 'разработка'
val_2 = 'сокет'
val_3 = 'декоратор'

print(val_1, type(val_1))
print(val_2, type(val_2))
print(val_3, type(val_3))

val_1_unicode = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
val_2_unicode = b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'
val_3_unicode = b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'

print(val_1_unicode, type(val_1_unicode))
print(val_2_unicode, type(val_2_unicode))
print(val_3_unicode, type(val_3_unicode))
