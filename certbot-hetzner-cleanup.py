#!/usr/bin/python
import json, requests, sys, getopt, argparse, time, re
from os import environ

f = open("hetzner-auth-token", "r")
api_token = f.read() # your Hetzner DNS-API Token
f.close()
domain = re.search(r'.*\.(.*\..*)', environ['CERTBOT_DOMAIN']).group(1)
subdomains = '.' + re.match(r'^(.*\.)?[^.]*\.[^.]*$', environ['CERTBOT_DOMAIN']).group(1)[:-1] if re.match(r'^(.*\.)?[^.]*\.[^.]*$', environ['CERTBOT_DOMAIN']) and re.match(r'^(.*\.)?[^.]*\.[^.]*$', environ['CERTBOT_DOMAIN']).group(1) else ''
headers = {'Auth-API-Token': api_token, 'Content-Type': 'application/json'}
response = requests.get('https://dns.hetzner.com/api/v1/zones', headers=headers)
zone_id = [x for x in json.loads(response.content.decode('utf-8'))['zones'] if x['name'] == domain][0]['id']
response = requests.get('https://dns.hetzner.com/api/v1/records?zone_id={0}'.format(zone_id), headers=headers)
records = [x for x in json.loads(response.content.decode('utf-8'))['records'] if x['name'] == '_acme-challenge' + subdomains]
for record in records:
  requests.delete('https://dns.hetzner.com/api/v1/records/{0}'.format(record['id']), headers=headers)
