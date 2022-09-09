import vapoursynth as vs
from TCPClip import Client

core = vs.core
core.max_cache_size = 6000
#功能：使用TCPClip.Client接收Server的网络Pipe推流
#参见：https://github.com/Beatrice-Raws/VapourSynth-TCPClip
clip = Client('192.168.20.136', port=14322, log_level='info', shutdown=True).as_source()
clip.set_output()