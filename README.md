# bmtoolkit

Reading data from Beurer BM 96 blood pressure device over USB-HID.

Many other HID-equipped Beurer blood pressure devices will work with a few changes.

**disclaimer**

This tool is NOT developed by Beurer or on their behalf. 

NO WARRANTIES AT ALL!

<ins>Please double check the values and see a doctor in case of health problems.</ins>

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
usage: bmquery.py [-h] [-u USER] [-i INDEX] [-f FORMAT] [-o PATH] [-d CHAR] FUNCTION [list|ecgraw|info|version]

positional arguments:
  FUNCTION [list|ecgraw|info|version]
                        function [ecgraw, list, info, version]

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

**example output**
```
dev     sensor  user    index   date_measurement        sys     dia     pulse   rest    arr     afib    param9  param10
BM96    bp      1       0       2025-02-20 11:26        157     102     76      0       0       0       3       0
BM96    bp      1       1       2025-02-20 12:35        161     107     77      1       0       0       2       0
BM96    bp      1       2       2025-02-22 21:02        145     90      70      1       0       0       2       0
BM96    ecg     1       3       2025-02-23 07:02                        70                              4       0
BM96    bp      1       4       2025-02-25 11:01        155     91      78              0       1       9       0
BM96    bp      1       5       2025-02-25 12:54        129     42      68              1       1       13      0
```

**missing parts**

For the BM 96 it's unknown how to interpret the ECG-Data. However it's possible to dump the data:

*ECG Data:*

```
./bmquery.py ecgraw
```
I would be glad for hints how to interpret and plot the values!

*Values on column index 10*

I guess it's the AFlB-detection for ECG-datasets. For blood pressure datasets maybe the cuff position control.

**rest/arr/afib data**

This is what i figured out so far. In case you see a '?'-character within these values, please get in touch with me or file an issue and let me know what is seen on the display + the values of param9 and param10.

Thank You!

**permissions**

In some enviroments connecting to the usb device may need special permissions. You may need to change udev-rules / user permissions.
