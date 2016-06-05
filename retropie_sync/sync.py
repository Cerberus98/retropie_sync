# This will eventually distinguish between all the statuses in the CSV
# (Ok, Untested, Has Issues, Doesn't Work) and could even move them
# into appropriate directories, or perhaps even across different
# emulators. Additionally, it could scrape all the gdoc spreadsheets
# itself.
import os
import sys


def load_csv(input_csv):
    registry = {}
    with open(input_csv, 'r') as f:
        for line in f:
            elem = line.split(',')
            registry[elem[0]] = elem[1]
    return registry


def sync(input_csv, run_path):
    registry = load_csv(input_csv)
    scanned, matched = 0, 0

    for root, subdirs, files in os.walk(run_path):
        for f in files:
            file_parts = f.split('.')
            if file_parts[0] in registry:
                click.echo(os.path.join(root, f))
                matched += 1
        scanned += len(files)
    return scanned, matched
