# opentension
This project provides a tool for monitoring blood pressure.

The tool will work in a local enviroment and will use a web interface, Chrome is the only browser supported for the moment.

It is able to retrieve data directely from Omoron MT10-IT device (only supported device for the moment).

It uses pywinusb for connecting to the device.
It uses flask as web server + jquery + jquery UI + amcharts + gijgo + bootstrap as client technology.
The tool is supposed to be used in local via web browser.

A lot of things need to be done...:
  - localisation
  - implement manual data entry
  - remove stub comments
  - add styling in the trend panel

