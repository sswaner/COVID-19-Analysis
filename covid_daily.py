import pandas as pd
#import arrow

def fips_glue(row):
    x = int(str(row['STATE']) + str(row['COUNTY']).zfill(3))
    return x

def pop_mortality(row):
    x = float("{:.4f}".format(row['Deaths'] / row['POPESTIMATE2019']* 100)) 
    return x

def case_mortality(row):
    if row['Confirmed'] == 0:
        return 0
    x = float("{:.4f}".format(row['Deaths'] / row['Confirmed']* 100)) 
    return x

def pop_confirmed(row):
    x = float("{:.4f}".format(row['Confirmed'] / row['POPESTIMATE2019']* 100)) 
    return x

def x_in_y(row):
    if row['Confirmed'] == 0:
        return 0
    x = int(row['POPESTIMATE2019'] / row['Confirmed'])
    return x

def case_per_1k(row):
    if row['Confirmed'] == 0:
        return 0
    x = float("{:.2f}".format(row['Confirmed'] / (row['POPESTIMATE2019'] / 1000)))
    return x 

def death_per_1k(row):
    if row['Confirmed'] == 0:
        return 0
    x = float("{:.2f}".format(row['Deaths'] / (row['POPESTIMATE2019'] / 1000)))
    return x 

def covid_daily_report(d):
    cvd_data = pd.read_csv("../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/{0}.csv".format(d))
    cvd_df = pd.DataFrame(cvd_data, columns = ['FIPS', 'Admin2', 'Province_State', 'Confirmed', 'Deaths'])


    dem_data = pd.read_csv("./data/CO-EST2019-alldata.csv")
    dem_df = pd.DataFrame(dem_data, columns = [ 'STATE', 'COUNTY', 'POPESTIMATE2019','DEATHS2019'])
    dem_df['FIPS'] = dem_df.apply(fips_glue, axis = 1)

    df3 = pd.merge(dem_df,cvd_df, on='FIPS')

    df3['TPOP_MORTALITY'] = df3.apply(pop_mortality, axis = 1)
    df3['CASE_MORTALITY'] = df3.apply(case_mortality, axis = 1)
    df3['TPOP_CONFIRMED'] = df3.apply(pop_confirmed, axis = 1)
    df3['Cases_per_1k'] = df3.apply(case_per_1k, axis = 1)
    #df3['one_in_x'] = df3.apply(x_in_y, axis = 1) # The 1 in x people confirmed.  i.e. 1% of total pop confirmed would by 100. 
    df3['Deaths_per_1k'] = df3.apply(death_per_1k, axis = 1)
    return df3