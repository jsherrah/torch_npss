
import pyworld as pw
import soundfile as sf

path = './data/gen_wav/29-test.wav'

# numpy_array, sample_rate
x, fs = sf.read(path)
# f0, spectrogram, aperiodicities
print('wav2world...')
f0, sp, ap = pw.wav2world(x, fs)
print('done')
# numpy_array
print('synthesize...')
y = pw.synthesize(f0, sp, ap, fs, pw.default_frame_period)
print('done')
sf.write("outputaudio.wav", y, fs)
