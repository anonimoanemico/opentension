#!/usr/bin/python

import export_db as dbExporter
import data_fetcher as dataFetcher
import sys, getopt, os

def create_dir(dir):
    try:
        os.stat(dir)
    except:
        print "Creating directory " + str(dir)         
        os.mkdir(dir)

        
def main(argv):

    profile     = 0
    outputdir   = None
    dbdir       = None
    db_name     = "bp.db"
    
    try:
        opts, args = getopt.getopt(argv,"hd:o:p:",["dbdir=","outputdir=", "profile="])
    except getopt.GetoptError:
        print 'main.py -d <database_directory> -o <output_directory> -p profile'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -d <database_directory> -o <output_directory> -p profile'
            sys.exit()
        elif opt in ("-d", "--dbdir"):
            dbdir = arg
        elif opt in ("-o", "--outputdir"):
            outputdir = arg
        elif opt in ("-p", "--profile"):
            profile = int(arg)
         
    if dbdir == None:
        dbdir = os.path.abspath("data")
    if outputdir == None:
        outputdir = os.path.abspath("output")
    
    print 'Database is located in : ', dbdir
    print 'Output will be located in : ', outputdir
    print 'Profile is : ', str(profile)
   
    create_dir(dbdir)
    create_dir(outputdir)
        
    db_file_path = os.path.join(dbdir, "bp.db")
    out_dir      = outputdir       

    print "Reading data from the device"
    has_reading = dataFetcher.retrieve_data(profile, db_file_path)
    
    if (has_reading):
        print "Exporting readings for profile: " + str(profile)    
        dbExporter.export_data(db_file_path, out_dir, profile)    
        print "Export finished"
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

    
