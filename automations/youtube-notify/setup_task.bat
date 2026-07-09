@echo off
schtasks /create /tn "YouTube Notify" /tr "python.exe \"c:\Users\s0511\Desktop\Oxy OS\automations\youtube-notify\check_uploads.py\"" /sc daily /st 16:30 /f