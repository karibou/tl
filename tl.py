#!/usr/bin/python3
# Add a new task to the gtimelog log file.
# Propose a list of task if only the category is supplied
#
# Copyright (c) 2015 Canonical Ltd.
# Author: Louis Bouchard <louis.bouchard@ubuntu.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

import re, sys, time
from os.path import expanduser

LogFile = '%s/.local/share/gtimelog/timelog.txt' % expanduser("~")

Categories = {
    'ua': 'L3 / L3 support',
    'lp': 'Launchpad & Public',
    'train': 'Mentoring / Edu / Training',
    'meet': 'Meetings',
    'seg' : 'SEG related activities',
    'charm' : 'Charm Devel',
    'doc' : 'Documentation',
    'kb' : 'Knowledge base Work',
    'z' : 'Mainframe related',
    'ib' : 'Mellanox related',
    'svvp' : 'SVVP/Virtio dev',
    'qe' : 'QE',
    'fan' : 'Fan development',
    'is' : 'IS bug work',
    'pers': 'Personal management',
    'comm': 'Community Involvment',
    }

ListLimit = 10


def show_help():
    try:
        # python3-prettytable will be used if installed
        import prettytable
        categories = prettytable.PrettyTable(["Key","Description"],
                                             sortby = "Key",padding_width = 1)
        categories.align["Key"] = "l"
        categories.align["Description"] = "l"
        categories.padding_width = 1
        for keys,description in Categories.items():
            categories.add_row([keys, description])
        print(categories)
    except:
        for keys,description in Categories.items():
            print("%s : %s" % (keys,description))


def select_tasks(category):
    cases = []
    mytask = 0
    regex = re.compile(r'{}'.format(Categories[category]))
    with open(LogFile, 'r') as timelog:
        for line in timelog:
            if regex.findall(line):
                case = regex.split(line)[-1].strip()
                if case.lstrip(": ") not in cases:
                    cases.append(case.lstrip(": "))
    # Get the last items first
    cases.reverse()
    for I in cases:
        if (cases.index(I) + 1) % ListLimit:
            print("{}) {}".format(cases.index(I) + 1, I))
        else:
            # account for modulo = 0 item
            print("{}) {}".format(cases.index(I) + 1, I))
            if cases.index(I) + 1 < len(cases):
                try:
                    mytask = input("Select task (0 to exit,<CR> to continue): ")
                    if mytask == '0':
                            return(None, None)
                    if mytask == '' or not mytask.isdecimal():
                        continue
                    else:
                        mytask = int(mytask)
                        break

                except KeyboardInterrupt:
                    print("Terminated\n")
                    sys.exit(1)

    if not mytask:
        try:
            mytask = input("Select task (0 or <CR> to exit): ")
            if mytask == '0' or mytask == '' or not mytask.isdecimal():
                    return(None, None)
            else:
                mytask = int(mytask)

        except KeyboardInterrupt:
            print("Terminated\n")
            sys.exit(1)

    if mytask > 0 and mytask <= len(cases):
        return(category, cases[mytask - 1])
    else:
        print("Invalid task number")
        return(None, None)


def log_activity(category, task=None):

    now = time.localtime()
    today = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}'.format(
            now.tm_year, now.tm_mon, now.tm_mday,
            now.tm_hour, now.tm_min)

    with open(LogFile, 'a') as timelog:
        if task is None:
            timelog.write('{}: {}\n'.format(today, category))
        else:
            if category in Categories.keys():
                timelog.write('{}: {} : {}\n'.format(
                    today, Categories[category], task))
            else:
                timelog.write('{}: {} : {}\n'.format(
                    today, category, task))
    return(0)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            raise ValueError

        if len(sys.argv) == 2:
            if sys.argv[1] == '?':
                show_help()
                sys.exit(0)
            elif sys.argv[1] == 'new':
                log_activity('new', 'Arrived')
            elif sys.argv[1] in Categories.keys():
                (category, task) = select_tasks(sys.argv[1])
                if category is not None:
                    log_activity(category, task)
            else:
                log_activity(sys.argv[1])
            sys.exit(0)
        else:
            log_activity(sys.argv[1], " ".join(sys.argv[3:]))
        sys.exit(0)

    except ValueError:
        print("Missing Argument")
        sys.exit(1)
