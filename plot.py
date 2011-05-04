import numpy as np
import pylab as pl
from matplotlib.transforms import offset_copy

filename = "data.csv"
types = {'names' : ['code', 'name', 'gdp', 'ppp', 'oilout', 'oilin', 'price'],
         'formats' : ['S30', 'S30', 'f4', 'f4', 'f4', 'f4', 'f4']
         }
data = np.loadtxt(filename, delimiter=",", dtype=types)

fig = pl.figure(figsize=(10,10))
ax = pl.subplot(1,1,1)
transOffset = offset_copy(ax.transData, fig=fig,
                          x = 0.05, y=0.10, units='inches')


# for i in xrange(len(data['code'])):
#     if data['price'][i] <= 0 or data['gdp'][i] <= 0:
#         continue

#     if data['oilout'][i] > data['oilin'][i]:
#         fuel = False
#     else:
#         fuel = True

#     symbol = "kx" if fuel else 'ko'
#     pl.plot(np.log(data['gdp'][i]), data['price'][i], symbol)
#     # pl.text(data[i,0], data[i,4], '%.1f' % (fuel), transform=transOffset)
#     pl.text(np.log(data['gdp'][i]), data['price'][i], data['name'][i], transform=transOffset)

total = []
for i in xrange(len(data['code'])):
    if data['price'][i] > 0:
        total += [(data['code'][i], data['price'][i])]

total2 = sorted(total, key= lambda x: x[1])
for j, v in enumerate(total2):
    pl.plot(j, v[1])
    pl.text(j, v[1], v[0], transform=transOffset)
pl.show()
