# import the main window object (mw) from aqt
import os
import pathlib
import pprint
from urllib import parse
import webbrowser
from datetime import datetime

import requests
from anki.hooks import addHook
from anki.notes_pb2 import Note
from aqt import mw
from aqt.editor import Editor
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from aqt.utils import tooltip

from swedish_addon.Translator import Translator, Word
from swedish_addon.utilities.WordProcessors import WordProcessor


class AnkiFileSystem:
    @staticmethod
    def get_file_path(file_name, ) -> str:
        collection_path = pathlib.Path(mw.col.path).parent.absolute()
        media_path = os.path.join(collection_path, "collection.media")
        file_path = os.path.join(media_path, file_name)

        return file_path



class NoteEditor:

    def __init__(self, note: Note):
        self.note: Note = note

    def add_word(self, word: Word):

        self.add_text(text=", ".join(word.translation))
        self.add_audio(audio_url=word.audio_url[0])
        self.add_image(image_url=word.image_url)

    def add_audio(self, audio_url: str, field=3):
        # Add audio to anki note
        if not audio_url:
            return

        # get audio path
        time = str(datetime.now())
        audio_name = time + audio_url.split('/')[-1]
        tooltip(audio_name)
        audio_path = AnkiFileSystem.get_file_path(audio_name)
        tooltip(audio_path)
        try:
            r = requests.get(url=audio_url)
            with open(audio_path, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            # TODO write different handlers for errors
            raise e

        # Generate audio section
        audio_section = f"[sound:{audio_name}]"

        # Insert audio in file
        self.add_content(field, audio_section)




    def add_text(self, text, field=1):
        # Add text to anki note
        if not text:
            return

        self.add_content(field, text)
        pass

    def add_image(self, image_url, field=1):
        # Add text to anki note
        if not image_url:
            return

        pass

    def add_content(self, field: int, content: str, overwrite: bool = True, new_line=False):
        # Add any string to note
        try:
            if overwrite:
                self.note.fields[field] = content
            else:
                self.note.fields[field] += content
            if new_line:
                self.add_content(field, "<br/>", new_line=False)
        except KeyError as e:
            raise KeyError("Unknown field " + str(field))


def print_all_notes(ed):
    # showInfo(ed.note.fields[0])
    # showInfo(str())
    try:
        search = WordProcessor.normalize_word(ed.note.fields[0])
        word: Word = translator.translate(ed.note.fields[0])
        # showInfo(str(word.__dict__))
        note: Note = ed.note
        note_editor = NoteEditor(note)
        # Add translation
        note_editor.add_text(", ".join(word.translation), field=1)

        search = parse.quote(search)
        url = "https://svenska.se/saol/?sok=$"
        url = url.replace("$", search)
        tooltip(url)
        webbrowser.open(url, 0, False)

        # Add audio
        if word.audio_url:
            note_editor.add_audio(word.audio_url[0], field=2)

        search = parse.quote(word.translation[0])
        url = "https://www.google.com/search?q=$&tbm=isch&safe=off&tbs&hl=en&sa=X"
        url = url.replace("$", search)

        webbrowser.open(url, 0, False)

        # Add Example
        if word.examples:

            note_editor.add_text(", ".join(word.examples), field=4)

        # Add definition
        if word.definition:
            note_editor.add_text(", ".join(word.definition), field=5)

        # Add part of speech
        if word.part_of_speech:
            note_editor.add_text(word.part_of_speech, field=6)

        ed.loadNote()

    except KeyError as e:
        tooltip(str(e))


def add_button(buttons, editor):
    both_button = editor.addButton(icon=os.path.join(os.path.dirname(__file__), "images", "icon30.png"),
                                   label="",
                                   cmd="AD",
                                   func=lambda ed: ed.saveNow(lambda: print_all_notes(ed)),
                                   toggleable=False,
                                   keys="cmd+shift+Y",
                                   disables=False)

    buttons.append(both_button)
    return buttons


# if __name__ == "main":
translator = Translator()
addHook("setupEditorButtons", add_button)
