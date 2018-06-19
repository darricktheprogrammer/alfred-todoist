#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

# Example inputs:
# pick up groceries
# pick up groceries !!1
# pick up groceries p1
# pick up groceries !!1 @errands
# pick up groceries @on_the_go
# pick up groceries p:single actions
# pick up groceries p:groceries
# devtodo pick up groceries !!1 @errands due:tomorrow note:check the grocery list note:check it twice
# pick up groceries !!1 p:groceries @errands due: tomorrow
# pick up groceries !!1 p:groceries @errands due: next week
# pick up groceries !!1 p:groceries @errands due:next week note:check the grocery list
# pick up groceries !!1 p:groceries @errands due:tomorrow note:check the grocery list note:check it twice
# pick up groceries !!1 p:groceries @errands note: check the grocery list
# pick up groceries note: check the grocery list
# pick up groceries #single actions
# pick up groceries #groceries
# pick up groceries !!1 #groceries @errands due: tomorrow
# pick up groceries !!1 #groceries @errands due: next week
# pick up groceries !!1 #groceries @errands due: next week note: check the grocery list
# pick up groceries !!1 #groceries @errands due: tomorrow note: check the grocery list
# pick up groceries !!1 #groceries @errands note: check the grocery list
# pick up groceries !!1 #stuff for the house @errands note: check the grocery list


from alfredtodoist import api


class TestParsingLabels():
	def setup_method(self):
		self.parser = api.TaskParser()

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
