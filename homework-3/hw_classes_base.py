import math

# Обучающие сообщения
TRAIN_CORPUS = [
    "Марс сигнал сигнал",
    "Марс пыль",
    "Марс сигнал антенна",
]

# Сообщения для проверки
CHECK_CORPUS = [
    "СИГНАЛ шум сигнал",
    "антенна пыль",
    "марс марс марс",
    "комета", "",
]


class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        self.vocabulary = {}
        self.lowercase = lowercase
        self.ngram_size = ngram_size

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, value):
        self._vocabulary = dict(value)

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}

    def add_word(self, word):
        if word not in self.vocabulary:
            self.vocabulary[word] = len(self.vocabulary)
        return self.vocabulary[word]

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()
        n = self.ngram_size
        return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]

    def fit(self, corpus):
        tokens = []
        for text in corpus:
            tokens += self.tokenize(text)
        if not tokens:
            raise ValueError("В корпусе нет токенов")
        self.vocabulary = {}
        for token in tokens:
            self.add_word(token)
        return self

    def transform(self, corpus):
        if not self.vocabulary:
            raise RuntimeError("Векторизатор не обучен")
        matrix = []
        for text in corpus:
            row = [0] * len(self.vocabulary)
            for token in self.tokenize(text):
                if token in self.vocabulary:
                    row[self.vocabulary[token]] += 1
            matrix.append(row)
        return matrix

    def get_feature_names(self):
        return sorted(self.vocabulary, key=self.vocabulary.get)

    def fit_transform(self, corpus):
        return self.fit(corpus).transform(corpus)

    def to_dict(self):
        return {
            "lowercase": self.lowercase,
            "ngram_size": self.ngram_size,
            "vocabulary": dict(self.vocabulary),
        }

    @classmethod
    def from_dict(cls, state):
        vectorizer = cls(state["lowercase"], state["ngram_size"])
        vectorizer.vocabulary = state["vocabulary"]
        return vectorizer


class BinaryVectorizer(CountVectorizer):
    def transform(self, corpus):
        matrix = super().transform(corpus)
        return [[min(x, 1) for x in row] for row in matrix]


class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase=True, ngram_size=1, use_idf=True):
        super().__init__(lowercase, ngram_size)
        self.use_idf = use_idf
        self._idf = []

    @classmethod
    def from_config(cls, config):
        return cls(
            lowercase=config.get("lowercase", True),
            use_idf=config.get("use_idf", True),
        )

    @property
    def idf(self):
        return list(self._idf)

    def fit(self, corpus):
        super().fit(corpus)
        self._idf = []
        if self.use_idf:
            texts = [self.tokenize(text) for text in corpus]
            for word in self.get_feature_names():
                df = len([words for words in texts if word in words])
                self._idf.append(math.log((len(corpus) + 1) / (df + 1)) + 1)
        return self

    def transform(self, corpus):
        matrix = []
        for row in super().transform(corpus):
            total = sum(row) or 1
            tf = [x / total for x in row]
            if self.use_idf:
                tf = [x * w for x, w in zip(tf, self._idf)]
            matrix.append(tf)
        return matrix


class KeywordExtractor:
    def __init__(self, vectorizer, top_n=3):
        self.vectorizer = vectorizer
        self.top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("top_n должен быть целым числом больше 0")
        self._top_n = value

    def fit(self, corpus):
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus):
        names = self.vectorizer.get_feature_names()
        result = []
        for row in self.vectorizer.transform(corpus):
            pairs = [(w, x) for w, x in zip(names, row) if x > 0]
            pairs.sort(key=lambda p: (-p[1], p[0]))
            result.append(pairs[:self.top_n])
        return result


def demo():
    print("1. Веса TF-IDF")
    tfidf = TfidfVectorizer.from_config({})
    train_matrix = tfidf.fit_transform(TRAIN_CORPUS)
    print("Слова:", tfidf.get_feature_names())
    print("IDF:", tfidf.idf)
    print("Матрица TRAIN_CORPUS:", train_matrix)
    print("Матрица CHECK_CORPUS:", tfidf.transform(CHECK_CORPUS))
    idf = tfidf.idf
    idf.clear()
    print("IDF после очистки списка:", tfidf.idf)
    print("Вывод: редкие слова получают больший вес,"
          " очистка полученного idf не меняет сохраненные веса")

    print("\n2. Настройки и новый fit()")
    tf = TfidfVectorizer.from_config({"lowercase": False, "use_idf": False})
    texts = ["Марс марс", "МАРС сигнал"]
    tf.fit(texts)
    print("Слова:", tf.get_feature_names())
    print("IDF:", tf.idf)
    print("TF:", tf.transform(texts))
    tfidf.fit(["Венера облака"])
    print("Слова:", tfidf.get_feature_names())
    print("IDF:", tfidf.idf)
    print("Матрица:", tfidf.transform(["Марс Венера облака"]))
    print("Вывод: без lowercase Марс, марс и МАРС - разные слова,"
          " без use_idf idf пустой")
    print("Новый fit() заменил словарь и idf, поэтому Марс не учитывается")

    print("\n3. Ключевые слова")
    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(TRAIN_CORPUS)
    print("top_n = 2:", extractor.extract(CHECK_CORPUS))
    extractor.top_n = 1
    print("top_n = 1:", extractor.extract(CHECK_CORPUS))
    try:
        extractor.top_n = 0
    except ValueError as e:
        print("top_n = 0:", e)
    print("Вывод: слова с нулевым весом пропускаются, при равных весах -"
          " по алфавиту, для пустого и неизвестного текста []")


if __name__ == "__main__":
    demo()
