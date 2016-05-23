#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
OMRON M10-IT Data retriever
"""
import sys, os, sqlite3, datetime, time
from time import sleep
from msvcrt import kbhit

#sys.path.append(os.path.abspath("lib"))
import bpreading 
import db_update

sys.path.append(os.path.abspath("pywinusb"))
import pywinusb.hid as hid

#global state vars
current_status = 0
current_device = None

status_NOT_INIT     = "NOT_INIT"
status_INIT_OK      = "INIT_OK"
status_SETUP_OK     = "SETUP_OK"
status_NEGO_OK      = "NEGO_OK"
status_READING      = "READING"
status_FINISH       = "FINISH"
status_END          = "END"
status_KO           = "KO"
status_PREREADING   = "PREREADING"
status_QUITTING     = "QUITTING"

sub_status_READ_DATE_TIME   = 0x01
sub_status_READ_VALUES      = 2
sub_status_NOT_READING      = 0
sub_status_READING_OK       = 3

status = [ status_NOT_INIT, status_INIT_OK, status_SETUP_OK, status_NEGO_OK, status_READING, status_FINISH, status_END, status_KO, status_PREREADING, status_QUITTING ]
reading_status = [sub_status_READ_DATE_TIME, sub_status_READ_VALUES, sub_status_READING_OK, sub_status_NOT_READING]

# buffer sent from the device when ready

init_ok_buffer  = [0x00]*9                         
ack_ok_setup   = [0, 8, 32, 0, 0, 0, 0, 0, 0]
nack_ok_nego   = [0, 5, 79, 70]
ack_request    = [0, 7, 79, 75]
ack_request_2  = [0, 2, 79, 75]
start_reading  = [0, 1]
end_reading    = [0, 3, 0]
cmd_error      = [0, 2, 78, 79]
cmd_reinit     = [0, 2, 0xA6, 0xF8, 0x5A, 0x98, 0xE1, 0x4F, 0x46 ]

readings_values = dict()
source_name     = ""
profile         = 0

    
# shared variables for counting the current readings and the totals
reading_no = 0
reading_found = 0
finish = False

# db data variables
new_readings_inserted = 0

# Error messages
error_msg = []
    
def send_ack_report():
    # browse feature reports
    report = get_current_device().find_feature_reports()
    print "Device initialisation..."
    for r in report:
        r.get()
        r.set_raw_data([0,0,0])
        r.send() 
        
def send_ack_report_reinit():
    # browse feature reports
    report = get_current_device().find_feature_reports()    
    for r in report:
        r.get()
        r.set_raw_data([0,1,1])
        r.send() 
        
def get_current_device():
    global current_device
    assert current_device != None
    return current_device

def set_current_device(new_device):
    global current_device    
    current_device = new_device
    
def get_status():
    global status, current_status
    assert current_status < len(status) # element not in the status list
    return status[current_status]

def set_status(new_status):
    global status, current_status
    el_index = status.index(new_status)
    assert el_index >= 0 # element not in the status list 
    current_status = el_index

def compare_reply(code, data):
    return code == data[:len(code)]
    
def save_reading_data(read_code, data, reading_no):
    global sub_status_READ_DATE_TIME, sub_status_READ_VALUES, sub_status_READING_OK, sub_status_NOT_READING
    global readings_values, source_name, profile
    if not reading_no in readings_values:
        readings_values[reading_no] = bpreading.BP_value(reading_no)
    
    a_reading = readings_values[reading_no]
    
    if (read_code == sub_status_READ_DATE_TIME):
        year    = data[5]
        month   = data[6]
        day     = data[7]
        hour    = data[8]        
        a_reading.save_part_A(year,month,day,hour)
        
        
    elif (read_code == sub_status_READ_VALUES):
        minute    = data[3]
        second    = data[4]
        diastolic = data[6]
        systolic  = data[7]
        pulse     = data[8]
        a_reading.save_part_B(minute,second,systolic,diastolic,pulse)
        
    elif (read_code == sub_status_READING_OK):
        is_irr = (data[3] & 1)
        #if (is_irr):
        #    print "irregular reading at " + str(reading_no)
        a_reading.save_part_C(is_irr)
        a_reading.set_source(source_name)
        a_reading.set_profile(profile)
        
    # saving back...
    readings_values[reading_no] = a_reading
    if readings_values[reading_no].is_complete():
        readings_values[reading_no].describe()
    

def conversation_handler(data):
    global init_ok_buffer, status, status_NOT_INIT, status_INIT_OK, status_READING, status_FINISH, status_END, status_SETUP_OK, status_NEGO_OK, status_KO, status_PREREADING, status_QUITTING
    global sub_status_READ_DATE_TIME, sub_status_READ_VALUES, sub_status_READING_OK, sub_status_NOT_READING
    global ack_ok_setup, nack_ok_nego, ack_request, end_reading, start_reading, cmd_error, reading_no, reading_found, ack_request_2, finish, profile, cmd_reinit
    max_error = 10
    
    read_code = sub_status_NOT_READING
    if (get_status() == status_QUITTING):
        return
    
    if compare_reply(init_ok_buffer, data):
        print "Acknowledge Init"
        set_status(status_INIT_OK)
        send_setup()
        
    elif compare_reply(ack_ok_setup, data):
        print "Acknowledge Setup"
        set_status(status_SETUP_OK)        
        send_negotiation(profile)
    
    elif compare_reply(nack_ok_nego, data):        
        max_error -= 1
        if (max_error <= 0):
            print "Exiting... I was not able to communicate with the device"
            finish = True            
            return
        print "Not Acknowledge: OFF - try to recover or uncable the device"
        set_status(status_NOT_INIT)
        send_setup()
        send_reset()
        send_reset()
           
    elif compare_reply(cmd_reinit, data):        
        print "Reinit requested"
        set_status(status_NOT_INIT)
        send_reset()
        
    elif compare_reply(cmd_error, data):
        print("Error data: {0}".format(data))
        if get_status() == status_READING or get_status() == status_FINISH:
            print "resending reading request"
            send_reading_request(reading_no, profile)
        else:
            print "resending setup request"
            send_reset()
        
    elif compare_reply(ack_request, data):
        if get_status() == status_SETUP_OK:
            reading_found = int(data[len(data)-1])
            if (reading_no == 0):
                print "Number of readings: " + str(reading_found)
            set_status(status_PREREADING)
            send_reading_request(reading_no, profile)

        if (get_status() == status_READING):
            read_code = sub_status_READ_DATE_TIME            
            
    elif compare_reply(ack_request_2, data):               
        if (get_status() == status_END):
            set_status(status_QUITTING)
            print "Exiting..."
            finish = True            
            return
        print "Acknowledge request OK - But don't know how to continue"
        set_status(status_SETUP_OK)
        send_negotiation(profile)
   
    elif compare_reply(start_reading, data):
        set_status(status_READING)
        
    elif compare_reply(end_reading, data):
        read_code = sub_status_READING_OK
        set_status(status_FINISH)
    
        
    elif (get_status() == status_READING):
        #print "Reading no. "+ str(reading_no) + " on-going"
        read_code = sub_status_READ_VALUES

    
    save_reading_data(read_code, data, reading_no)
    
    if (get_status() == status_FINISH):
        reading_no += 1
        if reading_no < reading_found:        
            send_reading_request(reading_no, profile)
            set_status(status_READING)
        else:
            print "All data has been read. Deconnecting device"
            send_end()
            set_status(status_END)            


def send_reading_request(reading_no = 0, profile = 0):
    device = get_current_device()
   
    # preparing output buffers
    bufferReq1= [0x00]*9
    bufferReq1[0]= 0x00
    bufferReq1[1]= 0x07
    bufferReq1[2]= 0x47
    bufferReq1[3]= 0x4D
    bufferReq1[4]= 0x45
    bufferReq1[6]= profile
    bufferReq1[8]= reading_no

    device.send_output_report(bufferReq1)
    send_reading_request_ack(reading_no, profile)
    
    print "Sent reading request for : " + str(reading_no)

def send_reading_request_ack(reading_no = 0, profile = 0):
    device = get_current_device()
    # preparing output buffers
    bufferInit= [0x00]*9
    bufferInit[0]= 0x00
    bufferInit[1]= 0x01
    if (profile == 0):
        bufferInit[2]=reading_no
    else:
        if (reading_no % 2 ) == 0:
            bufferInit[2]= abs(reading_no + 1)
        else:
            bufferInit[2]= abs(reading_no - 1)
        #print "written " + str(bufferInit[2])
            
    device.send_output_report(bufferInit)

def send_end():
    device = get_current_device()
    buffer_end= [0x00]*9
    buffer_end[0]=0x00
    buffer_end[1]=0x05
    buffer_end[2]=0x45
    buffer_end[3]=0x4e
    buffer_end[4]=0x44
    buffer_end[5]=0xFF
    buffer_end[6]=0xFF
    device.send_output_report(buffer_end)
    
def send_negotiation(profile = 0):
    device = get_current_device()
    print "Getting profile " + str(profile)
    # preparing output buffers
    bufferGDC   = [0x00]*9
    bufferGDC[0]= 0x00
    bufferGDC[1]= 0x06
    bufferGDC[2]= 0x47
    bufferGDC[3]= 0x44
    bufferGDC[4]= 0x43
    if (profile == 0):
        bufferGDC[8]= 0x01
    else:
        bufferGDC[6]= 0x01
    
    bufferNego   = [0x00]*9
    bufferNego[0]= 0x00
    bufferNego[1]= 0X02
    bufferNego[2]= 0X00
    bufferNego[3]= profile
    
    device.send_output_report(bufferGDC)
    device.send_output_report(bufferNego)
    
    print "Sent negotation request "

def send_reset():    
    print "Sending init to the device"
    send_setup_A()
    send_setup_B()
    
def send_setup(): 
    print "Sending init to the device"
    send_setup_A()
    send_setup_B()
    send_setup_A()
    send_setup_B()
    
    print "Sent setup request "
    
def send_setup_A():
    device = get_current_device()
    # preparing output buffers
    buffer7     = [0x00]*9
    buffer7[0]  = 0x00
    buffer7[1]  = 0x07
    device.send_output_report(buffer7)
    
def send_setup_B():
    device = get_current_device()
    # preparing output buffers
    buffer5     = [0x00]*9
    buffer5[0]  = 0x00
    buffer5[1]  = 0x05
    device.send_output_report(buffer5)
    
def send_ack():
    device = get_current_device()
    # preparing output buffers
    bufferInit= [0x00]*9
    bufferInit[0]=0x00
    bufferInit[1]=0x01
    
    device.send_output_report(bufferInit)
    print "Sent ack request "
        
def reset_status():
    global finish, error_msg    
    global readings_values, new_readings_inserted    
    global current_status, reading_no
    # resetting variables       
    new_readings_inserted = 0
    del error_msg[:]
    readings_values.clear()
    current_status = 0
    reading_no = 0
    finish = False
    
def read_values(target_usage, target_vendor_id, source_name):
    global finish, error_msg    
    global readings_values, new_readings_inserted    
    # resetting variables       
    new_readings_inserted = 0
    del error_msg[:]
    readings_values.clear()
    
    # browse all devices
    all_devices = hid.HidDeviceFilter(vendor_id = target_vendor_id).get_devices()
    
    if not all_devices:
        #print("Can't find " + source_name)
        error_msg.append("Can't find " + source_name)
        print  "\n".join(error_msg)
    else:
        # usually you'll find and open the target device, here we'll browse for the        
        # search for our target usage
        for device in all_devices:
            print "Device detected: " + str(device)
            
            try:
                device.open()
                set_current_device(device)
                #set custom raw data handler
                device.set_raw_data_handler(conversation_handler)
                # send ack to device
                send_ack_report()
                sleep(0.5)
                starting_timestamp = datetime.datetime.now()
                while not kbhit() and device.is_plugged():
                #just keep the device opened to receive events
                    sleep(2)
                    elapsedTime = datetime.datetime.now() - starting_timestamp
                    if (elapsedTime.total_seconds()>600):
                        print "Timeout!"
                        error_msg.append("Timeout on " + source_name + " - please unplug and re-plug the device and retry")
                        break
                    if (finish):
                        break           
            finally:
                device.close()   
                

def retrieve_data(input_profile, db_file_path):
    global readings_values, profile, source_name
    reset_status()
    profile = input_profile
    target_vendor_id = 0x0590
    target_usage = hid.get_full_usage_id(0xff00, 0x3)
    source_name = "OMRON M10-IT"

    read_values(target_usage, target_vendor_id, source_name)
    db_update.update(db_file_path, readings_values)
    if (len(readings_values)<1):
        return False
    else:
        return True
          
def retrieve_and_update(input_profile, db_file_path):
    global readings_values, new_readings_inserted, error_msg    
    profile = int(input_profile)
    if retrieve_data(profile, db_file_path):
        device_date = len(readings_values)        
        return [device_date, new_readings_inserted, ",".join(error_msg)]
    else:
        return [0, 0, ",".join(error_msg)]


if __name__ == '__main__':
    profile = 0
    db_file_path = os.path.join(os.path.abspath("data"), "bp.db")
    retrieve_data(profile, db_file_path)

