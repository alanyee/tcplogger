"""Logger for TCP connections by user"""

import csv
import random
import subprocess as sp
import time

from ids import UserIDs

CAT = "/bin/cat"
ID = "/bin/id"
PS = "/bin/ps"
HEADER = ['time', 'user', 'pid', 'uid', 'act']

file_name = raw_input("Please type the name of the output csv: ")
prompt = raw_input("Would you like to clear the cache? (y/n): ")
mapped = UserIDs()
unknowns = set()

# Tries to open cache, and creates one if it doesn't already exist
mapped.load()

# Clears cache
if prompt == "y":
    mapped.clear()

# Creates csv file
with open(file_name, 'w') as csv_file:
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
                mapped.add(uid, user)
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
