# opentension
This project provides a tool for monitoring blood pressure.

The tool will work in a local enviroment and will use a web interface, Chrome is the only browser supported for the moment.

It is able to retrieve data directely from Omron MT10-IT device (only supported device for the moment).

It uses pywinusb for connecting to the device.
It uses flask as web server + jquery + jquery UI + amcharts + gijgo + bootstrap as client technology.
The tool is supposed to be used in local via web browser.

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
  
Fixes:
  - sometime a second import from device may fail

Problems:
  - Device entry may be not edited (unless the comment) otherwise at the following import from device data may result duplicated (only source MANUAL can be fully edited)
  

![main window](https://raw.githubusercontent.com/anonimoanemico/opentension/master/previews/screen1.png)
![aggregation](https://raw.githubusercontent.com/anonimoanemico/opentension/master/previews/screen2.png)
![day period](https://raw.githubusercontent.com/anonimoanemico/opentension/master/previews/screen3.png)


