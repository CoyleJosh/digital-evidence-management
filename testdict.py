inputString = raw_input("Input: ")

def translate(promptInput) :
    translationInput = ["makedir", "files", "changedir", "printdir", "copy", "move", "md5", "sha1"]
    translationOutput = ["mkdir", "ls", "cd", "pwd", "cp", "cp", "md5sum", "sha1sum"]
    splitInput = inputString.split(" ")
    splitOutput = []
    promptString = ""
    for i in splitInput :
        if i not in translationInput :
            splitOutput.append(i)
        else :
            splitOutput.append(translationOutput[translationInput.index(i)])
    #print splitOutput
    promptString = " ".join(splitOutput)
    print promptString
    return splitOutput

translate(inputString)
