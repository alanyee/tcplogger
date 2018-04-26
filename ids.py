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
        except KeyError:
            print "No such user or uid found in cache"

    def clear(self):
        """Clear cache"""
        self.ids.clear()

    def resolve(self, user, pslines, unknowns):
        """Resolves finding unknown UIDs"""
        try:
            return sp.check_output([ID, "-u", user]).rstrip()
	except sp.CalledProcessError:
            try:
                for line in pslines:
                    if line.strip().split()[0] == user:
                        search = line[65:]
                        found = search.find("sshd: ")
                        if found != -1:
                            return search[6:13]
                unknowns.add(user)
                for line in pslines:
                    if line.strip().split()[0] == user:
                        unknowns.add(line)
                return None
            except sp.CalledProcessError:
                unknowns.add(user)
                for line in pslines:
                    if line.strip().split()[0] == user:
                        unknowns.add(line)
                return None

    def close(self):
        """Safely closes and saves files"""
        id_json = json.dumps(self.ids)
        json_file = open("ids.json", "w")
        json_file.write(id_json)
        json_file.close()
