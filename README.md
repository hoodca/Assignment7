# Assignment7

Usage

Place the CSV file in a known location.

Update the file_path variable in the script with your CSV file path:

file_path = 'C:/path/to/us_states_covid19_daily.csv'


Run the script:

python covid_state_deaths.py


Outputs are written in the same directory (or the path specified in the script):

per_state_totals.csv

all_states_cumulative.csv

CSV Output Formats

per_state_totals.csv

state,total_deaths
AL,389493
AK,9258
...


all_states_cumulative.csv

state,day,total_deaths
AL,1,10
AL,2,15
...

Notes

The script overwrites previous totals; the last value in the dataset is considered the final cumulative total for each state.

Designed for CSVs with headers state and deathConfirmed. Missing columns will raise an error.
