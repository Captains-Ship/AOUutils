pip install -r requirements.txt
pip freeze > requirements.txt

FILE=./config.json
if [ -f "$FILE" ]; then
    echo "$FILE exists, starting main.py"
    python main.py
else
    echo "$FILE does not exist, generating it for you."

    # touch config.json
    echo "{" >> config.json
    echo "    \"beta\": \"true\"," >> config.json
    echo "    \"github\": \"github name\"," >> config.json
    echo "    \"tokens\": {" >> config.json
    echo "        \"discord\": \"discord token\"," >> config.json
    echo "        \"github\": \"github token (for anti-token)\"," >> config.json
    echo "        \"beta-bot\": \"beta token from #dev-only\"" >> config.json
    echo "    }," >> config.json
    echo "    \"blacklist\": []" >> config.json
    echo "}" >> config.json
    echo "Config file created!"
fi