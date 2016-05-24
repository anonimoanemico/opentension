# all the imports
import sqlite3, sys, os, json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory

# import libraries at the parent level
root_dir = os.path.abspath("..")
common_lib_dir = os.path.join(root_dir, "lib")
pywinusb_lib_dir = os.path.join(common_lib_dir, "pywinusb")
print common_lib_dir
sys.path.append(common_lib_dir)
sys.path.append(pywinusb_lib_dir)
import data_fetcher as deviceDataFetcter
import db_data_fetcher as dbDataFetcher
import db_update
import data_adapter


#import export_db as dbExporter
def create_dir(dir):
    try:
        os.stat(dir)
    except:
        print "Creating directory " + str(dir)         
        os.mkdir(dir)
        
def get_db_file():    
    db_file_path_dir = os.path.abspath("..")
    db_file_path_dir = os.path.join(db_file_path_dir, "data")
    create_dir(db_file_path_dir)        
    db_file_path = os.path.join(db_file_path_dir, "bp.db")
    return db_file_path

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

    
# configuration
DATABASE = get_db_file()
DEBUG = True
#SECRET_KEY = 'ddasdas3232432-342'
USERNAME = ''
PASSWORD = ''

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
    
    
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response
    
@app.route('/')
def default_page():
    return render_template('index.html')

@app.route('/lib/<path:path>')
def send_js(path):
    return send_from_directory('lib', path)    
    
@app.route('/readDevice/<profile>')
def read_device_data(profile):
    db_file_path = get_db_file()
    readings_output = dict()
    print "Reading data from the device"
    readings = deviceDataFetcter.retrieve_and_update(profile, db_file_path)
    print str(len(readings))
    assert len(readings) == 3 # expected number of elements of the result
    readings_output["device"]   = readings[0] # nb of readings imported from device
    readings_output["db"]       = readings[1] # nb of affected rows
    readings_output["errors"]   = readings[2] #errors
    
    return json.dumps(readings_output)
    #out_dir      = outputdir
    #if (has_reading):
    #    print "Exporting readings for profile: " + str(profile)    
    #    dbExporter.export_data(db_file_path, out_dir, profile)    
    #    print "Export finished"
        

        
#If you have to send parameters, the right sintax is as calling the resoure
# with a kind of path, with the parameters separed with slash ( / ) and they 
# MUST to be written inside the lesser/greater than signs  ( <parameter_name> ) 
@app.route('/dataQuery/<profile>/<aggregation_type>/<day_period>')
def fetch_data(profile, aggregation_type, day_period):
    #     print json.dumps(readings)    
    start_period = 0
    end_period = 0
    if (request.args.get('start') != None):
        start_period = int(request.args.get('start'))
    if (request.args.get('end') != None):
        end_period = int(request.args.get('end'))
        
    data = dbDataFetcher.get_data(get_db_file(), int(profile), int(aggregation_type), int(day_period),start_period, end_period)
    
    return json.dumps(data)

@app.route('/dataQuery/<profile>/<aggregation_type>/<day_period>/<multipage>')
def fetch_data_by_page(profile, aggregation_type, day_period, multipage):
    #     print json.dumps(readings)   
    page = request.args.get('page')
    limit = request.args.get('limit')
    max_diastolic = request.args.get('maxdia')
    max_systolic  = request.args.get('maxsys')
    min_diastolic = request.args.get('mindia')
    min_systolic  = request.args.get('minsys')
    
    min_max_values = dict()
    min_max_values[dbDataFetcher.MIN_DIASTOLIC_LABEL()]   = 0
    min_max_values[dbDataFetcher.MIN_SYSTOLIC_LABEL()]    = 0
    min_max_values[dbDataFetcher.MAX_DIASTOLIC_LABEL()]   = 0
    min_max_values[dbDataFetcher.MAX_SYSTOLIC_LABEL()]    = 0

    if (page == None) or (limit==None):
        return None
        
    if (max_diastolic != None):
        min_max_values[dbDataFetcher.MAX_DIASTOLIC_LABEL()] = int(max_diastolic)
    if (max_systolic != None):
        min_max_values[dbDataFetcher.MAX_SYSTOLIC_LABEL()]  = int(max_systolic)
    if (min_diastolic != None):
        min_max_values[dbDataFetcher.MIN_DIASTOLIC_LABEL()] = int(min_diastolic)
    if (min_systolic != None):
        min_max_values[dbDataFetcher.MIN_SYSTOLIC_LABEL()]  = int(min_systolic) 
    
    start_period = 0
    end_period = 0
    if (request.args.get('start') != None):
        start_period = int(request.args.get('start'))
    if (request.args.get('end') != None):
        end_period = int(request.args.get('end'))
    
    print "Start date-range: " + str(start_period) + " end " + str(end_period)
    
    data  = dbDataFetcher.get_data_by_page(get_db_file(), int(profile), int(day_period), int(page), int(limit), min_max_values, start_period, end_period)
    count = dbDataFetcher.get_total_records(get_db_file(), int(profile), int(day_period), min_max_values, start_period, end_period)
    result = dict()
    result["records"]   = data
    result["total"]     = count
    return json.dumps(result)
    
    
@app.route('/saveData/<profile>')
def save_data(profile, methods=['POST', 'GET']):
    readings = 0
    
    if (request.args.get('update') != "null"):
        parsed_json = json.loads(request.args.get('update'))    
        print parsed_json
    
        # a_bp_value = data_adapter.create_BP_Value(request)
        # if (db_update.update_single_row(a_bp_value) > 0):
        # result = True     
        
    readings_output = dict()   
    readings_output["device"]   = 0 # nb of readings imported from device
    readings_output["db"]       = readings # nb of affected rows
    readings_output["errors"]   = 0 #errors
    
    return json.dumps(readings_output)

def init():
    db_update.init(DATABASE)
        
if __name__ == '__main__':
    init()
    app.run()
    
    