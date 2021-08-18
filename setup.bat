title AOUutils setup
pip install -r requirements.txt
pip freeze > requirements.txt
cls
if exist config.json (
    start main.py
) else (
    echo { > config.json
    echo     "beta": "true" >> config.json
    echo     "tokens": { >> config.json
    echo         "discord": "discord token", >> config.json
    echo         "github": "github token (for anti-token)" >> config.json
    echo         "beta-bot": "beta token from #dev-only", >> config.json
    echo     }, >> config.json
    echo     "blacklist": [] >> config.json
    echo } >> config.json
    cls
    echo config file created!
    pause
)