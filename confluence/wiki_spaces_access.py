'''
ToDo: Get all groups and users associated with VIEWSPACE permission for given wiki spaces
Requires: Python 3
'''

import requests
import xmlrpc.client
import getpass
import pprint

confluence_url = input("Provide base URL for Confluence application: ")
userid = input("Provide Username: ")
password = getpass.getpass("Provide Password: ")
spaces = input("Provide comma separated list fo wiki spaces: ")

confluence_session = xmlrpc.client.ServerProxy(confluence_url + "/rpc/xmlrpc")
token = confluence_session.confluence2.login(userid, password)

print
print (f"Logging into Confluence Instance {confluence_url}")

wiki_spaces = spaces.split(",")
print
print("SpaceKey;<total groups associated>;<comma separated groups>;<total users associated>;<comma separated usernames")
for spacekey in wiki_spaces:
    print (spacekey, end=",")
    permissions_set = confluence_session.confluence2.getSpacePermissionSets(token, spacekey)    
    for permission_set in permissions_set:
        if permission_set['type'] == 'VIEWSPACE':
            users = [ entry['userName'] for entry in permission_set['spacePermissions'] if 'userName' in entry]
            groups = [ entry['groupName'] for entry in permission_set['spacePermissions'] if 'groupName' in entry]
            print( str(len(groups)) + "," + ";".join(groups) + "," + str(len(users)) + ",Users:" + ";".join(users) )