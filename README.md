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

**example output**
```
dev     sensor  user    index   date_measurement        sys     dia     pulse   rest    info    param10
BM96    bp      1       0       2025-02-22 11:26        137     94      76      3               0
BM96    bp      1       1       2025-02-22 12:35        128     87      77      2               0
BM96    bp      1       2       2025-02-22 12:36        132     89      75      3               0
BM96    bp      1       3       2025-02-22 19:53        120     78      77      2               0
BM96    bp      1       4       2025-02-22 19:55        126     84      79      2               0
BM96    bp      1       5       2025-02-22 21:02        141     98      70      2               0
BM96    ecg     1       6       2025-02-23 07:02                        70              4       0
```

**missing parts**

For the BM 96 it's unknown how to interpret the ECG-Data. However it's possible to dump the data:

*ECG Data:*

```
./bmquery ecgraw
```
I would be glad for hints how to interpret and plot the values!

*Values on column index 10*

I guess it's the AFlB-detection for ECG-datasets. For blood pressure datasets maybe the cuff position control.

**rest data**

```
2 = OK
3 = NOT OK
```

**permissions**

In some enviroments connecting to the usb device may need special permissions. You may need to change udev-rules / user permissions.
