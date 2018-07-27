#!/usr/bin/env python
"""
Command line entry point into AlfredTodoist.

This is the script that alfred will actually run.
"""
import sys
from workflow import Workflow3

from parse import TaskParser


def label_ids_from_names(label_names, api):
	labels = api.state['labels']
	return [label['id'] for label in labels if label['name'] in label_names]


def main(wf):
	import todoist
	args = wf.args


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	log = wf.logger
	sys.exit(wf.run(main))
