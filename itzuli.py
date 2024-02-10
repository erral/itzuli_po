# -*- coding: utf-8 -*-
import argparse
import enum

import polib
import requests
import tqdm


def translate_text_itzuli_eus(text: str) -> str:
    """itzuli.eus webgunea erabiliz testu bat ingelesetik euskarara itzuli"""
    payload = {
        "mkey": "8d9016025eb0a44215c7f69c2e10861d",
        "model": "generic_en2eu",
        "text": text,
    }
    headers = {
        "Accept": "application/json",
        "Origin": "https://www.euskadi.eus",
    }
    response = requests.post(
        "https://api.euskadi.eus/itzuli/en2eu/translate",
        json=payload,
        headers=headers,
        timeout=5
    )

    result = response.json()
    if result.get("success", None):
        return result.get("message", "")

    return ""


def translate_text_elia_eus(text: str) -> str:
    """elia.eus webgunea erabiliz testu bat ingelesetik euskarara itzuli"""
    session = requests.Session()
    data = session.get("https://elia.eus", timeout=5)
    payload = {
        "source_language": "en",
        "input_text": text,
        "translation_engine": "1",
        "target_language": "eu",
        "csrfmiddlewaretoken": data.cookies.get("csrftoken"),
    }
    session.headers.update(
        {
            "Referer": "https://elia.eus/itzultzailea",
            "Origin": "https://elia.eus",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }
    )
    session.cookies.update({"cookies_accepted": "0"})
    response = session.post(
        "https://elia.eus/ajax/translate_string",
        data=payload,
    )

    if response.ok:
        result = response.json()
        return result.get("plain_translated_text", "")

    return ""


def translate_text_batua_eus(text:str) -> str:
    """batua.eus webgunea erabiliz testu bat ingelesetik euskarara itzuli"""
    payload = {
        "mkey": "b0d06b50ee07c14",
        "model": "generic_en2eu",
        "text": text,
    }
    headers = {
        "Accept": "application/json",
        "Origin": "https://batua.eus",
    }
    response = requests.post(
        "https://backend.batua.eus/en2eu/translate",
        json=payload,
        headers=headers,
        timeout=5
    )

    result = response.json()
    if result.get("success", None):
        return result.get("message", "")

    return ""


class Translator(enum.Enum):
    """ Itzultzaile posibleak gordetzeko Enum objektua"""
    elia = 'elia'
    itzuli = 'itzuli'
    batua = 'batua'

    def __str__(self):
        return self.value


ALL_TRANSLATION_FUNCTIONS = {
    Translator.batua: {
        "name": "batua.eus",
        "action": translate_text_batua_eus,
    },
    Translator.elia: {
        "name": "elia.eus",
        "action": translate_text_elia_eus,
    },
    Translator.itzuli:{
        "name": "itzuli.eus",
        "action": translate_text_itzuli_eus,
    },
}


def main(filepath:str, translator: Translator) -> None:
    """ Open the PO file and get all msgids in order to translate them
    """
    pofile = polib.pofile(filepath)

    translation_function = ALL_TRANSLATION_FUNCTIONS.get(translator)

    new_contents = []
    name = translation_function.get('name')
    translate = translation_function.get("action")

    print(f'Erabiltzen ari garen itzultzailea: {name}')

    print(f'Itzuli beharreko elementu kopurua: {len(pofile)}')

    for entry in tqdm.tqdm(pofile):
        try:
            translation = translate(entry.msgid)
            new_contents.append([entry.msgid, translation, entry.occurrences])
        except Exception as e:
            print('Huts egin du mezua itzultzean')

    translated_pofile = polib.POFile()
    translated_pofile.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2007-10-18 14:00+0100',
        'PO-Revision-Date': '2007-10-18 14:00+0100',
        'Last-Translator': name,
        'Language-Team': 'Euskara <eu@li.org>',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }
    print('Fitxategia sortzen')
    for msgid, msgstr, ocurrences in new_contents:
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
            ocurrences=ocurrences
        )
        translated_pofile.append(entry)
    translated_pofile.save(f'{name}.po')
    print('Eginda!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Itzuli PO',
        description="PO fitxategia euskarazko itzultzaile "
                    "automatikoak erabiliz euskarara itzultzeko tresna"
    )
    parser.add_argument('fitxategia', help='Itzuli beharreko po fitxategia')
    parser.add_argument(
        'itzultzailea',
        help='Aukeratu zein itzultzaile erabili',
        type=Translator,
        choices=(Translator.batua, Translator.elia, Translator.itzuli)
    )
    args = parser.parse_args()

    main(args.fitxategia, args.itzultzailea)
