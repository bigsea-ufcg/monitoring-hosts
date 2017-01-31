import socket
import subprocess


class SysbenchCPU():
    """
    """

    def __init__(self, num_threads, max_prime, start_time, output_dir):
        """ """
        self.start_time = start_time
        self.max_prime = max_prime
        self.num_threads = num_threads
        self.output_dir = output_dir

    def execute(self):
        """ Run sysbench cpu test with specified parameters
        """

        file_name = "{0}/{1}_{2}_sysbench_cpu_{3}.txt".format(
                    self.output_dir, self.start_time, socket.gethostname(),
                    self.num_threads)
        params = "--test=cpu --num-threads={0} --cpu-max-prime={1}".format(
                 self.num_threads, self.max_prime)
        cmd = "sysbench " + params + " run >> {0}".format(file_name)
        subprocess.call(cmd, shell=True)


class SysbenchMemory():
    """
    """

    def __init__(self, access, operation, block, start_time, output_dir):
        self.access = access
        self.operation = operation
        self.block_size = block
        self.start_time = start_time
        self.output_dir = output_dir

    def execute(self):
        """
        """
        file_name = "{0}/{1}_{2}_sysbench_memory_{3}_{4}.txt".format(
            self.output_dir, socket.gethostname(), self.operation,
            self.access)
        params = "--test=memory --memory-block=size={0} --memory-oper={1} \
                 --memory-access-mode={2}".format(
                 self.block_size, self.operation, self.access)
        cmd = "sysbench " + params + " run >> {0}".format(file_name)
        print cmd
        subprocess.call(cmd, shell=True)
