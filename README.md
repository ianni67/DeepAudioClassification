# MODIFIED Deep Audio Classification

This is a modified fork from "Finding the genre of a song with Deep Learning" (https://medium.com/@juliendespois/finding-the-genre-of-a-song-with-deep-learning-da8f59a61194#.yhemoyql0).

My modifications are aimed at experimenting with more informative formats of spectrogram-like images, keeping 16bit magnitude instead of 8 bit, and also keeping the phase.

Moreover, the vertical size of the slices is now 1024 instead of 128, so
the slices are rectangular instead of square.

This code is _heavily experimental_ and might not work from time to time.

Required install:

```
eyed3
sox --with-lame
librosa
numpy
Pillow (PIL)
tensorflow
tflearn
```

- Create folder Data/Raw/
- Place your labeled .mp3 files in Data/Raw/

To create the song slices (might be long):

```
python main.py slice
```

To train the classifier (long too):

```
python main.py train
```

To test the classifier (fast):

```
python main.py test
```

- Most editable parameters are in the config.py file, the model can be changed in the model.py file.
- I haven't implemented the pipeline to label new songs with the model, but that can be easily done with the provided functions, and eyed3 for the mp3 manipulation. Here's the full pipeline you would need to use.

![alt tag](https://github.com/despoisj/DeepAudioClassification/blob/master/img/pipeline.png)
