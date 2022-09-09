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

from math import floor
import zhyfunc as zhf
from rekt import *


core = vs.core
core.max_cache_size = 8000

#输入
src_BD = core.lsmas.LWLibavSource(source="NCOP.mkv",threads=1)#[22883:25854]
src16 = mvf.Depth(src_BD,16)

#Descale 逆向分辨率 目标根据getnative选择
Y = core.std.ShufflePlanes(src16,0,vs.GRAY)
downY = core.descale.Debilinear(Y,800*16/9,800)#.knlm.KNLMeansCL(d=2, a=2, s=3,  h=0.8, wmode=2, device_type="GPU")
U = src16.std.ShufflePlanes(1,vs.GRAY).fmtc.resample(800*16/9,800,kernel="bicubic",a1=0,a2=0.5,sx=0.25)#.knlm.KNLMeansCL(h=0.4, wmode=1, device_type="GPU")
V = src16.std.ShufflePlanes(2,vs.GRAY).fmtc.resample(800*16/9,800,kernel="bicubic",a1=0,a2=0.5,sx=0.25)#.knlm.KNLMeansCL(h=0.4, wmode=1, device_type="GPU")
YUV = core.std.ShufflePlanes([downY,U,V],planes=[0,0,0],colorfamily=vs.YUV)

#AA different method
AA = taa.TAAmbk(YUV,preaa=0,aatype=2,cycle=0,showmask=0,opencl=True,sharp=0,strength=0,aarepair=0)
AA2 = taa.TAAmbk(YUV,preaa=2,aatype=3,cycle=0,showmask=0,opencl=True,sharp=0,strength=0,aarepair=0)
AA3 = taa.TAAmbk(YUV,preaa=1,aatype=3,cycle=0,showmask=0,opencl=True,sharp=0,strength=0,aarepair=0)
AA4 = taa.TAAmbk(YUV,preaa=0,aatype=3,cycle=1,showmask=0,opencl=True,sharp=0,strength=0,aarepair=0)

#按帧范围替换帧 rekt进行矩形局部作用滤镜
YUV = fvf.rfs(YUV,AA4,"[24 53][393 462][523 1266][1277 1317][1466 1495][1714 1743][2057 2183]")
YUV = fvf.rfs(YUV,AA,"[54 87][1267 1276]")
YUV = fvf.rfs(YUV,rekt(AA4,AA, left=500, top=130, right=300, bottom=100),"[88 157]")

#一种Deband
def mydeband(clip):
	nr8    = mvf.Depth(clip, depth=8)
#	luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
	nrmasks = core.tcanny.TCannyCL(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?",""],vs.YUV420P16)
	nrmaskb = core.tcanny.TCannyCL(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
	nrmaskg = core.tcanny.TCannyCL(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
	nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks, nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?",""],vs.YUV420P16)
	nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
	nrmask  = core.rgvs.RemoveGrain(nrmask,[20,0])
	debd  = core.f3kdb.Deband(clip,9,24,16,16,0,0,output_depth=16)
	debd  = core.f3kdb.Deband(debd,15,56,32,32,0,0,output_depth=16)
	debd  = mvf.LimitFilter(debd,clip,thr=0.4,thrc=0.3,elast=2.0)
	res  = core.std.MaskedMerge(debd,clip,nrmask,first_plane=True)
	return res

#一种Deband
def mydeband2(clip):
	nr8    = mvf.Depth(clip, depth=8)
#	luma   = core.std.ShufflePlanes(nr8, 0, vs.YUV).resize.Bilinear(format=vs.YUV420P8)
	nrmasks = core.tcanny.TCannyCL(nr8,sigma=0.8,op=2,gmmax=255,mode=1,planes=[0,1,2]).std.Expr(["x 7 < 0 65535 ?","0"],vs.YUV420P16)
	nrmaskb = core.tcanny.TCannyCL(nr8,sigma=1.3,t_h=6.5,op=2,planes=0)
	nrmaskg = core.tcanny.TCannyCL(nr8,sigma=1.1,t_h=5.0,op=2,planes=0)
	nrmask  = core.std.Expr([nrmaskg,nrmaskb,nrmasks, nr8],["a 20 < 65535 a 48 < x 256 * a 96 < y 256 * z ? ? ?","0"],vs.YUV420P16)
#	nrmask  = core.std.Expr([nrmask,nr8],["y 60 < 65535 x ?",""],vs.YUV420P16)
#	nrmask = zhf.retinex_edgemask(clip)
	nrmask  = core.std.Maximum(nrmask,0).std.Maximum(0).std.Minimum(0)
	nrmask  = core.rgvs.RemoveGrain(nrmask,[20])
	debd  = core.f3kdb.Deband(clip,12,24,16,16,0,0,output_depth=16)
	debd  = core.f3kdb.Deband(debd,20,56,32,32,0,0,output_depth=16)
	debd  = mvf.LimitFilter(debd,clip,thr=0.6,thrc=0.5,elast=2.0)
	res  = core.std.MaskedMerge(debd,clip,nrmask,first_plane=True)
#	res = mvf.ToYUV(nrmask,css="420")
	return res
	
mask = zhf.retinex_edgemask(YUV).std.Expr("x 6000 < 0 x 40000 < x 65535 ? ?").std.Maximum(0).std.Maximum(0).std.Minimum(0).std.Minimum(0).rgvs.RemoveGrain(20)#.fmtc.resample(3840,2160)
nr16 = YUV.rgvs.RemoveGrain([20,11])
diff = core.std.MakeDiff(YUV,nr16)
edge = core.std.MergeDiff(YUV,diff)
edge = mvf.LimitFilter(edge,YUV,thr=3.5,thrc=2.5,elast=3.0)
#edge = haf.FineDehalo(edge,rx=2.0,darkstr=0.4,brightstr=1.0)
edge = haf.EdgeCleaner(edge)
#edge = nnrs.nnedi3_resample(edge,3840,2160,nns=4,mode="nnedi3cl",csp=vs.YUV420P16)
#edge = haf.HQDeringmod(edge,nrmode=2,mrad=2,drrep=1,thr=10.0,darkthr=2.5)
debd= mydeband(YUV.knlm.KNLMeansCL(h=0.8,a=2,s=3, wmode=1, device_type="GPU"))

res = core.std.MaskedMerge(clipa=debd, clipb=edge, mask=mask, planes=[0,1,2], first_plane=True)

res = mvf.ToRGB(res,matrix="709",full=False,depth=8)

res.set_output(0)

if __name__ == "__main__":
	#此部分为仅当使用python 在Terminal中载入时作用
	#Command: python example.vpy [INDEX]
	#功能：使用TCPClip.Server开启网络管道进行推流 [INDEX]为output index
	#参见：https://github.com/Beatrice-Raws/VapourSynth-TCPClip
	from TCPClip import Server
	index = sys.argv[1]
	Server('192.168.20.136', 14322, vs.get_output(int(index)), threads=4, log_level='info', compression_method=None, compression_level=1, compression_threads=1)