# -*- coding: utf-8 -*-
"""Untitled20.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U3uLQgQ5cM3je0wudBzCAiJ4u8rEy0I_
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds

imd_sentences =[]
imd_labels=[]

"""Importer le dataset IMDB Dataset"""

train_data = tfds.as_numpy(tfds.load('imdb_reviews', split='train'))

train_data

for item in train_data:
  print(item)
  break

imdb_sentences =[]
imdb_labels=[]
for item in train_data:
  imdb_sentences.append(str(item['text']))
  imdb_labels.append(item['label'])

len(imdb_sentences)

training_sentences = imdb_sentences[:20000]
test_sentences = imdb_sentences[20000:]

training_labels = imdb_labels[:20000]
test_labels = imdb_labels[20000:]

len(test_labels)

"""#Tokenisation (Phrases --> Liste de mots)"""

phrase = "Je suis en train de travailler"

phrase.split(" ")

phrases = ["je suis en train de travailler sur tenserflow","j'ai beaucoup appris aujourd'hui"]

from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()

#on lui fait apprendre les differents
tokenizer.fit_on_texts(phrases)

#quels sont les mots que tu as appris
tokenizer.word_index

#on va passer à la numerisation du texte
tokenizer.texts_to_sequences(phrases)

test =["qui suis je moi ?"]

tokenizer.texts_to_sequences(test)

#on precise le nbre de mot qu'on veut dans le vocabulaire,on peut le reduire pour prendre les mots les plus pertinants
#oov: out of vocabulary(un token speciale qui n'est pas dans notre vocabilaire)
tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
tokenizer.fit_on_texts(test)

tokenizer.word_index

"""#Paddind et Truncating"""

#les phrases ont des tailles differentes
#generalemet tous les exemples ou models ont la maille taille
#pour y remedier on utilise le padding
phrases = ["Je suis au marché",
           "Je travaille au marché",
           "es-tu rentré du marché?",
           "Je nettoie le marché tous les jours avant de commencer à vendre le matin"]


tokenizer = Tokenizer(num_words = 100, oov_token="")
tokenizer.fit_on_texts(phrases)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(phrases)

sequences

#pour faire le padding
from tensorflow.keras.preprocessing.sequence import pad_sequences

#le pré padding , il met les 0 avant
pad_sequences(sequences)

#le pré padding , il met les 0 apres
pad_sequences(sequences, padding="post")

#faire du truncating (couper la phrase)
pad_sequences(sequences, padding="post",maxlen=7)

#faire du truncating (couper la phrase)
pad_sequences(sequences, padding="post",maxlen=7, truncating="post")

"""#Stop words
Le terme stop word ou mot vide désigne tous les mots n'ayant pas de réelle signification. On dit aussi qu'ils ne sont pas porteurs de sens. En effet, ils sont si courants et reviennent de façon tellement régulière qu’ils ne permettent pas de caractériser, au sens lexical, un texte par rapport à un autre texte
"""

phrase = "Je vais au marché le Jeudi"

stopwords = ['au', "le"]

#on fait une sorte de tokenisation
#
words = phrase.split(' ')
phrase_nettoyee = []

for word in words:
  if word not in stopwords:
    phrase_nettoyee.append(word)

phrase_nettoyee

" ".join(phrase_nettoyee)

"""#Embending
Avoir un vecteur qui represente un mot donnee. On aura un vecteur qui represente un mot donee
"""

training_labels[42]

tokenizer = Tokenizer(num_words=20000, oov_token="")
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, padding="post", maxlen=15, truncating="post")

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, padding="post", maxlen=15, truncating="post")

training_padded[11]

training_labels = np.array(training_labels)
test_labels = np.array(test_labels)

test_labels[2]

#dans la couche  embending, on a 20000 mots et chaque mot à 20nbre qu'ils caracterisent.
#Cette couche à des weight (ces 20000 * 20 sont des W qu'il faudra apprendre.)
#on va commencer par des W aleatoire, puis on fait la moyenne et on lui donne a une couche de reseau de neurone
#En s'entrainant, il va s'ameliorer
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Embedding(20000, 20),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]
)

#on a 40000 Par = 20000*20
#dense = 20*8 + 8(ce sont les biais) = 168

model.summary()

#classification binaire
#on compile le model
model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])

model_ckp = tf.keras.callbacks.ModelCheckpoint(filepath="best_model.h5",
                            monitor="val_accuracy",
                            mode="max",
                            save_best_only=True)
stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True)



h = model.fit(training_padded, training_labels, epochs=50,
              validation_data=(test_padded, test_labels),
              callbacks=[model_ckp])

def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_'+string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_'+string])
    plt.show()

plot_graphs(h, 'accuracy')
plot_graphs(h, "loss")

#vocab size
#seul le mot frequent est considerer comme
vocab_size = 1
vocab_size = 78371

wc = tokenizer.word_counts

wc = sorted(wc.items(), key=lambda t:t[1], reverse=True)

df = pd.DataFrame(wc, columns=['mots', "frequence"])

df[df['frequence'] > 10]

#verifions dans le test_set combien de mot sont dans le training_test
test_tok = Tokenizer()
test_tok.fit_on_texts(test_sentences)

test_tok.word_index

test_words = test_tok.word_index.keys()

test_words

train_words = df['mots'].tolist()

len(train_words), len(test_words)

inter = set(train_words).intersection(test_words)

len(inter)

vocab_size = 29000

tokenizer = Tokenizer(num_words=vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, padding="post", maxlen=15, truncating="post")

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, padding="post", maxlen=15, truncating="post")

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Embedding(vocab_size, 20),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]
)

model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])
model_ckp = tf.keras.callbacks.ModelCheckpoint(filepath="best_model.h5",
                            monitor="val_accuracy",
                            mode="max",
                            save_best_only=True)
stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True)
h = model.fit(training_padded, training_labels, epochs=50,
              validation_data=(test_padded, test_labels),
     callbacks=[model_ckp])

plot_graphs(h, 'accuracy')
plot_graphs(h, "loss")

"""Embending dim"""

np.power(vocab_size, 1/4)

vocab_size = 29000
embedding_dim=13

tokenizer = Tokenizer(num_words=vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, padding="post", maxlen=15, truncating="post")

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, padding="post", maxlen=15, truncating="post")

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Embedding(vocab_size, embedding_dim),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]
)

model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])
model_ckp = tf.keras.callbacks.ModelCheckpoint(filepath="best_model.h5",
                            monitor="val_accuracy",
                            mode="max",
                            save_best_only=True)
stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True)
h = model.fit(training_padded, training_labels, epochs=50,
              validation_data=(test_padded, test_labels),
              callbacks=[model_ckp])

plot_graphs(h, 'accuracy')
plot_graphs(h, "loss")

"""Architecture du model"""

vocab_size = 29000
embedding_dim=13

tokenizer = Tokenizer(num_words=vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, padding="post", maxlen=15, truncating="post")

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, padding="post", maxlen=15, truncating="post")

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Embedding(vocab_size, embedding_dim),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(5, activation='relu'),
        tf.keras.layers.Dense(3, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]
)

model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])
model_ckp = tf.keras.callbacks.ModelCheckpoint(filepath="best_model.h5",
                            monitor="val_accuracy",
                            mode="max",
                            save_best_only=True)
stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True)
h = model.fit(training_padded, training_labels, epochs=50,
              validation_data=(test_padded, test_labels),
              callbacks=[model_ckp])

plot_graphs(h, 'accuracy')
plot_graphs(h, "loss")

"""Max len + Dropout"""

tailles = []

for sent in training_sentences:
  tailles.append(len(sent.split(" ")))

np.array(tailles).min(), np.array(tailles).max(), np.array(tailles).mean()

np.median(tailles)

vocab_size = 29000
embedding_dim=13
maxlen = 100

tokenizer = Tokenizer(num_words=vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, padding="post", maxlen=maxlen, truncating="post")

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, padding="post", maxlen=maxlen, truncating="post")

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Embedding(vocab_size, embedding_dim),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(5, activation='relu'),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(3, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]
)

model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])
model_ckp = tf.keras.callbacks.ModelCheckpoint(filepath="best_model.h5",
                            monitor="val_accuracy",
                            mode="max",
                            save_best_only=True)
stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True)
h = model.fit(training_padded, training_labels, epochs=50,
              validation_data=(test_padded, test_labels),
              callbacks=[model_ckp])

plot_graphs(h, 'accuracy')
plot_graphs(h, "loss")

"""Transfert Learning"""

!pip install --upgrade tensorflow_hub

import tensorflow_hub as hub

embed = hub.load("https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1")
embeddings = embed(["cat is on the mat", "dog is in the fog"])

embeddings.shape

train_data, test_data = tfds.load(name="imdb_reviews", split=["train", "test"],
                                  batch_size=-1, as_supervised=True)

train_examples, train_labels = tfds.as_numpy(train_data)
test_examples, test_labels = tfds.as_numpy(test_data)

training_sentences = train_examples[:20000]
training_labels = train_labels[:20000]

test_sentences = train_examples[20000:]
test_labels = train_labels[20000:]

train_labels[20000:]

train_examples[0]

hub_layer = hub.KerasLayer("https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1", output_shape=[20],
                           input_shape=[], dtype=tf.string)

model = tf.keras.models.Sequential(
    [
        hub_layer,
        tf.keras.layers.Dense(5, activation='relu'),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(3, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ]
)

model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])
model_ckp = tf.keras.callbacks.ModelCheckpoint(filepath="best_model.h5",
                            monitor="val_accuracy",
                            mode="max",
                            save_best_only=True)
stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True)
h = model.fit(training_sentences, training_labels, epochs=50,
              validation_data=(test_sentences, test_labels),
              callbacks=[model_ckp])

plot_graphs(h, 'accuracy')
plot_graphs(h, "loss")