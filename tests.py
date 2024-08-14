# import pycaw
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# print(volume.GetVolumeRange())
# volume.SetMasterVolumeLevel(0, None)



# from gtts import gTTS
# from  tempfile import TemporaryFile
#
#
# tts = gTTS(text='Hello', lang='en')
# f = TemporaryFile()
# tts.write_to_fp(f)
# # Play f
# f.close()


# from gtts import gTTS
# from time import sleep
# import os
# import pyglet
#
# tts = gTTS(text='Hello World', lang='en')
# #filename = '/tmp/temp.mp3'
# tts.save()
#
# music = pyglet.media.load(tts, streaming=False)
# music.play()
#
# sleep(music.duration) #prevent from killing
# os.remove(tts) #remove temperory file

# from gtts import gTTS
# from io import BytesIO
#
# mp3_fp = BytesIO()
# tts = gTTS('hello', lang='en')
# tts.write_to_fp(mp3_fp)

from gtts import gTTS
tts = gTTS('1', lang='en')
tts.save('hello.mp3')
