### Text Normalization
1. Remove accented characters
2. Expand contractions (ex. they're -> they are)
3. Remove special characters
4. Word stem & inflection:
    - inflection: jump --> jump*s*, jump*ed*, jump*ing*
    - stem: reverse of inflection
5. Lemmatization:
    - remove word affixes to get root *word*.
    root *word* is lexicographiocally correct word (=present in
    dictionary) whereas root *stem* may not be semantically correct.
6. Removing stopwords:
    - words that have little or no significance
    - ex) a, an, the, and


### Understanding Language Syntax and Structure
1. Parts of Speech (POS) Tagging:
    - tag each word with: N(oun), V(erb), Adj, Adv ...
2. Shallow Parsing or Chunking:
    - breaking structure of a sentence down into  its smallest
    constituents (tokens such as words) and group them together
    into its higher-level phrases.
    - NP(Noun Phrase), VP, ADJP, ADVP, PP(Prepositional Phrase)
3. Constituency Parsing
4. Dependency Parsing
