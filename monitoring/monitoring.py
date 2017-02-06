import os
import json
import sys
import time

from daemon import Daemon
from datetime import datetime
from benchmarks.sysbench import SysbenchCPU, SysbenchMemory
from benchmarks.dd import DDdisk
from threading import Thread


class MonitoringDaemon(Daemon):

    def __init__(self, pidfile, configuration, sleep):
        try:
            self.sleep = sleep
            with open(configuration) as conf:
                self.configuration = json.load(conf)
                conf.close()
            try:
                if not os.path.exists(self.configuration['output_dir']):
                    os.mkdir(self.configuration['output_dir'])
                self.output_dir = self.configuration['output_dir']
            except Exception as path_ex:
                print path_ex.message
                sys.exit(1)
            super(MonitoringDaemon, self).__init__(pidfile)
        except Exception as e:
            print e.message
            sys.exit(1)

    def get_benchmarks(self):
        selected = {}
        if 'benchmarks' in self.configuration:
            all_benchmarks = self.configuration['benchmarks']
            for bench_type in all_benchmarks:
                if any(all_benchmarks[bench_type]):
                    selected[bench_type] = all_benchmarks[bench_type]
            return selected
        else:
            return selected

    def run_cpu(self, timestamp, args):
        print 'start run_cpu'
        if 'sysbench' in args:
            if ('max_prime' in args['sysbench'] and
                    'number_of_threads' in args['sysbench']):

                for num_thread in args['sysbench']['number_of_threads']:
                    print num_thread
                    syscpu = SysbenchCPU(num_thread,
                                         args['sysbench']['max_prime'],
                                         timestamp, self.output_dir)
                    syscpu.execute()
        print 'end run_cpu'

    def run_memory(self, timestamp, args):
        print 'start run_memory'
        if 'sysbench' in args:
            if ("block_size" in args['sysbench'] and
                    "operation" in args['sysbench'] and
                    "acess" in args['sysbench']):
                for acess_type in args['sysbench']['acess']:
                    for op in args['sysbench']['operation']:
                        sysmem = SysbenchMemory(acess_type, op,
                                                args['sysbench']['block_size'],
                                                timestamp, self.output_dir)
                        sysmem.execute()
        print 'end run_memory'

    def run_disk(self, timestamp, args):
        print 'start run_disk'
        if 'dd' in args:
            dd_benchmark = DDdisk(timestamp, self.output_dir)
            dd_benchmark.execute()
        print 'end run_disk'

    def run(self):
        selected_benchmarks = self.get_benchmarks()
        timestamp_begin_execution = datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S")
        while True:
            timestamp_begin = datetime.now()
            timestamp_begin_execution = timestamp_begin.strftime(
                "%Y-%m-%dT%H:%M:%S")
            if 'cpu' in selected_benchmarks:
                Thread(target=self.run_cpu(timestamp_begin_execution,
                       selected_benchmarks['cpu']))
            if 'disk' in selected_benchmarks:
                Thread(target=self.run_disk(timestamp_begin_execution,
                       selected_benchmarks['disk']))
            print "waitting %s seconds before running again" % self.sleep
            time.sleep(self.sleep)
