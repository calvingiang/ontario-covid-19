import requests
import pandas


def get_ontario_data():
    base_url = 'https://data.ontario.ca'
    record_length = 1
    record_num = 0
    covid_df = pandas.DataFrame()

    while record_length > 0:
        path_url = '/api/3/action/datastore_search?offset={}00&resource_id=455fd63b-603d-4608-8216-7d8647f43350'
        url = base_url + path_url.format(str(record_num))
        covid_request = requests.get(url)
        records = covid_request.json()['result']['records']
        new_df = pandas.DataFrame(records)
        covid_df = pandas.concat([covid_df, new_df])
        record_length = len(records)
        record_num=record_num+1

    return covid_df


def get_ontario_cases():
    base_url = 'https://data.ontario.ca'
    record_length = 1
    record_num = 0
    covid_df = pandas.DataFrame()

    while record_length > 0:
        path_url = '/api/3/action/datastore_search?offset={}00&resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11'
        url = base_url + path_url.format(str(record_num))
        covid_request = requests.get(url)
        records = covid_request.json()['result']['records']
        new_df = pandas.DataFrame(records)
        covid_df = pandas.concat([covid_df, new_df])
        record_length = len(records)
        record_num=record_num+1
    return covid_df


def get_cases_only():
    covid_cases = get_ontario_cases()
    cases_df = covid_cases[['Reported Date','Total Cases']].fillna(0).reset_index().drop(columns=['index'])
    previous_cases = cases_df
    previous_cases = previous_cases.shift(periods=1).fillna(0).drop(columns=['Reported Date']).rename(columns={'Total Cases':'Yesterday Cases'})
    cases_df = pandas.merge(cases_df, previous_cases, left_index=True, right_index=True)
    cases_df['New Cases'] = cases_df['Total Cases'] - cases_df['Yesterday Cases']
    cases_df = cases_df[['Reported Date', 'Total Cases', 'New Cases']]
    cases_df['Reported Date'] = cases_df['Reported Date'].apply(time_format)
    return cases_df


def time_format(body):
    #return datetime.strptime(body, '%Y-%m-%d')
    return body.replace('T00:00:00','')

def get_all_ontario_data():
    df = get_ontario_data()
    df.to_csv('./src/ontario.csv')

#et_all_ontario_data()
