#!/usr/bin/env python3

import requests
import json
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
@click.pass_obj
def delete(crd, domain, id):
    """
    Delete your DNS records
    """
    r = requests.delete("{}/domains/{}/records/{}".format(API_URL, domain, id),
                        auth=HTTPBasicAuth(crd.user, crd.token))
    isValid(r)
    print("Deleted")


@main.command()
@click.option('-r', '--record', help='Type of record', required=True,
              type=click.Choice(['A', 'MX', 'CNAME', 'TXT',
                                'SRV', 'AAAA', 'NS', 'ANAME']))
@click.option('-d', '--domain', required=True,
              help='domain')
@click.option('-id', required=True,
              help='unique id record')
@click.pass_obj
def update(crd, record, domain, id):
    """
    Update your DNS records
    """
    r = requests.put("{}/domains/{}/records/{}".format(API_URL, domain, id),
                     auth=HTTPBasicAuth(crd.user, crd.token))
    isValid(r)
    data = r.json()
    print(json.dumps(data, indent=2))


@main.command()
@click.option('-d', '--domain', required=True,
              help='domain')
@click.option('-r', '--record', help='Type of record', required=True,
              type=click.Choice(['A', 'MX', 'CNAME', 'TXT',
                                'SRV', 'AAAA', 'NS', 'ANAME']))
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
    params = {
              "host": "{}".format(host),
              "type": "{}".format(record),
              "answer": "{}".format(answer),
              "ttl": "{}".format(ttl)
             }
    params = json.dumps(params)
    r = requests.post("{}/domains/{}/records".format(API_URL, domain),
                      data=params, auth=HTTPBasicAuth(crd.user, crd.token))
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
        r = requests.get("{}/domains/{}/records/{}".format(API_URL, domain, id),
                         auth=HTTPBasicAuth(crd.user, crd.token))
    else:
        r = requests.get("{}/domains/{}/records".format(API_URL, domain),
                         auth=HTTPBasicAuth(crd.user, crd.token))

    isValid(r)
    data = r.json()

    if id and minimal:
        print("ID: {}, TYPE: {}, FQDN: {}, ANSWER: {}".format(
              data['id'], data['type'], data['fqdn'], data['answer']))
    elif minimal:
        for reg in data['records']:
            print("ID: {}, TYPE: {}, FQDN: {}, ANSWER: {}".format(
                  reg['id'], reg['type'], reg['fqdn'], reg['answer']))
    else:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
