#!/bin/sh

APP=_build/default/bin/main.exe
HOME=/home/john/git/miiify

cd $HOME
($APP >/dev/null 2>&1)&

