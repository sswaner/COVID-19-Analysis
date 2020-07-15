import csv

from pprint import pprint


def county_population(county_list):
    count = 0
    f = open("./data/CO-EST2019-alldata.csv")
    results = []
    for line in f:
        parts = line.strip().split(',')
        if (parts[3], parts[4]) in county_list:
            data = {'SUMLEV': parts[0], 'REGION': parts[1], 'state_FIPS': parts[3], 'county_FIPS': parts[4],
                    'population_2019': parts[18], 'state_name': parts[5], 'county_name': parts[6]}
            results.append(data)
    return results


def trim_data(data, list):
    results = {}
    for k in list:
        results[k] = data[k]
    return results


def search(state_name, county_name=False):
    #print('--------------')
    #print(county_name)
    #print('--------------')
    if county_name is not False:
        if str(county_name).lower() == "new york city":
            return {'COUNTY': '153', 'CTYNAME': 'New York City (5 counties)',
                    'DEATHS2019': '62061',
                    'POPESTIMATE2019': '8336817',
                    'RDEATH2019': '7.6653',
                    'REGION': '?',
                    'STATE': '36',
                    'STNAME': 'New York',
                    'SUMLEV': '061',
                    'composite_fips': '36061'}
    key_list = ['SUMLEV', 'REGION', 'STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'POPESTIMATE2019', 'DEATHS2019', 'RDEATH2019', 'composite_fips']
    with open('./data/CO-EST2019-alldata.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            composite_fips = row['STATE'] + row['COUNTY']
            row['composite_fips'] = composite_fips
            if county_name == False:
                sumlev = '040'
                if row['STNAME'].lower() == state_name.lower() and row['SUMLEV'] == sumlev:
                    return trim_data(row, key_list)
            else:
                sumlev = '050'
                if row['STNAME'].lower() == state_name.lower() and row['CTYNAME'].replace(' County', '').lower() == county_name.lower() and row['SUMLEV'] == sumlev:
                    return trim_data(row, key_list)


if __name__ == "__main__":
    #pprint(county_population([('19', '049'), ('19', '003')]))
    pprint(search('new york', 'westchester'))
