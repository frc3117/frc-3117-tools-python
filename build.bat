@echo off

SET BASEDIR=%~dp0
cd %BASEDIR%

pip wheel --no-deps -w build .

del /S "./build/lib"
del /S "./build/bdist.*"
del /S "*.egg-info"