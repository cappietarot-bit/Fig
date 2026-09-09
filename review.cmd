@echo off
rem Fig. Opens the verse review screen.
rem Tap the verses you want as cards. Decisions save as you go, so you can stop
rem anywhere and come back. Export approved when you are done with a batch.

set PY=C:\Users\levia\AppData\Local\Programs\Python\Python312\python.exe
set PORT=8777

start "fig server" /min "%PY%" -m http.server %PORT% --directory "%~dp0."
timeout /t 1 /nobreak >nul
start "" "http://localhost:%PORT%/tools/review.html"
