import json
import sys
import os

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def adjust_timestamps(events, offset):
    for event in events:
        #event['ts'] += offset
        event['ts'] -= offset
    return events

def replace_pid(events, new_prefix):
    for event in events:
        old_pid = event['pid']
        new_pid = new_prefix + "-" + str(old_pid)
        event['pid'] = new_pid
    return events

def merge_profiles(profile1, profile2, prefix1, prefix2):
    # Find the minimum timestamp in each profile
    min_ts1 = min(event['ts'] for event in profile1['traceEvents'])
    min_ts2 = min(event['ts'] for event in profile2['traceEvents'])

    # Calculate the offset to align the timelines
    #offset = min_ts1 - min_ts2

    # change TS to relative time-stamp
    adjusted_profile1_events = adjust_timestamps(profile1['traceEvents'], min_ts1)
    adjusted_profile2_events = adjust_timestamps(profile2['traceEvents'], min_ts2)

    # Replace the "pid" values
    profile1_events_with_new_pid = replace_pid(adjusted_profile1_events, prefix1)
    profile2_events_with_new_pid = replace_pid(adjusted_profile2_events, prefix2)

    # Merge the events
    merged_events = profile1_events_with_new_pid + profile2_events_with_new_pid

    # Create the merged profile
    merged_profile = {
        "traceEvents": merged_events,
        "displayTimeUnit": "ns"
    }

    return merged_profile

def main(file1, file2, output_file):
    profile1 = load_json(file1)
    profile2 = load_json(file2)

    prefix1, _ = os.path.splitext(file1)
    prefix2, _ = os.path.splitext(file2)

    merged_profile = merge_profiles(profile1, profile2, prefix1, prefix2)

    save_json(merged_profile, output_file)
    print(f"Merged profile saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_profiles.py <file1.json> <file2.json> <output.json>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]

    main(file1, file2, output_file)
