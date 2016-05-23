import sys, os, sqlite3, datetime, time

def feed_txt(db_file_path, output_file_path, profile):
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
        bp_reading += datetime.datetime.utcfromtimestamp(int(aTimestamp)).strftime('%m/%d/%Y %H:%M:%S') + "\t"
        bp_reading += str(aSystolic) + "\t" + str(aDiastolic) + "\t" + str(aPulse) + "\t"
        
    # setup the TXT document    
    string = '''@BP-BACKUP V=3.0
@APP-V:3.1.0.0
@APP-P:WP7
@APP-T:pro
@BP-BACKUP EOH
@BPD-V=2.0
@BPD-LM=Sun, 24 Apr 2016 08:21:01 GMT
''' + bp_reading + '''
@BPD-END
@TLSET-V=1.0
@N_T=5
BlutdruckLog.Tools.ColorScheme, BlutdruckLog, Version=3.1.0.0, Culture=neutral, PublicKeyToken=null
TLIT.Tools.DescriptiveColor, TLIT, Version=3.1.0.0, Culture=neutral, PublicKeyToken=null
System.DateTime, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e
BlutdruckLog.Tools.StatDuration, BlutdruckLog, Version=3.1.0.0, Culture=neutral, PublicKeyToken=null
BlutdruckLog.Model.DaytimeFilter, BlutdruckLog, Version=3.1.0.0, Culture=neutral, PublicKeyToken=null
@N_C=1
<ArrayOfKeyValueOfstringanyType xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><KeyValueOfstringanyType><Key>ExportFilename</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:string">BloodPressure Values</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>EnableLiveTile</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:boolean">true</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>AdOnTop</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:boolean">true</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>ShowMenuBar</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:boolean">true</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>MainColorScheme</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Tools" i:type="d3p1:ColorScheme">RedOrangeBlue</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>TrendColorSys</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/TLIT.Tools" i:type="d3p1:DescriptiveColor">Green</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>TrendColorDia</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/TLIT.Tools" i:type="d3p1:DescriptiveColor">Orange</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>TrendColorPulse</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/TLIT.Tools" i:type="d3p1:DescriptiveColor">Blue</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>PeriodColorCurrent</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/TLIT.Tools" i:type="d3p1:DescriptiveColor">AccentColor</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>PeriodColorPrevious</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/TLIT.Tools" i:type="d3p1:DescriptiveColor">AccentDarkColor</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>SysCriticalHighLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">140</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>SysHighLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">130</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>SysLowLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">105</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>DiaCriticalHighLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">90</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>DiaHighLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">85</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>DiaLowLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">60</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>PulsCriticalHighLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">100</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>PulsHighLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">90</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>PulsLowLimit</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">50</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>UC</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">2</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>Thanks</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:int">0</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>MorningStart</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:dateTime">2000-01-01T05:00:00</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>MorningEnd</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:dateTime">2000-01-01T10:00:00</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>EveningStart</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:dateTime">2000-01-01T17:20:00</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>EveningEnd</Key><Value xmlns:d3p1="http://www.w3.org/2001/XMLSchema" i:type="d3p1:dateTime">2000-01-01T22:50:00</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>StatDurationDistrib</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Tools" i:type="d3p1:StatDuration">Months1</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>DaytimeFilterDistrib</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Model" i:type="d3p1:DaytimeFilter">All</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>StatDurationMinMaxAvg</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Tools" i:type="d3p1:StatDuration">Months1</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>DaytimeFilterMinMaxAvg</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Model" i:type="d3p1:DaytimeFilter">All</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>StatDurationTrend</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Tools" i:type="d3p1:StatDuration">Years1</Value></KeyValueOfstringanyType><KeyValueOfstringanyType><Key>DaytimeFilterTrend</Key><Value xmlns:d3p1="http://schemas.datacontract.org/2004/07/BlutdruckLog.Model" i:type="d3p1:DaytimeFilter">All</Value></KeyValueOfstringanyType></ArrayOfKeyValueOfstringanyType>
@TLSET-END'''
    file = open(output_file_path, "w")
    file.write(string)    
    file.close()
