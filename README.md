# Personal dotfiles

Personal configuration files for various linux utilities. Feel free to use as you wish.

There are two ways to install the configuration files:

- Directly copying the files

    All configuration files are stored under `config/XXX` folder. Copy those files you want to your `$HOME` folder.

- Use the simple dotinstall.py script

## Dependencies:
- Python 3.4+

## Usage:

``` 
$ python dotinstall.py
dotfiles installer
usage: dotinstall.py [-h] {list,install} ...

positional arguments:
  {list,install}

optional arguments:
  -h, --help      show this help message and exit
```

## List all configuration packages:

```
$ python dotinstall.py list
```

## Install configuration package `XXX`:
```
$ python dotinstall.py install -n XXX
```

> **NOTE:** you can force the installation (even if the target file exists) by supplying the option `--overwrite`

## Install modes:
There are two installation modes: `Copy` and `Link`.

- ``Copy`` mode copies the actual file from `configs/XXX` to your `$HOME` folder. 
- ``Link`` mode creates a softlink from your `$HOME` to the config file. This is useful if you keep the files sychronized between several computers and you want updates to be mirrored to the git repo.
