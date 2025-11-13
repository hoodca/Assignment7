# ------------------ CSV parsing ------------------

def parse_csv_line(line):
    """Parse a single CSV line into a list of fields (handles quoted commas)."""
    fields = []
    field = []
    i, in_quotes = 0, False
    
    while i < len(line):
        c = line[i]
        
        if c == '"':
            # Handle double quotes inside quoted fields
            if i + 1 < len(line) and line[i+1] == '"':
                field.append('"')
                i += 2
            else:
                in_quotes = not in_quotes
                i += 1
        elif c == ',' and not in_quotes:
            # Field separator outside quotes
            fields.append(''.join(field))
            field = []
            i += 1
        else:
            field.append(c)
            i += 1
    
    fields.append(''.join(field))
    return fields


def read_csv(file_path):
    """Read CSV file into a list of rows, each row is a list of strings."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [parse_csv_line(line.rstrip("\n\r")) for line in f if line.strip()]


# ------------------ Column extraction ------------------

def extract_columns(data, names):
    """
    Extract columns by name from CSV data.
    Returns a dictionary: {column_name: [values...]}.
    """
    if not data:
        return {n: [] for n in names}
    
    headers = data[0]
    result = {}
    
    for name in names:
        if name not in headers:
            raise KeyError(f"Column '{name}' not found in headers: {headers}")
        idx = headers.index(name)
        # Extract the column values for all rows (skip header)
        result[name] = [row[idx] if idx < len(row) else '' for row in data[1:]]
    
    return result


# ------------------ Utility functions ------------------

def _safe_to_int(s):
    """Convert string to int safely; returns 0 for empty, invalid, or None values."""
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return 0


# ------------------ Cumulative totals ------------------

def final_cumulative_deaths_by_state(states, deaths):
    """
    Get the final cumulative deathConfirmed for each state.
    Overwrites previous value for each state → last row wins.
    """
    totals = {}
    for st, d in zip(states, deaths):
        key = (st or "").strip()
        if not key:
            continue
        totals[key] = _safe_to_int(d)
    return totals


# ------------------ Running cumulative for each state ------------------

def running_cumulative_by_state(states, deaths):
    """
    Collect cumulative deathConfirmed values for each state day by day.
    Returns a dict: {state: [daily cumulative values]}.
    """
    out = {}
    for st, d in zip(states, deaths):
        key = (st or "").strip()
        if not key:
            continue
        out.setdefault(key, []).append(_safe_to_int(d))
    return out


# ------------------ CSV writing ------------------

def save_totals_csv(totals, out_path="per_state_totals.csv"):
    """Write final cumulative totals to CSV."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("state,total_deaths\n")
        for state in sorted(totals):
            f.write(f"{state.replace(',', ' ')},{totals[state]}\n")


def write_all_cumulative_one_csv(cumul_dict, out_path="all_states_cumulative.csv"):
    """Write all cumulative daily totals per state to CSV."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("state,day,total_deaths\n")
        for state in sorted(cumul_dict):
            for day, total in enumerate(cumul_dict[state], 1):
                f.write(f"{state},{day},{total}\n")


# ------------------ Main execution ------------------

if __name__ == "__main__":
    # Path to the input CSV file
    file_path = 'C:/Users/hoodca/downloads/archive/us_states_covid19_daily.csv'

    # Read CSV data
    data = read_csv(file_path)

    # Extract relevant columns
    try:
        cols = extract_columns(data, ['state', 'deathConfirmed'])
    except KeyError as e:
        print("Header error:", e)
        exit(1)

    states = cols['state']
    deaths = cols['deathConfirmed']

    # Compute final totals per state and save CSV
    totals = final_cumulative_deaths_by_state(states, deaths)
    save_totals_csv(totals)

    # Compute running cumulative totals per state and save CSV
    cumulative = running_cumulative_by_state(states, deaths)
    write_all_cumulative_one_csv(cumulative)

    print("Done! per_state_totals.csv and all_states_cumulative.csv written.")
