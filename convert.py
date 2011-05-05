import codecs
from numpy import log10

## Fuel
fuelfile = "fuel.txt"
fuelObj = open(fuelfile, "r")
fuel = {}
for line in fuelObj.readlines():
    country, price = line.strip().split(',')
    fuel[country] = float(price)

filename = "input.txt"
# Needs "replace", without that it chockes on certain chracters
fileObj = codecs.open(filename, "r", "utf-8", "replace")

database = {}
fields = {"Gross domestic product per capita, current prices": "GDP",
          "Implied PPP conversion rate": "PPP",
          "Value of oil imports" : "Oilin",
          "Value of oil exports" : "Oilout",
          }

nameexchange = {"TWN": "Taiwan",
                "CIV": "Ivory Coast",
                "STP": "Sao Tome and Principe",
                }

for line in fileObj.readlines():
    data = line.strip().split("\t")
    if (len(data) < 6) or (data[0] == "ISO"):
        continue
    ccode = data[0]
    if ccode not in database:

        if ccode in nameexchange:
            name = nameexchange[ccode]
        else:
            name = data[1]

        database[ccode] = {'Name' :name}
        for field in fields:
            database[ccode][fields[field]] = -1
 
    for field in fields:
        if data[2] == field:
            try:
                # Fix borked decimalization, e.g. 12,345.67
                value = data[5].replace(",", "")
                database[ccode][fields[field]] = float(value)
            except:
                pass
            break

## Sort by fuel price
name2iso = dict([(database[ccode]['Name'], ccode) for ccode in database.keys()])
def fuelval(ccode):
    return fuel[ccode] if (ccode in fuel) else -1
fuelsort = sorted(name2iso.keys(), key=lambda x:fuelval(x))
i = 1
fuelrank = {}
for country in fuelsort:
    if fuelval(country) < 0:
        fuelrank[country] = -1
    else:
        fuelrank[country] = i
        i += 1

fields = ['GDP', 'PPP', 'Oilout', 'Oilin']
## Save
headerfields = ['ISO', 'Countryname'] + fields + ['Fuelprice'] + ['Fuelrank']
print(",".join(headerfields))
for ccode in sorted(database.keys()):
    country = database[ccode]['Name']
    if country in fuel:
        price = fuel[country]
        del(fuel[country])
    else:
        # print("Missing fuel: "+country)
        price = -1

    data = [ccode] + [country] + ["%g" % database[ccode][field] for field in fields] + ["%.1f" % price] + ["%d" %fuelrank[country]]
    print(",".join(data))
