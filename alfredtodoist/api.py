"""
Docstring for main module in AlfredTodoist.

A longer description...
"""
import re


class TaskParser:
	label_regex = r'(?<=@)\w+'
	priority_regex = r'(?P<prefix>!!|p)(?P<priority>[1234])'

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

	def parse(self, text):
		labels, text = self._pop_labels(text)
		priority, text = self._pop_priority(text)
		return {
			'labels': labels,
			'priority': priority,
		}
