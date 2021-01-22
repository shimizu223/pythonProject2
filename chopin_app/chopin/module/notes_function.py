from music21 import *
import re
import numpy as np
from decimal import Decimal
import os

relative_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def Ts_load(file):
    Msure1 = []
    Msure2 = []

    for i in file:
            if str(i) == '<music21.stream.Part spine_1>' or str(i) == '<music21.stream.PartStaff P1-Staff1>':
                part = i
                for n in part:
                    if isinstance(n, stream.Measure) and n.quarterLength >= 3:
                        Msure1.append(n)
            if str(i) == '<music21.stream.Part spine_0>' or str(i) == '<music21.stream.PartStaff P1-Staff2>':
                part = i
                for n in part:
                    if isinstance(n, stream.Measure) and n.quarterLength >= 3:
                        Msure2.append(n)
    return Msure1, Msure2


def tone_load(Ts_notes):
    for cho in Ts_notes:

        flag = True

        for notes in cho:

            if isinstance(notes, stream.Voice):

                flag = False

                for no in notes:
                    if no.quarterLength % 0.25 != 0.0:

                        if no.quarterLength < 0.35:
                            no.quarterLength = 0.25

                        elif no.quarterLength < 0.65:
                            no.quarterLength = 0.25

                        elif no.quarterLength < 1.0:
                            no.quarterLength = 0.75

                sumn = Decimal(0)
                max_note = 0
                min_note = 0
                for i in notes:
                    sumn += Decimal(str(i.quarterLength))
                while sumn != 3.0:
                    maxn = 0
                    minn = 100
                    if sumn > 3:
                        for i in range(len(notes)):
                            if isinstance(notes[i], note.Note) or isinstance(notes[i], chord.Chord) or isinstance(
                                    notes[i], note.Rest):
                                if notes[i].quarterLength > maxn:
                                    maxn = notes[i].quarterLength
                                    max_note = i
                        notes[max_note].quarterLength = notes[max_note].quarterLength - 0.25
                    elif sumn < 3:
                        for i in range(len(notes)):
                            if isinstance(notes[i], note.Note) or isinstance(notes[i], chord.Chord) or isinstance(
                                    notes[i], note.Rest):
                                if notes[i].quarterLength < 1.0 and notes[i].quarterLength < minn:
                                    minn = notes[i].quarterLength
                                    min_note = i
                        notes[min_note].quarterLength = notes[min_note].quarterLength + 0.25
                    sumn = Decimal(0)
                    for i in notes:
                        sumn += Decimal(str(i.quarterLength))

            if isinstance(notes, note.Note) or isinstance(notes, chord.Chord) or isinstance(notes, note.Rest):
                if notes.quarterLength % 0.25 != 0.0:

                    if notes.quarterLength < 0.35:
                        notes.quarterLength = 0.25

                    elif notes.quarterLength < 0.65:
                        notes.quarterLength = 0.5

                    elif notes.quarterLength < 1.0:
                        notes.quarterLength = 0.75

        if flag:
            max_note = 0
            min_note = 0
            sumn = Decimal(0)
            for i in cho:
                sumn += Decimal(str(i.quarterLength))

            while sumn != 3:
                maxn = 0
                minn = 100
                if sumn > 3:
                    for i in range(len(cho)):
                        if isinstance(cho[i], note.Note) or isinstance(cho[i], chord.Chord) or isinstance(cho[i],
                                                                                                          note.Rest):
                            if cho[i].quarterLength > maxn:
                                maxn = cho[i].quarterLength
                                max_note = i
                    cho[max_note].quarterLength = cho[max_note].quarterLength - 0.25
                if sumn < 3:
                    for i in range(len(cho)):
                        if isinstance(cho[i], note.Note) or isinstance(cho[i], chord.Chord) or isinstance(cho[i],
                                                                                                          note.Rest):
                            if cho[i].quarterLength < 1.0 and cho[i].quarterLength < minn:
                                minn = cho[i].quarterLength
                                min_note = i
                    cho[min_note].quarterLength = cho[min_note].quarterLength + 0.25
                sumn = Decimal(0)
                for i in cho:
                    sumn += Decimal(str(i.quarterLength))

    return Ts_notes


def make_input_data(msure):
    input_data = []
    co = 0
    for cho in msure:
        for notes in cho:

            if isinstance(notes, stream.Voice):

                co0 = -3
                co1 = 0

                for r in range(len(notes)):
                    if isinstance(notes[r], note.Note):
                        String_tone = str(notes[r].pitch)
                    if isinstance(notes[r], chord.Chord):
                        String_tone = ','.join(str(p.pitch) for p in notes[r])
                    if isinstance(notes[r], note.Rest):
                        String_tone = "Rest"

                    p_length = int(notes[r].quarterLength * 4)

                    for n in range(p_length):
                        if co % 2 == 0:
                            if input_data == []:
                                input_data.append([String_tone])
                            elif len(input_data[-1]) < 4:
                                input_data[-1].append(String_tone)
                            elif len(input_data[-1]) >= 4:
                                input_data.append([String_tone])
                        if co % 2 == 1:
                            if input_data[co0][co1] == "Rest":
                                input_data[co0][co1] = (String_tone)
                            else:
                                if String_tone == "Rest":
                                    pass
                                else:
                                    input_data[co0][co1] = (String_tone) + "," + input_data[co0][co1]
                            co1 += 1
                            if co1 >= 4:
                                co0 += 1
                                co1 = 0

                co += 1

            else:

                if isinstance(notes, note.Note):
                    String_tone = str(notes.pitch)
                if isinstance(notes, chord.Chord):
                    String_tone = ','.join(str(p.pitch) for p in notes)
                if isinstance(notes, note.Rest):
                    String_tone = "Rest"
                p_length = int(notes.quarterLength * 4)

                for i in range(p_length):
                    if input_data == []:
                        input_data.append([String_tone])
                    elif len(input_data[-1]) < 4:
                        input_data[-1].append(String_tone)
                    elif len(input_data[-1]) >= 4:
                        input_data.append([String_tone])
    return input_data


def onkai(tones2):
    regex = re.compile('\d+')
    scale = ["C", "D", "E", "F", "G", "A", "B"]

    for i in range(len(tones2)):
        for r in range(len(scale)):
            if scale[r] in tones2[i] and "-" in tones2[i] and not "--" in tones2[i]:
                if scale[r] == "C":
                    number = int(regex.findall(tones2[i])[0])
                    tones2[i] = tones2[i].replace(tones2[i], "B#" + str(number - 1))
                else:
                    tones2[i] = tones2[i].replace(scale[r] + "-", scale[r - 1] + "#")

            if scale[r] in tones2[i] and "--" in tones2[i]:
                if scale[r] == "C":
                    number = int(regex.findall(tones2[i])[0])
                    tones2[i] = tones2[i].replace(tones2[i], "B" + str(number - 1))
                else:
                    tones2[i] = tones2[i].replace(scale[r] + "--", scale[r - 1])

            if scale[r] in tones2[i] and "##" in tones2[i]:
                if scale[r] == "B":
                    number = int(regex.findall(tones2[i])[0])
                    tones2[i] = tones2[i].replace(tones2[i], "C" + str(number + 1))
                else:
                    tones2[i] = tones2[i].replace(scale[r] + "##", scale[r + 1])
    return tones2


def getNearestValue(list, num):
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]


def search_near_note(n_note, dicts):
    note_index = []

    all_notes = {"A0": 1, "B0": 2, "C1": 3, "D1": 4, "E1": 5, "F1": 6, "G1": 7, "A1": 8, "B1": 9,
                 "C2": 10, "D2": 11, "E2": 12, "F2": 13, "G2": 14, "A2": 15, "B2": 16,
                 "C3": 17, "D3": 18, "E3": 19, "F3": 20, "G3": 21, "A3": 22, "B3": 23,
                 "C4": 24, "D4": 25, "E4": 26, "F4": 27, "G4": 28, "A4": 29, "B4": 30,
                 "C5": 31, "D5": 32, "E5": 33, "F5": 34, "G5": 35, "A5": 36, "B5": 37,
                 "C6": 38, "D6": 39, "E6": 40, "F6": 41, "G6": 42, "A6": 43, "B6": 44,
                 "C7": 45, "D7": 46, "E7": 47, "F7": 48, "G7": 49, "A7": 50, "B7": 51, "C8": 52}

    r = re.compile(r'(\w+)')
    for i in list(dicts.keys())[2:]:
        sum = 0
        r_note = re.findall(r, i)
        for n in r_note:
            sum += all_notes[n]
        note_index.append([sum, len(i)])

    r_note2 = re.findall(r, n_note)
    sum2 = 0

    for i in r_note2:
        sum2 += all_notes[i]
    note_index2 = [x[0] for x in note_index if x[1] == len(n_note)]
    before_index = [x[0] for x in note_index if x[1] > len(n_note)]

    return note_index2.index(getNearestValue(note_index2, sum2)) + len(before_index) + 2


def inverse_lookup(d, x):
    for k,v in d.items():
        if x == v:
            return k



def trans_data(data , notes_dict):
    for n in range(3):
        for i in range(len(data)):
            data[i] = onkai(data[i])

        for r in range(len(data)):
            for i in range(len(data[r])):
                data[r][i] = data[r][i].replace('#', '')

    t_r1 = []
    t_i_nd1 = []
    co = 0
    for n in range(len(data)):
        co += 1
        for i in range(len(data[n])):
            t_r1.append(data[n][i][:])
        if co % 3 == 0:
            t_i_nd1.append(t_r1[:])
            t_r1 = []

    t_i_nd2 = []
    co = 0
    for i in range(len(t_i_nd1)):
        for r in range(len(t_i_nd1[i])):
            t_i_nd2.append(t_i_nd1[i][:])
            t_i_nd2[co][r] = "None"
            co += 1

    for r in range(len(t_i_nd2)):
        for i in range(len(t_i_nd2[r])):
            try:
                t_i_nd2[r][i] = notes_dict[t_i_nd2[r][i]]
            except KeyError:
                t_i_nd2[r][i] = search_near_note(t_i_nd2[r][i], notes_dict)

    return t_i_nd2 ,max(notes_dict.values())



def new_chopin(cho,notes_dict):
    c1 = []
    new_chopin1 = []
    co = 0

    for i in range(len(cho)):
        c1.append([inverse_lookup(notes_dict, int(np.where(cho[i] == max(cho[i]))[0])), 0.25])
        co += 1
        if co == 12:
            new_chopin1.append(c1)
            co = 0
            c1 = []

    for i in new_chopin1:
        for r in range(len(i)):
            for n in range(r + 1, len(i)):
                if i[r][0] != i[n][0]:
                    break
                elif len(i[r]) == 1:
                    break
                elif i[r][0] == i[n][0]:
                    i[r][1] += 0.25
                    i[n].pop()

    for i in range(len(new_chopin1)):
        new_chopin1[i] = [x for x in new_chopin1[i] if len(x) == 2]

    noteList = []
    part = stream.Part()
    p = re.compile(r'(\w+)')
    for i in new_chopin1:
        for r in i:
            if len(r[0]) == 2:
                n = note.Note(pitch=r[0], quarterLength=r[1])
                noteList.append(n)
            elif len(r[0]) == 4:
                rest = note.Rest(quarterLength=r[1])
                noteList.append(rest)
            else:
                c = chord.Chord(re.findall(p, r[0]), quarterLength=r[1])
                noteList.append(c)

        measure = stream.Measure()
        measure.append(noteList)
        part.append(measure)
        noteList = []

    return part
