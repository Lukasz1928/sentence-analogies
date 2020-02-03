from gensim.models import KeyedVectors


class WordVectorModel:

    def __init__(self):
        self.model = KeyedVectors.load_word2vec_format('resources/cc.en.300.vec', binary=False)

    def get_word_vector(self, word):
        return self.model[word]

    def get_sentence_vectors(self, sentence):
        return [self.get_word_vector(w) for w in sentence]

    def predict_word(self, s1, s2, s3):
        s1 = self.get_sentence_vectors(s1)
        s2 = self.get_sentence_vectors(s2)
        s3 = self.get_sentence_vectors(s3)
        s1_sum = sum(s1)
        s2_sum = sum(s2)
        s3_sum = sum(s3)
        predicted_word_vector = [s2_sum - s1_sum + s3_sum]
        ms = self.model.most_similar(predicted_word_vector, topn=1)
        return ms[0]
