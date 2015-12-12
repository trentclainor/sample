# -*- coding: utf-8 -*-

import os


def find_commands(management_dir):
    command_dir = os.path.join(management_dir)
    try:
        return [f[:-3] for f in os.listdir(command_dir)
            if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []


def scripts(dir, manager):
    commands = find_commands(dir)
    class_list = [command.title() for command in commands]
    for command in commands:
        module = __import__("scripts." + command, fromlist=class_list)
        c = getattr(module, "Command")
        manager.add_command(command, c())
