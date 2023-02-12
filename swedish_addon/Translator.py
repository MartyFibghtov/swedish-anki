import os
from dataclasses import dataclass
from pprint import pprint
from typing import List, Dict
import xml.etree.ElementTree as ET

from .utilities import xmltodict

from .utilities.WordProcessors import WordProcessor

# import os
# from dataclasses import dataclass
# from pprint import pprint
# from typing import List, Dict
# import xml.etree.ElementTree as ET
#
# from utilities import xmltodict
#
# from utilities.WordProcessors import WordProcessor



class DictionaryXmlReader:

    def __init__(self, dict_path):
        self.dict_path = dict_path
    def xml_to_dict(self):
        with open(self.dict_path, 'r', encoding='utf-8') as file:
            my_xml = file.read()

        # Use xmltodict to parse and convert
        # the XML document
        my_dict = xmltodict.parse(my_xml)

        return my_dict

    def get_dictionary(self) -> Dict:
        translations: List = self.xml_to_dict()['xdxf']['lexicon']['ar']

        dictionary = {}
        # Reset all keys to swedish words

        for translation in translations:
            # TODO Choose from different options
            # Or add all options
            if translation['k'] not in dictionary:
                dictionary[translation['k']] = translation['def']

        return dictionary


@dataclass
class Word:
    part_of_speech: str = None
    translation: List[str] = None
    audio_url: List[str] = None
    definition: List[str] = None
    examples: List[str] = None
    image_url: str = None

    @staticmethod
    def to_list(value):
        if not isinstance(value, list):
            return [value]
        return value

    def __init__(self, word_dict: Dict):
        try:
            self.part_of_speech = word_dict['gr']
            self.translation = list(set(self.to_list(word_dict.get('dtrn'))))

            word_urls = word_dict.get('iref')

            audio_url = []
            if word_urls:
                audio_url = list(filter(lambda url: url.endswith(".mp3"), [url['@href'] for url in word_urls]))

            self.audio_url = audio_url
            self.definition = list(set(self.to_list(word_dict.get('def'))))

            examples = self.to_list(word_dict.get('ex'))
            if examples:
                examples = [ex['ex_orig'] for ex in examples if ex]

            self.examples = examples
        except Exception as e:
            pass


class Translator:
    DICTIONARY_PATH = os.path.join(os.path.dirname(__file__), "dict", "folkets_sv_en_public.xml")

    def __init__(self):
        dict_reader = DictionaryXmlReader(self.DICTIONARY_PATH)

        self.dictionary: dict = dict_reader.get_dictionary()
        # pprint(self.dictionary)

    def translate(self, word: str) -> Word:
        word_normalised = WordProcessor.normalize_word(word)
        try:
            word_translation = Word(self.dictionary[word_normalised])
        except KeyError as Error:
            raise KeyError(word)

        return word_translation


# translator = Translator()
#
# pprint(translator.translate("hund"))
