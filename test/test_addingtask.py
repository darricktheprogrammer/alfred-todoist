#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from alfredtodoist.addtask import (
	INBOX_ID,
	label_ids_from_names, project_id_from_name, convert_priority
	)


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
			],
			'projects': [
				{
					'id': 1,
					'name': 'plan birthday party'
				},
				{
					'id': 2,
					'name': 'hang shelves'
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


@pytest.mark.usefixtures("TodoistAccount")
class TestGettingProjectID():
	def test_ProjectIdFromName_GivenExistingProject_ReturnsProjectId(self):
		proj_id = project_id_from_name('plan birthday party', TodoistAccount())
		assert proj_id == 1

	def test_ProjectIdFromName_GivenNonExistingProject_ReturnsInboxId(self):
		proj_id = project_id_from_name('no', TodoistAccount())
		assert proj_id == INBOX_ID

	def test_ProjectIdFromName_GivenEmptyProjectName_ReturnsInboxId(self):
		proj_id = project_id_from_name('', TodoistAccount())
		assert proj_id == INBOX_ID


@pytest.mark.usefixtures("TodoistAccount")
class TestPriorityConversion():
	def test_ConvertPriority_GivenUiValues_ReturnsApiValues(self):
		assert convert_priority(1) == 4
		assert convert_priority(2) == 3
		assert convert_priority(3) == 2
		assert convert_priority(4) == 1

	def test_ConvertPriority_Given4_Returns1(self):
		assert convert_priority(4) == 1

	def test_ConvertPriority_GivenOutOfRange_DefaultsToNoPriority(self):
		assert convert_priority(5) == 1

	def test_ConvertPriority_GivenString_DefaultsToNoPriority(self):
		assert convert_priority('4') == 1

	def test_ConvertPriority_Given0_DefaultsToNoPriority(self):
		assert convert_priority(0) == 1
