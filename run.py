from src.recognizer import Recognizer
from src.nlp import NaturalLanguageProcessor


def menu():
    answers = {
        'language': '',
        'speaker': '',
        'block': ''
    }

    print('Bem-vindo ao SGBCloud!')
    print('Para sair, diga "batman".\n')

    while True:
        print('Selecione a linguagem a ser utilizada:')
        print('[0] Português (pt-BR)')
        print('[1] Inglês (en-US)')
        selected = input()
        if selected == '0':
            answers['language'] = 'pt-BR'
            break
        elif selected == '1':
            answers['language'] = 'en-US'
            break

    print('##################################################')
    print('Digite o nome do palestrante:')
    answers['speaker'] = input()

    print('##################################################')
    print('Digite o nome do bloco:')
    answers['block'] = input()

    return answers


if __name__ == '__main__':
    settings = menu()

    # Starts the recognizer synchronously
    recognizer = Recognizer(language_code=settings['language'])
    recognizer.recognize()

    # Starts the processor
    processor = NaturalLanguageProcessor()
    with open('speech.txt', 'r') as file:
        processor.generate_and_upload_words(file.read(),
                                            settings['speaker'],
                                            settings['block'])
