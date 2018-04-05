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
mapped_ids = UserIDs()
unknown_ids = []

# Tries to open cache, and creates one if it doesn't already exist
mapped_ids.load()

# Clears cache
if prompt == "y":
    mapped_ids.clear()

with open(file_name, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=HEADER)
    writer.writeheader()
    try:
        while True:
            ps = sp.check_output([PS, "aux"])
            tcp = sp.check_output([CAT, "/proc/net/tcp"])
            snap = time.time()
            pslines = ps.splitlines()
            tcplines = tcp.splitlines()
            user = random.choice(pslines).strip().split()
            while user[0] == "root" or user[0] == "USER" or user[0] == "libstor+":
                user = random.choice(pslines).strip().split()
            pid = user[1]
            user = user[0]
            if mapped_ids.have(user):
                uid = mapped_ids.access(user)
            elif user in unknown_ids:
                continue
            else:
                try:
                    uid = sp.check_output([ID, "%s" % user])
                    uid = uid[uid.find("=") + 1:uid.find("(")]
                    mapped_ids.add(user, uid)
                except sp.CalledProcessError:
                    unknown_ids.append(user)
                    for line in pslines:
                        if line.strip().split()[0] == user:
                            unknown_ids.append(line[64:])
                    continue
            acts = []
            for line in tcplines:
                if line.strip().split()[7] == uid:
                    acts.append(line)
            if acts:
                act = random.choice(acts).rstrip()
                if act:
                    writer.writerow({'time': '%d' % snap,
                                     'user': '%s' % user,
                                     'pid': '%s' % pid,
                                     'uid': '%s' % uid,
                                     'act': '%s' % act})
    except KeyboardInterrupt:
        mapped_ids.close()
        for unknown in unknown_ids:
            print unknown
