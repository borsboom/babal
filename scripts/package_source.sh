cd ..
textfiles="babal/*.txt babal/*.html babal/src/*.py babal/scripts/*.sh babal/scripts/*.bat"
binaryfiles="babal/data/*.map"

tar cvzf babal/babal-src.tgz $textfiles $binaryfiles

rm -f babal/babal-src.zip
zip -l babal/babal-src.zip $textfiles
zip babal/babal-src.zip $binaryfiles
