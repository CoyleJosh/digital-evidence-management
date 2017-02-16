inputStringCd = raw_input("Input: ")
logFile = 'log.txt'

def changedirectorycheck(cdCheck):
    fileHandle = open(logFile, 'r')
    lineList = fileHandle.readlines()
    fileHandle.close()
    #splitInputCd = inputStringCd.split(" ")
    print lineList[-1]

changedirectorycheck(inputStringCd)
