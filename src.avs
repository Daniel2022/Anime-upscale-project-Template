function OpenVideoAndAudio(filename)
{
    a=LWLibavAudioSource(filename,av_sync=True)
    v=LWLibavVideoSource(filename)
    return AudioDub(v,a)
}

#~ VSImport("src.vpy",index=0,prefetch=4) #Vapoursynth Import 将Vapoursynth流导入Avisynth便于使用ffmpeg 需要VapoursynthSource Avs plugin

#~ OpenVideoAndAudio("NCOP.mkv")  #导入音视频
#~ Trim(22883,25854-1) #切割