"""Class for cache of UIDs"""

import json
import subprocess as sp
import sys

ID = "/bin/id"

class UserIDs(object):
    """Interface for handling the cache"""

    def  __init__(self, ids=None, name=None):
        self.ids = ids if ids is not None else {}

    def load(self, cache):
        """Attemtps to load preexisting cache"""
        self.name = cache
        try:
            cache = open(cache)
            self.ids = json.load(cache)
        except:
            pass

    def access(self, user):
        """Access information in cache"""
        return self.ids[user]

    def add(self, user, uid):
        """Adds user and uid to cache"""
        self.ids[user] = uid
        self.ids[uid] = user

    def have(self, user):
        """Check if user's information is in cache"""
        return user in self.ids

    def remove(self, user):
        """Remove user and uid from cache"""
        try:
            del self.ids[self.ids[user]]
            del self.ids[user]
            return 0
        except KeyError:
            return 1

    def clear(self):
        """Clear cache"""
        self.ids.clear()

    def resolve(self, user, pslines, unknowns):
        """Resolves finding unknown UIDs"""
        try:
            return sp.check_output([ID, "-u", user], stderr=sys.stderr).rstrip()
	except sp.CalledProcessError:
            try:
                for line in pslines:
                    if line.strip().split()[0] == user:
                        search = line[65:]
                        found = search.find("sshd: ")
                        if found != -1:
                            return search[6:13]
                unknowns.add(user)
                return None
            except sp.CalledProcessError:
                unknowns.add(user)
                return None

    def close(self):
        """Safely closes and saves cache"""
        id_json = json.dumps(self.ids)
        json_file = open(self.name, "w")
        json_file.write(id_json)
        json_file.close()
