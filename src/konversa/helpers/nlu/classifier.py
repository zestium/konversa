# Taken and modified from:
# https://gist.githubusercontent.com/sjljrvis/0aa964f44fa81b2790b0887e21ae29aa/raw/033efe1936b975931ce7b8e815234378fb50bed3/classifier.py

import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize,pos_tag
import os
import json
import datetime
import csv
import numpy as np
import time

class ClassifyIntent:

    stemmer = LancasterStemmer()

    # 3 classes of training data
    training_data = []

    words=[]
    classes=[]
    documents=[]

    ERROR_THRESHOLD = 0.2

    def __init__(self, dataset_file):
        with open(dataset_file, newline='') as f:
            r = csv.reader(f)
            for a in r:
                the_set = ()
                the_set = {"class": a[0], "sentence": a[1]}
                self.training_data.append(the_set)

    #compute sigmoid nonlinearity
    def __sigmoid(self, x):
        output=1/(1+np.exp(-x))
        return output

    #convert output of sigmoid function to its derivative
    def __sigmoid_output_to_derivative(self, output):
        return output*(1-output)

    def __clean_up_sentence(self, sentence):

        #tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        #stem each word
        sentence_words=[self.stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    #return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def __bow(self, sentence, the_words, show_details=False):
        #tokenize the pattern
        sentence_words = self.__clean_up_sentence(sentence)
        #bag of words
        bag=[0]*len(the_words)
        for s in sentence_words:
            for i,w in enumerate(the_words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))


    def get_training_data(self):

        return self.training_data

    def preprocess_training_data(self):

        #organizing our data structures for documents , classes, words

        ignore_words=['?']

        #loop through each sentence in our training data
        for pattern in self.training_data:
            #tokenize in each word in the sentence
            w=nltk.word_tokenize(pattern['sentence'])
            #add to our words list
            self.words.extend(w)
            #add to documents in our corpus
            self.documents.append((w,pattern['class']))
            #add to our classes list
            if pattern['class'] not in self.classes:
                self.classes.append(pattern['class'])

        #stem and lower each word and remove duplicate
        self.words=[self.stemmer.stem(w.lower()) for w in self.words if w not in ignore_words]
        self.words=list(set(self.words))

        #remove duplicates
        classes=list(set(self.classes))

        print(len(self.documents)," documents")
        print(len(self.classes), " classes", self.classes)
        print(len(self.words)," unique stemmed words", self.words)

        #create our training data
        training=[]
        output=[]
        #create an empty array for our output
        output_empty=[0]*len(self.classes)

        #training set, bag of words for each sentence
        for doc in self.documents:
            #initialize our bag of words
            bag=[]
            #list of tokenized words for the pattern
            pattern_words=doc[0]
            #stem each word
            pattern_words=[self.stemmer.stem(word.lower()) for word in pattern_words]
            #create our bag of words array
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)
            training.append(bag)
            #output is a 0 for each tag and 1 for current tag
            output_row=list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            output.append(output_row)

        X_rop = np.array(training)  # rop: result of preprocess
        y_rop = np.array(output)

        return X_rop, y_rop

    def train(self, X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

        """
        synapse_file = 'intent_class.json'

        if os.path.exists(synapse_file):
            # load our calculated synapse values
            print("training results exist, no need to train anymore")
            with open(synapse_file) as data_file:
                synapse = json.load(data_file)
                synapse_0 = np.asarray(synapse['synapse0'])
                synapse_1 = np.asarray(synapse['synapse1'])
                return synapse_0, synapse_1
        """

        print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
        print ("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X),len(X[0]),1, len(self.classes)) )
        np.random.seed(1)

        last_mean_error = 1
        # randomly initialize our weights with mean 0
        synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
        synapse_1 = 2*np.random.random((hidden_neurons, len(self.classes))) - 1

        prev_synapse_0_weight_update = np.zeros_like(synapse_0)
        prev_synapse_1_weight_update = np.zeros_like(synapse_1)

        synapse_0_direction_count = np.zeros_like(synapse_0)
        synapse_1_direction_count = np.zeros_like(synapse_1)

        for j in iter(range(epochs+1)):

            # Feed forward through layers 0, 1, and 2
            layer_0 = X
            layer_1 = self.__sigmoid(np.dot(layer_0, synapse_0))

            if(dropout):
                layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

            layer_2 = self.__sigmoid(np.dot(layer_1, synapse_1))

            # how much did we miss the target value?
            layer_2_error = y - layer_2

            if (j% 10000) == 0 and j > 5000:
                # if this 10k iteration's error is greater than the last iteration, break out
                if np.mean(np.abs(layer_2_error)) < last_mean_error:
                    print ("delta after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error))) )
                    last_mean_error = np.mean(np.abs(layer_2_error))
                else:
                    print ("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error )
                    break

            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            layer_2_delta = layer_2_error * self.__sigmoid_output_to_derivative(layer_2)

            # how much did each l1 value contribute to the l2 error (according to the weights)?
            layer_1_error = layer_2_delta.dot(synapse_1.T)

            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            layer_1_delta = layer_1_error * self.__sigmoid_output_to_derivative(layer_1)

            synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
            synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))

            if(j > 0):
                synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
                synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))

            synapse_1 += alpha * synapse_1_weight_update
            synapse_0 += alpha * synapse_0_weight_update

            prev_synapse_0_weight_update = synapse_0_weight_update
            prev_synapse_1_weight_update = synapse_1_weight_update
        """
        now = datetime.datetime.now()

        # persist synapses
        synapse =   {   'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
                        'datetime': now.strftime("%Y-%m-%d %H:%M"),
                        'words': self.words,
                        'classes': self.classes
                    }

        with open(synapse_file, 'w') as outfile:
            json.dump(synapse, outfile, indent=4, sort_keys=True)
        print ("saved synapses to:", synapse_file)
        """
        return synapse_0, synapse_1

    def classify(self, sentence, syn_0, syn_1, show_details=False):

        x = self.__bow(sentence.lower(), self.words, show_details)
        if show_details:
            print("sentence:", sentence, "\n bow:", x)
        #input layer is our bag of words
        l0=x
        # matrix multiplication of input and hidden layer
        l1 = self.__sigmoid(np.dot(l0, syn_0))
        # output layer
        l2 = self.__sigmoid(np.dot(l1, syn_1))

        results = l2
        results = [[i,r] for i,r in enumerate(results) if r > self.ERROR_THRESHOLD ]
        results.sort(key=lambda x: x[1], reverse=True)
        return_results =[[self.classes[r[0]],r[1]] for r in results]
        #print ("%s \n classification: %s" % (sentence, return_results))

        # example of return_results:
        # [['greetings', 0.9971946847650717]]
        return return_results
