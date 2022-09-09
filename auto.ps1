# 自动调用TVE对坏帧重新渲染
Function Task($arg1, $arg2)
{
mkdir  ('alter/{0:d6}_{1:d6}' -f $arg1, $arg2)
For ($i=$arg1 ; $i -le $arg2 ; $i++)
{
cp ('frames/{0:d6}.png' -f ($i)) ('alter/{0:d6}_{1:d6}' -f $arg1, $arg2)
rename-Item ('alter/{0:d6}_{1:d6}/{2:d6}.png' -f $arg1, $arg2, ($i)) -NewName ('{0:d6}_0.png' -f $i)
cp ('frames/{0:d6}.png' -f ($i)) ('alter/{0:d6}_{1:d6}' -f $arg1, $arg2)
rename-Item ('alter/{0:d6}_{1:d6}/{2:d6}.png' -f $arg1, $arg2, ($i)) -NewName ('{0:d6}_1.png' -f $i)
cp ('frames/{0:d6}.png' -f ($i)) ('alter/{0:d6}_{1:d6}' -f $arg1, $arg2)
rename-Item ('alter/{0:d6}_{1:d6}/{2:d6}.png' -f $arg1, $arg2, ($i)) -NewName ('{0:d6}_2.png' -f $i)
}
mkdir ('alter/{0:d6}_{1:d6}/upscale' -f $arg1, $arg2)
veai -i ('alter/{0:d6}_{1:d6}/{2:d6}_0.png' -f $arg1, $arg2, $arg1) -o ('alter/{0:d6}_{1:d6}/upscale' -f $arg1, $arg2) -f png -s 4 -m gcg-1.0.1 -c 0
}

mkdir alter
# Task 1930 1985
# Task 751 751
# Task 1919 1919
# Task 1982 2015
# Task 2242 2262

# Task 0 0