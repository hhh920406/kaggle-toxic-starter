from sklearn.externals import joblib
from keras.preprocessing import text, sequence

from steps.base import BaseTransformer


class Tokenizer(BaseTransformer):
    def __init__(self, char_level, maxlen):
        self.char_level = char_level
        self.maxlen = maxlen

        self.tokenizer = text.Tokenizer(char_level=self.char_level)

    def fit(self, X, X_valid=None, train_mode=True):
        self.tokenizer.fit_on_texts(X)
        return self

    def transform(self, X, X_valid=None, train_mode=True):
        X_tokenized = self._transform(X)

        if X_valid is not None:
            X_valid_tokenized = self._transform(X_valid)
        else:
            X_valid_tokenized = None
        return {'X': X_tokenized,
                'X_valid': X_valid_tokenized,
                'tokenizer': self.tokenizer}

    def _transform(self, X):
        list_tokenized = self.tokenizer.texts_to_sequences(list(X))
        X_tokenized = sequence.pad_sequences(list_tokenized, maxlen=self.maxlen)
        return X_tokenized

    def load(self, filepath):
        object_pickle = joblib.load(filepath)
        self.char_level = object_pickle['char_level']
        self.maxlen = object_pickle['maxlen']
        self.tokenizer = object_pickle['tokenizer']
        return self

    def save(self, filepath):
        object_pickle = {'char_level': self.char_level,
                         'maxlen': self.maxlen,
                         'tokenizer': self.tokenizer}
        joblib.dump(object_pickle, filepath)