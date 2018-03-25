import json
import subprocess as sp

ALPHA = "abcdefghijklmnopqrstuvwxyz"
LIMIT = "abcdefghijklmnopqrs"
ID = "/bin/id"

abc = ALPHA
ids = {}
for i in LIMIT:
  if i == "s":
    abc = LIMIT
  for j in abc:
    user = "cs15x" + i + j
    uid = sp.check_output([ID, "%s" % user])
    uid = uid[uid.find("=") + 1:uid.find("(")]
    ids[uid] = user
  print i

id_json = json.dumps(ids)
json_file = open("ids.json", "w")
json_file.write(id_json)
json_file.close()
print id_json
