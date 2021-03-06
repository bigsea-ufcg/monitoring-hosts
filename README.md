# Monitoring Host Daemon

Daemon that monitors physical hosts performance

## Benchmarks used

- [CPU] [Sysbench](http://manpages.ubuntu.com/manpages/xenial/man1/sysbench.1.html)



Installation
------------

To install the monitoring-hosts daemon you will need a virtual machine with a fresh install environment and with the configuration described below.

**Minimal Server Configuration**
```
OS: Ubuntu 14.04
CPU: 1 core
Memory: 1G of RAM
Disk: there is no disk requirements
```

### Steps

1. Update and Upgrade your machine
    ```bash
    $ sudo apt-get update && sudo apt-get upgrade
    ```
2. Install pip and dependencies
    ```bash
    $ sudo apt-get install python-setuptools python-dev build-essential
    $ sudo easy_install pip
    ```
3. Install git
    ```bash
    $ sudo apt-get install git
    ```
4. Install sysbench
    ```bash
    $ sudo apt-get install sysbench
    ```
5. Clone the monitoring-hosts repository
    ```bash
    $ git clone https://github.com/bigsea-ufcg/monitoring-hosts
    ```
6. Access the bigsea-loadbalancer folder to install the requirements
    ```bash
    $ cd monitoring-hosts/
    $ sudo pip install -r requirements.txt --no-cache-dir
    ```

Configuration
-------------


## Backends

You can use two types of configuration, no backend (the output will be written in the output_dir),
or use monaca (the output will be directlly published.

### No backend
`default.cfg`
```
[DEFAULT]
type=CPU
name=sysbench
# Full path to access the sysbench.json file that is in sample directory.
parameters=/path/sysbench.json
output_dir=/tmp
backend=
```

### Monasca backend
`sample/default_monasca.cfg`
```
[DEFAULT]
type=CPU
name=sysbench
# Full path to access the sysbench.json file that is in sample directory.
parameters=/path/sysbench.json
output_dir=/tmp
backend=OS_MONASCA

[monasca]
username=<@username>
password=<@password>
project_name=<@project_name>
auth_url=<@auth_url>
monasca_api_version=v2_0
```

## Sysbench Parameters

You can set the `number_of_threads` and the `max_prime`parameters used by sysbench by
editing the `sysbench.json` file located in the `sample`directory.

Usage
-----

- Help command

```ubuntu@host:~/monitoring-hosts/monitoring$ python run.py -h```
```
usage: python monitoring.py [-h] {start,restart,stop} ...

Monitoring Host Daemon

positional arguments:
  {start,restart,stop}  Operation with the monitoring host daemon. Accepts any
                        of these values: start, stop, restart
    start               Starts python monitoring.py daemon
    restart             Restarts python monitoring.py daemon
    stop                Stops python monitoring.py daemon

optional arguments:
  -h, --help            show this help message and exit
```

* Start command

```ubuntu@host:~/monitoring-hosts/monitoring$ python run.py start -h```
```
usage: python monitoring.py start [-h] -time TIME_INTERVAL
                                  [-conf CONFIGURATION]

optional arguments:
  -h, --help            show this help message and exit
  -time TIME_INTERVAL, --time_interval TIME_INTERVAL
                        Number of seconds to wait before run the Monitoring
                        Daemon again.(Integer)
  -conf CONFIGURATION, --configuration CONFIGURATION
                        Filename with all benchmark information
```

* Stop command

```ubuntu@host1:~/monitoring-hosts/monitoring$ python run.py stop -h```
```
usage: python monitoring.py stop [-h] [-conf CONFIGURATION]

Stops the daemon if it is currently running.

optional arguments:
  -h, --help            show this help message and exit
  -conf CONFIGURATION, --configuration CONFIGURATION
                        Filename with all benchmark information
```

* Restart command

```ubuntu@host1:~/monitoring-hosts/monitoring$ python run.py restart -h```
```
usage: python monitoring.py restart [-h] -time TIME_INTERVAL
                                    [-conf CONFIGURATION]

optional arguments:
  -h, --help            show this help message and exit
  -time TIME_INTERVAL, --time_interval TIME_INTERVAL
                        Number of seconds to wait before run the Monitoring
                        Daemon again. (Integer)
  -conf CONFIGURATION, --configuration CONFIGURATION
                        Filename with all benchmark information
```

* Running

```root@host:~# python monitoring/run.py start -conf sample/default_monasca.cfg -time 1800```

```root@hots:~# python monitoring/run.py stop -conf sample/default.cfg ```

