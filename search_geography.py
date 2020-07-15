from pprint import pprint

from tabulate import tabulate

import population


def search_state(data, s):
        r = {}
    p_data = population.search(s, False)

    if p_data == None:
        print("No match for that geography.")
        return
    else:
        pprint(p_data)
    header = ['Date', 'Cases', 'Deaths']
    c_data = []
    prior_c = 0
    prior_d = 0
    row_count = 0
    for line in data:
        row_count += 1
        include = False
        row = line.strip().split(',')
        if len(row) == 5:
            if row[2] == p_data['STATE']:
                include = True
            if include:
                delta = int(row[3]) - prior_c
                delta_d = int(row[4]) - prior_d
                if prior_c > 0:
                    delta_p = float("{:.2f}".format((delta / prior_c) * 100))
                else:
                    delta_p = '-'
                    
                if prior_d > 0:
                    delta_dp = float("{:.4f}".format((delta_d / prior_d) * 100))
                else:
                    delta_dp = '-'
                    
                if delta > -1:
                    c_data.append([row[0], row[3], delta, delta_p, row[4], delta_d, delta_dp])
                prior_c = int(row[3])
                prior_d = int(row[4])

    #print("Row Count: ", row_count)
    if c_data == []:
        print("No case data for that geography.")
        return
    perc_infected = float("{:.4f}".format(int(c_data[-1][1]) / int(p_data['POPESTIMATE2019']) * 100))
    mortality_rate = float("{:.4f}".format(int(c_data[-1][4]) / int(p_data['POPESTIMATE2019']) * 100))
    case_mortality = float("{:.2f}".format(int(c_data[-1][4]) / int(c_data[-1][1]) * 100))
    #print("Case Rate: ", perc_infected, '%')
    r['case_rate'] = perc_infected
    #print("Mortality (vs. total population): ", mortality_rate, '%')
    r['total_population_mortality_rate'] = mortality_rate
    #print("Case Mortality %: ", case_mortality, '%')
    r['case_mortality_rate'] = case_mortality
    #print("2019 Average deaths/day: ", int(p_data['DEATHS2019']) / 365)
    r['deaths_2019'] = p_data['DEATHS2019']
    #print( "Last 7 day case increase  (%):", float("{:.2f}".format(((int(c_data[-1][1]) - int(c_data[-7][1]))/ int(c_data[-1][1])) * 100 )) )
    r['case_increase_rate_prior_7_days'] = float("{:.2f}".format(((int(c_data[-1][1]) - int(c_data[-7][1]))/ int(c_data[-7][1])) * 100 ))
    if int(c_data[-1][4]) > 0:
        #print( "Last 7 day death increase (%):", float("{:.2f}".format(((int(c_data[-1][4]) - int(c_data[-7][4]))/ int(c_data[-1][4])) * 100 )) )
        r['death_increase_rate_prior_7_days'] = float("{:.2f}".format(((int(c_data[-1][4]) - int(c_data[-7][4]))/ int(c_data[-7][4])) * 100 ))
    else:
        r['death_increase_rate_prior_7_days'] = 0
    #print(tabulate(c_data, headers=['Date', 'Cases', 'Delta', '% Inc', 'Deaths', 'Delta', '% Inc']))
    r['chronological_data'] = c_data
    r['chronological_data_table'] = tabulate(c_data, headers=['Date', 'Cases', 'Delta', '% Inc', 'Deaths', 'Delta', '% Inc'])
    r['demographic_data'] = p_data
    r['state'] = s
    r['county'] = c
    r['FIPS'] = p_data['composite_fips']
    
    return r


def search_county(data, s, c=False):
    r = {}
    if c == '':
        c = False
    p_data = population.search(s, c)

    if p_data == None:
        print("No match for that geography.")
        return
    else:
        pprint(p_data)
    header = ['Date', 'Cases', 'Deaths']
    c_data = []
    prior_c = 0
    prior_d = 0
    row_count = 0
    for line in data:
        row_count += 1
        include = False
        row = line.strip().split(',')
        if len(row) == 6:
            if c is not False:
                if c.lower() == "new york city":
                    if row[1] == 'New York City':
                        include = True
            if row[3] == p_data['composite_fips']:
                include = True
            if include:
                delta = int(row[4]) - prior_c
                delta_d = int(row[5]) - prior_d
                if prior_c > 0:
                    delta_p = float("{:.2f}".format((delta / prior_c) * 100))
                else:
                    delta_p = '-'
                    
                if prior_d > 0:
                    delta_dp = float("{:.4f}".format((delta_d / prior_d) * 100))
                else:
                    delta_dp = '-'
                    
                if delta > -1:
                    c_data.append([row[0], row[4], delta, delta_p, row[5], delta_d, delta_dp])
                prior_c = int(row[4])
                prior_d = int(row[5])
    #print("Row Count: ", row_count)
    if c_data == []:
        print("No case data for that geography.")
        return
    perc_infected = float("{:.4f}".format(int(c_data[-1][1]) / int(p_data['POPESTIMATE2019']) * 100))
    mortality_rate = float("{:.4f}".format(int(c_data[-1][4]) / int(p_data['POPESTIMATE2019']) * 100))
    case_mortality = float("{:.2f}".format(int(c_data[-1][4]) / int(c_data[-1][1]) * 100))
    #print("Case Rate: ", perc_infected, '%')
    r['case_rate'] = perc_infected
    #print("Mortality (vs. total population): ", mortality_rate, '%')
    r['total_population_mortality_rate'] = mortality_rate
    #print("Case Mortality %: ", case_mortality, '%')
    r['case_mortality_rate'] = case_mortality
    #print("2019 Average deaths/day: ", int(p_data['DEATHS2019']) / 365)
    r['deaths_2019'] = p_data['DEATHS2019']
    #print( "Last 7 day case increase  (%):", float("{:.2f}".format(((int(c_data[-1][1]) - int(c_data[-7][1]))/ int(c_data[-1][1])) * 100 )) )
    r['case_increase_rate_prior_7_days'] = float("{:.2f}".format(((int(c_data[-1][1]) - int(c_data[-7][1]))/ int(c_data[-1][1])) * 100 ))
    if int(c_data[-1][4]) > 0:
        #print( "Last 7 day death increase (%):", float("{:.2f}".format(((int(c_data[-1][4]) - int(c_data[-7][4]))/ int(c_data[-1][4])) * 100 )) )
        r['death_increase_rate_prior_7_days'] = float("{:.2f}".format(((int(c_data[-1][4]) - int(c_data[-7][4]))/ int(c_data[-1][4])) * 100 ))
    else:
        r['death_increase_rate_prior_7_days'] = 0
    #print(tabulate(c_data, headers=['Date', 'Cases', 'Delta', '% Inc', 'Deaths', 'Delta', '% Inc']))
    r['chronological_data'] = c_data
    r['chronological_data_table'] = tabulate(c_data, headers=['Date', 'Cases', 'Delta', '% Inc', 'Deaths', 'Delta', '% Inc'])
    r['demographic_data'] = p_data
    r['state'] = s
    r['county'] = c
    r['FIPS'] = p_data['composite_fips']
    
    return r