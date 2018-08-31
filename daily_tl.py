#!/usr/bin/env python3

import datetime
import argparse
import os
from gtimelog.timelog import TimeLog, format_duration_short, as_minutes

virtual_midnight = datetime.time(2, 0)


def set_logfile(argfile=None):
    if argfile is not None:
        return argfile[0]
    else:
        env = os.environ.get("GTIMELOG_FILE")
        if env is not None:
            return env
    return '%s/.local/share/gtimelog/timelog.txt' % os.path.expanduser("~")


def set_userid(user=None):
    if user is not None:
        return user[0]
    else:
        env = os.environ.get("GTIMELOG_USER")
        if env is not None:
            return env
    return '<replace by your user identification>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logfile', nargs=1, metavar='LOGFILE',
                        help='Path to the gtimelog logfile to be use')
    parser.add_argument('-u', '--user', nargs=1, metavar='USER',
                        help='User Identification to be used for report')
    parser.add_argument('-t', '--time',
                        help='Print daily report with spent time',
                        action='store_false')
    parser.add_argument('-H', '--header',
                        help='Print category headers',
                        action='store_true')
    parser.add_argument('-m', '--minutes',
                        help='Print daily report with spent time in minutes',
                        action='store_true')
    parser.add_argument('-b', '--back',
                        help='Print daily report back # of days',
                        metavar='BACK', type=int)
    args = parser.parse_args()

    if args.logfile is not None:
        LogFile = set_logfile(args.logfile)
    else:
        LogFile = set_logfile()

    if args.user is not None:
        UserId = set_userid(args.user)
    else:
        UserId = set_userid()

    day_start = datetime.datetime.today().replace(hour=0, minute=0, second=0,
                                                  microsecond=0)
    if args.back:
        day_start = day_start - datetime.timedelta(days=args.back)
    day_end = day_start.replace(hour=23, minute=59, second=59,
                                                microsecond=999)
    Log = TimeLog(LogFile, virtual_midnight)
    log_entries = Log.window_for(day_start, day_end)
    total_work, _ = log_entries.totals()
    entries, totals = log_entries.categorized_work_entries()

    print("Today's work for %s" % UserId)
    if entries:
        if None in entries:
            categories = sorted(entries)
            categories.append('No category')
            entries['No category'] = e
            t = totals.pop(None)
            totals['No category'] = t
        else:
            categories = sorted(entries)
        for cat in categories:
            if args.header:
                print('- %s:' % cat)

            work = [(entry, duration)
                    for start, entry, duration in entries[cat]]
            work.sort()
            for entry, duration in work:
                if not duration:
                    continue  # skip empty "arrival" entries

                entry = entry[:1].upper() + entry[1:]
                if args.time:
                    print(u"  - %-61s  " % entry)
                else:
                    if args.minutes:
                        print(u"  - %-59s  %+5s %+4s" %
                              (entry, format_duration_short(duration),
                               as_minutes(duration)))
                    else:
                        print(u"  - %-59s  %+5s" %
                              (entry, format_duration_short(duration)))

            if args.time:
                pass
                # print("")
            else:
                if args.minutes:
                    print('-' * 75)
                    print(u"%+70s %4s" % (format_duration_short(totals[cat]),
                                          as_minutes(totals[cat])))
                else:
                    print('-' * 70)
                    print(u"%+70s" % (format_duration_short(totals[cat])))
        print("Total work done : %s" % format_duration_short(total_work))


if __name__ == '__main__':

    main()
