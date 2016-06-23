#!/usr/bin/python3

from gtimelog.timelog import Reports, TimeWindow, format_duration_short
import datetime

gt_file = '/home/caribou/Dropbox/gtimelog/timelog.txt'
virtual_midnight = datetime.time(2, 0)


def get_time():
    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    week_first = today - datetime.timedelta(days=today.weekday())
    week_last = week_first + datetime.timedelta(days=6)
    week_last = week_last.replace(hour=23, minute=59, second=59)
    return (week_first, week_last)


def main():
    report = Reports
    (week_first, week_last) = get_time()
    log_entries = TimeWindow(gt_file, week_first, week_last, virtual_midnight)
    total_work, total_slack = log_entries.totals()
    entries, totals = log_entries.categorized_work_entries()

    print("[ACTIVITY] %s to %s (louis-bouchard)" %
          (week_first.isoformat().split("T")[0],
           week_last.isoformat().split("T")[0]))
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
                print(u"  %-61s  %+5s" %
                      (entry, format_duration_short(duration)))

            print('-' * 70)
            print(u"%+70s" % format_duration_short(totals[cat]))
        print("Total work done : %s" % format_duration_short(total_work))
if __name__ == '__main__':

    main()
