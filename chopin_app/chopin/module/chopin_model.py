from . import notes_function
from music21 import *
import numpy as np
from tensorflow.python.keras.models import load_model
from keras.utils import np_utils
import pickle
import os

relative_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data

def Chopin_NeuralNetwork(file):
    treble_data = []
    bass_data = []

    notes_dict1 = pickle_load(str(relative_path) + '/media/dicts/TrebleDict.pickle')
    notes_dict2 = pickle_load(str(relative_path) + '/media/dicts/BassDict.pickle')

    try:
        chopin = converter.parse(file)
        Treble, Bass = notes_function.Ts_load(chopin)
        Treble = notes_function.tone_load(Treble)
        Bass = notes_function.tone_load(Bass)
        treble_data.extend(notes_function.make_input_data(Treble))
        bass_data.extend(notes_function.make_input_data(Bass))
    except:
        return None

    try:

        Treble_input , max_length1= notes_function.trans_data(treble_data, notes_dict1)
        Bass_input , max_length2= notes_function.trans_data(bass_data, notes_dict2)

        Treble_input = np.array(Treble_input)
        Bass_input = np.array(Bass_input)

        Treble_input = Treble_input / max_length1
        Bass_input = Bass_input / max_length2

        Treble_model = load_model(str(relative_path) + '/media/chopin_model/ChopinMazurekTrebleModel.h5')
        Bass_model = load_model(str(relative_path) + '/media/chopin_model/ChopinMazurekBassModel.h5')
        Treble_model.load_weights(str(relative_path) + "/media/chopin_model/ChopinMazurekTrebleWeigths.h5")
        Bass_model.load_weights(str(relative_path) + "/media/chopin_model/ChopinMazurekBassWeigths.h5")

        treble = Treble_model.predict(Treble_input)
        bass = Bass_model.predict(Bass_input)

        treble_part = notes_function.new_chopin(treble, notes_dict1)
        bass_part = notes_function.new_chopin(bass, notes_dict2)

        score = stream.Score()
        score.append(treble_part)
        score.append(bass_part)

        return score

    except:
        return None

