#!/usr/bin/env python3
# License: MIT License

import hid
import sys
import csv
import json
import io
from argparse import ArgumentParser

try:

    # cmd
    init_cmd = bytes([ 0xAA, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # full device name
    info_name_cmd = bytes([ 0xA1, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # cmd
    cnt_cmd = bytes([ 0xA2, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # cmd, user, row
    fetch_cmd = bytearray([ 0xA3, 0x00, 0x00, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # cmd
    exit_cmd = bytes([ 0xF6, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # cmd
    end_cmd = bytes([ 0xF7, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # cmd, user, row
    ecg_cnt_cmd   = bytearray([ 0xA4, 0x01, 0x00, 0xF4, 0xF4, 0xF4, 0xF4, 0xF4 ])
    # cmd, user, row, page
    ecg_fetch_cmd = bytearray([ 0xA5, 0x01, 0x00, 0x00, 0x00, 0xF4, 0xF4, 0xF4 ])

    vid = 0x314A
    pid = 0x0102

    version = '0.9'

    sensors = ['bp', 'ecg']

    parser = ArgumentParser()
    parser.add_argument("-u", "--user", dest="user", help="measurements for the given user only", metavar="USER")
    parser.add_argument("-i", "--index", dest="index", help="measurements for the given index only", metavar="INDEX")
    parser.add_argument("-f", "--format", dest="format", help="output format [json, csv]", metavar="FORMAT", choices=['json', 'csv'])
    parser.add_argument("-o", "--outfile", dest="outfile", help="save output to a file", metavar="PATH")
    parser.add_argument("-d", "--delimiter", dest="delimiter", help="data delimiter", metavar="CHAR")
    parser.add_argument("func", help="function [ecgraw, list, ecgraw] (default: list)", metavar="FUNCTION [list|ecgraw|info|version]")

    args = parser.parse_args()

    if args.func == 'version':
        print(version)
        sys.exit()

    delimiter = "\t" if not args.delimiter else args.delimiter
    if not args.delimiter and args.format == 'csv':
       delimiter = ","

    h = hid.device()
    h.open(vid, pid)
    h.set_nonblocking(0)
    
    hid_product = h.get_product_string()
    
    def query_data(query, length = 64):
        h.write(query)
        while True:
            d = h.read(length)
            if d and d[0] != 0xF4:
                return d
            elif not d:
                return False
            
    def trim_string(data):
        out = ''
        for byte in data:
            if byte == 0xF4:
                break
            out += chr(byte)
        return out
    
    def process_data(d):
        dt = str(2000 + d[8]) + '-' + str(d[7]).zfill(2) + '-' + str(d[6]).zfill(2)+' '+str(d[4]).zfill(2)+':'+str(d[5]).zfill(2)
        sensor = sensors[d[3] - 1]

        if d[3] == 2:
            out = [ hid_product, sensor, d[0] + 1, d[1], dt,    '',    '', d[11],   '', '', '', d[9], d[10] ]
        else:
            # flag byte - more measurements needed to get a glue about the bit meanings
            afib = 0
            arr  = 0
            rest = ''
            if d[9] == 13:
                arr = 1
                afib = 1
            elif d[9] == 9:
                afib = 1
            elif d[9] == 2:
                rest = 1
            elif d[9] == 3:
                rest = 0
            else:
                afib = '?'
                arr  = '?'
                rest = '?'

            out = [ hid_product, sensor, d[0] + 1, d[1], dt, d[11], d[12], d[13], rest, arr, afib, d[9], d[10] ]
        return out;
    
    def bye():
        # in case we quit properly, we need to reconnect to get back into PC-Mode
        # regardless, better disconnect the device from PC to save energy
        #query_data(end_cmd)
        #time.sleep(0.05)
        #query_data(exit_cmd)
        return

    if args.func == 'info':
        print("Product: %s" % trim_string(query_data(info_name_cmd)))
        print("HID Manufacturer: %s" % h.get_manufacturer_string())
        print("HID Product: %s" % hid_product)
        print("HID Serial No: %s" % h.get_serial_number_string().encode().hex())
        print("HID Vendor-ID: %s" % hex(vid))
        print("HID Product-ID: %s" % hex(pid))
        bye()
        sys.exit()

    result_list = []

    # init connect
    res = query_data(init_cmd)
    if res[0] != 85:
        sys.stderr.write('unrecognized init response')

    # count data
    res = query_data(cnt_cmd)
    if not res:
        sys.stderr.write('no users found')
        sys.exit()
    user_cnt = res[:2]

    # fetch data
    for user in range(len(user_cnt)):
        if args.user and args.user != user + 1:
            continue
        fetch_cmd[1] = user
        for row in range(user_cnt[user]):
           if args.index and args.index != row:
               continue
           fetch_cmd[2] = row
           res = query_data(fetch_cmd)
           result_list.append(res)

    result = []

    if args.func != 'ecgraw':
        header = ["dev", "sensor", "user", "index", "date_measurement", "sys", "dia", "pulse", "rest", "arr", "afib", "param9", "param10"]
        for data in result_list:
            result.append(process_data(data))
    else:
        header = False
        result = []
        for data in result_list:
            if data[3] == 2:
                ecg_cnt_cmd[1] = data[0]
                ecg_cnt_cmd[2] = data[1]
                res = query_data(ecg_cnt_cmd)
                pages = res[2]
                lastrow = res[3]
                for p in range(pages + 1): #res[3]):
                    ecg_fetch_cmd[1] = data[0]
                    ecg_fetch_cmd[2] = data[1]
                    ecg_fetch_cmd[4] = p
                    rows = 255
                    if p == pages:
                        rows = lastrow
                    for i in range(rows):
                        ecg_fetch_cmd[3] = i
                        res = query_data(ecg_fetch_cmd, 128)
                        result.append(res)

    output = io.StringIO()

    if args.format == 'json':
        if header:
            out = []
            for item in result:
                row = {}
                for i in range(len(header)):
                    row[str(header[i])] = item[i]
                out.append(row)
            json.dump(out, output)
        else:
            json.dump(result, output)

    else:
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=delimiter)
        if header:
            writer.writerow(header)
        for item in result:
            writer.writerow(item)

    if args.outfile:
        with open("output.txt", "w") as f:
            f.write(output.getvalue())
    else:
        print(output.getvalue())

    bye()

except IOError as ex:
    print(ex)
    print("Is the device connected to USB?")
