# import the main window object (mw) from aqt
import pprint

from anki.hooks import addHook
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from aqt.utils import tooltip

from swedish_addon.Translator import Translator


def print_all_notes(ed):
    # showInfo(ed.note.fields[0])
    # showInfo(str(translator.translate(ed.note.fields[0])))
    ed.note.fields[1] = ", ".join(translator.translate(ed.note.fields[0]).translation)

    ed.loadNote()


def add_button(buttons, editor):
    both_button = editor.addButton(icon=os.path.join(os.path.dirname(__file__), "images", "icon30.png"),
                                   label="",
                                   cmd="AD",
                                   func=lambda ed: ed.saveNow(lambda: print_all_notes(ed)),
                                   toggleable=False,
                                   disables=False)

    buttons.append(both_button)
    return buttons


translator = Translator()

addHook("setupEditorButtons", add_button)
