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

# Throw away header
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
            database[ccode][fields[field]] = 0
 
    for field in fields:
        if data[2] == field:
            try:
                value = data[5].replace(",", "")
                database[ccode][fields[field]] = float(value)
            except:
                pass
            break

fields = ['GDP', 'PPP', 'Oilin', 'Oilout']
## Save
for ccode in sorted(database.keys()):
    country = database[ccode]['Name']
    if country in fuel:
        price = fuel[country]
        del(fuel[country])
    else:
        # print("Missing fuel: "+country)
        price = -1

    data = [ccode] + [country] + ["%g" % database[ccode][field] for field in fields] + ["%.1f" % price]
    print(",".join(data))

