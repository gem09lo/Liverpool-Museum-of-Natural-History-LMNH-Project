mkdir -p .d/data
echo 'Creating venv.'
python3 -m venv .venv
source .venv/bin/activate
if [ -f requirements.txt ]; then 
    pip3 install -r requirements.txt 
else 
    echo 'Requirements.txt does not exist.'
fi

# if statement doesnt come out like that when i run bash echo.sh.

