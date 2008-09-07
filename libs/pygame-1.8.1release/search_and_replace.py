#!/usr/bin/python

import sys
import string


def useage():
  print ""
  print "useage: search_and_replace.py searchword replaceword <filenames>"
  print ""

if(__name__ == "__main__"):
  if(len(sys.argv) <= 2):
    useage()

  else:

    try:
      searchword = sys.argv[1]
      replaceword = sys.argv[2]
      

    except:
      print "Error: Could not read the number of spaces that you supplied."
      useage()
      sys.exit(-1)
    

    for x in sys.argv[3:]:
      
      try:
        f = open(x)
      except:
        print "could not open file:" + x
        print "continuing with other files."
        break
      
      file_contents = f.read()
      new_contents = file_contents.replace(searchword, replaceword)

      f.close()
      # try to write to the file.
      
      try:
	f = open(x, "w")
      except:
	print "Could not write file:" +x
	print "Continuing with other files."
	break
      f.write(new_contents)
      f.close()
          


