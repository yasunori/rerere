# -*- coding: utf-8 -*-
from rerere.commandmanager import CommandManager
from rerere.textmanager import TextManager


def search(mask_str, dt):
    text_manager = TextManager(dt)
    command_manager = CommandManager(mask_str, text_manager=text_manager)
    return text_manager.exec(command_manager=command_manager)
