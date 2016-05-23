import sys, os, sqlite3, datetime, time

class BP_value:

    def __init__(self, no_read = 0, timestamp = 0, diastolic = 0, systolic = 0, pulse = 0, restflag = 0, irregular = 0, source = "", comment = "", profile = 0):               
        self.year      = 0
        self.month     = 0
        self.day       = 0
        self.hour      = 0
        self.minute    = 0
        self.second    = 0
        self.diastolic = 0
        self.systolic  = 0
        self.pulse     = 0
        self.irregular = 0        
        self.stepA = False
        self.stepB = False
        self.stepC = False
        self.source = source
        self.no_read = 0
        self.profile = 0
        self.timestamp = 0
        self.comment = comment
    
    def set_no_of_readings(no_read = 0):
        self.no_read = no_read
        
    def set_source(self, source_name):
        self.source = source_name
        
    def set_profile(self, profile):
        self.profile = profile
        
    def save_part_A(self, year, month, day, hour):
        self.year      = 2000+year
        self.month     = month
        self.day       = day
        self.hour      = hour
        self.stepA = True       
        
    def save_part_B(self, minute, second, diastolic, systolic, pulse):
        self.minute    = minute
        self.second    = second
        self.diastolic = diastolic
        self.systolic  = systolic
        self.pulse     = pulse
        self.stepB = True
    
    def save_part_C(self, irregular):
        self.irregular = irregular
        self.stepC = True
        
    def is_complete(self):
        return (self.stepA and self.stepB and self.stepC) or (self.timestamp != 0 and self.diastolic!=0 and self.systolic!=0 and self.pulse!=0)
    
    def describe(self):             
        print "Record "+str(self.no_read)+ " Date " + str(self.day) + "-" +  str(self.month) +  "-" +  str(self.year) + " at " +  str(self.hour) +":"+str(self.minute)+":"+str(self.second)+" BP: " + str(self.diastolic)+"/"+str(self.systolic) + " Pulse: " + str(self.pulse) + " Irr: " + str(self.irregular)+ " - Valid: " + str(self.is_complete())
        
    def get_timestamp(self):        
        if (self.timestamp == 0):
            if (self.second < 0 ) or (self.second > 59):
                print "Error in seconds format : " + str(self.second) + " - value forced to zero"
                self.second = 0
            aDate = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
            self.timestamp = (aDate - datetime.datetime(1970, 1, 1)).total_seconds()
        return self.timestamp
    
#    def toTuple(self):
#        return [self.timestamp, ]
    