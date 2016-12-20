import json
import sys
import time

from daemon import Daemon
from datetime import datetime
from benchmarks.sysbench import SysbenchCPU

class MonitoringDaemon(Daemon):

    def __init__(self, pidfile, configuration):
        try:
            with open(configuration) as conf:
                self.configuration = json.load(conf)
                conf.close()
            self.output_dir = self.configuration['output_dir']
            super(MonitoringDaemon, self).__init__(pidfile)
        except Exception as e:
            print e.message
            sys.exit(1)

    def get_benchmarks(self):
        selected = {}
        if self.configuration.has_key('benchmarks'):
            all_benchmarks = self.configuration['benchmarks']
            for bench_type in all_benchmarks:
                if any(all_benchmarks[bench_type]):
                    selected[bench_type] = all_benchmarks[bench_type]
            return selected
        else:
            return selected

    def run_cpu(self, timestamp, args):
        if args.has_key('sysbench'):
            if (args['sysbench'].has_key('max_prime') and
                    args['sysbench'].has_key('number_of_threads') ):

                for num_thread in args['sysbench']['number_of_threads']:
                    print num_thread
                    syscpu = SysbenchCPU(num_thread,
                            args['sysbench']['max_prime'], timestamp,
                            self.output_dir)
                    syscpu.execute()

    def run(self):
        selected_benchmarks = self.get_benchmarks()
        timestamp_begin_execution = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S")
        if selected_benchmarks.has_key('cpu'):
            self.run_cpu(timestamp_begin_execution, selected_benchmarks['cpu'])

