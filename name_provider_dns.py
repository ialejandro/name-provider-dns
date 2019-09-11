#!/usr/bin/env python3

"""
AUTHOR: hello@ialejandro.rocks
REPOSITORY: ialejandro/name-provider-dns
"""


import requests, json, sys
import click
from requests.auth import HTTPBasicAuth


"""
Global vars
"""
API_URL = 'https://api.name.com/v4'


class Credentials(object):
    """
    Create class to pass paramenters
    """
    def __init__(self, user=None, token=None):
        self.user = user
        self.token = token


def isValid(r):
    """
    Valid requests function
    """
    r.raise_for_status()


@click.group()
@click.option('-u', '--user', required=True,
        metavar='<user>')
@click.option('-t', '--token', required=True,
        metavar='<token>')
@click.pass_context
def main(crd, user, token):
    """
    Manage DNS name.com provider
    """
    crd.obj = Credentials(user, token)
    pass


@main.command()
@click.option('-d', '--domain', required=True,
        help='domain')
@click.option('-id', required=True,
        help='unique id record')
#@click.option('-a', '--all',
#        help='delete all records. BE CAREFUL!!')
@click.pass_obj
def delete(crd, domain, id):
    """
    Delete your DNS records
    """
    r = requests.delete(f'{API_URL}/domains/{domain}/records/{id}', auth=HTTPBasicAuth(crd.user, crd.token))
    isValid(r)
    print("Deleted")


@main.command()
@click.option('-r', '--record', help='Type of record', required=True,
        type=click.Choice(['A','MX','CNAME','TXT','SRV','AAAA','NS','ANAME']))
@click.option('-d', '--domain', required=True,
        help='domain')
@click.option('-id', required=True,
        help='unique id record')
@click.pass_obj
def update(crd, record, domain, id):
    """
    Update your DNS records
    """
    r = requests.put(f'{API_URL}/domains/{domain}/records/{id}', auth=HTTPBasicAuth(crd.user, crd.token))
    isValid(r)
    data = r.json()
    print(json.dumps(data, indent=2))


@main.command()
@click.option('-d', '--domain', required=True,
        help='domain')
@click.option('-r', '--record', help='Type of record', required=True,
        type=click.Choice(['A','MX','CNAME','TXT','SRV','AAAA','NS','ANAME']))
@click.option('-a', '--answer', required=True,
        help='answer')
@click.option('-h', '--host', required=True,
        help='host')
@click.option('--ttl', required=False, default=300,
        help='ttl')
@click.pass_obj
def create(crd, domain, record, host, answer, ttl):
    """
    Create your DNS records
    """
    params = {"host":f'{host}',"type":f'{record}',"answer":f'{answer}',"ttl":f'{ttl}'}
    params = json.dumps(params)
    r = requests.post(f'{API_URL}/domains/{domain}/records', data=params, auth=HTTPBasicAuth(crd.user, crd.token))
    isValid(r)
    data = r.json()
    print(json.dumps(data, indent=2))


@main.command()
@click.option('-d', '--domain', required=True,
        help='domain')
@click.option('-id', type=int, required=False,
        help='unique id record')
@click.option('-m', '--minimal', is_flag=True, required=False,
        help='only ids, fqdn, record type and answer without format')
@click.pass_obj
def records(crd, domain, id, minimal):
    """
    List your DNS records
    """
    if id:
        r = requests.get(f'{API_URL}/domains/{domain}/records/{id}', auth=HTTPBasicAuth(crd.user, crd.token))
    else:
        r = requests.get(f'{API_URL}/domains/{domain}/records', auth=HTTPBasicAuth(crd.user, crd.token))

    isValid(r)
    data = r.json()

    if id and minimal:
        print(f'ID:', data['id'], f'\nTYPE:', data['type'], f'\nFQDN:', data['fqdn'], f'\nANSWER:', data['answer'],f'\n')
    elif minimal:
        for reg in data['records']:
            print(f'ID:', reg['id'], f'\nTYPE:', reg['type'], f'\nFQDN:', reg['fqdn'], f'\nANSWER:', reg['answer'],f'\n')
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
