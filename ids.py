"""Class for cache of UIDs"""

import json
import subprocess as sp

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
            print "Preexisting cache could not be found"

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
