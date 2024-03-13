import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Embedding, Layer
from tensorflow.keras.models import Model
from tensorflow.keras.constraints import Constraint
from tensorflow.keras.initializers import Constant


class EmbeddingConstraint(Constraint):
    """
    NonNeg + norm constraint
    """
    def __init__(self, n):
        self.n = n

    def __call__(self, w):
        w = w / (
            tf.keras.backend.epsilon()
            + tf.keras.backend.sqrt(
                tf.reduce_sum(tf.square(w), axis=0, keepdims=True)
            )
        )
        w = w * tf.cast(tf.greater_equal(w, 0.0), tf.keras.backend.floatx())
        return np.sqrt(self.n) * w


class FractionLayer(Layer):
    def __init__(self, mat):
        super().__init__()
        self.mat = tf.constant(mat, dtype=tf.float32)

    def call(self, inputs):
        pattern = inputs[0]
        pref = inputs[1]
        pref_all = inputs[2]
        denominator = tf.matmul(self.mat, pref_all)
        denominator = tf.gather(denominator, tf.cast(pattern, tf.int32))
        return tf.reshape(pref / denominator, (-1, 1))


class PreferenceModel(Model):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.set_index()
        self.n_songs = len(self.title_map)
        self.preference_layer = Embedding(self.n_songs, 1, embeddings_initializer=Constant(1.),
                                     embeddings_constraint=EmbeddingConstraint(self.n_songs))
        self.fraction_layer = FractionLayer(mat = self.make_matrix())

    def set_index(self):
        def make_idx(series):
            cat = series.astype("category")
            idx_map = pd.Series(cat.cat.categories)
            return cat.cat.codes, idx_map
        self.pattern_id, self.pattern_map = make_idx(self.df["pattern"])
        self.title_id, self.title_map = make_idx(self.df["title"])

    def make_matrix(self):
        count_pattern = self.df.groupby("pattern")["count"].transform(sum)
        pick_ratio = self.df["count"] / count_pattern
        mat = np.zeros(shape=(len(self.pattern_map), len(self.title_map)), dtype=int)
        mat[self.pattern_id, self.title_id] = 1
        return mat

    def fit(self, **kwargs):
        df = self.df
        count_pattern = df.groupby("pattern")["count"].transform(sum)
        pick_ratio = df["count"] / count_pattern
        super().fit([self.title_id, self.pattern_id], pick_ratio, **kwargs)

    def call(self, inputs):
        title, pattern = inputs
        preference = self.preference_layer(title)
        preference_all = self.preference_layer(np.arange(self.n_songs))
        result = self.fraction_layer([pattern, preference, preference_all])
        return result

    def get_preference(self):
        preference = pd.Series(
            self.get_weights()[0].flatten(),
            index=self.title_map.values,
            name="Preference"
        )
        preference.index.name="Title"
        return preference.sort_values(ascending=False)

    def run(self):
        self.compile(optimizer="adam", loss="binary_crossentropy")
        self.fit(epochs=100)
        return self.get_preference()
