import argparse
import locale
import logging
from Accorder_guitare import *
from aiy.board import Board
from aiy.cloudspeech import CloudSpeechClient


def get_hints(language_code): #Enregistre des propositions de commande
    if language_code.startswith('fr_'):
        return ('Accorde ma guitare',
                'A plus')
    return None

def locale_language(): #Initialisation de la langue
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Accordeur de guitare')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initialisation de la langue %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            if hints:
                logging.info('Dis quelque chose, ex. %s.' % ', '.join(hints))
            else:
                logging.info('Dis quelque chose pelo.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('Répète stp')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()

            if 'Accorde ma guitare' is in text :
                print("ok")'''accord_de_la_guitare()'''
            elif 'A plus' is in text:
                break


if __name__ == '__main__':
    main()
