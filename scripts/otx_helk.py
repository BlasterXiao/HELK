#!/usr/bin/env python
from OTXv2 import OTXv2
from pandas.io.json import json_normalize

otx = OTXv2("API Key")

def OTXEnrichment():
    pulses = otx.getall()
    data = []
    object = {}
    for p in pulses:
        for i in p['indicators']:
            object = {
                'industries': p['industries'],
                'tlp': p['tlp'],
                'description' : p['description'],
                'created' : p['created'],
                'pulse_name' : p['name'],
                'tags' : p['tags'],
                'author_name' : p['author_name'],
                'created': p['created'],
                'modified' : p['modified'],
                'targeted_countries' : p['targeted_countries'],
                'id' : p['id'],
                'extract_source' : p['extract_source'],
                'references' : p['references'],
                'adversary' : p['adversary'],
                'indicator_name': i['indicator'],
                'indicator_description': i['description'],
                'indicator_title': i['title'],
                'indicator_created': i['created'],
                'indicator_content': i['content'],
                'indicator_type': i['type'],
                'indicator_id': i['id']
            }    
            data.append(object)
    
    IPV4 = []
    IMPHASH = []
    MD5 = []
    SHA256 = []
    SHA1 = []

    def pull_indicators(lst, name):
        object = {
            'indicator_name' : i['indicator_name'],
            'pulse_name' : i['pulse_name'],
            'ioc_name': name
        }
        return object
    for i in data:
        if i['indicator_type'] == "IPv4":
            IPV4.append(pull_indicators(IPV4, 'ipv4'))
        elif i['indicator_type'] == "FileHash-MD5":
            MD5.append(pull_indicators(MD5, 'md5'))
        elif i['indicator_type'] == "FileHash-SHA1":
            SHA1.append(pull_indicators(SHA1, 'sha1'))
        elif i['indicator_type'] == "FileHash-SHA256":
            SHA256.append(pull_indicators(SHA256, 'sha256'))
        elif i['indicator_type'] == "FileHash-IMPHASH":
            IMPHASH.append(pull_indicators(IMPHASH, 'imphash'))

    iocs = [IPV4, IMPHASH, MD5, SHA1, SHA256]
    for i in iocs:
        df = json_normalize(i)
        df.to_csv(('/opt/otx/otx_'+i[0]['ioc_name']+'_.csv'), index=False, header=False, encoding='utf-8', columns=("indicator_name", "pulse_name"))

if __name__=="__main__":
    OTXEnrichment()