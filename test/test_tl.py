import unittest, subprocess, sys, tempfile, os, shutil
from mock import patch
import tl


class TlTest(unittest.TestCase):
    @classmethod
    def setUpClass(letest):
        letest.workdir = tempfile.mkdtemp()
        tl.LogFile = os.path.join(letest.workdir, 'timelog.txt')
        # Prepare timelog file with existing tasks
        with open(tl.LogFile, 'w') as timelog:
            timelog.write("2015-03-13 13:21: lunch** :\n")
            timelog.write("2015-03-13 16:34: Upstream Ubuntu :  lp1415880\n")
            timelog.write("2015-03-13 17:45: L3 / L3 support :  SF7-openafs\n")
            timelog.write("2015-03-16 08:41: arrived\n")
            timelog.write("2015-03-16 09:57: Personal management :  email\n")
            timelog.write("2015-03-16 11:07: L3 / L3 support :  SF7-openafs\n")
            timelog.write("2015-03-16 11:11: L3 / L3 support :  SF801-kdump\n")
            timelog.write("2015-03-17 11:01: Skills building :  python\n")
            timelog.write("2015-03-17 11:02: Skills building :  ruby\n")
            timelog.write("2015-03-17 11:03: Skills building :  c\n")
            timelog.write("2015-03-17 11:04: Skills building :  apl\n")
            timelog.write("2015-03-17 11:05: Skills building :  perl\n")
            timelog.write("2015-03-17 11:06: Skills building :  go\n")
            timelog.write("2015-03-17 11:07: Skills building :  java\n")
            timelog.write("2015-03-17 11:08: Skills building :  nodejs\n")
            timelog.write("2015-03-17 11:09: Skills building :  erlang\n")
            timelog.write("2015-03-17 11:10: Skills building :  basic\n")
            timelog.write("2015-03-17 11:11: Skills building :  pascal\n")
            timelog.write("2015-03-18 11:10: Internal meetings : maas\n")
            timelog.write("2015-03-18 11:11: Internal meetings : juju\n")
            timelog.write("2015-03-18 11:12: Internal meetings : supp\n")
            timelog.write("2015-03-18 11:13: Internal meetings : team\n")
            timelog.write("2015-03-18 11:14: Internal meetings : mgr\n")
            timelog.write("2015-03-18 11:15: Internal meetings : foundation\n")
            timelog.write("2015-03-18 11:16: Internal meetings : server\n")
            timelog.write("2015-03-18 11:17: Internal meetings : sabdfl\n")
            timelog.write("2015-03-18 11:18: Internal meetings : kernel\n")
            timelog.write("2015-03-18 11:19: Internal meetings : mom\n")

    @classmethod
    def tearDownClass(letest):
        shutil.rmtree(letest.workdir)

    def test_new(self):
        '''testing only 'new' argument'''
        tl.log_activity('new', 'Arrived')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('Arrived'))

    def test_ua_entry(self):
        '''testing a UA entry'''
        tl.log_activity('ua', 'This is one entry')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('L3 / L3 support : This is one entry'))

    def test_not_logged(self):
        '''testing argument with two asterix'''
        tl.log_activity('lunch**')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('lunch**'))

    def test_absolutely_not_logged(self):
        '''testing argument with three asterix'''
        tl.log_activity('lunch***')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('lunch***'))

    def test_help(self):
        '''testing ? to get help '''
        self.assertEqual(tl.show_help(), ("Categories : ['comm', 'know', 'meet', "
                                          "'pers', 'skill', 'team', 'ua', "
                                          "'ubu', 'up']"))

    def test_select_tasks_out_of_range(self):
        '''testing category only and giving out of range answer'''
        with patch('builtins.input', return_value='3'):
            tl.select_tasks('ua')
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs\nInvalid task number')

    def test_select_tasks_select_0(self):
        '''testing category only and answering 0'''
        with patch('builtins.input', return_value='0'):
            self.assertEqual(tl.select_tasks('ua'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs')

    def test_select_tasks_select_nothing(self):
        '''testing category only and answering nothing'''
        with patch('builtins.input', return_value=''):
            self.assertEqual(tl.select_tasks('ua'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs')

    def test_select_tasks_select_first_task(self):
        '''testing category only and selecting first task'''
        with patch('builtins.input', return_value='1'):
            self.assertEqual(tl.select_tasks('ua'), ('ua', 'SF801-kdump'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs')

    def test_category_with_exactly_10_items(self):
        '''testing category with 10 entries and selecting last task'''
        with patch('builtins.input', return_value='10'):
            self.assertEqual(tl.select_tasks('meet'), ('meet', 'maas'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) mom\n2) kernel\n3) sabdfl\n4) server\n5) foundation\n6) mgr\n7) team\n8) supp\n9) juju\n10) maas','maas')

    def test_category_with_exactly_10_items_no_selection(self):
        '''testing category with 10 entries and no selection'''
        with patch('builtins.input', return_value=''):
            self.assertEqual(tl.select_tasks('meet'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) mom\n2) kernel\n3) sabdfl\n4) server\n5) foundation\n6) mgr\n7) team\n8) supp\n9) juju\n10) maas')

    def test_category_with_12_items(self):
        '''testing category with 12 entries and selecting first task'''
        with patch('builtins.input', return_value='1'):
            self.assertEqual(tl.select_tasks('skill'), ('skill', 'pascal'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) pascal\n2) basic\n3) erlang\n4) nodejs\n5) java\n6) go\n7) perl\n8) apl\n9) c\n10) ruby')

    def test_category_with_12_items_no_selection(self):
        '''testing category with 12 entries and not selecting task'''
        with patch('builtins.input', return_value=''):
            self.assertEqual(tl.select_tasks('skill'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) pascal\n2) basic\n3) erlang\n4) nodejs\n5) java\n6) go\n7) perl\n8) apl\n9) c\n10) ruby\n11) python')

    def test_category_with_12_items_last_selection(self):
        '''testing category with 12 entries and selecting first task'''
        with patch('builtins.input', return_value='11'):
            self.assertEqual(tl.select_tasks('skill'), ('skill', 'python'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) pascal\n2) basic\n3) erlang\n4) nodejs\n5) java\n6) go\n7) perl\n8) apl\n9) c\n10) ruby')


    def _get_last_log_line(self):
        with open(tl.LogFile, 'r') as timelog:
            for line in timelog:
                continue
        return(line)
