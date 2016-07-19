import sys
import json

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from pprint import pprint

FIELD = 'brand'

brands = {}
for item in json.loads(open(sys.argv[1]).read()):
    if item[FIELD] == 'TOP':
        continue

    if item[FIELD] not in brands:
        brands[item[FIELD]] = {}
    try:
        if int(item['year']) < 2006:
            continue

        if 'km' not in brands[item[FIELD]]:
            brands[item[FIELD]]['km'] = []

        brands[item[FIELD]]['km'].append(int(item['kilometers']))

        if 'price' not in brands[item[FIELD]]:
            brands[item[FIELD]]['price'] = []

        brands[item[FIELD]]['price'].append(int(item['price']))

        if 'year' not in brands[item[FIELD]]:
            brands[item[FIELD]]['year'] = []

        brands[item[FIELD]]['year'].append(int(item['year']))

    except:
        continue

# pprint(brands)
result = {}
for brand in brands:
    if len(brands[brand]) == 0:
        continue

    if len(brands[brand]['price']) == 0:
        continue

    if len(brands[brand]['year']) == 0:
        continue

    if len(brands[brand]['km']) == 0:
        continue

    result[brand] = {
        'price': sum(brands[brand]['price']) / len(brands[brand]['price']),
        'km': sum(brands[brand]['km']) / len(brands[brand]['km']),
        'year': int(sum(brands[brand]['year']) / len(brands[brand]['year'])),
    }


total = {}
for brand in result:
    total[brand] = result[brand]['km'] / (2017 - result[brand]['year'])

for brand in sorted(total, key=total.get):
    print(brand, total[brand])

result = []
for idx, brand in enumerate(brands):
    if len(brands[brand]) == 0:
        continue

    if len(brands[brand]['price']) == 0:
        continue

    if len(brands[brand]['year']) == 0:
        continue

    if len(brands[brand]['km']) == 0:
        continue

    years, prices = zip(*sorted(zip(brands[brand]['km'], brands[brand]['price']), key=lambda x: x[0]))
    years = list(years)
    prices = list(prices)

    if len(years) < 30:
        continue

    f = interp1d(years, prices)

    plt.title('{0} Graph'.format(brand))
    plt.xlabel('Year')
    plt.ylabel('Price (€)')
    plt.axhline(y=15000, linewidth=4, color='r')
    plt.plot(years, prices, 'o', years, f(years), '-')
    plt.legend(['target', 'data', 'linear'], loc='best')
    plt.savefig('{0}.png'.format(brand))
    plt.clf()

