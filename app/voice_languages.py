"""Explicit language gate for the reservation voice path."""
import json
import re
from pathlib import Path
# Nova-3 language codes from the vendor's Models & Languages Overview, checked 2026-10-22.
STT_LANGUAGES = set('af ar hy as be bn bs bg ca zh hr cs da nl en et fi fr ka de el gu he hi hu id it ja kn kk ko lv lt mk ms mr mn ne no ps fa pl pt pa ro ru sr sk sl es sv tl ta te th tr uk ur vi'.split())
COUNTRY_LANGUAGE = {'TR':'tr','GB':'en','IE':'en','US':'en','CA':'en','AU':'en','NZ':'en','FR':'fr','DE':'de','IT':'it','ES':'es','PT':'pt','JP':'ja','KR':'ko','CN':'zh','NL':'nl','RU':'ru','IN':'hi','ZA':'en','AE':'ar','SA':'ar'}
COUNTRY_ZONE = {'TR':'Europe/Istanbul','IE':'Europe/Dublin','GB':'Europe/London','FR':'Europe/Paris','DE':'Europe/Berlin','IT':'Europe/Rome','ES':'Europe/Madrid','PT':'Europe/Lisbon','JP':'Asia/Tokyo','KR':'Asia/Seoul','CN':'Asia/Shanghai','NL':'Europe/Amsterdam','IN':'Asia/Kolkata','AE':'Asia/Dubai','SA':'Asia/Riyadh'}


def supported():
    data = json.loads(Path(__file__).with_name('voice_models.json').read_text(encoding='utf-8'))
    return {language: ('eleven_flash_v2_5' if language in data['eleven_flash_v2_5'] else 'eleven_v3')
            for language in STT_LANGUAGES & (set(data['eleven_flash_v2_5']) | set(data['eleven_v3']))}


def normalize_language(language):
    if not isinstance(language,str) or not re.fullmatch(r'[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8}){0,2}',language):
        raise ValueError('Geçerli bir görüşme dili seç.')
    return language.split('-')[0].lower()


def model_for(language):
    language=normalize_language(language)
    model = supported().get(language)
    if not model:
        raise ValueError('Bu dil için uçtan uca konuşma desteği yok. Desteklenen bir görüşme dili seç.')
    return model
