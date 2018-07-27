#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from alfredtodoist.addtask import label_ids_from_names


@pytest.fixture
def TodoistAccount():
	class APIMock:
		state = {
			'labels': [
				{
					'id': 1,
					'name': 'errands'
				},
				{
					'id': 2,
					'name': 'shopping'
				}
			]
		}
	return APIMock()


@pytest.mark.usefixtures("TodoistAccount")
class TestGettingLabelIDs():
	def test_LabelIdsFromNames_GivenSingleExistingLabel_ReturnsSingleId(self):
		ids = label_ids_from_names(['errands'], TodoistAccount())
		assert len(ids) == 1
		assert ids[0] == 1

	def test_LabelIdsFromNames_GivenMultipleExistingLabels_ReturnsAllIds(self):
		ids = label_ids_from_names(['errands', 'shopping'], TodoistAccount())
		assert len(ids) == 2
		assert ids == [1, 2]

	def test_LabelIdsFromNames_GivenNoLabels_ReturnsEmptyList(self):
		ids = label_ids_from_names([], TodoistAccount())
		assert len(ids) == 0

	def test_LabelIdsFromNames_GivenNonExistentLabel_IgnoresLabel(self):
		ids = label_ids_from_names(['grocery'], TodoistAccount())
		assert len(ids) == 0
		# Make sure it still grabs any that exist
		ids = label_ids_from_names(['grocery', 'errands'], TodoistAccount())
		assert len(ids) == 1
		assert ids[0] == 1
