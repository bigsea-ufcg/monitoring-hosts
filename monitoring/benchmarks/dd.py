import socket
import subprocess


class DDdisk():

    def __init__(self, start_time, output_dir):
        self.start_time = start_time
        self.output_dir = output_dir

    def execute(self):

        write_outputfile_name = "{0}/{1}_{2}_ddwrite.txt".format(
                self.output_dir, self.start_time, socket.gethostname())
        read_outputfile_name = "{0}/{1}_{2}_ddread.txt".format(
                self.output_dir, self.start_time, socket.gethostname())

        cmd_write = "dd if=/dev/zero of=/tmp/dd_test bs=1024MB count=1 >> {0}"\
                .format(write_outputfile_name)
        cmd_read = "dd if=/tmp/dd_test of=/dev/null bs=1024MB count=1 >> {0}"\
                .format(read_outputfile_name)
        subprocess.call(cmd_write, shell=True)
        subprocess.call(cmd_read, shell=True)
        remove_files = "rm -rf /tmp/dd_test"
        subprocess.call(remove_files, shell=True)
