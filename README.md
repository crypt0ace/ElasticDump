# ElasticDump
A simple script to dump Elastic Search data if the authentication is disabled.

- `Help` Menu
```


  ______ _           _   _      _____
 |  ____| |         | | (_)    |  __ \
 | |__  | | __ _ ___| |_ _  ___| |  | |_   _ _ __ ___  _ __
 |  __| | |/ _` / __| __| |/ __| |  | | | | | '_ ` _ \| '_ \
 | |____| | (_| \__ | |_| | (__| |__| | |_| | | | | | | |_) |
 |______|_|\__,_|___/\__|_|\___|_____/ \__,_|_| |_| |_| .__/
                                                      | |
                                                      |_|

    Made by Crypt0ace :)

usage: ElasticDump.py [-h] -i IP -p PORT [-d DUMP] [-s SIZE]

Dump unauthenticated Elasticsearch database.

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP address of the Elasticsearch server
  -p PORT, --port PORT  Port number of the Elasticsearch server
  -d DUMP, --dump DUMP  Indices to dump
  -s SIZE, --size SIZE  Size of data to retrieve
```

- Note:
Needs `tabulate`. Can be installed using:
```bash
pip install tabulate
```
