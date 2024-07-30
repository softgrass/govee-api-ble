# govee-api-ble
*A Python API for Govee RGB lighting strips*
#### This API is confirmed to work with the following Govee Models:
- H6127
- H6139
- H6159 

*The model number can typically be located in the app or by looking at the device's default Bluetooth name*

*If you have tested any Govee models not listed on here, please make an issue and I will add it in!*

[Python PIP Package Site!](https://pypi.org/project/govee-api-ble/)

**This project is still in progress! If you have any issue, post an issue. If you have a fix, make a pull request**

*Huge thanks to [BeauJBurroughs](https://github.com/BeauJBurroughs/Govee-H6127-Reverse-Engineering) for their amazing research! Without them this would not be possible :-)*


## Requirements and Setup
For this package you will need
- Python >=3.8
- Bleak (install via [PIP](https://pypi.org/project/bleak/))

~~Once setup, install this package by typing:~~

```
pip install govee-api-ble
```

__**I currently have no access to my PyPi account, so you will have to install this update from the source before the PIP repo is updated.**__
Download the repo above or clone it using `git clone https://github.com/softgrass/govee-api-ble` and then run:
```
pip install govee-api-ble/
```

## Initialization
You will first need the MAC address for your light strip

This can easily be found by doing `hcitool scan` on a Raspberry Pi or by looking in your settings on the Govee app

To other devices, the strip will most likely be named ihoment-hXXXX (with XXXX being the model number) since that is the manufacturer's old name.

To initialize an object, add to your code:
```python
from govee_api_ble import GoveeDevice

my_device = GoveeDevice('FA:KE:MA:CH:ER:E0')
```
Replacing the argument with your device's MAC address
## Usage
### Power On/Off Example
my_device.setPower(status)

Accepts boolean value to turn device on/off
```python
from govee_api_ble import GoveeDevice
# Initialize the device
my_device = GoveeDevice('FA:KE:MA:CH:ER:E0')

my_device.setPower(True) # Turns device on
my_device.setPower(False) # Turns device off
```
### Set Device Color Example
my_device.setColor(\[r,g,b])

Accepts three RGB values as a list
```python
from govee_api_ble import GoveeDevice
# Initialize the device
my_device = GoveeDevice('FA:KE:MA:CH:ER:E0')

my_device.setColor([0,0,255]) # Sets entire light strip to blue
```
### Set Device Brightness Example
my_device.setBrightness(level)

Accepts int between 0-100 and sets device brightness to number
```python
from govee_api_ble import GoveeDevice
# Initialize the device
my_device = GoveeDevice('FA:KE:MA:CH:ER:E0')

my_device.setBrightness(50) # Sets brightness to 50%
```
### Set Device Scene Example
my_device.setScene(setting)

Accepts string, uses name of any scene setting that can be found in the Govee app
```python
from govee_api_ble import GoveeDevice
# Initalize the device
my_device = GoveeDevice('FA:KE:MA:CH:ER:E0')

my_device.setScene("blinking") # Sets scene to blinking mode
```
### Set Music Mode Example
my_device.setColorMusic(setting,\[r,g,b])

Accepts string using name of the music mode, which can be found in the Govee app

Also accepts three RGB values as a list for the spectrum mode

At the moment, rolling mode does not work
```python
from govee_api_ble import GoveeDevice
# Initalize the device
my_device = GoveeDevice('FA:KE:MA:CH:ER:E0')

my_device.setColorMusic("rhythm") # Sets music mode to rhythm
my_device.setColorMusic("spectrum",[0,0,255]) # Sets music mode to spectrum with the color blue
```

## Help with Development!
* Run `pip install setuptools wheel`
* Fork and clone the repository
* Create a branch with a descriptive name
* Run tests & debug before pulling
* Commit and start a pull request!
