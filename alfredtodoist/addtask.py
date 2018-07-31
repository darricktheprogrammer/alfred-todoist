#!/usr/bin/env python
"""
Command line entry point into AlfredTodoist.

This is the script that alfred will actually run.
"""
import sys
from workflow import Workflow3

from parse import TaskParser


INBOX_ID = 0


def label_ids_from_names(label_names, api):
	labels = api.state['labels']
	return [label['id'] for label in labels if label['name'] in label_names]


def project_id_from_name(project_name, api):
	projects = api.state['projects']
	for project in projects:
		if project['name'] == project_name:
			return project['id']
	return INBOX_ID


def convert_priority(priority):
	"""
	Flips the priority from the interface version to the api version

	In the user interface, 1 is most important and 4 is least important.
	In the api, 4 is most important, and 1 is least important.

	Args:
		priority (int): The user inputted priority
	Returns:
		int

		The API version of the priority.
	"""
	try:
		return [4, 3, 2, 1][priority - 1]
	except (IndexError, TypeError):
		return 1


def main(wf):
	import todoist
	args = wf.args


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	log = wf.logger
	sys.exit(wf.run(main))
