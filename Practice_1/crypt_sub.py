from collections import Counter


f = open("D:\Programs\VScode\MOZI\Practice_1\enc.txt", "r")
string_in = f.read() 
string = ""
for l in string_in:
    if l.isalpha():
        l = l.upper()
        string += l
n = list(string)
b = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
list = []
for i in b:
    list.append(i)
d = Counter(n)
sorted_tuple = sorted(d.items(), key=lambda x: x[1])
d = dict(sorted_tuple)
l = len(string)
t = {}
for key, value in d.items():
    value = round(value * 100 / l, 2)
    value = str(value) + " %"
    t[key] = value
print("length of string (only letters) is: ", len(string))
print(t)
r = {}
for key, value in d.items():
    value = round(value * 100 / l, 2)
    r[key] = value
print(r)