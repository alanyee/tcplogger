"""Class for cache of UIDs"""

import json
import subprocess as sp

ALPHA = "abcdefghijklmnopqrstuvwxyz"
ALPHA15 = "abcdefghij"
ID = "/bin/id"

class UserIDs(object):
    """Interface for handling the cache"""

    def  __init__(self, ids=None):
        self.ids = ids if ids is not None else {}

    def load(self):
        """Load cache, otherwise just create new cache"""
        try:
            json_file = open('ids.json')
            self.ids = json.load(json_file)
        except IOError:
            self.create()

    def access(self, user):
        """Access information in cache"""
        return self.ids[user].encode('utf-8')

    def add(self, user, uid):
        """Adds user and uid to cache"""
        self.ids[user] = uid

    def have(self, user):
        """Check if user's information is in cache"""
        return user in self.ids

    def clear(self):
        """Clear cache"""
        self.ids.clear()

    def close(self):
        """Safely closes and saves files"""
        id_json = json.dumps(self.ids)
        json_file = open("ids.json", "w")
        json_file.write(id_json)
        json_file.close()

    def create(self):
        """Prepopulate cache, eventually will remove"""
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
