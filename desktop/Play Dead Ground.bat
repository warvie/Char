@echo off
setlocal EnableExtensions
rem ---- Dead Ground desktop launcher (Windows) ----
rem Starts Chrome or Edge in its own window with the frame-rate cap and
rem background throttling switched off, pointing at the game file next to
rem this script. Uses its own browser profile so the flags always apply,
rem even when your normal browser is already running.
set "DIR=%~dp0"
set "URL=file:///%DIR:\=/%index.html"
set "PROFILE=%LocalAppData%\DeadGroundBrowser"
for %%B in ("%ProgramFiles%\Google\Chrome\Application\chrome.exe" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" "%LocalAppData%\Google\Chrome\Application\chrome.exe" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe") do (
  if exist %%B (
    start "" %%B --user-data-dir="%PROFILE%" --disable-gpu-vsync --disable-frame-rate-limit --disable-background-timer-throttling --disable-renderer-backgrounding --autoplay-policy=no-user-gesture-required --app="%URL%"
    exit /b
  )
)
echo Could not find Chrome or Edge, opening in your default browser instead (the frame-rate cap stays on there).
start "" "%URL%"
