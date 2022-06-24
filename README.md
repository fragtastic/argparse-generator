# argparse-generator
Generates argparse structures based on functions defined within a class.

Supports:
- generating documentation at each level
- positional arguments
- default arguments

## Example output

```
python3 ./argparsegenerator.py
usage: argparsegenerator.py [-h] {files,users} ...

positional arguments:
  {files,users}
    files        Manage files
    users        Manage users

optional arguments:
  -h, --help     show this help message and exit
  --debug          debug flag
```

```
python3 ./argparsegenerator.py files
usage: argparsegenerator.py files [-h] [--debug] {upload} ...

positional arguments:
  {upload}
    upload    Uploads to destination and authenticates with auth_credentials

optional arguments:
  -h, --help     show this help message and exit
  --debug          debug flag
```

```
python3 ./argparsegenerator.py files upload
usage: argparsegenerator.py files upload [-h] [--debug] --destination DESTINATION [--auth_credentials AUTH_CREDENTIALS]
argparsegenerator.py files upload: error: the following arguments are required: --destination
```

```
python3 ./argparsegenerator.py users
usage: argparsegenerator.py users [-h] [--debug] {create,delete} ...

positional arguments:
  {create,delete}
    create         Deletes a user.
    delete         Creates a user.

optional arguments:
  -h, --help     show this help message and exit
  --debug          debug flag
```
