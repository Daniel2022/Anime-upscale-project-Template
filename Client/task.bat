vspipe Client.vpy - --y4m | ^
x265-10b --preset slower ^
--no-open-gop --keyint 240 --min-keyint 1 --colormatrix bt709 --colorprim bt709 --transfer bt709 --deblock -1:-1 ^
--ctu 64 --qg-size 8 --me 3 --subme 5 --merange 57 --b-intra --limit-tu 4 --no-amp ^
--ref 5 --weightb --bframes 8 --rc-lookahead 72 --rd 3 ^
--no-sao --crf 15.0 --aq-mode 1 --aq-strength 0.8 --psy-rd 1.8 --psy-rdoq 0.7 --rdoq-level 2 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --qcomp 0.65 ^
--vbv-bufsize 80000 --vbv-maxrate 75000 ^
--no-strong-intra-smoothing ^
--y4m -D 10 ^
--output "output.hevc" -

@REM vspipe Client.vpy - --y4m | ^
@REM x265-10b --preset slower ^
@REM --no-open-gop --keyint 240 --min-keyint 1 --colormatrix bt709 --colorprim bt709 --transfer bt709 --deblock -1:-1 ^
@REM --ctu 64 --qg-size 8 --me 3 --subme 4 --merange 57 --b-intra --limit-tu 4 --no-amp ^
@REM --ref 5 --weightb --bframes 8 --rc-lookahead 72 --rd 3 ^
@REM --no-sao --crf 15.0 --aq-mode 1 --aq-strength 0.8 --psy-rd 1.7 --psy-rdoq 0.8 --rdoq-level 2 --pbratio 1.2 --cbqpoffs -2 --crqpoffs -2 --qcomp 0.65 ^
@REM --vbv-bufsize 80000 --vbv-maxrate 75000 ^
@REM --no-strong-intra-smoothing ^
@REM --y4m -D 10 ^
@REM --output "Chase_4K_931-3045.hevc" -

pause