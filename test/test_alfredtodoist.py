#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from alfredtodoist.parse import TaskParser


class TestParsingLabels():
	def setup_method(self):
		self.parser = TaskParser()

	def test_Parse_GivenSingleLabel_ReturnsSingleLabel(self):
		task = 'pick up groceries @errands'
		parsed = self.parser.parse(task)
		assert parsed['labels'] == ['errands']

	def test_Parse_GivenMultipleLabels_ReturnsAllLabels(self):
		task = 'pick up groceries @errands @grocery'
		parsed = self.parser.parse(task)
		assert parsed['labels'] == ['errands', 'grocery']

	def test_Parse_GivenNoLabels_ReturnsNoLabels(self):
		task = 'pick up groceries'
		parsed = self.parser.parse(task)
		assert len(parsed['labels']) == 0

	def test_Parse_GivenLabelWithUnderscore_ReturnsLabel(self):
		task = 'pick up groceries @on_the_go'
		parsed = self.parser.parse(task)
		assert parsed['labels'] == ['on_the_go']

	@pytest.mark.xfail(strict=True)
	def test_Parse_GivenLabelWithUnicode_ReturnsLabel(self):
		task = 'pick up groceries @grøcery'
		parsed = self.parser.parse(task)
		assert parsed['labels'] == ['grøcery']

	@pytest.mark.xfail(strict=True)
	def test_Parse_GivenLabelWithEmoji_ReturnsLabel(self):
		task = 'pick up groceries @📱phone'
		parsed = self.parser.parse(task)
		assert parsed['labels'] == ['📱phone']


class TestParsingPriority():
	def setup_method(self):
		self.parser = TaskParser()

	def test_Parse_ExclamationPointPriorityFormat_ParsesNumber(self):
		task = 'pick up groceries !!1'
		parsed = self.parser.parse(task)
		assert parsed['priority'] == '1'

	def test_Parse_PPriorityFormat_ParsesNumber(self):
		task = 'pick up groceries p1'
		parsed = self.parser.parse(task)
		assert parsed['priority'] == '1'

	def test_Parse_NoPriority_ReturnsEmptyPriority(self):
		task = 'pick up groceries'
		parsed = self.parser.parse(task)
		assert parsed['priority'] == ''


class TestParsingProject():
	def setup_method(self):
		self.parser = TaskParser()

	def test_Parse_WithOnlyProject_ParsesProject(self):
		task = 'pick up groceries #shopping'
		parsed = self.parser.parse(task)
		assert parsed['project'] == 'shopping'

	def test_Parse_WithoutProject_EmptyProjectReturned(self):
		task = 'pick up groceries'
		parsed = self.parser.parse(task)
		assert parsed['project'] == ''

	def test_Parse_WithoutProjectLabelAndPriority_ParsesCorrectly(self):
		task = 'pick up groceries #shopping !!3 @errands @grocery'
		parsed = self.parser.parse(task)
		assert parsed['project'] == 'shopping'

	def test_Parse_MultiWordProject_ParsesCorrectly(self):
		tasks = [
			'pick up groceries #{grocery shopping} !!3 @errands @grocery',
			'pick up groceries #(grocery shopping) !!3 @errands @grocery',
			'pick up groceries #`grocery shopping` !!3 @errands @grocery',
			'pick up groceries #"grocery shopping" !!3 @errands @grocery',
			"pick up groceries #'grocery shopping' !!3 @errands @grocery",
			]
		for task in tasks:
			parsed = self.parser.parse(task)
			assert parsed['project'] == 'grocery shopping'

	def test_Parse_NonAlpha_ParsesCorrectly(self):
		task = 'pick up groceries #grocery_shopping !!3 @errands @grocery'
		parsed = self.parser.parse(task)
		assert parsed['project'] == 'grocery_shopping'

		task = 'pick up groceries #grocery-shopping !!3 @errands @grocery'
		parsed = self.parser.parse(task)
		assert parsed['project'] == 'grocery-shopping'

		task = 'pick up groceries #grocery_shopping2 !!3 @errands @grocery'
		parsed = self.parser.parse(task)
		assert parsed['project'] == 'grocery_shopping2'


class TestParsingDueDate():
	def setup_method(self):
		self.parser = TaskParser()

	def test_Parse_WithOnlyDueDate_ParsesDueDate(self):
		task = 'pick up groceries due:tonight'
		parsed = self.parser.parse(task)
		assert parsed['due'] == 'tonight'

	def test_Parse_MultiWordDueDate_ParsesDueDate(self):
		task = 'pick up groceries due:every monday starting on the first'
		parsed = self.parser.parse(task)
		assert parsed['due'] == 'every monday starting on the first'

	def test_Parse_WithSpaceAfterColon_ParsesDueDate(self):
		task = 'pick up groceries due: next week'
		parsed = self.parser.parse(task)
		assert parsed['due'] == 'next week'

	def test_Parse_WithLabelAfter_ParsesBoth(self):
		task = 'pick up groceries due: next week @errands'
		parsed = self.parser.parse(task)
		assert parsed['due'] == 'next week'
		assert parsed['labels'] == ['errands']

	def test_Parse_WithNoteAfter_ParsesDueDate(self):
		task = 'pick up groceries due: next week note: go to the new place'
		parsed = self.parser.parse(task)
		assert parsed['due'] == 'next week'

	def test_Parse_WithNoteBefore_ParsesDueDate(self):
		task = 'pick up groceries note: go to the new place due: next week'
		parsed = self.parser.parse(task)
		assert parsed['due'] == 'next week'


class TestParsingNotes():
	def setup_method(self):
		self.parser = TaskParser()

	def test_Parse_WithoutNote_ReturnsEmptyList(self):
		task = '# pick up groceries !!1 #groceries @errands'
		parsed = self.parser.parse(task)
		assert parsed['notes'] == []

	def test_Parse_SingleNote_ParsesNote(self):
		task = '# pick up groceries !!1 #groceries @errands note: check the grocery list'
		parsed = self.parser.parse(task)
		assert parsed['notes'] == ['check the grocery list']

	def test_Parse_WithMultipleNotes_ParsesNotes(self):
		task = '# pick up groceries !!1 #groceries @errands note: check the grocery list note: check it again'
		parsed = self.parser.parse(task)
		assert parsed['notes'] == ['check the grocery list', 'check it again']

	def test_Parse_WithDueDateBefore_ParsesNotes(self):
		task = '# pick up groceries !!1 #groceries @errands due: next week note: check the grocery list note: check it again'
		parsed = self.parser.parse(task)
		assert parsed['notes'] == ['check the grocery list', 'check it again']

	def test_Parse_WithDueDateAfter_ParsesNotes(self):
		task = '# pick up groceries !!1 #groceries @errands note: check the grocery list note: check it again due: next week'
		parsed = self.parser.parse(task)
		assert parsed['notes'] == ['check the grocery list', 'check it again']


class TestTodoTextParsing():
	def setup_method(self):
		self.parser = TaskParser()

	def test_Parse_TodoTextInFront_ParsesTodoOnly(self):
		inputs = [
			'pick up groceries',
			'pick up groceries !!1',
			'pick up groceries p1',
			'pick up groceries !!1 @errands',
			'pick up groceries @on_the_go',
			'pick up groceries !!1 @errands due:tomorrow note:check the grocery list note:check it twice',
			'pick up groceries note: check the grocery list',
			'pick up groceries #groceries',
			'pick up groceries !!1 #groceries @errands due: tomorrow',
			'pick up groceries !!1 #groceries @errands due: next week',
			'pick up groceries !!1 #groceries @errands due: next week note: check the grocery list',
			'pick up groceries !!1 #groceries @errands due: tomorrow note: check the grocery list',
			'pick up groceries !!1 #groceries @errands note: check the grocery list',
		]
		for task in inputs:
			parsed = self.parser.parse(task)
			assert parsed['todo'] == 'pick up groceries'

	def test_Parse_TodoTextBehindOthers_ParsesTodoOnly(self):
		inputs = [
			'!!1 pick up groceries',
			'p1 pick up groceries',
			'!!1 @errands pick up groceries',
			'@on_the_go pick up groceries',
			'!!1 pick up groceries @errands due:tomorrow note:check the grocery list note:check it twice',
			'pick up groceries note: check the grocery list',
			'#groceries pick up groceries',
			'!!1 #groceries @errands pick up groceries due: tomorrow',
			'!!1 #groceries @errands pick up groceries due: next week',
			'!!1 #groceries @errands pick up groceries due: next week note: check the grocery list',
			'!!1 #groceries @errands pick up groceries due: tomorrow note: check the grocery list',
			'!!1 #groceries @errands pick up groceries note: check the grocery list',
		]
		for task in inputs:
			parsed = self.parser.parse(task)
			assert parsed['todo'] == 'pick up groceries'
