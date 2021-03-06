#!/usr/bin/env python
"""
Give the user immediate feedback to how what they are typing is received.

This script parses out the user's input and provides it back in an easy
to read manner.
"""
import sys
from workflow import Workflow3, PasswordNotFound

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
	# Ensure there is an API key set upfront. Don't bother providing any other
	# feedback until that is done.
	try:
		wf.get_password('todoist')
	except PasswordNotFound:
		wf.add_item('Cannot find API key.',
			'Use `todo:setkey <key>` to add your Todoist API key.',
			valid=False)
		wf.send_feedback()
		return 0

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
