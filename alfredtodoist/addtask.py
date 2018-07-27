#!/usr/bin/env python
"""
Command line entry point into AlfredTodoist.

This is the script that alfred will actually run.
"""
import sys
from workflow import Workflow3

from alfredtodoist.parse import TaskParser


def main(wf):
	import todoist
	args = wf.args


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	log = wf.logger
	sys.exit(wf.run(main))
