import pretty_midi
import music21
import numpy as np
import pandas as pd
import os

np.int = np.int64 # Fix for pretty_midi

# Function to compute the pitch histogram
def compute_pitch_histogram(midi_data):
    """
    Compute the pitch histogram for a MIDI file and return a dictionary with keys like key_0, key_1, ..., key_87.
    """
    # Initialize histogram with zeros for each pitch (128 pitches in total)
    pitch_range_histogram = np.zeros(128)
    
    # Populate histogram
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            pitch_range_histogram[note.pitch] += 1

    piano_range_histogram = pitch_range_histogram[21:109] # Slice for piano range (A0 to C8)

    # Convert histogram to a dictionary with pitch_x keys
    pitch_class_histogram_dict = {f"key_{i}": piano_range_histogram[i] for i in range(88)}
    return pitch_class_histogram_dict

# Function to compute pitch-related features
def compute_pitch_range(midi_data):
    """
    Compute pitch range and related features.
    """
    all_pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
    pitch_range = max(all_pitches) - min(all_pitches)
    return pitch_range

# Function to compute rhythm-related features
def compute_rhythm_features(midi_data):
    """
    Compute tempo and average note duration.
    """
    duration = midi_data.get_end_time()
    tempo = midi_data.estimate_tempo()
    note_durations = [note.end - note.start for instrument in midi_data.instruments for note in instrument.notes]
    avg_note_duration = np.mean(note_durations)
    return duration, tempo, avg_note_duration

# Function to compute dynamic-related features
def compute_dynamic_features(midi_data):
    """
    Compute average velocity and velocity range.
    """
    velocities = [note.velocity for instrument in midi_data.instruments for note in instrument.notes]
    avg_velocity = np.mean(velocities)
    velocity_range = max(velocities) - min(velocities)
    return avg_velocity, velocity_range

def fetch_key_from_midi(midi_file):
    """
    Fetch the key of a MIDI file using music21.
    """

    # Load the MIDI file
    midi_data = music21.converter.parse(midi_file)

    # Analyze the key
    analyzed_key = midi_data.analyze('key')

    # Return the key signature
    return analyzed_key

# Master function to extract all MIDI features
def extract_midi_features(midi_data):
    result = {}

    duration, tempo, avg_note_duration = compute_rhythm_features(midi_data)

    # duration
    result["duration"] = duration

    # Pitch histogram
    result.update(compute_pitch_histogram(midi_data))

    # Pitch range
    result["pitch_range"] = compute_pitch_range(midi_data)

    # Rhythm features
    result["tempo"], result["avg_note_duration"] = tempo, avg_note_duration

    # Dynamic features
    result["avg_velocity"], result["velocity_range"] = compute_dynamic_features(midi_data)

    return result