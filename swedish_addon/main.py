from pprint import pprint

from Translator import Translator

t = Translator()


pprint(t.dictionary['ursäkta'])
pprint(t.dictionary['ursäkt'])


pprint(t.translate('ursäkta'))
pprint(t.translate('ursäkt'))