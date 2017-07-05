import os
import json
import sys
import time
import ConfigParser

from daemon import Daemon
from datetime import datetime
from benchmarks.sysbench import SysbenchCPU


class MonitoringDaemon(Daemon):
    """
    Monitoring Daemon Class
    Responsible for monitor the system with the select configuration.
    """

    def __init__(self, pidfile, configuration, sleep):
        try:
            self.sleep = sleep
            self.configuration = ConfigParser.RawConfigParser()
            self.configuration.read(configuration)

            try:
                out_dir = self.configuration.get('DEFAULT', 'output_dir')
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                self.output_dir = out_dir
            except Exception as path_ex:
                print path_ex.message
                sys.exit(1)
            super(MonitoringDaemon, self).__init__(pidfile)
        except Exception as e:
            print e.message
            sys.exit(1)

        print "Monitoring Daemon"

    def run_cpu(self, name, params, timestamp):
        """
        Function to run cpu benchmarks
        :param name: the benchmark name
        :param params: the parameters necessary to run the benchmark
        :param timestamp: the start timestamp
        """
        print 'start run_cpu'
        if name == 'sysbench':
            if ('max_prime' in params and 'number_of_threads' in params):
                for num_thread in params['number_of_threads']:
                    print "number of threads %s" % num_thread
                    syscpu = SysbenchCPU(self.configuration, num_thread,
                                         params['max_prime'],
                                         timestamp)
                    syscpu.execute()
        print 'end run_cpu'

    def run(self):

        name = self.configuration.get('DEFAULT', 'name')
        with open(self.configuration.get('DEFAULT', 'parameters')) as params:
            parameters = json.load(params)
            params.close()
        while True:
            timestamp_begin = datetime.now()
            timestamp_begin_execution = timestamp_begin.strftime(
                "%Y-%m-%dT%H:%M:%S")
            if self.configuration.get('DEFAULT', 'type') == 'CPU':
                self.run_cpu(name, parameters, timestamp_begin_execution)

            print "waitting %s seconds before running again" % self.sleep
            time.sleep(self.sleep)
