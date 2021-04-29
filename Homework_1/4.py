# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
# в байтовое и выполнить обратное преобразование (используя методы encode и decode).

val_1 = 'разработка'
val_2 = 'администрирование'
val_3 = 'protocol'
val_4 = 'standard'

val_1_bytes = val_1.encode('utf-8')
val_2_bytes = val_2.encode('utf-8')
val_3_bytes = val_3.encode('utf-8')
val_4_bytes = val_4.encode('utf-8')
print(val_1_bytes)
print(val_2_bytes)
print(val_3_bytes)
print(val_4_bytes)

val_1_original = val_1_bytes.decode('utf-8')
val_2_original = val_2_bytes.decode('utf-8')
val_3_original = val_3_bytes.decode('utf-8')
val_4_original = val_4_bytes.decode('utf-8')
print(val_1_original)
print(val_2_original)
print(val_3_original)
print(val_4_original)