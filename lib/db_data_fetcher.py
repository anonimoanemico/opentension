#!/usr/bin/env python

import time
import sys, os, sqlite3, datetime, time

# import libraries at the parent level
root_dir = os.path.abspath("..")
common_lib_dir = os.path.join(root_dir, "lib")
print root_dir
print common_lib_dir
sys.path.append(root_dir)
sys.path.append(common_lib_dir)
from bpreading import BP_value

def MIN_DIASTOLIC_LABEL():
    return "MinDia"
def MAX_DIASTOLIC_LABEL():
    return "MaxDia"
def MIN_SYSTOLIC_LABEL():
    return "MinSys"
def MAX_SYSTOLIC_LABEL():
    return "MaxSys"

    
no_aggregation  = 0
repetitive_aggregation  = 4
day_aggregation = 1
week_aggregation = 2
month_aggregation = 3
aggregation_types = [no_aggregation, day_aggregation, week_aggregation, month_aggregation, repetitive_aggregation]

allday_period  = 0
morning_period = 1
afternoon_period = 2
evening_period = 3
night_period = 4
day_periods = [allday_period, morning_period, afternoon_period, evening_period, night_period]

# make constant types..
order_asc  = 0
order_desc = 1

    
def check_if_repetitive_reading(now_timestamp, last_timestamp):
    max_time_span = 10 * 360 # = 60 minutes
    fmt = '%Y-%m-%d %H:%M:%S'
    now_timestamp_dt  = datetime.datetime.strptime(now_timestamp, fmt)
    last_timestamp_dt = datetime.datetime.strptime(last_timestamp, fmt)
    minutes_diff = (now_timestamp_dt-last_timestamp_dt).total_seconds()
    if (minutes_diff > max_time_span):
        return False
    return True

def get_day_period(day_period):
    global allday_period, morning_period, afternoon_period, evening_period, night_period, day_periods
    if (day_period == morning_period):
        return ['07:00', '11:59']
    elif (day_period == afternoon_period):
        return ['12:00', '16:59']
    elif (day_period == evening_period):
        return ['17:00', '20:59']
    elif (day_period == night_period):
        return ['21:00', '06:59']
    return ['00:00','23:59']

def where_and(sql_where):
    if sql_where != "":
        return sql_where + " AND " 
    return sql_where

def where_or(sql_where):
    if sql_where != "":
        return sql_where + " OR " 
    return sql_where
    
def build_day_period_in_where(day_period = allday_period, prefix_verb = " AND "):
    global allday_period, morning_period, afternoon_period, evening_period, night_period, day_periods
    assert day_period in day_periods
    sql_day_period = ""
    if (day_period != allday_period):
        period_tuple = get_day_period(day_period)
        sql_day_period = prefix_verb + " strftime('%H:%M',datetime(timestamp, 'unixepoch')) BETWEEN strftime('%H:%M','" + str(period_tuple[0]) + "') AND strftime('%H:%M','" + str(period_tuple[1]) + "') "
    return sql_day_period

def build_date_period_in_where(start_period_ts = 0, end_period_ts = 0, prefix_verb = " AND "):    
    sql_date_period = ""
    if start_period_ts > 0:
        sql_date_period = " timestamp > " + str(start_period_ts)
    
    if (end_period_ts > 0):
        sql_date_period = where_and(sql_date_period) + " timestamp < " + str(end_period_ts)
    
    if sql_date_period!= "":
        sql_date_period = prefix_verb + sql_date_period
    return sql_date_period
    

def build_max_values_in_where(min_max_values = dict(), prefix_verb = " AND "):
    sql_where = ""
    print min_max_values
    if (len(min_max_values) != 4):
        return sql_where
        
    max_systolic = min_max_values[MAX_SYSTOLIC_LABEL()]
    max_diastolic = min_max_values[MAX_DIASTOLIC_LABEL()]    
    min_systolic = min_max_values[MIN_SYSTOLIC_LABEL()]    
    min_diastolic = min_max_values[MIN_DIASTOLIC_LABEL()]
    
    if (max_systolic > 0):
        sql_where = " systolic < " + str(max_systolic)
    
    if (max_diastolic > 0):
        sql_where = where_and(sql_where) + " diastolic < " + str(max_diastolic)
    
    if (min_systolic > 0) and (min_diastolic> 0):
        sql_where = where_and(sql_where) + " (systolic >= " + str(min_systolic)
        sql_where = where_or(sql_where) + " diastolic >= " + str(min_diastolic) + ")"
    
    if (sql_where != ""):
            sql_where = prefix_verb + sql_where
            
    return sql_where
    
""" 0 is ASC, 1 DESC """
def build_query(profile, aggregation_type = no_aggregation, day_period = allday_period, order = order_asc, min_max_values = dict(), start_period = 0, end_period = 0):
    global no_aggregation, day_aggregation, week_aggregation, month_aggregation, aggregation_types, repetitive_aggregation, order_asc, order_desc
    
    print "Using aggregation_type " + str(aggregation_type) + " on profile #" + str(profile)
    assert aggregation_type in aggregation_types
    
    sql_day_period          = build_day_period_in_where(day_period, prefix_verb = " AND ")
    sql_max_values_where    = build_max_values_in_where(min_max_values, prefix_verb = " AND ")
    sql_date_period_where   = build_date_period_in_where(start_period, end_period, prefix_verb = " AND ")    
    and_where_clause        = sql_day_period + sql_max_values_where + sql_date_period_where
    
    order_value = ""
    if (order == order_desc):
        order_value = " DESC "
        
    query = "SELECT strftime('%Y-%m-%d %H:%M:%S',datetime(timestamp, 'unixepoch')), systolic, diastolic, pulse, irregular FROM pression WHERE profile = " + str(profile) + and_where_clause +" ORDER BY timestamp" + order_value
    print "Aggregation type: " + str(aggregation_type)
    if aggregation_type == day_aggregation:
        query = "SELECT strftime('%Y-%m-%d 00:00:00',datetime(MIN(timestamp), 'unixepoch')), avg(systolic), avg(diastolic), avg(pulse), avg(irregular) FROM pression WHERE profile = " + str(profile) + and_where_clause + " GROUP BY strftime('%Y-%m-%d',datetime(timestamp, 'unixepoch')) ORDER BY timestamp" + order_value
    elif aggregation_type == week_aggregation:        
        query = "SELECT strftime('%Y-%m-%d 00:00:00',datetime(MIN(timestamp), 'unixepoch')), avg(systolic), avg(diastolic), avg(pulse), avg(irregular) FROM pression WHERE profile = " + str(profile) + and_where_clause + " GROUP BY strftime('%Y-%W',datetime(timestamp, 'unixepoch')) ORDER BY timestamp" + order_value
    elif aggregation_type == month_aggregation:
        query = "SELECT strftime('%Y-%m-%d 00:00:00',datetime(MIN(timestamp), 'unixepoch')), avg(systolic), avg(diastolic), avg(pulse), avg(irregular) FROM pression WHERE profile = " + str(profile) + and_where_clause + " GROUP BY strftime('%Y-%m',datetime(timestamp, 'unixepoch')) ORDER BY timestamp" + order_value
    #else if aggregation_type == repetitive_aggregation:
    else:
        print "No aggregation/Repetitive"
            
    return query

def build_query_full_row(profile, day_period = allday_period, order = order_asc, min_max_values = dict(), start_period = 0, end_period = 0):
    global order_asc, order_desc
    
    sql_day_period          = build_day_period_in_where(day_period, prefix_verb = " AND ")
    sql_max_values_where    = build_max_values_in_where(min_max_values, prefix_verb = " AND ")
    sql_date_period_where   = build_date_period_in_where(start_period, end_period, prefix_verb = " AND ")    
    and_where_clause        = sql_day_period + sql_max_values_where + sql_date_period_where
    
    order_value = ""
    if (order == order_desc):
        order_value = " DESC "
        
    query = "SELECT strftime('%Y-%m-%d %H:%M:%S',datetime(timestamp, 'unixepoch')), systolic, diastolic, pulse, irregular, source, comment FROM pression WHERE profile = " + str(profile) + and_where_clause +" ORDER BY timestamp" + order_value
                
    return query    
    
def get_count(db_file_path, profile, day_period = allday_period, start_period = 0, end_period = 0, min_max_values = dict()):
    sql_day_period          = build_day_period_in_where(day_period, prefix_verb = " AND ")
    sql_max_values_where    = build_max_values_in_where(min_max_values, prefix_verb = " AND ")
    sql_date_period_where   = build_date_period_in_where(start_period, end_period, prefix_verb = " AND ")
    and_where_clause        = sql_day_period + sql_max_values_where + sql_date_period_where

    query = "SELECT count(*) FROM pression WHERE profile = " + str(profile) + and_where_clause
    print query
    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()    
    cur.execute(query)
    (number_of_rows,)=cur.fetchone()
    return number_of_rows    

def get_readings(db_file_path, profile, aggregation_type = no_aggregation, day_period = allday_period, order = order_asc, start_period = 0, end_period = 0, min_max_values = dict(), limit = -1, offset = -1):
    global no_aggregation, day_aggregation, week_aggregation, month_aggregation, aggregation_types, repetitive_aggregation, order_asc, order_desc

    query = build_query(profile, aggregation_type, day_period, order, min_max_values, start_period, end_period)
    
    if (limit>-1 and offset>-1):
        assert (aggregation_type == no_aggregation) # "Aggregation type NOT compatible with paging query
        query += " LIMIT " + str(limit) + " OFFSET " + str(offset)
        
    # setup the readings values
    bp_reading = []    
    # create a db connection
    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()    
    # execute the QUERY
    cur.execute(query)
    last_timestamp = '1970-01-01 00:00:00'
    nb_aggregation = 1
    for row in cur:        
        aTimestamp = row[0]
        aSystolic  = int(row[1])
        aDiastolic = int(row[2])
        aPulse     = int(row[3])
        aIrregular = int(row[4])
        a_reading  = {} 
        a_reading["date"]       = aTimestamp
        a_reading["systolic"]   = aSystolic
        a_reading["diastolic"]  = aDiastolic
        a_reading["pulse"]      = aPulse
        a_reading["aritmia"]    = aIrregular
        
        if aggregation_type == repetitive_aggregation:
            if (check_if_repetitive_reading(aTimestamp, last_timestamp)):
                bp_reading[-1]["systolic"]  = ((bp_reading[-1]["systolic"]*nb_aggregation) + aSystolic)/(nb_aggregation+1)
                bp_reading[-1]["diastolic"] = ((bp_reading[-1]["diastolic"]*nb_aggregation) + aDiastolic)/(nb_aggregation+1)
                bp_reading[-1]["pulse"]     = ((bp_reading[-1]["pulse"]*nb_aggregation) + aPulse)/(nb_aggregation+1)
                if (bp_reading[-1]["aritmia"] == 0) and (aIrregular == 1):
                    bp_reading[-1]["aritmia"] = 1                
                nb_aggregation += 1
            else:
                nb_aggregation = 1
                bp_reading.append(a_reading)
        else:
            bp_reading.append(a_reading)
        last_timestamp = aTimestamp
        
    return bp_reading
 
def get_readings_full_row(db_file_path, profile, day_period = allday_period, order = order_asc, start_period = 0, end_period = 0, min_max_values = dict(), limit = -1, offset = -1):
    global order_asc, order_desc

    query = build_query_full_row(profile, day_period, order, min_max_values, start_period, end_period)
    
    if (limit>-1 and offset>-1):
        query += " LIMIT " + str(limit) + " OFFSET " + str(offset)
            
    # setup the readings values
    bp_reading = []    
    # create a db connection
    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()    
    # execute the QUERY
    cur.execute(query)
    for row in cur:        
        a_reading = {}
        a_reading["date"]       = row[0]
        a_reading["systolic"]   = int(row[1])
        a_reading["diastolic"]  = int(row[2])
        a_reading["pulse"]      = int(row[3])
        a_reading["aritmia"]    = int(row[4])
        a_reading["source"]     = row[5]
        if (row[6] != None):
            a_reading["comment"] = row[6]
        else:
            a_reading["comment"] = ""
        bp_reading.append(a_reading)
    return bp_reading
 

def get_data(db_file, profile, aggregation_type = no_aggregation, day_period = allday_period, start_period = 0, end_period = 0):
    global order_asc, order_desc
    readings = get_readings(db_file, profile, aggregation_type, day_period, order_asc, start_period, end_period)
    if readings <1:
        print "No data to display"
    return readings

def get_total_records(db_file, profile, day_period = allday_period, min_max_values = dict(), start_period = 0, end_period = 0):
    return get_count(db_file, profile, day_period, start_period, end_period, min_max_values)
    
def get_data_by_page(db_file, profile, day_period = allday_period, page = 0, limit = 10, min_max_values = dict(), start_period = 0, end_period = 0):
    global order_asc, order_desc
    offset = int(limit) * (int(page)-1)    
    readings = get_readings_full_row(db_file, profile, day_period, order_desc, start_period, end_period, min_max_values, limit, offset )
    if readings <1:
        print "No data to display"
    return readings    
        
