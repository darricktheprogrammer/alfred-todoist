"""
Docstring for main module in AlfredTodoist.

A longer description...
"""
import re


class TaskParser:
	label_regex = r'(?<=@)\w+'
	priority_regex = r'(?P<prefix>!!|p)(?P<priority>[1234])'
	project_regex = r'(?<=#)\w+'

	def _pop_labels(self, text):
		labels = [g for g in re.findall(self.label_regex, text)]
		for label in labels:
			text = text.replace('@' + label, '')
		return labels, text

	def _pop_priority(self, text):
		priority = re.search(self.priority_regex, text)
		if priority:
			priority_number = priority.group('priority')
			replacement = priority.group('prefix') + priority_number
			text = text.replace(replacement, '')
		else:
			priority_number = ''
		return priority_number, text

	def _pop_project(self, text):
		project = re.search(self.project_regex, text)
		if project:
			project_name = project.group()
			text = text.replace('#' + project_name, '')
		else:
			project_name = ''
		return project_name, text

	def _pop_due_date(self, text):
		if 'due:' not in text:
			return '', text
		# if `note:` follows `due:`, get all of the text up until then. If
		# there is no note, this just gets the entire string after `due:`.
		due_text = text.split('due:')[1]
		due_text = due_text.split('note:')[0]
		return due_text.strip(), text.replace('due:' + due_text, '')

	def parse(self, text):
		labels, text = self._pop_labels(text)
		priority, text = self._pop_priority(text)
		project, text = self._pop_project(text)
		due, text = self._pop_due_date(text)
		return {
			'labels': labels,
			'priority': priority,
			'project': project,
			'due': due,
		}
