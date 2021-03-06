#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import urllib.request
from tabulate import tabulate
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-a", "--attribs", action="store", dest="attributes", default="user,version")
parser.add_option("-d", "--hide-deleted", action="store_false", dest="show_deleted", default=True)

(options, args) = parser.parse_args()

show_attrib = options.attributes.split(',')

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
    line += [key, tag['value']] + [tag['attrib'][attrib_name] for attrib_name in show_attrib]
    final.append(line)

if options.show_deleted:
    headers = ['']
else:
    headers = []

headers += ['key', 'value'] + show_attrib

print(tabulate(final, headers=headers))
