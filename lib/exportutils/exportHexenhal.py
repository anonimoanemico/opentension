import sys, os, sqlite3, datetime, time
import xml.etree.ElementTree as ElementTree
import xml.etree.cElementTree as xmlTree


def feed_xml(db_file_path, output_file_path, profile):
    bp_index = 1
    
    # setup the XML document
    root = xmlTree.Element("ArrayOfBPEntry")
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    
    # execute the QUERY
    #create a db connection
    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, systolic, diastolic, pulse, restflag, irregular FROM pression WHERE profile = " + str(profile) + " ORDER BY timestamp")
    
    for row in cur:
        aTimestamp = row[0]
        aSystolic  = row[1]
        aDiastolic = row[2]
        aPulse     = row[3]
        aRestFlag  = row[4]
        aIrregular = row[5]
        
        aBP_Entry = xmlTree.SubElement(root, "BPEntry")    
        xmlTree.SubElement(aBP_Entry, "BPEntryId").text = str(bp_index)    
        xmlTree.SubElement(aBP_Entry, "PersonId").text = "0" # to be hanlded... as input parameters
        xmlTree.SubElement(aBP_Entry, "Stance").text = "SITTING" # to be hanlded... as input parameters ????
        xmlTree.SubElement(aBP_Entry, "Time").text = datetime.datetime.utcfromtimestamp(int(aTimestamp)).strftime('%Y-%m-%dT%H:%M:%S')
        xmlTree.SubElement(aBP_Entry, "Systolic").text = str(aSystolic)
        xmlTree.SubElement(aBP_Entry, "Diastolic").text = str(aDiastolic)
        xmlTree.SubElement(aBP_Entry, "PulseRate").text = str(aPulse)
        xmlTree.SubElement(aBP_Entry, "TagSalt").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagAlcohol").text = "false"
        if aRestFlag == 0:
            xmlTree.SubElement(aBP_Entry, "TagStress").text = "false"
        else:            
            xmlTree.SubElement(aBP_Entry, "TagStress").text = "true"
        
        xmlTree.SubElement(aBP_Entry, "TagExcercise").text = "false"
        
        if aIrregular == 0:
            xmlTree.SubElement(aBP_Entry, "TagCustom1").text = "false"
        else:
            xmlTree.SubElement(aBP_Entry, "TagCustom1").text = "true"
        
        xmlTree.SubElement(aBP_Entry, "TagCustom2").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagCustom3").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagCustom4").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagCustom5").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagCustom6").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagCustom7").text = "false"
        xmlTree.SubElement(aBP_Entry, "TagCustom8").text = "false"
    
    tree = xmlTree.ElementTree(root)
    tree.write(output_file_path,encoding='utf-8', xml_declaration=True)