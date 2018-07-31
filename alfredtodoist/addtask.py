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


def should_sync_upfront(task):
	return bool(task['labels'] or task['project'])


def build_api_payload(task, api):
	if should_sync_upfront(task):
		# don't bother making upfront api calls if we don't need existing IDs.
		api.sync()
		label_ids = label_ids_from_names(task['labels'], api)
		project_id = project_id_from_name(task['project'], api)
	else:
		label_ids = []
		project_id = INBOX_ID
	return {
		'labels': label_ids,
		'project': project_id,
		'priority': convert_priority(task['priority']),
		'date_string': task['due']
	}


def create_task(task_text, project_id, api,
				additional_properties=None, notes=None):
	if additional_properties is None:
		additional_properties = {}
	task = api.items.add(task_text, project_id, **additional_properties)
	api.commit()
	if notes:
		for note in notes:
			api.notes.add(task['id'], note)
		api.commit()


def main(wf):
	import todoist

	wf.logger.info("parsing task: '{}'".format(wf.args[0]))
	task = TaskParser().parse(wf.args[0])
	api = todoist.TodoistAPI('')
	payload = build_api_payload(task, api)
	project_id = payload.pop('project')

	wf.logger.debug("task: {}".format(repr(task['todo'])))
	wf.logger.debug("project id: {}".format(repr(project_id)))
	wf.logger.debug("args: {}".format(repr(payload)))
	create_task(task['todo'], project_id, api,
				additional_properties=payload, notes=task['notes'])


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	sys.exit(wf.run(main))
