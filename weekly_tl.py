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


def get_time(back):
    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    if back:
        back = int(back[0])
        today = today - datetime.timedelta(weeks=back)
    week_first = today - datetime.timedelta(days=today.weekday())
    week_last = week_first + datetime.timedelta(days=6)
    week_last = week_last.replace(hour=23, minute=59, second=59)
    return (week_first, week_last)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logfile', nargs=1, metavar='LOGFILE',
                        help='Path to the gtimelog logfile to be use')
    parser.add_argument('-u', '--user', nargs=1, metavar='USER',
                        help='User Identification to be used for report')
    parser.add_argument('-n', '--no-time',
                        help='Print weekly report without spent time',
                        action='store_true')
    parser.add_argument('-m', '--minutes',
                        help='Print weekly report with spent time in minutes',
                        action='store_true')
    parser.add_argument('-d', '--days',
                        help='Print weekly report with spent time in days',
                        action='store_true')
    parser.add_argument('-b', '--back',
                        help='Print weekly report back # of weeks',
                        nargs=1)
    args = parser.parse_args()

    if args.logfile is not None:
        LogFile = set_logfile(args.logfile)
    else:
        LogFile = set_logfile()

    if args.user is not None:
        UserId = set_userid(args.user)
    else:
        UserId = set_userid()

    (week_first, week_last) = get_time(args.back)
    Log = TimeLog(LogFile, virtual_midnight)
    log_entries = Log.window_for(week_first, week_last)
    total_work, _ = log_entries.totals()
    entries, totals = log_entries.categorized_work_entries()

    print("[ACTIVITY] %s to %s (%s)" %
          (week_first.isoformat().split("T")[0],
           week_last.isoformat().split("T")[0],
           UserId))
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
            print('%s:' % cat)

            work = [(entry, duration)
                    for start, entry, duration in entries[cat]]
            work.sort()
            for entry, duration in work:
                if not duration:
                    continue  # skip empty "arrival" entries

                entry = entry[:1].upper() + entry[1:]
                if args.no_time:
                    print(u"  %-61s  " % entry)
                elif args.minutes:
                    print(u"  %-85s  %+5s %+4s" %
                        (entry, format_duration_short(duration),
                        as_minutes(duration)))
                elif args.days:
                    print(u"  %-85s  %+5s %.1f" %
                        (entry, format_duration_short(duration),
                        as_minutes(duration)/480))
                else:
                    print(u"  %-85s  %+5s" %
                        (entry, format_duration_short(duration)))

            if args.no_time:
                print("")
            else:
                if args.minutes:
                    print('-' * 100)
                    print(u"%+94s %4s" % (format_duration_short(totals[cat]),
                                        as_minutes(totals[cat])))
                elif args.days:
                    print('-' * 98)
                    print(u"%+94s %.1f" % (format_duration_short(totals[cat]),
                                        as_minutes(totals[cat])/480))
                else:
                    print('-' * 94)
                    print(u"%+94s" % (format_duration_short(totals[cat])))
                    
        print("Total work done : %s" % format_duration_short(total_work))


if __name__ == '__main__':

    main()
