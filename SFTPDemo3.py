import paramiko
import SSHLibrary
from stat import S_ISDIR
server, username, password = ('127.0.0.1', 'root', 'Baconpancakes')
ssh = paramiko.SSHClient()
paramiko.util.log_to_file("ssh.log")
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')
print "output", ssh_stdout.read() #Reading output of the executed command
error = ssh_stderr.read()
#Transfering files to and from the remote machine
sftp = ssh.open_sftp()
#print sftp.getcwd()
#print sftp.get_channel()
#print sftp.listdir("/home")
sftp.chdir("/private/var/mobile/Media/DCIM/117APPLE")
print sftp.listdir("/private/var/mobile/Media/DCIM/117APPLE")
sftp.get("IMG_7316.MOV", r"C:\Users\admin\Desktop\IMG_7316.MOV")  #---> facing problem here
sftp.close()
ssh.close()
