import sys, os, sqlite3, datetime, time

def setup(conn):
    cur = conn.cursor()    
    #cur.execute('''CREATE TABLE IF NOT EXISTS pression (timestamp INTEGER NOT NULL, diastolic INTEGER NOT NULL, systolic INTEGER NOT NULL, pulse INTEGER NOT NULL, restflag INTEGER DEFAULT 0, irregular INTEGER DEFAULT 0, source TEXT DEFAULT NULL, profile INTEGER DEFAULT 0, comment TEXT DEFAULT NULL CONSTRAINT uniquekey PRIMARY KEY (timestamp, diastolic, systolic, pulse, irregular, profile) )''')
    #key based on timestamp and profile only    
    cur.execute('''CREATE TABLE IF NOT EXISTS pression (timestamp INTEGER NOT NULL, diastolic INTEGER NOT NULL, systolic INTEGER NOT NULL, pulse INTEGER NOT NULL, restflag INTEGER DEFAULT 0, irregular INTEGER DEFAULT 0, source TEXT DEFAULT NULL, profile INTEGER DEFAULT 0, comment TEXT DEFAULT NULL, CONSTRAINT uniquekey PRIMARY KEY (timestamp, profile) )''')
    conn.commit()
    
def add_row(conn, aBP_value):
    cur = conn.cursor()
    #print '''INSERT OR IGNORE INTO pression (timestamp, diastolic, systolic, pulse, restflag, irregular, source, profile) VALUES ( ''' + str(aBP_value.get_timestamp())+ ''','''+str(aBP_value.diastolic)+ ''','''+str(aBP_value.systolic)+''','''+str(aBP_value.pulse)+''','','''+str(aBP_value.irregular)+''',"'''+str(aBP_value.source)+'''",'''+str(aBP_value.profile)+''' )'''
    cur.execute('''INSERT OR IGNORE INTO pression (timestamp, diastolic, systolic, pulse, restflag, irregular, source, profile, comment) VALUES ( ''' + str(aBP_value.get_timestamp())+ ''','''+str(aBP_value.diastolic)+ ''','''+str(aBP_value.systolic)+''','''+str(aBP_value.pulse)+''','','''+str(aBP_value.irregular)+''',"'''+str(aBP_value.source)+'''",'''+str(aBP_value.profile)+''',"'''+str(aBP_value.comment)+'''" )''')
    return cur.rowcount
    
def update_single_row(db_file_path, a_BP_value):
    #create a db connection
    conn = sqlite3.connect(db_file_path)    
    #create the table if does not exist
    setup(conn)    
    new_readings_inserted = 0
    if a_BP_value.is_complete():           
        new_readings_inserted += add_row(conn, a_BP_value)    
    print "Data saved"
    conn.commit()
    return new_readings_inserted
    
def update(db_file_path, readings_values, new_readings_inserted = 0):
    if (len(readings_values)<1):
        print "No values found"
        return new_readings_inserted
    try:
    
        #create a db connection
        conn = sqlite3.connect(db_file_path)    
        #create the table if does not exist
        setup(conn)    
        for key in readings_values:
            if readings_values[key].is_complete():           
                new_readings_inserted += add_row(conn, readings_values[key])
            else:
                print "BP value #"+str(key)+" error: Unknown format"  
        print "Data saved"
        conn.commit()
    finally:
        conn.close()
    return new_readings_inserted
    