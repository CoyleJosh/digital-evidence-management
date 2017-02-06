import base64, getpass, os, socket, sys, traceback, shlex, datetime
from paramiko.py3compat import input
import paramiko
from time import gmtime, strftime

# ------------------------------------------------------------------------------

#Global Variable Definitions
#Dictionary translation for Linux commands
translationInput = ["makedir", "files", "changedir", "printdir", "copy", "move", "md5", "sha1"]
translationOutput = ["mkdir", "ls", "cd", "pwd", "cp", "cp", "md5sum", "sha1sum"]
# Paramiko client configuration
UseGSSAPI = True #Figure out what these do
DoGSSAPIKeyExchange = True #^^
port = 22
logFile = 'log.txt'

#Function Definitions

def verify(verifyFile) :
    preTransferMD5 = ""
    postTransferMD5 = ""
    
def translate(promptInput) :
    #translationInput = ["makedir", "files", "changedir", "printdir", "copy", "move", "md5", "sha1"]
    #translationOutput = ["mkdir", "ls", "cd", "pwd", "cp", "cp", "md5sum", "sha1sum"]
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
        #print prompt
        if prompt == "close" :
            SHELL_STATUS_RUN = 0        
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
        username + '@' + hostname + ':' + str(port) + ' >> ' + prompt + '\n')
        #print(prompt) # To show whether the whole command is being interpreted coorectly
        # cmd_tokens = nltk.word_tokenize(prompt)
        # This is the point where commands will be interpreted by the definitions of the program
        # This part of the program hasnt been written yet.
        # This needs to be done using the function translate() defined above
        # it takes the user input, seperates using spaces, translates, then returns the splitOutput;
        # the list of commands. -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        
        client_stdin, client_stdout, client_stderr = client.exec_command(translate(prompt))
        #print translate(prompt)
        # The path to where images are stored on the test device is:
        # ./private/var/mobile/Media/DCIM/100APPLE/ ls -l"
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

print hostname, username, password

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    print " !*!*!*! Connecting !*!*!*!"
    client.connect(hostname, port, username, password, allow_agent = True)
    print " Connected "
    chan = client.invoke_shell()
    print(repr(client.get_transport()))
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
