import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as pli
from scipy import ndimage
import librosa
import librosa.display # must be imported separately

def SoundToSpectroImage(inFilename, outFilename):
    y,r=librosa.load(inFilename)
    D = librosa.stft(y)

    #D_abs=np.abs(D)
    D_angle=np.angle(D)

    # Magnitude, in dB
    DD = librosa.amplitude_to_db(D, ref=np.max)
    # Normalize values
    XV = (DD-np.min(DD))*512

    # Split to channels
    XV_c = np.array([divmod(xi,256)[0] for xi in XV])
    XV_f = np.array([divmod(xi,256)[1] for xi in XV])

    # Phase
    XV_angle = (D_angle-np.min(D_angle))*40 #while reconstructing we'll suppose that min is -80db.

    #Compose image
    rgbArray = np.zeros((XV_c.shape[0],XV_c.shape[1],3), 'uint8')
    rgbArray[..., 0] = XV_c
    rgbArray[..., 1] = XV_f
    rgbArray[..., 2] = XV_angle
    img = pli.fromarray(rgbArray)
    
    # Save spectroImage image to outFilename
    img.save(outFilename)
    return None

def SpectroImageToSound(inFilename, outFilename):
    # Load SpectroImage
    img = pli.open(inFilename)
    rgbArray = np.asarray(img)
    
    # Split the channels: the first two compose the magnitude (8+8bit)
    XV_c = rgbArray[..., 0].astype("uint8")
    XV_f = rgbArray[..., 1].astype("uint8")
    # The third channel contains the phase
    XV_angle_ = rgbArray[..., 2].astype("uint8")
    XV_angle = (XV_angle_.astype("float32"))/40
    
    # Recompose 16 bit magnitude (in dB)
    XV = (XV_c*256+XV_f)
    
    # Convert to linear scale
    DDD_ = np.asarray(librosa.db_to_amplitude(XV.astype("int16")/512-80)*10000, dtype="int16")
    
    # Combine magnitude and phase to complex number
    DDD = DDD_ * np.exp(1j*XV_angle)
    
    # Convert back to sound
    skyline_ifft = librosa.istft(DDD).astype("float32")
    # Save the music file to wav (umpf... librosa does not save to mp3)
    librosa.output.write_wav(outFilename, skyline_ifft, 22050, True)
    return None    
