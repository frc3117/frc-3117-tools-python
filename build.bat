@echo off

SET BASEDIR=%~dp0
cd %BASEDIR%

SET FRCTOOLS_VERSION=0.0.12

pip wheel --no-deps -w build .

del /S "./build/lib"
del /S "./build/bdist.*"
del /S "*.egg-info"