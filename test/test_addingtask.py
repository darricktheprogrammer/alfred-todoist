#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mock import Mock

import pytest

from alfredtodoist.addtask import (
	INBOX_ID,
	label_ids_from_names, project_id_from_name, convert_priority,
	build_api_payload, create_task
	)


@pytest.fixture
def TodoistAccount():
	return Mock()


@pytest.fixture
def DummyTask():
	return {
		'labels': [],
		'project': '',
		'priority': 1,
		'due': ''
	}


@pytest.fixture
def existing_labels():
	return [
		{'id': 1, 'name': 'errands'},
		{'id': 2, 'name': 'shopping'}
	]


@pytest.fixture
def existing_projects():
	return [
		{'id': 1, 'name': 'plan birthday party'},
		{'id': 2, 'name': 'hang shelves'}
	]


@pytest.mark.usefixtures("TodoistAccount", "existing_labels")
class TestGettingLabelIDs():
	def test_LabelIdsFromNames_GivenSingleExistingLabel_ReturnsSingleId(self):
		api = TodoistAccount()
		api.state = {'labels': existing_labels()}
		ids = label_ids_from_names(['errands'], api)
		assert len(ids) == 1
		assert ids[0] == 1

	def test_LabelIdsFromNames_GivenMultipleExistingLabels_ReturnsAllIds(self):
		api = TodoistAccount()
		api.state = {'labels': existing_labels()}
		ids = label_ids_from_names(['errands', 'shopping'], api)
		assert len(ids) == 2
		assert ids == [1, 2]

	def test_LabelIdsFromNames_GivenNoLabels_ReturnsEmptyList(self):
		api = TodoistAccount()
		api.state = {'labels': existing_labels()}
		ids = label_ids_from_names([], api)
		assert len(ids) == 0

	def test_LabelIdsFromNames_GivenNonExistentLabel_IgnoresLabel(self):
		api = TodoistAccount()
		api.state = {'labels': existing_labels()}
		ids = label_ids_from_names(['grocery'], api)
		assert len(ids) == 0
		# Make sure it still grabs any that exist
		ids = label_ids_from_names(['grocery', 'errands'], api)
		assert len(ids) == 1
		assert ids[0] == 1


@pytest.mark.usefixtures("TodoistAccount", "existing_projects")
class TestGettingProjectID():
	def test_ProjectIdFromName_GivenExistingProject_ReturnsProjectId(self):
		api = TodoistAccount()
		api.state = {'projects': existing_projects()}
		proj_id = project_id_from_name('plan birthday party', api)
		assert proj_id == 1

	def test_ProjectIdFromName_GivenNonExistingProject_ReturnsInboxId(self):
		api = TodoistAccount()
		api.state = {'projects': existing_projects()}
		proj_id = project_id_from_name('no', api)
		assert proj_id == INBOX_ID

	def test_ProjectIdFromName_GivenEmptyProjectName_ReturnsInboxId(self):
		api = TodoistAccount()
		api.state = {'projects': existing_projects()}
		proj_id = project_id_from_name('', api)
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


@pytest.mark.usefixtures("TodoistAccount", "DummyTask", "existing_labels", "existing_projects")
class TestApiCalls():
	def test_BuildApiPayload_NoLabelsOrProjects_DoesNotSync(self):
		api = TodoistAccount()
		task = DummyTask()
		build_api_payload(task, api)
		api.sync.assert_not_called()

	def test_BuildApiPayload_LabelsButNoProjects_ShouldSync(self):
		api = TodoistAccount()
		api.state = {'labels': existing_labels(), 'projects': []}
		task = DummyTask()
		task.update({'labels': ['errands']})
		build_api_payload(task, api)
		api.sync.assert_called()

	def test_BuildApiPayload_ProjectButNoLabels_ShouldSync(self):
		api = TodoistAccount()
		api.state = {'labels': [], 'projects': existing_projects()}
		task = DummyTask()
		task.update({'project': 'a project'})
		build_api_payload(task, api)
		api.sync.assert_called()

	def test_BuildApiPayload_BothProjectAndLabels_ShouldSync(self):
		api = TodoistAccount()
		api.state = {'labels': existing_labels(), 'projects': existing_projects()}
		task = DummyTask()
		task.update({'labels': ['errands'], 'project': 'a project'})
		build_api_payload(task, api)
		api.sync.assert_called()

	def test_CreateTask_GivenNoPayload_CallsApiWithEmptyPayload(self):
		api = TodoistAccount()
		create_task('test todo', 0, api)
		api.items.add.assert_called_with('test todo', 0)

	def test_CreateTask_GivenPayload_CallsApiWithPayload(self):
		api = TodoistAccount()
		payload = {
			'labels': [1],
			'priority': 1,
			'date_string': ''
		}
		create_task('test todo', 0, api, additional_properties=payload)
		api.items.add.assert_called_with('test todo', 0,
			labels=[1], priority=1, date_string='')

	def test_CreateTask_GivenSingleNote_AddsNoteAfterCreatingTask(self):
		api = TodoistAccount()
		api.items.add.return_value = {'id': 1}
		create_task('test todo', 0, api, notes=['a note'])
		api.notes.add.assert_called_with(1, 'a note')
		api.commit.assert_called()

	def test_CreateTask_GivenMultipleNotes_AddsMultipleNotesAfterCreatingTask(self):
		api = TodoistAccount()
		api.items.add.return_value = {'id': 1}
		create_task('test todo', 0, api, notes=['a note', 'second note'])
		api.notes.add.assert_any_call(1, 'a note')
		api.notes.add.assert_any_call(1, 'second note')
		assert api.notes.add.call_count == 2
		api.commit.assert_called()

	def test_CreateTask_GivenNoNotes_DoesntAddNotes(self):
		api = TodoistAccount()
		api.items.add.return_value = {'id': 1}
		create_task('test todo', 0, api)
		api.items.add.assert_called()
		api.notes.add.assert_not_called()
		api.commit.assert_not_called()
