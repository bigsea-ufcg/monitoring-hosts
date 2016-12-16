import argparse
import sys
import time
import json

from daemon import Daemon
from datetime import datetime
from benchmarks.sysbench import SysbenchCPU

class MonitoringDaemon(Daemon):

    def __init__(self, pidfile, configuration):
        try:
            self.configuration = json.load(configuration)
        except Exception as e:
            print e.message
            sys.exit(1)
        super(MonitoringDaemon, self).__init__(pidfile)


    def run_sysbench(self, timestamp):
        print type(self.configuration)
        print self.configuration



    def run(self):
        timestamp_begin_execution = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S")
        self.run_sysbench(timestamp_begin_execution)



def command_line_parser():
    parser = argparse.ArgumentParser(prog='python monitoring.py',
            description='Monitoring Host Daemon')
    subparsers = parser.add_subparsers(help= 'Operation with the monitoring \
            host daemon. Accepts any of these values: start, stop, restart',
            dest='operation')

    start = subparsers.add_parser("start", help='Starts %(prog)s daemon')
    start.add_argument('-conf','--configuration',
            help='File with all information about cloud providers',
            required=True)
    start.add_argument('-pid','--pid_filename',
            help='Maximum lifetime of each instance (in minutes)',
            required=True)

    restart = subparsers.add_parser("restart", help='Restarts %(prog)s daemon')
    restart.add_argument('-conf','--configuration',
            help='File with all information about cloud providers',
            required=True)
    restart.add_argument('-pid','--pid_filename',
            help='Maximum lifetime of each instance (in minutes)',
            required=True)

    stop = subparsers.add_parser("stop", help='Stops %(prog)s daemon',
            description='Stops the daemon if it ts currently running.')

    return parser



def main():
    cmd = command_line_parser()
    arguments = cmd.parse_args()
    monitoring = MonitoringDaemon('/tmp/monitoring-daemon.pid','conf.json')
    if arguments.operation == 'start':
        monitoring.start()
    elif arguments.operation == 'stop':
        monitoring.stop()
    elif arguments.operation == 'restart':
        monitoring.restart()
    else:
        print "Unknown command"
        sys.exit(2)


if __name__ == '__main__':
    main()

