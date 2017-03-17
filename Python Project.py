import getpass, sys, paramiko, hashlib, os #base63, socket, traceback, shlex, datetime, sshlibraru, time #import base64, getpass, os, socket, sys, traceback, shlex, datetime, SSHLibrary, paramiko, time, hashlib
from stat import S_ISDIR
from paramiko.py3compat import input
from time import gmtime, strftime
from Tkinter import *

# ------------------------------------------------------------------------------

#Global Variable Definitions
#Dictionary translation for Linux commands
translationInput = ["makedir", "files", "changedir", "printdir", "copy", "move",
                    "md5", "sha256"]
translationOutput = ["mkdir", "ls", "cd", "pwd", "sftp", "sftp", "md5sum",
                     "sha256sum"]
# Paramiko client configuration
UseGSSAPI = True #Figure out what these do
DoGSSAPIKeyExchange = True #^^
port = 22
logFile = 'log.txt'
#dirPath = os.path.dirname(os.path.realpath(__file__))
innerDirPath = (r"C:\Users\Josh\Desktop\Evidence")
remoteDirTest = "/private/var/mobile/Media/DCIM/117APPLE/"
target = open(logFile, 'a')
validated = False
hostname = ""
username = ""
password = ""
client = ""

#Function Definitions

def establishConnection(hostname, username, password) :
    #print ("function has been called")
##    try:
    global client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#paramiko.WarningPolicy()) # This needs to be asked at the beginning of the program being run.

    print " !*!*!*! Connecting !*!*!*!"
    client.connect(hostname, port, username, password, allow_agent = True)
    print "Connected "
    chan = client.invoke_shell()
    shell_loop()
    #chan.close()
    #client.close()

##    except Exception as e:
##        print ("Exited.")
##        #try :
##            #traceback.print_exc()
##        #except UnboundLocalError :
##        #    print("Traceback cannot be printed.")
##        try:
##            client.close()
##            target.close()
##        except:
##            pass
##        sys.exit(1)

def directorySetup() :
    if not os.path.exists(r"C:\Users\Josh\Desktop\Evidence") :
        os.makedirs(r"C:\Users\Josh\Desktop\Evidence")
    else :
        print ("Directory already setup.")

def verifyMD5(veriFile) :
    try :
        commandTempPre = str("md5sum " + remoteDirTest + veriFile)
        commandTempPost = str(hashlib.md5(open(str(innerDirPath + "\\" + veriFile), 'rb').read()).hexdigest())
        print (commandTempPre)
        client_stdin, client_stdout, client_stderr = client.exec_command(commandTempPre)
        output = client_stdout.read()
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
        username + '@' + hostname + ':' + str(port) + ' << ' + output)
        splitOutput = output.split("  ")
        preTransferMD5 = splitOutput[0]
        postTransferMD5 = commandTempPost
        print (preTransferMD5, postTransferMD5)
        if preTransferMD5 == postTransferMD5 :
            print ("MD5 Match")
            return True
        else :
            print ("MD5 Mismatch")
            return False
    except IOError :
        print("The file could not be found.")
    except Error as e:
        print("An unexpected error occured.")
        print("Exception: %s: %s" % (e.__class__, e))

def verifySHA256(veriFile) :
    try :
        commandTempPre = str("sha256sum " + remoteDirTest + veriFile)
        commandTempPost = str(hashlib.sha256(open(str(innerDirPath + "\\" + veriFile), 'rb').read()).hexdigest())
        print (commandTempPre)
        client_stdin, client_stdout, client_stderr = client.exec_command(commandTempPre)
        output = client_stdout.read()
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
        username + '@' + hostname + ':' + str(port) + ' << ' + output)
        splitOutput = output.split("  ")
        preTransferSHA256 = splitOutput[0]
        postTransferSHA256 = commandTempPost
        print (preTransferSHA256, postTransferSHA256)
        if preTransferSHA256 == postTransferSHA256 :
            print ("SHA256 Match")
            return True
        else :
            print ("SHA256 Mismatch")
            return False
    except IOError :
        print("The file could not be found.")
    except :
        print("An unexpected error occured.")
    
def translate(promptInput) : # translate has no try and catch to prevent failure at the present
    splitInput = promptInput.split(" ")
    splitOutput = []
    print "splitInput: ", splitInput
    print "splitOutput: ", splitOutput
    promptString = ""
    for i in splitInput :
        if i not in translationInput :
            splitOutput.append(i)
        else :
            splitOutput.append(translationOutput[translationInput.index(i)])
    promptString = " ".join(splitOutput)
    return promptString


def shell_loop():
    print("Entered Shell")
    SHELL_STATUS_RUN = 1 # for running the loop
    directorySetup()
    
    while SHELL_STATUS_RUN :
        prompt = raw_input('%s@%s: ' % (username, hostname))
        #fileNameFind = prompt.split()
        #print fileNameFind
        translatedPrompt = translate(prompt)
        print translatedPrompt
        #global client
        if (translatedPrompt == "close") :
            try :
                SHELL_STATUS_RUN = 0        
                target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Input
                username + '@' + hostname + ':' + str(port) + ' >> ' + translatedPrompt + '\n')#
                output = client_stdout.read()
                target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Output
                username + '@' + hostname + ':' + str(port) + ' << ' + "Exiting Program." + '\n')#
            except :
                print("Exiting...")
        elif (translatedPrompt == "sftp") : # should be elif
            try :
                print("1")
                #trans = paramiko.Transport((hostname, port))
                print("2")
                sftp = client.open_sftp()
                print("3")
                sftp.chdir("/private/var/mobile/Media/DCIM/117APPLE")
                print("4")
                fileName = input("Filename for SFTP transfer: ")
                fileTransferPath = (r"C:\Users\Josh\Desktop\Evidence\\" + fileName)
                sftp.get(fileName, fileTransferPath)
                target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Input
                username + '@' + hostname + ':' + str(port) + ' << ' + "Transferring " + fileName + " to " + innerDirPath + "." + '\n')#
                target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +# Output
                username + '@' + hostname + ':' + str(port) + ' >> ' + "Transferred " + fileName + " to " + innerDirPath + "." + '\n')#
                print ("Successfully transferred " + fileName + " to " + innerDirPath + ".")
                sftp.close()
            except IOError :
                print("The file could not be found.")
            except :
                print("An unexpected error occured in SFTP.")

                
        elif (translatedPrompt == "md5sum") : #translatedPrompt.split(""))[0] == "md5sum"
            veriFile = input("Please type the name of the file to verify: ")
            validated = verifyMD5(veriFile)
        elif (translatedPrompt == "sha256sum") : #translatedPrompt.split(""))[0] == "sha256sum"
            veriFile = input("Please type the name of the file to verify: ")
            validated = verifySHA256(veriFile)
        else :
            try :
                client_stdin, client_stdout, client_stderr = client.exec_command(translatedPrompt)
                output = client_stdout.read()
                target.write(strftime("[%d-%m-%Y] [%H:%M:%S]" , gmtime()) + ' ' +
                username + '@' + hostname + ':' + str(port) + ' << ' + output)
                print "Output: ", output
            except :
                print("An unexpected error occured in non-dictionary command execution.")


    target.close()
    trans.close()
    client.close()

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-



class LoginFrame(Frame) :
    
    def __init__(self, master) :

        def submitLogin() :
            #global hostname
            hostname = UIHostname.get()
            #global username
            username = UIUsername.get()
            #global password
            password = UIPassword.get()
            print(hostname, username, password)

            establishConnection(hostname, username, password)
            
        UIHostname = StringVar()
        UIUsername = StringVar()
        UIPassword = StringVar()
        
        master.title("Digital Evidence Management System")
        master.geometry("210x100")
        master.maxsize(210, 100)
        master.minsize(210, 100)
        label1 = Label(master, text = "Hostname: ")
        label2 = Label(master, text = "Username: ")
        label3 = Label(master, text = "Password: ")
        
        entry1 = Entry(master, textvariable = UIHostname)
        entry2 = Entry(master, textvariable = UIUsername)
        entry3 = Entry(master, textvariable = UIPassword, show = "*")

        label1.grid(row = 0, sticky = E)
        label2.grid(row = 1, sticky = E)
        label3.grid(row = 2, sticky = E)

        entry1.grid(row = 0, column = 1)
        entry2.grid(row = 1, column = 1)
        entry3.grid(row = 2, column = 1)

        button1 = Button(root, text = "Login", command = submitLogin)
        #button1.bind("<Button-1>", submitLogin)
        button1.grid(row = 4)



root = Tk()
loginMenu = LoginFrame(root)
root.mainloop()


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#class CommandFrame(Frame) :
    
    #def __init__(self, master) :

        #def submitCommand() :


##            #global hostname
##            hostname = UIHostname.get()
##            #global username
##            username = UIUsername.get()
##            #global password
##            password = UIPassword.get()
##            print(hostname, username, password)
##
##            establishConnection(hostname, username, password)
##            
##        UIHostname = StringVar()
##        UIUsername = StringVar()
##        UIPassword = StringVar()
##        
##        master.title("Digital Evidence Management System")
##        master.geometry("210x100")
##        master.maxsize(210, 100)
##        master.minsize(210, 100)
##        label1 = Label(master, text = "Hostname: ")
##        label2 = Label(master, text = "Username: ")
##        label3 = Label(master, text = "Password: ")
##        
##        entry1 = Entry(master, textvariable = UIHostname)
##        entry2 = Entry(master, textvariable = UIUsername)
##        entry3 = Entry(master, textvariable = UIPassword, show = "*")
##
##        label1.grid(row = 0, sticky = E)
##        label2.grid(row = 1, sticky = E)
##        label3.grid(row = 2, sticky = E)
##
##        entry1.grid(row = 0, column = 1)
##        entry2.grid(row = 1, column = 1)
##        entry3.grid(row = 2, column = 1)
##
##        button1 = Button(root, text = "Login", command = submitLogin)
##        #button1.bind("<Button-1>", submitLogin)
##        button1.grid(row = 4)
##
##
##
##root = Tk()
##loginMenu = LoginFrame(root)
##root.mainloop()

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
### get hostname
##username = ""
##if len(sys.argv) > 1:
##    hostname = sys.argv[1]
##    if hostname.find("@") >= 0:
##        username, hostname = hostname.split("@")
##else:
##    hostname = input("Hostname: ")
##if len(hostname) == 0:
##    print("Hostname required")
##    sys.exit(1)
##
##if hostname.find(":") >= 0:
##    hostname, portstr = hostname.split(":")
##    port = int(portstr)
##    
### get username
##if username == '':
##    default_username = getpass.getuser()
##    username = input('Username [%s]: ' % default_username)
##    if len(username) == 0:
##        username = default_username
##    password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

#print hostname, username, password

sys.exit("Exited.")

    


