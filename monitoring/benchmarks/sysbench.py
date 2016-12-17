import socket, subprocess

class SysbenchCPU():
    """
    """

    def __init__(self, num_threads, max_prime, start_time):
        """ """
        self.start_time = start_time
        self.max_prime = max_prime
        self.num_threads = num_threads

    def execute(self):
        """ Run sysbench cpu test with specified parameters
        """

        file_name = "{0}_{1}_sysbench_cpu_{2}.txt".format(self.start_time,
                socket.gethostname(), self.num_threads)
        params = "--num-threads={0} --test=cpu --cpu-max-prime={1}".format(
                self.num_threads, self.max_prime)
        cmd = "sysbench " + params+ " run >> {0}".format(file_name)
        subprocess.call(cmd, shell=True)

