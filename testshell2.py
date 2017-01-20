import sys, shlex, os

SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP = 0


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        # Display a command prompt
        sys.stdout.write('> ')
        sys.stdout.flush()

        # Read command input
        cmd = sys.stdin.readline()

        # Tokenize the command input
        cmd_tokens = tokenize(cmd)

        # Execute the command and retrieve new status
        status = execute(cmd_tokens)

def tokenize(string):
    return shlex.split(string)

def execute(cmd_tokens):
    os.execvp(cmd_tokens[0], cmd_tokens)
    return SHELL_STATUS_RUN
