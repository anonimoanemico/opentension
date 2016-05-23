"""This script will feed data from csv to sqlite and will generate an xml in output"""
import sys, os, sqlite3, datetime, time

sys.path.append(os.path.abspath("lib"))
import exportHexenhal as exportHexenhal
import exportBloodPressureW8 as exportBPW8
import exportCsv as exportCsv

profile = 0

def export_data(db_file_path, out_dir, profile):
    ts = time.time()
        
    output_file_path      =  os.path.join(out_dir, "Hexenhal_BPTracker.bak." + str(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')).split('.')[0])
    output_file_path2      = os.path.join(out_dir, "BloodPressure Backup.txt." + str(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')).split('.')[0])
    output_file_path3      = os.path.join(out_dir, "BloodPressureValues_coma." + str(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')).split('.')[0]+ ".csv")
    output_file_path4      = os.path.join(out_dir, "BloodPressureValues_semi." + str(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')).split('.')[0]+ ".csv")
    
    exportHexenhal.feed_xml(db_file_path, output_file_path, profile)
    exportBPW8.feed_txt(db_file_path, output_file_path2, profile)
    exportCsv.feed_csv(db_file_path, output_file_path3, profile)
    exportCsv.feed_csv(db_file_path, output_file_path4, profile, ";")
  
def main(argv=None):
    db_file_path = os.path.join(os.path.abspath("data"), "bp.db")
    out_dir      = os.path.abspath("output")    
    profile = 0       
    print "Exporting readings for profile: " + str(profile)    
    export_data(db_file_path, out_dir, profile)    
    print "Export finished"
    
    
if __name__ == "__main__":
    sys.exit(main())

    
