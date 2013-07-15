#!/usr/bin/python
import os
import json
from subprocess import call, check_output
from optparse import OptionParser

WORKSPACES_HOME = '.guakews'
FORMAT = '.ws'

guake_rename = lambda name: call(['guake', '-r', name])
guake_new = lambda path: call(['guake', '-n', path])
guake_run = lambda command: call(['guake', '-e', command])
guake_focus = lambda index: call(['guake', '-s', index])
guake_current = lambda: check_output(['guake', '-g']).strip()
guake_quit = lambda: call(['guake', '-q'])
guake_start = lambda: call(['guake'])


def main():
    usage = "usage: %prog [options] workspace"
    parser = OptionParser(usage=usage)
    parser.add_option('-r', '--reset', dest="reset",
                      help='close all other tabs.', action='store_true', default=False)
    parser.add_option('-k', '--keep', dest="keep",
                      help='keep current tab.', action='store_true', default=False)

    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    config = load_config(args[0])
    build_workspace(config, opts.reset, opts.keep)


def init_tab(tab):
    guake_rename(tab['name'])

    for command in tab['commands']:
        guake_run(command)


def load_config(name):
    config_path = u'{}/{}/{}.ws'.format(os.environ['HOME'], WORKSPACES_HOME, name)
    with open(config_path) as config_file:
        return json.loads(config_file.read())


def build_workspace(config, reset, keep):
    if reset:
        guake_quit()
        guake_start()

    current_tab_index = guake_current()

    for i, tab in enumerate(config):
        if i != 0 or keep:
            guake_new(tab['path'])
        init_tab(tab)

    guake_focus(current_tab_index)


if __name__ == "__main__":
    main()
