# bmtoolkit

Reads data from Beurer Devices.

The Beurer BM 96 is the only supported yet. Many others may work with just a few changes.

**disclaimer**

This tool is NOT developed by Beurer or on their behalf. 

NO WARRANTIES AT ALL!

Please double check the values and see a doctor in case of health problems.

**requirements**

requires python 3 and python-hid

(please note ... it's NOT the hid module from https://pypi.org/project/hid/)

In case the python-hid binding is missing, just install it:

```
apt install python3-hid
```
(on debian / ubuntu based OS)

**usage**

```
usage: bmquery.py [-h] [-u USER] [-i INDEX] [-f FORMAT] [-o PATH] [-d CHAR] FUNCTION [list|ecgraw|info]

positional arguments:
  FUNCTION [list|ecgraw|info]
                        function [ecgraw, list, ecgraw] (default: list)

options:
  -h, --help            show this help message and exit
  -u USER, --user USER  measurements for the given user only
  -i INDEX, --index INDEX
                        measurements for the given index only
  -f FORMAT, --format FORMAT
                        output format [json, csv]
  -o PATH, --outfile PATH
                        save output to a file
  -d CHAR, --delimiter CHAR
                        data delimiter
```

**missing parts**

For the BM 96 it's unknown how to interpret the ECG-Data. However it's possible to dump the data:

*ECG Data:*

```
./bmquery ecgraw
```
I would be glad for hints how to interpret and plot the values!

*Values on column index 10*

I guess it's the AFIB-detected for ECG-datasets. For blood pressure datasets maybe the cuff position control.

**Rest Data**

```
2 = OK
3 = NOT OK
```

**permissions**

In some enviroments connecting to the usb device may need special permissions. You may need to change udev-rules / user permissions.
