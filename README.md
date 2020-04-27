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
1. Parts of Speech (POS) Tagging
    - tag each word with: N(oun), V(erb), Adj, Adv ...
2. Shallow Parsing or Chunking
    - breaking structure of a sentence down into  its smallest
    constituents (tokens such as words) and group them together
    into its higher-level phrases.
    - NP(Noun Phrase), VP, ADJP, ADVP, PP(Prepositional Phrase)
3. Constituency Parsing
    - Parse a sentence into multiple "constituents" or "structure"
    - S -> VP NP = Structure is a Verb Phrase followed by a Noun Phrase
    - similar to the shallow parsing, but *deeper*!
        - lookup example tree output to see difference
4. Dependency Parsing
    - analyze & infer *both structure and semantic dependencies* and
    relationships between tokens in a sentence. 
5. Named Entity Recognition
    - Classify words into named entities, such as PEOPLE, PLACES,
    ORGANIZATIONS, PRODUCTS, DATE, ...
    - find more: https://spacy.io/api/annotation#named-entities
6. Emotion and Sentiment Analysis




ref: https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72

## Supervised vs. Unsupervised learning:
1. Supervised learning *trains* the known model using training data.
    - we can validate the accuracy of the trained model using validation data.