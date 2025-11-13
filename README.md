# Assignment7

# COVID-19 State Deaths CSV Processor

This Python script reads a CSV file containing daily COVID-19 data for U.S. states, extracts the **`state`** and **`deathConfirmed`** columns, and outputs two CSV files:

1. **`per_state_totals.csv`** – The final cumulative deaths for each state.  
2. **`all_states_cumulative.csv`** – Daily cumulative deaths for each state.

## Features

- Pure Python CSV parsing (no external libraries).  
- Handles quoted fields and commas inside quotes.  
- Safely converts strings to integers.  
- Computes both **final totals** and **running cumulative totals**.

## Usage

1. Place your CSV file in a known location.  
2. Update the `file_path` variable in the script with the path to your CSV file:

```python
file_path = 'C:/path/to/us_states_covid19_daily.csv'
```
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
