@echo off
rem Fig. Starts a tiny local server and opens the app.
rem A page opened straight off the disk is not allowed to read its own data
rem files, so it has to be served. Nothing here touches the internet.

set PY=C:\Users\levia\AppData\Local\Programs\Python\Python312\python.exe
set PORT=8777

start "fig server" /min "%PY%" -m http.server %PORT% --directory "%~dp0."
timeout /t 1 /nobreak >nul
start "" "http://localhost:%PORT%/www/index.html"
