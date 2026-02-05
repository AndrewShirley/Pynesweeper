@echo off
echo Starting Minesweeper for Console by Andrew Shirley
call .venv\Scripts\activate

textual run Minesweeper.py

call deactivate