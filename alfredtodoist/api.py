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

	def _pop_notes(self, text):
		if 'note:' not in text:
			return [], text
		note_fragments = text.split('note:')
		notes = []
		for fragment in note_fragments[1:]:
			notes.append(fragment.strip())
			text = text.replace('note:' + fragment, '')
		return notes, text

	def parse(self, text):
		# Parse the todo in order from more rigidly defined specs to more
		# free-flowing text. `TaskParser` does rely somewhat on the order of
		# parsing. By popping things like labels and priority out of the text,
		# it makes it easier to deal with things like due dates and notes.
		#
		# Notes is a special case, in that it relies on `due` to be parsed
		# first. This could be updated, to check for `due`, but by keeping the
		# order of `due` being parsed first, the notes parsing is simpler, but
		# just as effective.
		#
		# The actual todo is considered any text left over after all of the
		# other properties have been parsed out.
		labels, text = self._pop_labels(text)
		priority, text = self._pop_priority(text)
		project, text = self._pop_project(text)
		due, text = self._pop_due_date(text)
		notes, text = self._pop_notes(text)

		return {
			'labels': labels,
			'priority': priority,
			'project': project,
			'due': due,
			'notes': notes,
			'todo': text.strip()
		}
