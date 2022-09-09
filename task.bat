@REM 拆帧
@REM mkdir frame
@REM ffmpeg -i src.avs -f image2 -start_number 955 frames_head2\%%06d.png

@REM 生成比较用Stack视频（使用NVENC）
@REM vspipe temp.vpy -o 0 - --y4m | ^
@REM ffmpeg -i - -c:v h264_nvenc -colorspace 1 -color_trc 1 -color_primaries 1 -profile:v high -b:v 12M temp_test.mp4 -y

@REM 开启网络Pipe
@REM python output_4K.vpy 0

@REM 编码Flac
@REM ffmpeg -vn -i src.avs -c:a copy -f wav - | flac -8 - -o output.flac 

@REM 主压制命令
@REM vspipe output_4K.vpy - --y4m | ^
@REM x265-10b --preset slower ^
@REM --no-open-gop --keyint 240 --min-keyint 1 --colormatrix bt709 --colorprim bt709 --transfer bt709 --deblock -1:-1 ^
@REM --ctu 64 --qg-size 8 --me 3 --subme 5 --merange 57 --b-intra --limit-tu 4 --no-amp ^
@REM --ref 5 --weightb --bframes 8 --rc-lookahead 72 --rd 3 ^
@REM --no-sao --crf 15.0 --aq-mode 1 --aq-strength 0.8 --psy-rd 1.8 --psy-rdoq 0.7 --rdoq-level 2 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --qcomp 0.65 ^
@REM --vbv-bufsize 80000 --vbv-maxrate 75000 ^
@REM --no-strong-intra-smoothing ^
@REM --y4m -D 10 ^
@REM --output "output.hevc" -

pause