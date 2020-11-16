#!/usr/bin/env python
# coding: utf-8

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn.functional as F
import torch.distributions
import torch.optim as optim
from torch import nn 
from torch.autograd import Variable

import torchtext
from torchtext import data
from torchtext import datasets
from torchtext.vocab import Vectors, GloVe



class Model(torch.nn.Module):
    def __init__(self, batch_size, num_classes, mlp_out_size, vocab_size, embedding_length, weights, num_layers, hidden_size = 100, biDirectional = False):
        super(Model, self).__init__() 
        """
        Arguments
        ---------
        batch_size : Size of the batch which is same as the batch_size of the data returned by the TorchText BucketIterator
        num_classes : 28 = (For full classification)
        hidden_sie : Size of the hidden_state of the LSTM  
        vocab_size : Size of the vocabulary containing unique words
        embedding_length : Embeddding dimension of GloVe word embeddings
        weights : Pre-trained GloVe word_embeddings which we will use to create our word_embedding look-up table 
        --------

        """

        self.batch_size = batch_size
        self.num_classes = num_classes
        self.vocab_size = vocab_size
        self.embedding_length = embedding_length
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.mlp_out_size = mlp_out_size
        self.biDirectional = biDirectional

        self.word_embeddings = nn.Embedding(vocab_size, embedding_length)
        self.word_embeddings.weights = nn.Parameter(weights, requires_grad=False)
        
        self.lstm_layer = LSTM(self.batch_size, self.hidden_size, self.embedding_length, self.biDirectional, self.num_layers)

        if(self.biDirectional):
            self.mlp = MLP(self.hidden_size*2, self.mlp_out_size, self.num_classes)
        else:
            self.mlp = MLP(self.hidden_size, self.mlp_out_size, self.num_classes)

    def forward(self, input_sequence):
        input_ = self.word_embeddings(input_sequence)
        out_lstm, final_hidden_state = self.lstm_layer(input_)
        if self.biDirectional:
            final_hidden_state = final_hidden_state.view(self.num_layers, 2, input_.shape[0], self.hidden_size) # num_layer x num_dir x batch x hidden
            final_hidden_state = final_hidden_state[-1]
            final_hidden_state = final_hidden_state.transpose(0,1).reshape(input_.shape[0], self.hidden_size*2)
        else:
            final_hidden_state = final_hidden_state[-1]
        
        mlp_output = self.mlp(final_hidden_state)
        predictions = torch.softmax(mlp_output, dim = -1)
        return predictions


class LSTM(torch.nn.Module):
    """
        Arguments
        ---------
        batch_size : Size of the batch which is same as the batch_size of the data returned by the TorchText BucketIterator
        hidden_size : Size of the hidden_state of the LSTM  
        embedding_length : Embeddding dimension of GloVe word embeddings
        --------
    """
    def __init__(self, batch_size, hidden_size, embedding_length, biDirectional = False, num_layers = 2):

        super(LSTM, self).__init__()
        self.batch_size = batch_size
        self.hidden_size = hidden_size
        self.embedding_length = embedding_length
        self.biDirectional= biDirectional
        self.num_layers = num_layers

        self.lstm = nn.LSTM(self.embedding_length, self.hidden_size, bidirectional = self.biDirectional, batch_first = True, num_layers = self.num_layers)   # Dropout  

    def forward(self, input_sequence, batch_size=None):
        out_lstm, (final_hidden_state, final_cell_state) = self.lstm(input_sequence)   # ouput dim: ( batch_size x seq_len x hidden_size )
        return out_lstm, final_hidden_state


class MLP(torch.nn.Module):
    def __init__(self, input_dim, output_dim, num_classes):
        super(MLP, self).__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_classes = num_classes

        self.ff_1 = nn.Linear(self.input_dim, self.output_dim)
        self.relu = nn.ReLU()
        self.ff_2 = nn.Linear(self.output_dim, self.num_classes)

    def forward(self,x):
        out_1 = self.ff_1(x)
        out_relu = self.relu(out_1)
        out_2 = self.ff_2(out_relu)


        return out_2

def load_data(batch_size= 16, embedding_length = 100):
    tokenize = lambda x: x.split()
    TEXT = data.Field(sequential=True, tokenize=tokenize, lower=True, include_lengths=True, batch_first=True, fix_length=30)
    LABELS = data.LabelField(batch_first=True, dtype=torch.float)


    train, val, test = data.TabularDataset.splits(path=  'app/data/multi_class_15/', train='train.tsv',
      validation='dev.tsv', test='test.tsv', format='tsv',
      fields=[('text', TEXT), ('labels', LABELS)])
    
    # train_iter, val_iter, test_iter = data.BucketIterator.splits(
    #   (train, val, test), batch_sizes=(batch_size, batch_size, batch_size), sort_key=lambda x: len(x.text), device=0)

    # # build the vocabulary
    TEXT.build_vocab(train, vectors=GloVe(name='6B', dim=embedding_length))
    # LABELS.build_vocab(train)
    # print(LABELS.vocab.__dict__)

    # word_embeddings = TEXT.vocab.vectors
    # vocab_size = len(TEXT.vocab)

    return TEXT

def test_sentence(sentence, TEXT, loaded_model):
    test_sen_list = TEXT.preprocess(sentence)
    sentence = [[TEXT.vocab.stoi[x] for x in test_sen_list]]
    # print(test_sen)

    sentence = np.asarray(sentence)
    sentence = torch.LongTensor(sentence)
    test_tensor = Variable(sentence)

    loaded_model.eval()
    prediction = loaded_model(test_tensor)

    out_class = torch.argmax(prediction)
    
    # Can hardcode class label text instead of index
    return out_class

def prediction(sentence):
    vocab_size = torch.load('app/models/class_15/BiLSTM_vocab')
    word_embeddings = torch.load('app/models/class_15/BiLSTM_word_embeddings')

    batch_size = 32
    num_classes = 15
    embedding_length = 100
    mlp_out_size = 64
    weights = word_embeddings
    hidden_size = 100
    num_layers = 3


# learning_rate = 2e-4
# embedding_length = 100
# num_classes = 15
# mlp_out_size = 64
# weights = word_embeddings
# hidden_size = 100
# num_layers = 4

    TEXT = load_data(batch_size, embedding_length)

    loaded_model = Model(batch_size, num_classes, mlp_out_size, vocab_size, embedding_length, weights, num_layers, hidden_size, biDirectional=True)
    loaded_model.load_state_dict(torch.load('app/models/class_15/BiLSTM_BS_32'))
    loaded_model.eval()

    label = test_sentence(sentence, TEXT, loaded_model).item()

    d = {0 : "admiration, desire", 1 : "disapproval, disgust, disappointment, embarrasement", 2 : "anger, annoyance", 
        3: "excitement, amusement", 4 : "love, caring", 5 : "approval", 6 : "gratitude", 7 : "curiosity", 
        8 : "sadness , grief, remorse", 9 : "joy , pride, relief", 10 : "optimism", 11 : "confusion", 12 : "realization", 
        13 : "surprise", 14 : "fear, nervousness"}

    return label













