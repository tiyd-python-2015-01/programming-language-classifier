__author__ = 'jasonaylward'

import os

#Create a jSON file that we'll write to
#or overwrite the existing file
jSONFile = open("plateContents.json", "w")

#Open the jSON Object
jSONString = "{"

#Get the names of each plate directory.
#These will be used as keys for each jSON pair
entries = os.listdir(".")
plates = [];
for entry in entries:
    if os.path.isdir(entry) and entry[:1] != ".":
        plates.append( entry)



for plate in plates:
    # plateString = "key":[ ...
    plateString = "\""+plate+"\":["
    for dir, subdirs, files in os.walk(plate):
        dir = dir[len(plate):]
        for file in files:
            #if the file is a .png image files, add to the array.
            if ".png" in file:
                fileString = "\"" + dir + "/" + file + "\","
                plateString = plateString + fileString
    #if string ends in a ',' then remove before adding ']'
    if plateString[-1:] == ",":
        plateString = plateString[:-1]

    #close plateString so it is "key":[...]
    plateString = plateString + "],"
    jSONString = jSONString + plateString


# delete the last comma in the list of files
if jSONString[-1:] == ",":
    jSONString = jSONString[:-1]

#Close the jSON Object
jSONString = jSONString+"}"

#print jSONString
jSONFile.write(jSONString)
jSONFile.close()