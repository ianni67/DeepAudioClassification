#Define paths for files
spectrogramsPath = "Data/Spectrograms/"
slicesPath = "Data/Slices/"
datasetPath = "Data/Dataset/"
rawDataPath = "Data/Raw/"

#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128
sliceHeight = 256

#Dataset parameters
filesPerGenre = 1000
validationRatio = 0.3
testRatio = 0.1

#Model parameters
batchSize = 128
learningRate = 0.000005
nbEpoch = 240
