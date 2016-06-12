# This will eventually distinguish between all the statuses in the CSV
# (Ok, Untested, Has Issues, Doesn't Work) and could even move them
# into appropriate directories, or perhaps even across different
# emulators. Additionally, it could scrape all the gdoc spreadsheets
# itself.
import os
import shutil
import sys

STATUSES = {"untested": 0, "ok": 1, "doesn't work": 2, "has issues": 3, '': 4}


def _status_int(status):
    s = status.lower()
    assert s in STATUSES, "Invalid status '%s' in CSV" % status
    return STATUSES[s]


def _read_functional_line(registry, line):
    elem = line.split(',')
    registry[elem[0]] = {"Full Name": elem[1],
                         "RP1": STATUSES["ok"],
                         "RP2": STATUSES["ok"],
                         "RP3": STATUSES["ok"],
                         "Parent": None,
                         "BIOS": None,
                         "Samples": None,
                         "Notes": None,
                         "Year": None,
                         "Publisher": None}


def _read_full_line(registry, line):
    # Example line:
    # 1941,1941 - Counter Attack (900227 World),Untested,OK,OK,,,,,1990,Capcom
    # (rom, full name, RP1, RP2, RP3, Parent, Bios, Samples, Notes, Year,
    #  Publisher)
    # Statuses: (Untested, OK, Doesn't Work, Has Issues)
    # Problem line:
    # 1942abl,"1942 (Revision A, bootleg) [Bootleg]",Untested,Untested,Untested,1942,,,,1984,Capcom
    elem = line.split(',')

    # TODO: Ignore problem lines for now, with stray commas in one of
    #       the fields
    if len(elem) > 11:
        return

    (rom, full_name, rp1, rp2, rp3, parent, bios,
     samples, notes, year, publisher) = elem
    registry[rom] = {"Full Name": elem,
                     "RP1": _status_int(rp1),
                     "RP2": _status_int(rp2),
                     "RP3": _status_int(rp3),
                     "Parent": parent,
                     "BIOS": bios,
                     "Samples": samples,
                     "Notes": notes,
                     "Year": year,
                     "Publisher": publisher}


def load_csv(input_csv):
    registry = {}
    with open(input_csv, 'r') as f:
        line = f.readline()
        elem = line.split(',')
        reader = None

        # This is clearly unsafe
        if len(elem) == 4:
            reader = _read_functional_line
        elif len(elem) == 11:
            reader = _read_full_line

            # Skip the first two lines, which is column titles + meta
            line = f.readline()
            line = f.readline()
        else:
            raise Exception("Unrecognized CSV, cannot continue")

        while True:
            reader(registry, line)
            line = f.readline()
            if len(line) == 0:
                break

    return registry


def _make_path(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def sync(input_csv, run_path):
    registry = load_csv(input_csv)
    scanned, matched = 0, 0

    for path in ["has_issues", "unsupported"]:
        _make_path(os.path.join(run_path, path))

    for root, subdirs, files in os.walk(run_path):
        for f in files:
            file_parts = f.split('.')
            if os.path.exists(os.path.join(run_path, f)):
                if file_parts[0] in registry:
                    matched += 1
                else:
                    shutil.move(f, os.path.join(run_path, "unsupported"))
        scanned += len(files)
    return len(registry), scanned, matched
