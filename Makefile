#!/usr/bin/make

override undefine GTIMELOG_USER
tests:
	@nosetests3 -v --with-coverage --cover-package=tl,rep_tl,weekly_tl
