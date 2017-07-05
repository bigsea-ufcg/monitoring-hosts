import sys
import time
import socket
import subprocess

from backend.monasca import MonascaMonitor


class SysbenchCPU():
    """ Class responsible to execute sysbench benchmark using CPU Test
        It can publish the total time in Monasca or generate a file with the
        sysbench output.
    """

    def __init__(self, configuration, num_threads, max_prime, start_time):
        """ """
        self.configuration = configuration
        self.start_time = start_time
        self.max_prime = max_prime
        self.num_threads = num_threads
        self.output_dir = configuration.get('DEFAULT', 'output_dir')
        self.backend = configuration.get('DEFAULT', 'backend')

    def execute(self):
        """ Run sysbench cpu test with specified parameters
        """

        params = "--test=cpu --num-threads={0} --cpu-max-prime={1}".format(
                 self.num_threads, self.max_prime)
        if self.backend == 'OS_MONASCA':
            monasca = MonascaMonitor(self.configuration)
            cmd = "sysbench " + params + " run"
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            if err is None:
                try:
                    split_out = out.split('\n')
                    total_time = None
                    for out_part in split_out:
                        if 'total time:' in out_part:
                            total_time = out_part.split(':')[1]
                            total_time = float(total_time.replace('s', ''))
                            metric = {
                                'name': 'sysbench.cpu.performance',
                                'value': total_time,
                                'timestamp': time.time() * 1000,
                                'dimensions': {
                                    'hostname': socket.getfqdn(),
                                    'benchmark': 'sysbench',
                                    'type': 'CPU',
                                    'threads': self.num_threads
                                }

                            }
                            monasca.send_metrics([metric])
                except Exception as e:
                    print e.message
            else:
                print "Sysbench error: %s" % err
                sys.exit(2)
        else:
            file_name = "{0}/{1}_{2}_sysbench_cpu_{3}.txt".format(
                self.output_dir, self.start_time, socket.gethostname(),
                self.num_threads
            )

            cmd = "sysbench " + params + " run >> {0}".format(file_name)
            subprocess.call(cmd, shell=True)
