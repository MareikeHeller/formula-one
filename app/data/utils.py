import time
import requests
import json
import pandas as pd
import math

#from IPython.display import clear_output


def load_data(url, test = False):
    '''
    Load data from Ergast API. Iterate through API calls with a defined limit of 30 results per call.
    Append responses from separate calls to list.
    
    Input arguments:
    url - (string) Url to API endpoint.
    test - (boolean) If true, only 1 API call is initiated. For testing purposes.
    
    Output:
    responses - (list) List of responses of all API calls. List elements are dictionaries.
    
    '''
    # define url

    # initialize list of dataframes
    responses = []

    # set initial call counter and offset, limit and total number of results
    counter = 0
    offset = 0
    limit = 30
    
    # do a test call, if test == True
    if test == True:
        total = 30
    else:
        total = int(json.loads(requests.get(url).text)['MRData']['total'])

    while offset < total:
        # call API
        r = requests.get(url + '?limit={}&offset={}'.format(limit, offset))

        # append dataframes to list
        responses.append(r.json())

        # increment call counter and offset
        counter += 1
        offset += limit
        # feedback
        if test == True:
            print('Test load, 1 call.')
        else:
            print('Call {} from {}, sleep now.'.format(counter, math.ceil(total/limit)))
            time.sleep(0.5)
            print('Continue...')
            #clear_output(wait = True)

    print('Data successfully loaded from url {}.'.format(url))
    
    return responses


def process_data(data_list, table, details):
    '''
    Process data list of dictionaries to store them in a pandas dataframe.
    
    Input arguments:
    data_list - (list) List elements are dictionaries.
    table - (string) Table of interest in dictionary above.
    details - (string) Details of interest in table above.
    
    Output:
    df - (dataframe) Merged dataframe of all dictionaries based on relevant table and details.
    '''
    frames = [pd.DataFrame(pd.json_normalize(data_list[r]['MRData'][table][details])) for r in range(0,len(data_list))]
    df = pd.concat(frames).reset_index(drop=True)
    
    print('Processed data list into dataframe based on table "{}" and details "{}".'.format(table, details))
    return df