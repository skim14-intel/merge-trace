# merge-trace

## How to run
Usage: python merge_profiles.py <file1.json> <file2.json> <output.json>

### PID will be adjusted 
new_pid = new_prefix + "-" + str(old_pid)
1. new_prefix : file name of the orignal file
2. new PID = "{new prefix}-{original PID}"

### Time-stamp will be adjuste to zero base to combine two traces into one