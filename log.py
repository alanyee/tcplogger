import csv
import json
import random
import subprocess as sp
import time

CAT = "/bin/cat"
ID = "/bin/id"
PS = "/bin/ps"

json_file = open('ids.json')
ids_dict= json.load(json_file)

with open('names2.csv', 'w') as csvfile:
  fieldnames = ['time', 'user', 'pid', 'uid', 'act']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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
    uid = ""
    if user.isdigit():
      uid = ids_dict[user].encode('utf-8')
    else:
      uid = sp.check_output([ID, "%s" % user])
      uid = uid[uid.find("=") + 1:uid.find("(")]
    acts = []
    for line in tcplines:
      if line.strip().split()[7] == uid: 
        acts.append(line)
    if acts:
      act = random.choice(acts).rstrip()
      if act:
        writer.writerow({'time': '%d' % snap, 'user': '%s' % user, 'pid': '%s' % pid,
                           'uid': '%s' % uid, 'act': '%s' % act})

json_file.close()
