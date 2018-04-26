"""Offline cache editor"""

from ids import UserIDs

mapped = UserIDs()
mapped.load()

print "Cache is loaded offline. Proceed with caution." 
print "Would you like to add, remove, or clear the cache?" 

while True:
    answer = raw_input("(add/remove/clear/exit): ")
    if answer == "add":
        user = raw_input("Please enter the user you wish to add: ")
        uid = raw_input("Please enter the uid you wish to associate with the user: ")
        mapped.add(user, uid)
        mapped.add(uid, user)
        print "Added " + user + " and " + uid + " successfully" 
    elif answer == "remove":
        user = raw_input("Please enter the user or uid you wish to remove: ")
        if mapped.have(user):
            mapped.remove(user)
            print "Removed " + user + " successfully"
    elif answer == "clear":
        sure = raw_input("Are you sure to want to clear all the cache? (y/n): ")
        if sure == "y":
            mapped.clear()
            print "Cleared successfully"
    else:
        exit = raw_input("Would you like to continue working? (y/n): ")
        if exit == "n":
            save = raw_input("Would you like to save your work? (y/n): ")
            if save == "y":
                mapped.close()
            break
