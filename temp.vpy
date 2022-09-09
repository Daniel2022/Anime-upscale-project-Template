import vapoursynth as vs

core = vs.core
core.max_cache_size = 8000

#此脚本用于生成Vertical Stacked 视频用于超分结果和源比较

src_BD = core.lsmas.LWLibavSource(source="NCOP.mkv",threads=1)#[22883:25854]
up = core.imwri.Read(filename=r'frames\TVE\%06d.png', firstnum=0).std.AssumeFPS(None,24000,1001)
res = core.std.StackVertical(clips=[src_BD.resize.Bicubic(1280,720,format=vs.YUV420P8), up.resize.Bicubic(1280,720,range_in_s="full",range_s="limited",matrix_s="709",format=vs.YUV420P8)])
#res = core.lsmas.LWLibavSource(source="temp_test.MP4",threads=4) #输入压制结果

res.set_output()