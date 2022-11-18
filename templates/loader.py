import json
from typing import Any

from core.settings import (
    TEMPLATE_FOLDER,
    LANG_CODES
)


class LangManager:
    lang_codes = LANG_CODES
    languages: dict = {}

    def __init__(self, version: str = 'default') -> None:
        for lang in self.lang_codes:
            self.languages = {lang: load_lang(lang, version)}

    async def load_phrase(
        self,
        phrase: str,
        lang_code: str = 'en',
        **format: Any
    ) -> str:
        if lang_code not in self.lang_codes:
            lang_code = 'en'
        phrases_cur_lang = self.languages.get(lang_code)
        get_phrase = phrases_cur_lang.get(phrase)

        if format != {}:
            return get_phrase.format(**format)
        return get_phrase


def load_lang(
    lang_code: str = 'en',
    version: str = 'default'
) -> dict[str]:
    current_file = f'{TEMPLATE_FOLDER}/languages/{lang_code}/{version}.json'

    f = open(current_file, encoding='utf8')
    data = json.load(f)
    f.close()

    return data.get('phrases')
