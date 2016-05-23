from distutils.core import setup
import py2exe
import xml.etree.ElementTree
import os,sys

sys.path.append(os.path.abspath("lib"))
import export_db as dbExporter
import data_fetcher as dataFetcher 
import bpreading 
import exportHexenhal as exportHexenhal
import exportBloodPressureW8 as exportBPW8
import exportCsv as exportCsv

setup(console=['main.py'])