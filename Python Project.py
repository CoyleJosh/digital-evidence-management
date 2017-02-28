import base64, getpass, os, socket, sys, traceback, shlex, datetime, SSHLibrary, paramiko, time
from stat import S_ISDIR
from paramiko.py3compat import input
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
#dirPath = os.path.dirname(os.path.realpath(__file__))
innerDirPath = (r"C:\Users\admin\Desktop\Evidence")
remoteDirTest = "/private/var/mobile/Media/DCIM/117APPLE/IMG_7294.PNG"

#Function Definitions

def directorySetup() :
    if not os.path.exists(r"C:\Users\admin\Desktop\Evidence") :
        os.makedirs(r"C:\Users\admin\Desktop\Evidence")
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
        fileNameFind = prompt.split()
        directorySetup()
       
        if (prompt == "close") :
            #client_stdin, client_stdout, client_stderr = client.exec_command(translate(prompt))
            #output = client_stdout.read()
            SHELL_STATUS_RUN = 0        
            target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Input
            username + '@' + hostname + ':' + str(port) + ' >> ' + prompt + '\n')#
            output = client_stdout.read()
            target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Output
            username + '@' + hostname + ':' + str(port) + ' << ' + "Exiting Program." + '\n')#  
        elif (translate(prompt) == "sftp") :
            #client_stdin, client_stdout, client_stderr = client.exec_command(translate(prompt))
            #output = client_stdout.read()
            trans = paramiko.Transport((hostname, port))
            sftp = client.open_sftp()
            sftp.chdir("/private/var/mobile/Media/DCIM/117APPLE")
            #print sftp.listdir("/private/var/mobile/Media/DCIM/117APPLE")
            fileName = input("Filename for SFTP transfer: ")
            fileTransferPath = (r"C:\Users\admin\Desktop\Evidence\\" + fileName)
            sftp.get(fileName, fileTransferPath)
            target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Input
            username + '@' + hostname + ':' + str(port) + ' << ' + "Transferring " + fileName + " to " + innerDirPath + "." + '\n')#
            target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Output
            username + '@' + hostname + ':' + str(port) + ' >> ' + "Transferred " + fileName + " to " + innerDirPath + "." + '\n')#
            print ("Successfully transferred " + fileName + " to " + innerDirPath + ".")
            sftp.close()
        elif (translate(prompt) == "md5") :
            print ("This has not been successfully implemeted yet.")
            #verify function call
        client_stdin, client_stdout, client_stderr = client.exec_command(translate(prompt))
        output = client_stdout.read()
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
        username + '@' + hostname + ':' + str(port) + ' << ' + output)
        print "Output: ", output

    target.close()























# setting up logging
#paramiko.util,log_to_file("demo_simple.log")
#this comment is to test the use of GitHub


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

#print hostname, username, password

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print " !*!*!*! Connecting !*!*!*!"
    client.connect(hostname, port, username, password, allow_agent = True)
    print "Connected "
    chan = client.invoke_shell()
    #print(repr(client.get_transport()))
    #shell = client.invoke_shell() See if this change prevents subprocesses being created

    shell_loop()


    

    #print "Error: ", client_stderr.read()
    chan.close()
    client.close()
    #input = close
    #close

except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        client.close()
        target.close()
    except:
        pass
    sys.exit(1)




#def translate(prompt) :
#    splitInput = prompt.split(" ")
#    splitOutput = []
#    promptString = ""
#    for i in splitInput :
#        if i not in translationInput :
 #           splitOutput.append(i)
 ##       else :
 #           splitOutput.append(translationOutput[translationInput.index(i)])
 #   for i in splitOutput :
  ##      promptString + i
  #      print promptString
  #  
  #  return splitOutput


#def PolicyWarning():
#    paramiko.WarningPolicy()
#    paramiko.AutoAddPolicy()
    
# now, connect and use paramiko Client to negotiate SSH2 across the connection
#try:
#    client = paramiko.SSHClient()
#    client.load_system_host_keys()
#    client.set_missing_host_key_policy(paramiko.WarningPolicy())
#    print('*** Connecting...')
#    if not UseGSSAPI or (not UseGSSAPI and not DoGSSAPIKeyExchange):
#        client.connect(hostname, port, username, password)
#    else:
#        # SSPI works only with the FQDN of the target host
#        hostname = socket.getfqdn(hostname)
 #       try:
 ##           client.connect(hostname, port, username, gss_auth=UseGSSAPI,
 #                          gss_kex=DoGSSAPIKeyExchange)
 #       except Exception:
 #           password = getpass.getpass('Password for %s@%s: ' % (username, hostname))
  #          client.connect(hostname, port, username, password)
##
#    chan = client.invoke_shell()
#    print(repr(client.get_transport()))
#    print('*** Here we go!\n')
 #   interactive.interactive_shell(chan)
 #   chan.close()
 ##   client.close()
 
#except Exception as e:
#    print('*** Caught exception: %s: %s' % (e.__class__, e))
#    traceback.print_exc()
#    try:
#        client.close()
#    except:
#        pass
#    sys.exit(1)



#paramiko.util.log_to_file('ssh.log') # sets up ssh logging
#client = paramiko.SSHClient()
#client.load_system_host_keys()
#client.set_missing_host_key_policy
#client.connect('127.0.0.1', username='root', password='baconpancakes 22')
#stdin, stdout, stderr = client.exec_command('ls -l')
