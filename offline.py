#!/usr/bin/env python
"""Offline cache editor"""

import argparse

from ids import UserIDs

parser = argparse.ArgumentParser(description='Offline cache editor')
parser.add_argument("cache", help="Required cache file")
parser.add_argument("-a", "--add", nargs=2, metavar=('username', 'uid'),
                    help="Adds specified username and uid to cache")
parser.add_argument("-d", "--delete", nargs=1, metavar='username|uid',
                    help="Deletes specified username or uid from cache")
parser.add_argument("-C", "--clear", action='store_true', help="Clears all cache")
args = parser.parse_args()

mapped = UserIDs()
mapped.load(args.cache)

code = 0
# Add specified username and uid to cache
if args.add:
    user, uid = args.add[0], args.add[1]
# Deletes specified username or uid from cache
if args.delete:
    user = args.delete[0]
    if mapped.have(user):
        code = mapped.remove(user)
    else:
        code = 1
#Clears all cache
if args.clear:
    mapped.clear()

mapped.close()
exit(code)
