# Monitoring Host Daemon

Daemon that monitors any physical host

### Benchmarks used

- Sysbench [CPU, Memory]
- dd [disk]

### Usage

* Help
```
ubuntu@host:~/monitoring-hosts/monitoring$ python run.py -h

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

* Start
```
ubuntu@host:~/monitoring-hosts/monitoring$ python run.py start -h
usage: python monitoring.py start [-h] -dir DIRECTORY -time TIME_INTERVAL
                                  [-conf CONFIGURATION]

optional arguments:
  -h, --help            show this help message and exit
  -dir DIRECTORY, --directory DIRECTORY
                        The directory path where will be the configuration
                        file.
  -time TIME_INTERVAL, --time_interval TIME_INTERVAL
                        Number of seconds to wait before run the Monitoring
                        Daemon again.(Integer)
  -conf CONFIGURATION, --configuration CONFIGURATION
                        Filename with all benchmark information, if not used
                        will try to find a file named conf.json in the
                        directory of the argument -dir/--directory

```

* Stop
```
ubuntu@host1:~/monitoring-hosts/monitoring$ python run.py stop -h
usage: python monitoring.py stop [-h] -dir DIRECTORY [-conf CONFIGURATION]

Stops the daemon if it ts currently running.

optional arguments:
  -h, --help            show this help message and exit
  -dir DIRECTORY, --directory DIRECTORY
                        The directory path where will be the configuration
                        file.
  -conf CONFIGURATION, --configuration CONFIGURATION
                        Filename with all benchmark information, if not used
                        will try to find a file named conf.json in the
                        directory of the argument -dir/--directory
```

* Restart
```
ubuntu@host1:~/monitoring-hosts/monitoring$ python run.py restart -h
usage: python monitoring.py restart [-h] -dir DIRECTORY -time TIME_INTERVAL
                                    [-conf CONFIGURATION]

optional arguments:
  -h, --help            show this help message and exit
  -dir DIRECTORY, --directory DIRECTORY
                        The directory path where will be the configuration
                        file.
  -time TIME_INTERVAL, --time_interval TIME_INTERVAL
                        Number of seconds to wait before run the Monitoring
                        Daemon again. (Integer)
  -conf CONFIGURATION, --configuration CONFIGURATION
                        Filename with all benchmark information, if not used
                        will try to find a file named conf.json in the
                        directory of the argument -dir/--directory

```
