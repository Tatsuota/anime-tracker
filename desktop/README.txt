Anime Tracker — Desktop
=======================

A standalone Windows application for the Anime New Episode Tracker.
It runs in its own native window (no browser, no tabs, no address bar).

HOW TO RUN
----------
  Double-click  "Anime Tracker.exe"

That's it — no install, no setup. The app opens in its own window.

PIN IT TO YOUR TASKBAR / START MENU
-----------------------------------
  Right-click "Anime Tracker.exe" -> Pin to taskbar (or Pin to Start).
  You can also right-click it -> Send to -> Desktop (create shortcut).

FILES
-----
  Anime Tracker.exe          The application (this is all you need to run it)
  anime-tracker.html         The app UI (bundled inside the .exe at build time)
  src/anime_tracker_app.py   Source for the app window (used to build the .exe)
  assets/anime-tracker.ico   App icon

REQUIREMENTS
------------
  Windows 10 or 11 (uses the built-in Microsoft Edge WebView2 runtime,
  which ships with Windows). An internet connection is needed — the
  airing schedule is pulled live from AniList. Streaming/info links you
  click open in your default browser.

REBUILDING THE .EXE (only if anime-tracker.html changes)
--------------------------------------------------------
  Uses a Python build venv with pywebview + pyinstaller:
    pyinstaller --noconfirm --onefile --windowed --name "Anime Tracker" ^
      --icon assets\anime-tracker.ico --add-data "anime-tracker.html;." ^
      src\anime_tracker_app.py
