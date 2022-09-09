import vapoursynth as vs

core = vs.core
core.max_cache_size = 8000

res = core.lsmas.LWLibavSource(source="La.hevc").text.ClipInfo() #主要用于查看编码后码流的IPB帧信息
res.set_output()
