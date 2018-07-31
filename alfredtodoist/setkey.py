#!/usr/bin/env python
"""
Set the user's Todoist api key
"""
import sys
from workflow import Workflow3


def main(wf):
	pass


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	sys.exit(wf.run(main))
