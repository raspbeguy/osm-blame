#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import urllib.request
import json
from pprint import pprint

from tabulate import tabulate
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-a", "--attribs", action="store", dest="attributes", default="user,version")
parser.add_option("-d", "--hide-deleted", action="store_false", dest="show_deleted", default=True)
parser.add_option("-c", "--changeset-attribs", action="store", dest="changeset_attribs", default=None)

(options, args) = parser.parse_args()

show_attrib = options.attributes.split(',')

show_changeset_attrib=[]
if options.changeset_attribs is not None:
    show_changeset_attrib = options.changeset_attribs.split(',')
    changeset_cache = {}
    print ("/mn/ FIXME debug show_changeset_attrib=", show_changeset_attrib)
    
def get_changeset_attrib(changeset, find_tag):
        if (not changeset_cache.get(changeset)):
            crequest = f"https://www.openstreetmap.org/api/0.6/changeset/{changeset}"
            #print ("/mn/ debug crequest=", crequest)
            cresponse = urllib.request.urlopen(crequest)
            changeset_xml = cresponse.read()
            changeset_cache[changeset] = changeset_xml
            #print (f"/mn/ fetched new changeset_cache[{changeset}]={changeset_xml}")

        changeset_root = ET.fromstring(changeset_cache[changeset])

#        print ();
#        print ("dump changeset_root:");
#        ET.dump(changeset_root)
#        print (type(changeset_root))
#        pprint(changeset_root)
#        json.dump(changeset_root)
#        print ();
#        print ("dump history_root:");
#        ET.dump(history_root)
#        print ();
        
        for cversion in changeset_root:
#        for cversion in sorted(changeset_root, key=lambda x: int(x.get('version'))):
#        for cversion in sorted(history_root, key=lambda x: int(x.get('version'))):
            attrib = dict(cversion.attrib)
            for tag in cversion.findall('tag'):
                tag_key = tag.get('k')
                tag_val = tag.get('v')
                #print (f"changeset k={tag_key} v={tag_val}")
                if tag_key == find_tag:
                    print (f"Found requested tag {tag_key}, returning value {tag_val}")
                    return tag_val
        return None
        

item = args[0]

request = "https://www.openstreetmap.org/api/0.6/{}/history".format(item)
response = urllib.request.urlopen(request)
history_xml = response.read()

history_root = ET.fromstring(history_xml)

blame_tag = {}


for version in sorted(history_root, key=lambda x: int(x.get('version'))):

    attrib = dict(version.attrib)

    for tag in version.findall('tag'):
        tag_key = tag.get('k')
        tag_val = tag.get('v')
        if (
                tag_key not in blame_tag or
                tag_val != blame_tag[tag_key]['value']
            ):
            blame_tag[tag_key] = {'value': tag_val, 'attrib': attrib}

    for key in blame_tag.keys():
        if (
                version.find("./tag[@k='{}']".format(key)) is None and 
                blame_tag[tag_key]['value'] is not None
            ):
            blame_tag[key] = {'value': None, 'attrib': attrib}


final = []
for key, tag in blame_tag.items():
    if options.show_deleted:
        line = ['+' if tag['value'] else '-']
    else:
        if tag['value'] is None:
            continue
        line = []

    if show_changeset_attrib is not None:
        for find_c_attrib in show_changeset_attrib:
            #print (f"/mn/ getting {find_c_attrib}")
            c_a = get_changeset_attrib(tag['attrib']['changeset'], find_c_attrib)

    line += [key, tag['value']] + [tag['attrib'][attrib_name] for attrib_name in show_attrib] + \
            [get_changeset_attrib(tag['attrib']['changeset'], c_attrib_name) for c_attrib_name in show_changeset_attrib]
    final.append(line)

if options.show_deleted:
    headers = ['']
else:
    headers = []

headers += ['key', 'value'] + show_attrib + show_changeset_attrib

print(tabulate(final, headers=headers))
