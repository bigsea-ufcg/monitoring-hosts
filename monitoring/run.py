import argparse
import os
import sys

from monitoring import MonitoringDaemon


def command_line_parser():
    parser = argparse.ArgumentParser(prog='python monitoring.py',
            description='Monitoring Host Daemon')
    subparsers = parser.add_subparsers(help= 'Operation with the monitoring \
            host daemon. Accepts any of these values: start, stop, restart',
            dest='operation')

    start = subparsers.add_parser("start", help='Starts %(prog)s daemon')
    start.add_argument('-dir', '--directory', help='The directory path \
            where will be the configuration file.', required=True)
    start.add_argument('-time', '--time_interval', help='Number of seconds \
            to wait before run the Monitoring Daemon again.(Integer)',
            required=True)
    start.add_argument('-conf', '--configuration', help='Filename with all \
            benchmark information, if not used will try to find a file named \
            conf.json in the directory of the argument -dir/--directory',
            required=False)

    restart = subparsers.add_parser("restart", help='Restarts %(prog)s daemon')
    restart.add_argument('-dir', '--directory', help='The directory path \
            where will be the configuration file.', required=True)
    restart.add_argument('-time', '--time_interval', help='Number of seconds \
            to wait before run the Monitoring Daemon again. (Integer)',
            required=True)
    restart.add_argument('-conf', '--configuration', help='Filename with all \
            benchmark information, if not used will try to find a file named \
            conf.json in the directory of the argument -dir/--directory',
            required=False)

    stop = subparsers.add_parser("stop", help='Stops %(prog)s daemon',
            description='Stops the daemon if it ts currently running.')
    stop.add_argument('-dir', '--directory', help='The directory path \
            where will be the configuration file.', required=True)

    stop.add_argument('-conf', '--configuration', help='Filename with all \
            benchmark information, if not used will try to find a file named \
            conf.json in the directory of the argument -dir/--directory',
            required=False)
    return parser


def validate_cmd(arguments):
    if (arguments.operation == 'start' or arguments.operation == 'restart' or
            arguments.operation == 'stop'):
        try:
            if os.path.isdir(arguments.directory) and os.path.exists(
                    arguments.directory):

                directory_name = arguments.directory
                if arguments.directory[-1] == '/':
                    directory_name =  arguments.directory[:-1]

                if arguments.configuration is not None:
                    if arguments.configuration[0] == '/':
                        file_path = (directory_name + arguments.configuration)
                    else:
                        file_path = (directory_name + '/' +
                                arguments.configuration)

                    if os.path.isfile(file_path):
                        arguments.configuration = file_path
                    else:
                        message = ("Can't find %s in %s directory" %
                                (arguments.configuration, directory_name))
                        raise Exception(message)

                else:
                    file_path = directory_name + '/conf.json'
                    if os.path.isfile(file_path):
                        arguments.configuration = file_path
                    else:
                        message = ("Can't find conf.json in %s directory" %
                                directory_name)
                        raise Exception(message)
            else:
                message = ("Can't find %s directory" % arguments.directory)
                raise Exception(message)

            if hasattr(arguments, 'time_interval'):
                if not arguments.time_interval.isdigit():
                    raise Exception("time/time_interval should be integer")
                else:
                    arguments.time_interval = float(arguments.time_interval)
            else:
                arguments.time_interval = 0

            return arguments
        except Exception as e:
            print e
            sys.exit(2)
    else:
        print "Unknown command"
        sys.exit(2)


def main():
    cmd = command_line_parser()
    arguments = validate_cmd(cmd.parse_args())
    if arguments.directory[-1] == '/':
        pid = arguments.directory + 'monitoring_daemon.pid'
    else:
        pid = arguments.directory + '/monitoring_daemon.pid'

    monitoring = MonitoringDaemon(pid,
        arguments.configuration, arguments.time_interval)

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
