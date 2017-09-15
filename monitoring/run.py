import argparse
import os
import sys

from monitoring import MonitoringDaemon


def command_line_parser():
    """ Function that add command line arguments to the daemon.
    :return: argument parser
    """
    parser = argparse.ArgumentParser(prog='python monitoring.py',
                                     description='Monitoring Host Daemon')
    subparsers = parser.add_subparsers(help='Operation with the monitoring \
            host daemon. Accepts any of these values: start, stop, restart',
                                       dest='operation')

    start = subparsers.add_parser("start", help='Starts %(prog)s daemon')
    start.add_argument('-time', '--time_interval', help='Number of seconds \
            to wait before run the Monitoring Daemon again.(Integer)',
                       required=False)
    start.add_argument('-conf', '--configuration', help='Filename with all \
            benchmark information', required=True)

    restart = subparsers.add_parser("restart", help='Restarts %(prog)s daemon')
    restart.add_argument('-time', '--time_interval', help='Number of seconds \
            to wait before run the Monitoring Daemon again. (Integer)',
                         required=False)
    restart.add_argument('-conf', '--configuration', help='Filename with all \
            benchmark information', required=True)

    stop = subparsers.add_parser("stop", help='Stops %(prog)s daemon',
                                 description='Stops the daemon if it is \
                                         currently running.')
    stop.add_argument('-conf', '--configuration', help='Filename with all \
            benchmark information', required=True)
    return parser


def validate_cmd(arguments):
    """ Function to validate the command line
    :param arguments: comand line arugments to validate
    :return: True if arguments are valid False otherwise
    """
    if (arguments.operation == 'start' or arguments.operation == 'restart' or
            arguments.operation == 'stop'):
        try:
            if hasattr(arguments, 'configuration'):
                if not os.path.isfile(arguments.configuration):
                    message = ("Couldn't find configuration file %s" %
                               arguments.configuration)
                    print message
                    raise Exception(message)
            else:
                message = "Please provide a configuration file"
                print message
                raise Exception(message)

            if hasattr(arguments, 'time_interval') and arguments.time_interval:
                if not arguments.time_interval.isdigit():
                    message = "time/time_interval should be integer"
                    print message
                    raise Exception(message)
                else:
                    arguments.time_interval = float(arguments.time_interval)
            else:
                arguments.time_interval = 0

            return arguments
        except Exception as e:
            print e.message
            sys.exit(2)
    else:
        print "Unknown command"
        sys.exit(2)



def main():
    """
    Function to start the daemon
    """
    cmd = command_line_parser()
    arguments = validate_cmd(cmd.parse_args())
    cwd = os.getcwd()
    pid = cwd + '/monitoring_daemon.pid'

    monitoring = MonitoringDaemon(pid,
                                  arguments.configuration,
                                  arguments.time_interval)

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
