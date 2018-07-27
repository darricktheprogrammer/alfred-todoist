#!/usr/bin/env python
"""
Command line entry point into AlfredTodoist.

This is the script that alfred will actually run.
"""
import sys
from workflow import Workflow3

from parse import TaskParser


def transform_for_feedback(task):
	task = {k: v for k, v in task.iteritems()}
	task['labels'] = ', '.join(task['labels'])
	if not task['due']:
		task.pop('due')
	if task['notes']:
		task['notelen'] = len(task['notes'])
	task.pop('notes')
	properties_as_str = ', '.join([k for k in task.keys()])
	wf.logger.debug('properties after transform: ' + properties_as_str)
	return task


def main(wf):
	task_text = wf.args[0]
	wf.logger.info("parsing task: '{}'".format(task_text))
	task = TaskParser().parse(task_text)
	todo = task.pop('todo')
	task = transform_for_feedback(task)
	msg = [': '.join([k, str(v)]) for k, v in task.iteritems()]
	msg = ' | '.join(msg)

	feedback = msg.format(msg, **task)
	wf.logger.debug('parsed message: ' + feedback)
	wf.add_item(title='Add task: ' + todo,
		subtitle=feedback,
		arg=task_text,
		valid=True)
	wf.send_feedback()


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	sys.exit(wf.run(main))
