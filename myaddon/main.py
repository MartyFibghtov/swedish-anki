"""Add button to anki editor."""
import os
import urllib
import webbrowser
from typing import List

from anki.hooks import addHook
from aqt.utils import tooltip

from .AnkiWrappers.anki_file_system import get_content_folder_path
from .AnkiWrappers.note_editor import NoteEditor
from .translator import Translator, Word
from .utilities.loader import download_url_to_file
from .utilities.word_processors import normalize_word
from .utilities.reverso_context_api.client import Client

import itertools

def open_url(url, search) -> None:
    """Open passed url in browser.

    Args:
        url: url to open, must be ready for formatting using .format
        search: string to be placed in url
    """
    search = urllib.parse.quote(search)
    url = url.format(search)
    webbrowser.open(url, 0, autoraise=False)


def add_audio_to_card(word: Word, note_editor: NoteEditor):
    """Download audio from word url and adds it to card.

    Args:
        word: Word from which url should be extracted
        note_editor: Editor class
    """
    if word.audio_url:
        audio_url = word.audio_url[0]
        folder = get_content_folder_path()
        file_name = download_url_to_file(audio_url, folder)

        note_editor.insert_audio_in_field(audio_path=file_name, field=2)


def fill_anki_card(ed: NoteEditor):
    """
    Add content to anki card.

    Args:
        ed: Editor class, automatically passes by Anki
    """
    search = normalize_word(ed.note.fields[0])

    # Search in context Reverso

    client = Client("sv", "en")


    # Init Note
    note_editor = NoteEditor(ed.note)


    # Add translation
    note_editor.insert_text_in_field(
        text_to_write=', '.join(list(client.get_translations(search))),
        field=1,
    )

    # Add audio
    try:
        words: List[Word] = translator.translate(ed.note.fields[0])
        for word in words:
            add_audio_to_card(word, note_editor)
    except KeyError:
        tooltip("Not found {0}".format(search))

    # Add Example
    examples = list(itertools.islice(client.get_translation_samples(search, cleanup=False), 2))

    for example in examples:
        # Insert swedish example
        note_editor.insert_text_in_field(
            text_to_write='{0}<br>'.format(example[0]),
            field=4,
            overwrite=False
        )

        # Insert english example
        note_editor.insert_text_in_field(
            text_to_write='{0}<br>'.format(example[1]),
            field=5,
            overwrite=False
        )


    # Open url in SAOL
    open_url('https://context.reverso.net/translation/swedish-english/{0}', search)
    open_url('https://svenska.se/saol/?sok={0}', search)
    # open_url(
    #     'https://www.google.com/search?q={0}&tbm=isch&safe=off&tbs&hl=en&sa=X',
    #     "{0} illustration".format(search),
    # )

    ed.loadNote()


def add_button(buttons, editor):
    both_button = editor.addButton(
        icon=os.path.join(os.path.dirname(__file__), 'images', 'icon30.png'),
        cmd='asd',
        func=lambda ed: ed.saveNow(lambda: fill_anki_card(ed)),
        tip="AutoDefine Word (ctrl+alt+o)",
        toggleable=False,
        label='',
        keys='ctrl+alt+o',
        disables=False,
    )
    """Sets button to fill_anki_card, called by anki

    Args:
        buttons: array of current buttons
        : array of current buttons
    """

    buttons.append(both_button)
    return buttons


translator = Translator()
addHook('setupEditorButtons', add_button)
