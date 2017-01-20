prompt = raw_input("Input: ")
translationInput = ["makedir", "files", "changedir", "printdir", "copy", "move", "md5", "sha1"]
translationOutput = ["mkdir", "ls", "cd", "pwd", "cp", "cp", "md5sum", "sha1sum"]
splitInput = prompt.split(" ")
splitOutput = []

#def translate(promptInput) :
#    for i in splitInput :
#        print "Looking for: ", i
#        for j in translationInput :
#            print "Checking: ", j
#            if i == j :
#                print "Found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#                #splitOutput at index location J in translationInput = the value at location J in splitOutput
#                splitOutput[translationInput.index(j)] = splitOutput[translationOutput.index(j)]
#                #splitOutput.append(translationOutput[translationInput.index(j)])
#        print "\n"
#        
#        
#        print splitOutput
        #        splitOutput.append(j)
        #splitOutput.append(i)
    #print splitOutput

#translate(splitInput)
    
            



#def translate(translation_map):
    #use raw input and split the sentence into a list of words
#    input_list = raw_input('Enter a phrase: ').split()
#    output_list = []

    #iterate the input words and append translation
    #(or word if no translation) to the output
#    for word in input_list:
#        translation = translation_map.get(word)
#        output_list.append(translation if translation else word)

    #convert output list back to string
#    return ' '.join(output_list)
#import sys

#prompt = raw_input("Input: ")

#translationList = dict("makedir" = "mkdir", "files" = "ls", "changedir" = "cd", "printdir" = "pwd", "copy" = "cp", "move" = "cp", "md5" = "md5sum")#

#def translate():
#    commandList = prompt.split(" ")
#    for i in commandList :
#        if i in translationList :
#            print "Found: ", i            
#        #print i
#    sys.exit(0)
#    
#translate()


