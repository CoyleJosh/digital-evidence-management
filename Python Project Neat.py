import base64, getpass, os, socket, sys, traceback, shlex, datetime
from paramiko.py3compat import input
import paramiko
from time import gmtime, strftime

# ------------------------------------------------------------------------------

#Global Variable Definitions
#Dictionary translation for Linux commands
translationInput = ["makedir", "files", "changedir", "printdir", "copy", "move", "md5", "sha1"]
translationOutput = ["mkdir", "ls", "cd", "pwd", "sftp", "sftp", "md5sum", "sha1sum"]
# Paramiko client configuration
UseGSSAPI = True #Figure out what these do
DoGSSAPIKeyExchange = True #^^
port = 22
logFile = 'log.txt'
dirPath = os.path.dirname(os.path.realpath(__file__))
innerDirPath = (dirPath + "\Evidence Folder")
remoteDirTest = "/private/var/mobile/Media/DCIM/100APPLE/IMG_0012.JPG"

#Function Definitions

def directorySetup() :
    if not os.path.exists(dirPath + "\Evidence Folder") :
        os.makedirs("Evidence Folder")
    else :
        print ("Directory already setup.")

def verify(verifyFile) :
    preTransferMD5 = ""
    postTransferMD5 = ""
    if preTransferMD5 == postTransferMD5 :
        return true
    else :
        return false
    
def translate(promptInput) :
    splitInput = promptInput.split(" ")
    splitOutput = []
    promptString = ""
    for i in splitInput :
        if i not in translationInput :
            splitOutput.append(i)
        else :
            splitOutput.append(translationOutput[translationInput.index(i)])
    #print splitOutput
    promptString = " ".join(splitOutput)
    #print promptString
    return promptString


def shell_loop():
    SHELL_STATUS_RUN = 1 # for running the loop
    
    while SHELL_STATUS_RUN :
        target = open(logFile, 'a')
        prompt = raw_input('%s@%s: ' % (username, hostname))
        directorySetup()
        if prompt == "close" :
            SHELL_STATUS_RUN = 0        
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
        username + '@' + hostname + ':' + str(port) + ' >> ' + prompt + '\n')
        if translate(prompt) == "sftp" :
            #target.close()
            ###
            #SSHclient = paramiko.SSHClient()

            transport = paramiko.Transport((hostname, port))
            transport.connect(username, password)
            print " !*!*!*! Connecting !*!*!*!"
            #client.connect(hostname, port, username, password)

            #SSHclient.load_system_host_keys()
            #SSHclient.set_missing_host_key_policy(paramiko.WarningPolicy())

            ###

            #trans.connect(hostname, port, username, password, allow_agent = True)
            sftp = paramiko.SFTPClient.from_transport(client)
            print "Connected "
            sftp.get(remoteDirTest, innerDirTest)
        output = client_stdout.read()
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
        username + '@' + hostname + ':' + str(port) + ' << ' + output)
        print "Output: ", output

    target.close()

#Start

# get hostname
username = ""
if len(sys.argv) > 1:
    hostname = sys.argv[1]
    if hostname.find("@") >= 0:
        username, hostname = hostname.split("@")
else:
    hostname = input("Hostname: ")
if len(hostname) == 0:
    print("Hostname required")
    sys.exit(1)

if hostname.find(":") >= 0:
    hostname, portstr = hostname.split(":")
    port = int(portstr)
    
# get username
if username == '':
    default_username = getpass.getuser()
    username = input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username
    password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

print hostname, username, password

try:
    #client = paramiko.SSHClient()
    #client.load_system_host_keys()
    #client.set_missing_host_key_policy(paramiko.WarningPolicy())
    #print " !*!*!*! Connecting !*!*!*!"
    #client.connect(hostname, port, username, password, allow_agent = True)
    #print "Connected "
    #chan = client.invoke_shell()
    #print(repr(client.get_transport()))
    shell_loop()
    chan.close()
    client.close()

except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        client.close()
    except:
        pass
    sys.exit(1)




