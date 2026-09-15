@echo off
title Winners Academy Bot
color 0A
echo.
echo  ==========================================
echo   Winners Academy Bot - ishga tushmoqda...
echo  ==========================================
echo.
echo  Bot: @WinnersAcadeemybot
echo  Toxtatish uchun: Ctrl + C bosing
echo.
cd /d "%~dp0"
python -X utf8 -m bot.main
echo.
echo  Bot toxtatildi. Davom etish uchun istalgan tugmani bosing...
pause > nul
