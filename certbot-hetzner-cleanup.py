#!/usr/bin/python

import json, requests, sys, getopt, argparse, time
from os import environ



api_token = 'XXX' # your Hetzner DNS-API Token


headers = {'Auth-API-Token': api_token, 'Content-Type': 'application/json'}
response = requests.get('https://dns.hetzner.com/api/v1/zones', headers=headers)
zone_id = [x for x in json.loads(response.content.decode('utf-8'))['zones'] if x['name'] == environ['CERTBOT_DOMAIN']][0]['id']
response = requests.get('https://dns.hetzner.com/api/v1/records?zone_id={0}'.format(zone_id), headers=headers)
records = [x for x in json.loads(response.content.decode('utf-8'))['records'] if x['name'] == '_acme-challenge']
for record in records:
  requests.delete('https://dns.hetzner.com/api/v1/records/{0}'.format(record['id']), headers=headers)