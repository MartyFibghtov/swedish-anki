"""Wrapper for AnkiNote Class."""
from anki.notes import Note


class NoteEditor(object):
    """
    Wrapper for Note.

    Allows adding audio, video and text content.
    """

    def __init__(self, note: Note):
        """Set note to self.note.

        Args:
            note: note to interact later.
        """
        self.note: Note = note

    def insert_audio_in_field(
        self,
        field: int,
        audio_path: str,
        overwrite: bool = True,
        new_line=False,
    ):
        """Add any string to note.

        Args:
            field: Filed number starting form 0.
            audio_path: path to audio
            overwrite: Replace field value or just add.
            new_line: Add new_lines at the end of content.

        """
        audio_section = '[sound:{0}]'.format(audio_path)

        # Insert audio in file
        self.insert_text_in_field(field, audio_section, overwrite, new_line)

    def add_image(self, image_path, field=1):
        """Add an image to anki card.

        Args:
            image_path: path to image that must be added.
            field: Field number starting form 0.

        Raises:
            NotImplementedError: Not implemented
        """
        raise NotImplementedError

    def insert_text_in_field(
        self,
        field: int,
        text_to_write: str,
        overwrite: bool = True,
        new_line=False,
    ):
        """Add any string to note.

        Args:
            field: Filed number starting form 0.
            text_to_write: What to write in field.
            overwrite: Replace field value or just add.
            new_line: Add new_lines at the end of content.

        Raises:
            KeyError: If no such field.
        """
        if len(self.note.fields) < field:
            raise KeyError('Unknown field: {0} '.format(field))

        if overwrite:
            self.note.fields[field] = text_to_write
        else:
            self.note.fields[field] += text_to_write

        if new_line:
            self.insert_text_in_field(field, '<br/>', new_line=False)
