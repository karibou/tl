#!/usr/bin/env python3
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

import argparse
import re
import sys
import time
import os

# Categories = {
    # 'train': 'Mentoring / Edu / Training',
    # 'meet': 'Meetings',
    # 'doc': 'Documentation',
    # 'pers': 'Personal management',
    # 'pto': 'Paid Timeout',
    # 'cp': 'Compute Team',
    # 'dev': 'Non Compute development',
    # 'dr': 'Compute Doctor',
    # 'self': 'Self Training',
    # 'help': 'Help Out La Maison',
    # }


def import_file(import_file):
    """
    Import existing task list
    """
    if not os.path.dirname(import_file):
        import_file = os.curdir + '/' + import_file
    if os.path.exists(import_file):
        with open(import_file, 'rb') as infile:
            with open(LogFile, 'wb') as outfile:
                count = outfile.write(infile.read())
        print("Imported %d bytes of data" % count)


def create_logfile(newfile):
    """
    Create a new logfile
    """
    if not os.path.exists(newfile):
        os.makedirs(os.path.dirname(newfile), exist_ok=True)
        with open(newfile, 'w') as newfile:
            newfile.write('')


def set_logfile(argfile=None):
    """
    Set logfile accorting to env variable or option
    """
    if argfile is not None:
        logfile = argfile[0]
    else:
        env = os.environ.get("GTIMELOG_FILE")
        if env is not None and env is not '':
            logfile = env
        else:
            home = os.path.expanduser("~")
            logfile = '%s/.local/share/gtimelog/timelog.txt' % home
    create_logfile(logfile)
    return logfile


class tasklog():
    def __init__(self):
        self.cases = []
        self.LogFile = ''
        self.categories = {}
        self.ListLimit = 10

    def get_categories(self):
        """
        Define the valid categories from entries in the log file
        """
        regex = re.compile(r'new_?category.*[**]\n')
        self.categories = {}
        for line in self.cases:
            if regex.findall(line):
                case = line.split(' ')
                self.categories[case[3]] = ' '.join(case[4:]).rstrip('**\n')


    def print_categories(self, Raw=None):
        """
        Print the list of categories
        """
        if Raw:
            for k in sorted(self.categories):
                print(k)
            return
        try:
            # python3-prettytable will be used if installed
            import prettytable
            cat_list = prettytable.PrettyTable(["Key", "Description"],
                                                 sortby="Key", padding_width=1)
            cat_list.align["Key"] = "l"
            cat_list.align["Description"] = "l"
            cat_list.padding_width = 1
            for keys, description in self.categories.items():
                cat_list.add_row([keys, description])
            print(cat_list)
        except:
            for keys, description in self.categories.items():
                print("%s : %s" % (keys, description))

    def print_tasks(self, category, **kwargs):
        """
        Print the list of tasks for a given category
        """
        tasks = self.get_tasks_by_category(category)
        if "escape" in kwargs and kwargs["escape"]:
            new_tasks = [t.replace(" ", "\\ ") for t in tasks]
            tasks = new_tasks
        print("\n".join(tasks))


    def get_all_cases(self):
        """
        Get all cases from the logfile
        """
        with open(self.logfile, 'r') as timelog:
            all_cases = timelog.readlines()
        all_cases.reverse()
        self.cases = all_cases

    def get_tasks_by_category(self, category):
        """
        Get all tasks for a given category
        """
        regex = re.compile(r'{} '.format(self.categories[category]))
        cat_cases = []
        for line in self.cases:
            if regex.findall(line):
                case = regex.split(line)[-1].strip()
                if case.lstrip(": ") not in cat_cases:
                    cat_cases.append(case.lstrip(": "))
        return cat_cases


    def select_tasks(self, category):
        """
        Select existing tasks for a given category
        """
        task_cases = self.get_tasks_by_category(category)
        mytask = 0
        for I in task_cases:
            if (task_cases.index(I) + 1) % self.ListLimit:
                print("{}) {}".format(task_cases.index(I) + 1, I))
            else:
                # account for modulo = 0 item
                print("{}) {}".format(task_cases.index(I) + 1, I))
                if task_cases.index(I) + 1 < len(task_cases):
                    try:
                        mytask = input("Select task (0 to exit,<CR> to continue): "
                                       )
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

        if mytask > 0 and mytask <= len(task_cases):
            return(category, task_cases[mytask - 1])
        else:
            print("Invalid task number")
            return(None, None)


    def log_activity(self, category, task=None):
        """
        Enter a new task for a category
        """
        now = time.localtime()
        today = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}'.format(
            now.tm_year, now.tm_mon, now.tm_mday,
            now.tm_hour, now.tm_min)

        with open(self.logfile, 'a') as timelog:
            if task is None:
                timelog.write('{}: {}\n'.format(today, category))
            else:
                if category in self.categories.keys():
                    timelog.write('{}: {} : {}\n'.format(
                        today, self.categories[category], task))
                else:
                    timelog.write('{}: {} : {}\n'.format(
                        today, category, task))
        return 0


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('task', nargs='*',
                        help='category | category : task title')
    parser.add_argument('-c', '--list-categories',
                        help='list available task categories',
                        action='store_true')
    parser.add_argument('-t', '--list-tasks', nargs=1, metavar='CATEGORY',
                        help='list available tasks for a given category')
    parser.add_argument('-r', '--raw',
                        help='produce raw output (without pretty formatting)',
                        action='store_true')
    parser.add_argument('-l', '--logfile', nargs=1, metavar='LOGFILE',
                        help='Path to the gtimelog logfile to be use')
    parser.add_argument('-i', '--importfile', nargs=1, metavar='IMPORTFILE',
                        help='Path to a gtimelog file to import')
    args = parser.parse_args()

    Tl = tasklog()

    if args.logfile is not None:
        Tl.logfile = set_logfile(args.logfile)
    else:
        Tl.logfile = set_logfile()

    Tl.get_all_cases()

    Tl.get_categories()

    if args.list_categories:
        Tl.print_categories(args.raw)
        sys.exit(0)

    if args.list_tasks:
        Tl.print_tasks(args.list_tasks[0], escape=args.raw)
        sys.exit(0)

    if args.importfile:
        import_file(args.importfile[0])
        sys.exit(0)

    if args.task:
        import pdb
        pdb.set_trace()
        if len(args.task) == 1 or args.task[-1].endswith('**'):
            if args.task[0] == '?':
                show_help()
                sys.exit(0)
            elif args.task[0] == 'new':
                Tl.log_activity('new', 'Arrived')
            elif args.task[0] in Tl.categories:
                (category, task) = Tl.select_tasks(args.task[0])
                if category:
                    Tl.log_activity(category, task)
            else:
                Tl.log_activity(args.task[0])
        else:
            if args.task[0].rstrip(':') in [ 'newcategory', 'new_category' ]:
                Tl.log_activity(args.task[0], " ".join(args.task[1:]))
            else:
                Tl.log_activity(args.task[0], " ".join(args.task[2:]))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

