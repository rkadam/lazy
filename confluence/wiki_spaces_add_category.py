# Add category to given list of wiki spaces
# https://community.atlassian.com/t5/Confluence-questions/How-to-set-a-space-s-category-by-REST-API/qaq-p/714279
# There are no REST APIs to rescue; we gotta use old deprecated XML RPC calls!
# Need Python 3 and XMP RPC library

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
print

wiki_spaces = spaces.split(",")

print ("Adding category to wiki spaces...")
for spacekey in wiki_spaces:
    print (spacekey, end=",")
    confluence_session.confluence2.addLabelByNameToSpace(token, "team:engineering", spacekey)