"""This script will feed data from csv to sqlite and will generate an xml in output"""
import sys, os, sqlite3, datetime, time

def feed_csv(db_file_path, output_file_path, profile, sep = ","):
    # setup the readings values
    bp_reading = ""
    
    # execute the QUERY
    #create a db connection
    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()    
    cur.execute("SELECT timestamp, systolic, diastolic, pulse, irregular FROM pression WHERE profile = " + str(profile) + " ORDER BY timestamp")
    is_first_line = True
    for row in cur:
        aTimestamp = row[0]
        aSystolic  = row[1]
        aDiastolic = row[2]
        aPulse     = row[3]
        aIrregular = row[4]
        if (is_first_line):
            is_first_line = False
        else:
            bp_reading += "\n"
        comment = ""
        if (aIrregular):
            comment = "aritmia"
        bp_reading += datetime.datetime.utcfromtimestamp(int(aTimestamp)).strftime('%d.%m.%Y %H:%M:%S') + sep + str(aSystolic) + sep + str(aDiastolic) + sep + str(aPulse) + sep + comment
        
    # setup the TXT document    
    string = bp_reading 

    file = open(output_file_path, "w")
    file.write(string)    
    file.close()    
    