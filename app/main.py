from data.utils import load_data, process_data
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# load data
races_data_list = load_data(url='http://ergast.com/api/f1/races.json')

# process data
df_races = process_data(races_data_list, table = 'RaceTable', details = 'Races')

@app.get("/")
def root():
    '''
    Show welcome message.
    '''
    return {"message": "Go to endpoint '/races-per-season' to see an example JSON output."}


@app.get("/races-per-season")
def get_races_per_season():
    '''
    Show example output.
    '''
    races_per_season = df_races.groupby('season')['round'].nunique().to_dict()
    return races_per_season
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)