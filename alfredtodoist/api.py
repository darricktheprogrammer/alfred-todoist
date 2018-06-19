"""
Docstring for main module in AlfredTodoist.

A longer description...
"""
import re


class TaskParser:
	label_regex = r'(?<=@)\w+'

	def _pop_labels(self, text):
		labels = [g for g in re.findall(self.label_regex, text)]
		for label in labels:
			text = text.replace('@' + label, '')
		return labels, text

	def parse(self, text):
		labels, text = self._pop_labels(text)
		return {
			'labels': labels,
		}
