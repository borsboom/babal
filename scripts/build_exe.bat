set python=C:\Python22
set zip=C:\zip\zip

cd src

REM build EXE
%python%\python setup.py py2exe --console --excludes OpenGL --includes string
pause

REM copy docs
set d=babal
copy ..\*.txt dist\%d%
pause

REM copy data
mkdir dist\%d%\data
copy ..\data\*.map dist\%d%\data
pause

REM copy OpenGL
set gl=%python%\Lib\site-packages\OpenGL
mkdir dist\%d%\OpenGL
mkdir dist\%d%\OpenGL\GL
mkdir dist\%d%\OpenGL\GLU
copy %gl%\__init__*.* dist\%d%\OpenGL
copy %gl%\*.pyd dist\%d%\OpenGL
copy %gl%\*.dll dist\%d%\OpenGL
copy %gl%\GL\__init__*.* dist\%d%\OpenGL\GL
copy %gl%\GLU\__init__*.* dist\%d%\OpenGL\GLU
pause

REM create zip
cd dist\%d%
del zip.zip
%zip% -r %zip%.zip *
move %zip%.zip ..\..\..\babal-win32.zip
cd ..\..\..
pause
