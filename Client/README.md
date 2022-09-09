# Encoding Client Template
使用TCPClip时接收端的Vapoursynth脚本

## Code
```python
from TCPClip import Client
clip = Client('<ip address>', port=14322, log_level='info', shutdown=True).as_source()
clip.set_output()
```
## 用法
按普通Vapoursynth脚本使用
参见 [Beatrice-Raws/VapourSynth-TCPClip](https://github.com/Beatrice-Raws/VapourSynth-TCPClip)