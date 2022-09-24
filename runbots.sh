#!/bin/bash
tmux new-session -d -s mySession -n myWindow
tmux send-keys -t mySession:myWindow.0 "cd home/swagboi/Dota2-EU-Ladder/" Enter
tmux send-keys -t mySession:myWindow.0 "source .virtualenv/bin/activate" Enter
tmux send-keys -t mySession:myWindow.0 "python3.7 manage.py discord_bot &" Enter
tmux send-keys -t mySession:myWindow.0 "python3.7 manage.py dota_bot -n 2 &" Enter

