import vapoursynth as vs
import sys
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import nnedi3_resample as nnrs
import vsTAAmbk as taa
import descale
import fvsfunc as fvf
import kagefunc as kgf
from TCPClip import Server
from math import floor
import zhyfunc as zhf

core = vs.core
core.max_cache_size = 8000

# 坏帧替换
def AlterFrame(clip,start,end):
	filename = r'alter/%06d_%06d/upscale/' % (start, end) + r"%06d.png"
	RGB = core.imwri.Read(filename,firstnum=0).std.SelectEvery(cycle=3,offsets=1).std.AssumeFPS(None,24000,1001)
	return (clip[0:start]+RGB+clip[end+1:clip.num_frames])

def AlterFrame2(clip,start,end):
	filename = r'alter/%06d_%06d/upscale/' % (start, end) + r"%06d.png"
	RGB = core.imwri.Read(filename,firstnum=0).std.SelectEvery(cycle=4,offsets=2).std.AssumeFPS(None,24000,1001)
	return (clip[0:start]+RGB+clip[end+1:clip.num_frames])
	
def AlterFrame_Real(clip,start,end):
	filename = r'real-cugan/%06d_%06d/' % (start, end) + r"%06d_3x_tile3_cache0_alpha1.0.png"
	YUV = mvf.ToYUV(core.imwri.Read(filename,firstnum=start),matrix="709",full=False,css="444",depth=32).std.AssumeFPS(None,24000,1001)
	res = mvf.Depth(muf.SSIM_downsample(YUV,3840,2160,use_fmtc=True,gamma=True,a1=0,a2=0.5),16)
	if start> 0 :
		return clip[0:start]+res+clip[end+1:clip.num_frames]
	else:
		return res+clip[end+1:clip.num_frames]

# 载入RGB From TVE & Real-CUGAN
src_RGB_Topaz = core.imwri.Read(r"frames\TVE\%06d.png",firstnum=0).std.AssumeFPS(None,24000,1001)
src_RGB_Real = core.imwri.Read(r"frames\real\%06d_3x.png",firstnum=0).std.AssumeFPS(None,24000,1001)
#src_RGB_Topaz = AlterFrame(src_RGB_Topaz,1930,1985)
#src_RGB_Topaz = AlterFrame(src_RGB_Topaz,751,751)
#src_RGB_Topaz = AlterFrame(src_RGB_Topaz,1919,1919)

src_YUV444_Topaz = mvf.ToYUV(src_RGB_Topaz,matrix="709",full=False,css="444",depth=32)
src_YUV444_Topaz = mvf.Depth(muf.SSIM_downsample(src_YUV444_Topaz,3840,2160,use_fmtc=True,gamma=True,a1=0,a2=0.5),16)
src_YUV444_Real = mvf.ToYUV(src_RGB_Real,matrix="709",full=False,css="444",depth=32)
src_YUV444_Real = mvf.Depth(muf.SSIM_downsample(src_YUV444_Real,3840,2160,use_fmtc=True,gamma=True,a1=0,a2=0.5),16)

def main_process(input):
	src16 = input
#	src16 = haf.HQDeringmod(src16,nrmode=3,mrad=4,show=False)
	nr16 = core.rgvs.RemoveGrain(src16, mode=[20,11])
	diff = core.std.MakeDiff(src16,nr16)
	mask = zhf.retinex_edgemask(src16,1).std.Expr("x 35900 < 0 x 36000 < x 65535 ? ?").std.Maximum(0).std.Maximum(0).std.Maximum(0).std.Minimum(0).std.Minimum(0).rgvs.RemoveGrain(20)#.std.BinarizeMask(256*200)
	edge = core.std.MergeDiff(src16,diff)
	edge = mvf.LimitFilter(edge, src16, thr=4.0, thrc=3.0, elast=4.0)

	edge = core.std.Transpose(haf.daa(core.std.Transpose(haf.daa(edge,opencl=True)),opencl=True))
	edge = haf.FineDehalo(edge,rx=2.0,darkstr=0.3,brightstr=1.9)
	edge = haf.EdgeCleaner(edge)
#	edge = haf.HQDeringmod(edge,nrmode=3,mrad=4,show=False)
#	edge = core.std.Transpose(haf.daa(core.std.Transpose(haf.daa(edge,opencl=True)),opencl=True))
#	edge = taa.TAAmbk(edge,preaa=0, aatype=2,cycle=0, mtype=0, opencl=True,cuda=True)
	
	db = core.f3kdb.Deband(src16, 12, 24, 16, 16, 0, 0, output_depth=16)
	db = core.f3kdb.Deband(db, 24, 56, 32, 32, 0, 0, output_depth=16)
	nonedge = mvf.LimitFilter(db, src16, thr=0.3, thrc=0.2, elast=2.0)
#	nonedge = core.std.MergeDiff(nonedge,diff)
	
	res = core.std.MaskedMerge(clipa=nonedge, clipb=edge, mask=mask, first_plane=True)
	res = haf.HQDeringmod(res,nrmode=2,mrad=4,show=False)
#	res = mvf.ToYUV(mask,css="444")
#	res = edge
	return res

def main_process2(input):
	src16 = input
#	src16 = taa.TAAmbk(src16,aatype=2,cycle=0,showmask=0,opencl=True,sharp=0,strength=0,aarepair=0)
#	src16 = haf.HQDeringmod(src16,nrmode=3,mrad=4,show=False)
	nr16 = core.rgvs.RemoveGrain(src16, mode=[20,11])
	diff = core.std.MakeDiff(src16,nr16)
	mask = zhf.retinex_edgemask(src16,1).std.Expr("x 10000 < 0 x 30000 < x 65535 ? ?").std.Maximum(0).std.Maximum(0).std.Maximum(0).std.Minimum(0).std.Minimum(0).std.Minimum(0).rgvs.RemoveGrain(20)#.std.BinarizeMask(256*200)
	edge = core.std.MergeDiff(src16,diff)
	edge = mvf.LimitFilter(edge, src16, thr=3.0, thrc=3.0, elast=3.0)

#	edge = core.std.Transpose(haf.daa(core.std.Transpose(haf.daa(edge,opencl=True)),opencl=True))
#	edge = haf.FineDehalo(edge,rx=2.0,darkstr=0.4,brightstr=1.5)
	edge = haf.EdgeCleaner(edge)
#	edge = haf.HQDeringmod(edge,nrmode=3,mrad=4,show=False)
#	edge = core.std.Transpose(haf.daa(core.std.Transpose(haf.daa(edge,opencl=True)),opencl=True))
#	edge = taa.TAAmbk(edge,preaa=0, aatype=2,cycle=0, mtype=0, opencl=True,cuda=True)
	
	db = core.f3kdb.Deband(src16, 12, 24, 16, 16, 0, 0, output_depth=16)
	db = core.f3kdb.Deband(db, 24, 56, 32, 32, 0, 0, output_depth=16)
	nonedge = mvf.LimitFilter(db, src16, thr=0.3, thrc=0.2, elast=2.0)
#	nonedge = core.std.MergeDiff(nonedge,diff)
	
	res = core.std.MaskedMerge(clipa=nonedge, clipb=edge, mask=mask, first_plane=True)
#	res = haf.HQDeringmod(res,nrmode=2,mrad=4,show=False)
#	res = mvf.ToYUV(mask,css="444")
#	res = edge
	return res
	
def process_real(clip):
	src16 = clip
	res = haf.FineDehalo(src16,rx=2.0,darkstr=0.3,brightstr=1.8)
#	res = clip
	return res
	
res = main_process(src_YUV444_Topaz)

res = fvf.rfs(res,process_real(src_YUV444_Real),"[1318 1465][1496 1713][1744 2056]")

Debug = False
if Debug:
#	encoded = mvf.ToYUV(encoded,css="444",depth=16)
	res = core.std.Interleave([src_YUV444_Topaz, res])
	res = mvf.ToRGB(res,matrix="709",full=False,depth=8)
else: 
	res = mvf.ToYUV(res,full=False,matrix="709",css="420",depth=10)

res.set_output()


if __name__ == "__main__":
	#此部分为仅当使用python 在Terminal中载入时作用
	#Command: python example.vpy [INDEX]
	#功能：使用TCPClip.Server开启网络管道进行推流 [INDEX]为output index
	#参见：https://github.com/Beatrice-Raws/VapourSynth-TCPClip
	index = sys.argv[1]
	Server('192.168.20.136', 14322, vs.get_output(int(index)), threads=4, log_level='info', compression_method=None, compression_level=1, compression_threads=1)