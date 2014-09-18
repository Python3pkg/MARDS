import sys, os, getopt
# the action below is a no-no in standard python, but it is done here for
# easy on-the-fly testing.

# this setup assumes that MARDS is NOT in the python library on the local
# machine, but is instead in a parrallel directory.
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))
#print sys.path
import MARDS

def main(argv):
   inputfile = ''
   sfile = 'mr recipe.MARDS-schema'
   debug = False
   warnings = False
   logs = False
   try:
      opts, args = getopt.getopt(argv,"hdwli:s:",["ifile=","sfile=","debug"])
   except getopt.GetoptError:
      print 'test.py -i <docfile> -s <schemafile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'export-test.py -i <ifile> -s <sfile> (default = mr recipe.MARDS-schema> -d <debug> -w -l'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-s", "--sfile"):
         sfile = arg
      elif opt in ("-d", "--debug"):
         debug = True
      elif opt in ("-w", "--warnings"):
         warnings = True
      elif opt in ("-l", "--logs"):
         logs = True

   print 'docfile is: ', inputfile
   print 'Schema file is: ', sfile
   with open(inputfile, 'r') as docfile:
      doc = docfile.read()
   with open(sfile, 'r') as schemafile:
      schema = schemafile.read()

   if debug == True:
      x,e = MARDS.ml.SCHEMA_to_rolne(schema)
   else:
      x,e = MARDS.string_to_rolne(doc, schema)
   
   print "FINAL:\n"
   print x._explicit()
   print "ERRORS:\n\n"
   if warnings:
        print "* warnings shown\n"
   else:
        print "* warnings NOT shown\n"
   if logs:
        print "* logs shown\n\n"
   else:
        print "* logs NOT shown\n\n"
   print "{:<9} {:<6} {:<10} {}\n".format("level", "source", "seq", "message")
   for entry in e:
        show = False
        if entry[0]=='[error]':
            show = True
        if entry[0]=='[warning]' and warnings:
            show = True
        if entry[0]=='[logs]' and logs:
            show = True
        if show:
            print "{:<9} {:<6} {:<10} {}\n".format(entry[0], entry[1], entry[2], entry[3])

   print "EOL\n"
if __name__ == "__main__":
   main(sys.argv[1:])



