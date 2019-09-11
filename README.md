## INITIAL VERSION
**ONLY WORKS ON PYTHON 3.6**

### Install
```bash
git clone git@github.com:ialejandro/name-provider-dns.git
cd name-provider-dns
pip install -r requirements.txt
```

### Usage
```bash
python name_provider_dns.py

Usage: name_provider_dns.py [OPTIONS] COMMAND [ARGS]...

  Manage DNS name.com provider

Options:
  -u, --user <user>    [required]
  -t, --token <token>  [required]
  --help               Show this message and exit.

Commands:
  create   Create your DNS records
  delete   Delete your DNS records
  records  List your DNS records
  update   Update your DNS records
```
