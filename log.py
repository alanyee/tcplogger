import csv
import random
import subprocess as sp
import time

from ids import UserIDs

CAT = "/bin/cat"
ID = "/bin/id"
PS = "/bin/ps"
HEADER = ['time', 'user', 'pid', 'uid', 'act']

csv_file = raw_input("Please type the name of the output csv: ")
prompt = raw_input("Would you like to clear the cache? (y/n): ")
ids_obj = UserIDs()

# Tries to open cache, and creates one if it doesn't already exist
ids_obj.load()

# Clears cache
if prompt == "y":
    ids_obj.clear()

with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=HEADER)
    writer.writeheader()
    while True:
        ps = sp.check_output([PS, "aux"])
        tcp = sp.check_output([CAT, "/proc/net/tcp"])
        snap = time.time()
        pslines = ps.splitlines()
        tcplines = tcp.splitlines()
        user = random.choice(pslines).strip().split() 
        while (user[0] == "root" or user[0] == "USER" or user[0] == "libstor+"):
          user = random.choice(pslines).strip().split()
        pid = user[1]
        user = user[0]
        if ids_obj.have(user):
            uid = ids_obj.access(user)
        else:
            uid = sp.check_output([ID, "%s" % user])
            uid = uid[uid.find("=") + 1:uid.find("(")]
            ids_obj.add(user, uid)
        acts = []
        for line in tcplines:
            if line.strip().split()[7] == uid: 
                acts.append(line)
        if acts:
            act = random.choice(acts).rstrip()
            if act:
                writer.writerow({'time': '%d' % snap, 'user': '%s' % user, 
                  'pid': '%s' % pid, 'uid': '%s' % uid, 'act': '%s' % act})

ids.obj.close()