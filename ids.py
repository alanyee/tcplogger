import json
import subprocess as sp

ALPHA = "abcdefghijklmnopqrstuvwxyz"
ALPHA15 = "abcdefghij"
ID = "/bin/id"

class UserIDs(object):
    def __init__(self, ids=None):
        self.ids = ids if ids is not None else {}

    def load(self):
        try:
            json_file = open('ids.json')
            self.ids = json.load(json_file)
        except IOError:
            self.create()

    def access(self, user):
        return self.ids[user].encode('utf-8')

    def add(self, user, uid):
        self.ids[user] = uid

    def have(self, user):
        return user in self.ids

    def clear(self):
        self.ids.clear()

    def close(self):
        id_json = json.dumps(self.ids)
        json_file = open("ids.json", "w")
        json_file.write(id_json)
        json_file.close()
        print id_json

    def create(self):
        abc = ALPHA
        for i in abc:
            if i == "h":
                abc = ALPHA15
            for j in abc:
                user = "cs12x" + i + j
                uid = sp.check_output([ID, "%s" % user])
                uid = uid[uid.find("=") + 1:uid.find("(")]
                self.ids[uid] = user
            print i
            if i == "h":
                break
