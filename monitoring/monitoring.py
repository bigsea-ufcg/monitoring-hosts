import json
import sys
from daemon import Daemon
from datetime import datetime
from benchmarks.sysbench import SysbenchCPU

class MonitoringDaemon(Daemon):

    def __init__(self, pidfile, configuration):
        try:
            self.configuration = json.load(configuration)
        except Exception as e:
            print e.args
            print e.__unicode__
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

