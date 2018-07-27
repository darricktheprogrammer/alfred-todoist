"""
Parsing for Todos.
"""
import re


class TaskParser:
	"""
	For parsing a string of todo text into its various parts.
	"""
	label_regex = r'(?<=@)\w+'
	priority_regex = r'(?P<prefix>!!|p)(?P<priority>[1234])'
	project_regex = r'''#([`{\("'](?P<project_space>[\w ]+)[`}\)"']|(?P<project>[-\w]+))'''

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
			for groupname in ['project_space', 'project']:
				if project.group(groupname):
					project_name = project.group(groupname)

			text = re.sub(self.project_regex, '', text)
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
			text = note_fragments[0].strip()
		return notes, text

	def parse(self, text):
		"""
		Parse the todo text

		Extracts the following components:
			labels: `@label`
			priority: `!!1`, `p3`
			project: `#project`
			due date: `due: tomorrow`
			notes: `note: this is a note`
			todo: Anything left over after the other properties have been parsed

		* The todo must come before any notes or due date.
		* You can have as many separate notes as you want.
		* multi-word projects can be delimited by any of the following:
			* #{grocery shopping}
			* #(grocery shopping)
			* #`grocery shopping`
			* #"grocery shopping"
			* #'grocery shopping'

		Example:
			TaskParser.parse('get milk !!3 #{grocery shopping} @errands @grocery_store due: tomorrow note: get whole milk note: check the expiration date')
			{
				'labels': [@errands, @grocery_store],
				'priority': '3',
				'project': 'grocery shopping',
				'due': 'tomorrow',
				'notes': ['get whole milk', 'check the expiration date'],
				'todo': 'get milk'
			}
		Args:
			text (string): The text to parse
		Returns:
			dict

			{
				'labels': list,
				'priority': str,
				'project': str,
				'due': str,
				'notes': list,
				'todo': str
			}
		"""
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
