# Predicting Historical Periods for Classical Piano Performances

## Overview

This project applies machine learning to classify classical piano performances into historical periods such as Baroque, Classical, Romantic, and Modern. By analyzing performance features derived from MIDI files, the model aims to assist educators, students, and music enthusiasts in understanding and categorizing piano compositions.

## Dataset

- 1276 piano performances
- High-precision MIDI recordings
- Performance metadata

Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang, Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. ["Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."](https://goo.gl/magenta/maestro-paper) In International Conference on Learning Representations, 2019.

## Features

- **split**: proposal for separation of `train`, `test` and `validation`
- **duration**: performance duration
- **key_0...key_87**: pitch frequency for each key (88 keys in total for piano)
- **pitch_range**: difference between highest and lowest pitch
- **tempo**: inferred tempo
- **avg_note_duration**: average duration of all notes
- **avg_velocity**: average velocity of all notes
- **velocity_range**: difference between highest and lowest velocity

## Models

### K-Nearest Neighbours

- Linear search for the best value of K using cross-validation.
- Best accuracy achieved with K=77.

### Random Forest

- Optimised number of trees using Grid Search.
- Best accuracy achieved with 300 trees, no depth limit and 5 as min split.

## Conclusion

- Achieved relatively high accuracy for predicting historical periods.
- Random Forest outperformed KNN, making it the final model choice.
- Chosen features were useful to classify pieces into their respective era.

## Proof of Concept

### Python REST API

`POST /predict endpoint`

- **Input:** MIDI file
- **Output:** Gistorical period

### Mobile App

- Single screen to pick, upload and analyse a MIDI file
- Fetch JSON response from Python server and parse it

## Future Work

- Key, chord and cadence analysis as extra features
- Test advanced ML models like Neural Networks.
- Expand dataset with more compositions and periods.
