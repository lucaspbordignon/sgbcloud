def sgb_most_common_words(corpus, add_stop_words = [], tema='' , palestrante='', arquivo='Most_Common_Words.csv'):
    """
        Função que recebe um texto, recebe identificadores (tema, palestrante...) e
        exporta um csv com contagem das palavras para o tema/palestrante.

        Parâmetros:

            str     corpus:         Texto a ter as palavras contadas
            list    add_stop_words: (opcional) Lista dedicada a palavras que a biblioteca nltk não remove sozinha.
            str     tema:           (opcional) Tema do texto
            str     palestrante:    (opcional) Palestrante
            str     arquivo:        (padrão: 'Most_Common_Words.csv') Nome do Arquivo a ser lido/salvo. 

    """
    
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter
    import csv
    import os.path

    tokens = [w for w in word_tokenize(corpus.lower()) if w.isalpha()]

    stopWords_nltk = set(stopwords.words('portuguese'))

    stopWords = stopWords_nltk.union(set(add_stop_words))

    no_stops = [w for w in tokens if w not in stopWords]

    bag_of_words = Counter(no_stops)

    Most_Common_Words = bag_of_words.most_common()

    if not os.path.isfile(arquivo):
        with open(arquivo, 'w') as csvfile:
            Writer = csv.writer(csvfile)
            Writer.writerow(['palavra','contagem','tema','palestrante'])
            
    for word_count in Most_Common_Words:
        with open(arquivo,'a') as csvfile:
            Writer = csv.writer(csvfile)
            Writer.writerow([word_count[0],word_count[1],tema,palestrante])

    return Most_Common_Words









