# op

`op` is a deployments management tool.


## Installation

Use `git` to install `op`.

```bash
$ git clone https://github.com/slasyz/op.git
$ cd op
$ make init

# On OS X:
$ brew install coreutils
$ sudo bash -c "echo \"\$(grealpath .)/venv/bin/python3 \$(grealpath main.py) \\\"\\\$@\\\"\" > /usr/bin/local/op"
# On Linux:
$ sudo bash -c "echo \"\$(realpath .)/venv/bin/python3 \$(realpath main.py) \\\"\\\$@\\\"\" > /usr/bin/local/op"
```

## Usage

```
usage: main.py SUBCOMMAND ...

positional arguments:
  SUBCOMMAND
    help      show help
    init      initialize project
    generate  create or update generated files
    deploy    deploy project to the environment
    debug     start project dependencies
    tests     tests
    stat      information about project
    logs      attach to logs
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)