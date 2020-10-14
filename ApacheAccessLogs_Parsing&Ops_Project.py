"""
Sean Lacey, sean.lacey@ucdconnect.ie, 18902826
This program analyses an Apache access log file, taking several possible
commands to do multiple operations on the log file. The commands, and their use
for analysis, can be found in the main of the program.
"""

import argparse
import os
import sys
from collections import Counter
import datetime
import re

#counts the unique ips
def count_unique_ip(logfile):
    IPset = set()
    for line in logfile:
        IP, sep, tail = line.partition(" ")
        if(len(IP) > 1):
            if(IP != '::1'):
                IPset.add(IP)


    print(len(IPset))
    return

def print_top_n_ip(n, logfile):
    IPset = set()
    occurence = {}
    for line in logfile:
        print_top_n_ip_iterative(n, line, IPset, occurence)

    print("IP                Requests")
    for i in range(n):
        max_value = max(occurence.values())
        max_key = [k for k, v in occurence.items() if v == max_value]
        print(max_key, max_value)
        occurence.pop(max_key.pop())
    return

def print_top_n_ip_iterative(n, line, IPset, occurence):
    IP, sep, tail = line.partition(" ")
    if(IP != '::1'):
        if IP in IPset:
            occurence[IP] = occurence[IP] + 1
        else:
            occurence[IP] = 1
        IPset.add(IP)
    return

def number_of_visits(n, logfile):
    time = datetime.time(0,0,0)
    count = 0
    for line in logfile:
        IP, sep, tail = line.partition(" ")
        if(IP == n):
            if(count > 0):
                previous_time = time
                time = parse_time(tail)
                time_difference = time - previous_time
                #3600 seconds in an hour. Count is incremented if and only if
                #the IP is requested an hour after the last request.
                if(time_difference > datetime.timedelta(0,0,0,0,0,1,0)):
                    count += 1
            else:
                time = parse_time(tail)
                count += 1
    print(count)
    return

def parse_time(tail):
    day1 = int(tail[5])
    day2 = int(tail[6])
    day = day1*10 + day2
    #parse the month
    monthAsStr = tail[8] +tail[9] +tail[10]
    date = datetime.datetime.strptime(monthAsStr, '%b')
    month = date.month
    #parse year
    year1 = int(tail[12])
    year2 = int(tail[13])
    year3 = int(tail[14])
    year4 = int(tail[15])
    year = year1*1000 +year2*100 +year3*10 +year4
    #parse the hour
    hour1 = int(tail[17])
    hour2 = int(tail[18])
    hour = hour1*10 + hour2
    #parse the minute
    minute1 = int(tail[20])
    minute2 = int(tail[21])
    minute = minute1*10 + minute2
    #parse the second
    second1 = int(tail[23])
    second2 = int(tail[24])
    second = second1*10 + second2
    #create the datetime object
    return datetime.datetime(year, month, day, hour, minute, second)


def list_of_requests(n, logfile):
    print("IP             Request")
    for line in logfile:
        IP, sep, tail = line.partition(" ")
        if(IP == n):
            print(IP, re.findall('"([^"]*)"', tail))
    return


def visits_on_date(n, logfile):
    IPset = set()
    occurence = {}
    for line in logfile:
        IP, sep, tail = line.partition(" ")
        time = parse_time(tail)
        day = time.day
        datetimeobj = datetime.datetime.strptime(str(time.month), '%m')
        monthAsStr = datetimeobj.strftime("%b")
        year = time.year
        time_string = "0"+str(day)+monthAsStr+str(year)
        if(time_string == n):
            print_top_n_ip_iterative(n, line, IPset, occurence)

    print("IP                Requests")
    for i in range(5):
        max_value = max(occurence.values())
        max_key = [k for k, v in occurence.items() if v == max_value]
        print(max_key, max_value)
        occurence.pop(max_key.pop())
    return


def main():
    parser = argparse.ArgumentParser(description="An appache log file processor")

    parser.add_argument('-l', '--log-file', help='The log file to analyse', required=True)
    parser.add_argument('-n', help='Prints the number of unique IP adresses', action='store_true')
    parser.add_argument('-t', help='Prints top n IP adresses', type=int)
    parser.add_argument('-v', help='Prints the number of visits of an IP adress')
    parser.add_argument('-L', help='Prints all of the requests made by an IP address')
    parser.add_argument('-d', help='Prints the number of visits of all the requests on a specific date (ddMMMyyy format)')

    arguments = parser.parse_args()

    if(os.path.isfile(arguments.log_file)):
        logfile = open(arguments.log_file)
    else:
        print('The file <', arguments.log_file, '> does not exist')
        sys.exit

    if(arguments.n):
        count_unique_ip(logfile)
    if(arguments.t):
        print_top_n_ip(arguments.t, logfile)
    if(arguments.v):
        number_of_visits(arguments.v, logfile)
    if(arguments.L):
        list_of_requests(arguments.L, logfile)
    if(arguments.d):
        visits_on_date(arguments.d, logfile)

    return


if __name__ == '__main__':
  main()

