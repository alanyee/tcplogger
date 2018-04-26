"""Offline cache editor"""
import argparse

from ids import UserIDs

parser = argparse.ArgumentParser(description='Offline cache editor')
parser.add_argument("-a", "--add", nargs=2, metavar=('username', 'uid'),
                    help="Adds specified username and uid to cache")
parser.add_argument("-d", "--delete", nargs=1, metavar='username|uid',
                    help="Deletes specified username or uid from cache")
parser.add_argument("-c", "--clear", action='store_true', help="Clears all cache")
args = parser.parse_args()

mapped = UserIDs()
mapped.load()

# Add specified username and uid to cache
if args.add:
    user, uid = args.add[0], args.add[1]
    mapped.add(user, uid)
# Deletes specified username or uid from cache
if args.delete:
    user = args.delete[0]
    if mapped.have(user):
        mapped.remove(user)
#Clears all cache
if args.clear:
    mapped.clear()

mapped.close()
