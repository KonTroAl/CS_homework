# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

val_1 = b'class'
val_2 = b'function'
val_3 = b'method'

print(type(val_1), val_1, len(val_1))
print(type(val_2), val_2, len(val_2))
print(type(val_3), val_3, len(val_3))