"""Logger for TCP connections by user"""

import argparse
import csv
import random
import subprocess as sp
import time

from ids import UserIDs

CAT = "/bin/cat"
ID = "/bin/id"
PS = "/bin/ps"
HEADER = ['time', 'user', 'pid', 'uid', 'act']

parser = argparse.ArgumentParser(description='Smart TCP Logger')
parser.add_argument("-f", "--filename", nargs=1, metavar="filename",
                    help="Writes to specified filename")
parser.add_argument("-c", "--clear", action='store_true', help="Clears all cache")
args = parser.parse_args()

mapped = UserIDs()
unknowns = set()

# Tries to open cache, and creates one if it doesn't already exist
mapped.load()

# Clears cache
if args.clear:
    mapped.clear()

if args.filename:
    filename = args.filename[0]
else:
    filename = "output.csv"
   
# Creates csv file
with open(filename, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=HEADER)
    writer.writeheader()
    try:
        while True:
            # Saves a snapshot of TCP and UID information
            ps = sp.check_output([PS, "aux"])
            tcp = sp.check_output([CAT, "/proc/net/tcp"])
            snap = time.time()
            # Cleans the data
            pslines = ps.splitlines()
            tcplines = tcp.splitlines()
            user = random.choice(pslines).strip().split()
            # Ignores noise
            while user[0] == "root" or user[0] == "USER" or user[0] == "libstor+":
                user = random.choice(pslines).strip().split()
            pid = user[1]
            user = user[0]
            # Relies on cache first for finding user information
            if mapped.have(user):
                uid = mapped.access(user)
            # Ignores username or uid if misconfigured
            elif user in unknowns:
                continue
            # Attempts to figure out username and uid
            else:
                uid = mapped.resolve(user, pslines, unknowns)
                if uid is None:
                    continue
                mapped.add(user, uid)
            # Checks and corrects uid misconfiguration from ps table
            if user.isdigit():
                user, uid = mapped.access(user), mapped.access(uid)
            # Finds all of a given user's active TCP connections
            acts = []
            for line in tcplines:
                if line.strip().split()[7] == uid:
                    acts.append(line)
            # Randomly assigns TCP connection to process
            if acts:
                act = random.choice(acts).rstrip()
                if act:
                    writer.writerow({'time': '%d' % snap,
                                     'user': '%s' % user,
                                     'pid': '%s' % pid,
                                     'uid': '%s' % uid,
                                     'act': '%s' % act})
# Saves cache and prints out unknown users upon shutdown
    except KeyboardInterrupt:
        mapped.close()
        for unknown in unknowns:
            print "Unknown IDs: " + str(unknown)
