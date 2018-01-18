# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

f = open('D:\\python\\myfiles\\black charts\\pre_rank.txt','r')
data = f.readlines()
data = data[:6]
f.close()

sta = []
pre = []
for i in data:
    sta.append(i.split()[1])
    pre.append(float(i.split()[0]))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(range(1,len(data)+1), pre, color='darkcyan', edgecolor='none', hatch='//')

ax.set_xticks(range(len(data)))
ax.set_xticklabels(sta)

plt.show()