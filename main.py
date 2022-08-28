from data.utils import load_data, process_data
from fastapi import FastAPI

app = FastAPI()

# load data
races_data_list = load_data(url='http://ergast.com/api/f1/races.json')

# process data
df_races = process_data(races_data_list, table = 'RaceTable', details = 'Races')
races_per_season = df_races.groupby('season')['round'].nunique().to_dict()

@app.get("/")
def root():
    '''
    Show welcome message.
    '''
    return {"message": "Go to endpoint '/example' to see an example JSON output."}

@app.get("/example")
def get_example():
    '''
    Show example output.
    '''
    return races_per_season
    