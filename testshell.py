import sys, shlex, nltk, datetime
from time import gmtime, strftime

username = 'root' # remove these when implemented to main program
hostname = '127.0.0.1' # same as above
filename = 'log.txt' # log.txt will be the file name of the command log when transferred into the main program body
port = '22' # remove when implemented above

def shell_loop():
    SHELL_STATUS_RUN = 1 # for running the loop that allows the input of commands
    while SHELL_STATUS_RUN :
        target = open(filename, 'a')
        prompt = raw_input('%s@%s: ' % (username, hostname))
        if prompt == "close" :
            SHELL_STATUS_RUN = 0
        target.write(strftime("[%d-%m-%Y] [%H:%M:%S]", gmtime()) + ' ' + username + '@' + hostname + ':' + port + ' >>' + ' ' + prompt + '\n')
        cmd_tokens = nltk.word_tokenize(prompt)
        # print cmd_tokens
        target.close()
        
shell_loop()
