def sgb_most_common_words(corpus,
                          add_stop_words=[""],
                          bloco='' ,
                          palestrante='',
                          arquivo='Most_Common_Words.csv',
                          save_csv=False
                          ):

    """
        Função que recebe um texto, recebe identificadores (bloco, palestrante...) e
        exporta um csv com contagem das palavras para o bloco/palestrante.

        Parâmetros:

            str     corpus:         Texto a ter as palavras contadas
            list    add_stop_words: (opcional) Lista dedicada a palavras que a biblioteca nltk não remove sozinha.
            str     bloco:           (opcional) bloco do festival
            str     palestrante:    (opcional) Palestrante
            bool    save_csv:       (opcional) 
            str     arquivo:        (padrão: 'Most_Common_Words.csv') Nome do Arquivo a ser lido/salvo.

    """

    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter
    import csv
    import os.path

    tokens = [w for w in word_tokenize(corpus.lower()) if w.isalpha()]

    stopWords_nltk = set(stopwords.words('portuguese'))

    chumbadas = set(["apenas","outro","pode","trás","lado","frente"])

    stopWords = stopWords_nltk.union(set(add_stop_words)).union(chumbadas)

    no_stops = [w for w in tokens if w not in stopWords and len(w) > 2]

    if save_csv:    
        if not os.path.isfile(arquivo):
            with open(arquivo, 'w') as csvfile:
                Writer = csv.writer(csvfile)
                Writer.writerow(['palavra','bloco','palestrante'])
        for word in no_stops:
            with open(arquivo,'a') as csvfile:
                Writer = csv.writer(csvfile)
                Writer.writerow([word,bloco,palestrante])

    rows = [[w,bloco,palestrante] for w in no_stops]
    return rows


if __name__ == '__main__':

    teste = """ Teste: 3 pratos de trigo para 3 tristes tigres."""

    from sgb_sheets_api import update_spreadsheet

    rows = sgb_most_common_words(teste, palestrante="Ditado Popular", bloco="Trava línguas")

    update_spreadsheet( rows,
                        headers = [['palavra','bloco','palestrante']],
                        spreadsheetId='12nX-xkjk5YiZvNhf0SXHDusefO942CRpxlgkDJeD5qg',
                        sheet='Tabela1'
                    )


