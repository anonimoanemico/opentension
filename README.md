# opentension
This project provides a monitoring blood pressure application.

The tool works in a local environment and is accessed via a web browser such as IE or Chrome.
The user is supported to first run the server application written in python and then connect to a local address provided by the server, usually it is http://localhost:5000

The application is able to retrieve data directly from the Omron MT10-IT device (which is the only supported device at the moment) and feed them into a sqlite database file.
The database is saved in a local folder a no data is sent to an external resource.

Several aggregations and data selection are provided in order to best understand their own blood pressure.

Two profiles are supported.

It uses pywinusb for connecting to the device.
It uses flask as web server + jquery + jquery UI + amcharts + gijgo + bootstrap as client technology.
The tool is supposed to be used in local via web browser.

# how to use
Please download the zip file from the following address:
https://github.com/anonimoanemico/opentension/archive/master.zip

Once on your computer:
- Unzip all files into a new folder
- Double click on the file: run_server(.vbs)
- The tool should be shown in your favorite browser if not please go to this address: http://127.0.0.1:5000


# Features to be implemented:
A lot of things need to be done...:
  - localisation
  - implement manual data entry
  - remove stub comments
  - add styling in the trend panel
  - implement a preference panel
  - add feature to create and set default view
  - open default at access
  - set default profile
  - add support for more devices
  - add import from csv
  - add export to csv
  - add printing & sending to feature
  - add area showing weekend 
  - add pressure targets feature
  - customization of the pressure classification and add other standard such as european hypertension society & american ones
  - add weight and age information (based on date of birth)
  
# Fixes
  - sometime a second import from device may fail

# Problems
  - Device entry may be not edited (unless the comment) otherwise at the following import from device data may result duplicated (only source MANUAL can be fully edited)
  

![main window](https://raw.githubusercontent.com/anonimoanemico/opentension/master/previews/screen1.png)
![aggregation](https://raw.githubusercontent.com/anonimoanemico/opentension/master/previews/screen2.png)
![day period](https://raw.githubusercontent.com/anonimoanemico/opentension/master/previews/screen3.png)


