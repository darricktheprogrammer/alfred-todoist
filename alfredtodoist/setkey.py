#!/usr/bin/env python
"""
Save the user's Todoist api key in the keychain.
"""
import sys
from workflow import Workflow3


def main(wf):
	wf.save_password('todoist', wf.args[0])


if __name__ == '__main__':
	wf = Workflow3(libraries=['./lib'])
	sys.exit(wf.run(main))
