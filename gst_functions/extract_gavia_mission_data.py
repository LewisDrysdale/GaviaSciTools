from pathlib import Path
import re
import numpy as np
import pandas as pd

# ---------- SETTINGS ----------
DATA_FOLDER = Path('.')
MISSION_MANAGER_FILE = DATA_FOLDER / 'missionmanager.csv'
INPUT_FILES = [
    DATA_FOLDER / 'autopilotdata.csv',
    DATA_FOLDER / 'auvdata.csv',
    DATA_FOLDER / 'GPSdata.csv',
    DATA_FOLDER / 'NAVdata.csv',
]
OUTPUT_FOLDER = DATA_FOLDER / 'mission_only'
CHUNK_SIZE = 200_000
MIN_MISSION_SECONDS = 0  # e.g. use 30 to remove very short aborted test starts
# ------------------------------


def mission_name_from_command(command):
    """Extract a readable mission name from 'Run missionplan: .../name.xml'."""
    if pd.isna(command):
        return None
    match = re.search(r'Run missionplan:\s*(.+)', str(command), flags=re.I)
    if not match:
        return None
    return Path(match.group(1).strip()).stem


def build_mission_intervals(mission_manager_file, min_duration_seconds=0):
    """
    Build mission intervals using explicit Gavia Mission Manager events.

    Start: Status == 'Mission begin'
    Stop:  Status == 'Mission end', or Command contains 'Mission aborted/halted'
    """
    mm = pd.read_csv(mission_manager_file)
    mm['timestamp'] = pd.to_numeric(mm['timestamp'], errors='coerce')
    mm = mm.dropna(subset=['timestamp']).sort_values('timestamp')

    intervals = []
    active = None
    pending_name = None

    for row in mm.itertuples(index=False):
        timestamp = float(row.timestamp)
        command = getattr(row, 'Command', None)
        status = getattr(row, 'Status', None)

        new_name = mission_name_from_command(command)
        if new_name:
            pending_name = new_name

        status_text = '' if pd.isna(status) else str(status).strip().lower()
        command_text = '' if pd.isna(command) else str(command).strip().lower()

        if status_text == 'mission begin':
            # Defensive handling if a new start appears before a stop event.
            if active is not None:
                active['end_timestamp'] = timestamp
                active['end_reason'] = 'next mission began'
                intervals.append(active)

            active = {
                'mission_name': pending_name or 'unknown_mission',
                'start_timestamp': timestamp,
                'start_time': getattr(row, 'time', None),
                'end_timestamp': np.nan,
                'end_reason': 'still active at end of log',
            }

        is_normal_end = status_text == 'mission end'
        is_forced_end = ('mission aborted' in command_text or
                         'mission halted' in command_text)

        if active is not None and (is_normal_end or is_forced_end):
            active['end_timestamp'] = timestamp
            active['end_reason'] = ('mission end' if is_normal_end
                                    else 'mission aborted/halted')
            intervals.append(active)
            active = None
            pending_name = None

    # Preserve an unclosed mission. It will be treated as continuing to file end.
    if active is not None:
        intervals.append(active)

    result = pd.DataFrame(intervals)
    if result.empty:
        raise ValueError('No mission intervals were found in missionmanager.csv')

    result['duration_seconds'] = result['end_timestamp'] - result['start_timestamp']
    keep = result['end_timestamp'].isna() | (result['duration_seconds'] >= min_duration_seconds)
    result = result.loc[keep].reset_index(drop=True)
    result.insert(0, 'mission_id', np.arange(1, len(result) + 1))
    return result


def add_mission_labels(chunk, intervals):
    """Return only rows inside a mission interval, with mission metadata added."""
    chunk = chunk.copy()
    chunk['timestamp'] = pd.to_numeric(chunk['timestamp'], errors='coerce')
    valid = chunk['timestamp'].notna()

    starts = intervals['start_timestamp'].to_numpy(dtype=float)
    ends = intervals['end_timestamp'].fillna(np.inf).to_numpy(dtype=float)
    timestamps = chunk.loc[valid, 'timestamp'].to_numpy(dtype=float)

    # Index of the most recent mission start at or before each data timestamp.
    interval_index = np.searchsorted(starts, timestamps, side='right') - 1
    inside = interval_index >= 0
    safe_index = np.maximum(interval_index, 0)
    inside &= timestamps <= ends[safe_index]

    selected_rows = chunk.loc[valid].iloc[np.flatnonzero(inside)].copy()
    selected_intervals = interval_index[inside]

    selected_rows.insert(0, 'mission_id',
                         intervals.iloc[selected_intervals]['mission_id'].to_numpy())
    selected_rows.insert(1, 'mission_name',
                         intervals.iloc[selected_intervals]['mission_name'].to_numpy())
    return selected_rows


def filter_csv_to_missions(input_file, output_file, intervals, chunk_size=200_000):
    """Memory-efficient filtering suitable for large CSV files."""
    wrote_header = False
    rows_written = 0

    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        if 'timestamp' not in chunk.columns:
            raise KeyError(f'{input_file} has no timestamp column')

        selected = add_mission_labels(chunk, intervals)
        if not selected.empty:
            selected.to_csv(
                output_file,
                mode='a' if wrote_header else 'w',
                header=not wrote_header,
                index=False,
            )
            wrote_header = True
            rows_written += len(selected)

    # Still create a valid empty CSV if there were no matching rows.
    if not wrote_header:
        header = pd.read_csv(input_file, nrows=0)
        header.insert(0, 'mission_id', pd.Series(dtype='int64'))
        header.insert(1, 'mission_name', pd.Series(dtype='object'))
        header.to_csv(output_file, index=False)

    return rows_written


OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
intervals = build_mission_intervals(
    MISSION_MANAGER_FILE,
    min_duration_seconds=MIN_MISSION_SECONDS,
)

interval_file = OUTPUT_FOLDER / 'mission_intervals.csv'
intervals.to_csv(interval_file, index=False)
print(f'Found {len(intervals)} mission interval(s)')
display(intervals)  # Works in Jupyter; replace with print(intervals) in a normal script

for input_file in INPUT_FILES:
    output_file = OUTPUT_FOLDER / f'{input_file.stem}_mission_only.csv'
    rows = filter_csv_to_missions(input_file, output_file, intervals, CHUNK_SIZE)
    print(f'{input_file.name}: wrote {rows:,} mission rows to {output_file}')
