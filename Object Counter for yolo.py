# This cell can be used to count the instance of single object in the provided directory containing using
# YOLO text file

import os

# Method to read the text file in the given path. It returns the all the lines in the file
def read_text_file(file_path):
    with open(file_path, 'r') as f:
      Lines = f.readlines()
      return Lines

# Method used to count the instance of each object in the given text file.
def match_object(lines, mydict):
  for each_line in lines:
    if int(each_line[0]) not in mydict:
        mydict[int(each_line[0])] = 1

    else:
        mydict[int(each_line[0])] += 1

  
  return mydict

# Method to read all the text file in the given directory inorder to count the instance of given class.
def match_all(path):
    mydict = {}
    for file in os.listdir(path):
        if file.endswith(".txt"):
            lines = read_text_file(path + "/" + file)
            mydict = match_object(lines, mydict)
    return mydict

# Add the path
path = ""
print(match_all(path))
