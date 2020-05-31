#!/usr/bin/python

import json, requests, sys, getopt, argparse, time
from os import environ

f = open("hetzner-auth-token.txt", "r")
api_token = f.read() # your Hetzner DNS-API Token
f.close()
headers = {'Auth-API-Token': api_token, 'Content-Type': 'application/json'}
response = requests.get('https://dns.hetzner.com/api/v1/zones', headers=headers)
zone_id = [x for x in json.loads(response.content.decode('utf-8'))['zones'] if x['name'] == environ['CERTBOT_DOMAIN']][0]['id']
response = requests.post('https://dns.hetzner.com/api/v1/records', headers=headers, json={'value': environ['CERTBOT_VALIDATION'], 'ttl': 86400, 'type': 'TXT', 'name': '_acme-challenge', 'zone_id': zone_id})
time.sleep(30)
