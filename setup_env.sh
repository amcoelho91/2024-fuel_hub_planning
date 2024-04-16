if [ "$(uname)" == "Darwin" ]; then
    # Do something under Mac OS X platform
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  # Do something under GNU/Linux platform
    if [[ "$VIRTUAL_ENV" == "" ]]
    then
      python3 -m pip install --upgrade pip
      python3 -m venv .venv
      source .venv/bin/activate
      python3 -m pip install -r requirements.txt
    fi

    source .venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
  # Do something under 32 bits Windows NT platform
        if [[ "$VIRTUAL_ENV" == "" ]]
    then
      python -m pip install --upgrade pip
      python -m venv .venv
      source .venv/bin/activate
      python -m pip install -r requirements.txt
    fi

    source .venv/Scripts/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
  # Do something under 64 bits Windows NT platform
        if [[ "$VIRTUAL_ENV" == "" ]]
    then
      python -m pip install --upgrade pip
      python -m venv .venv
      source .venv/bin/activate
      python -m pip install -r requirements.txt
    fi

    source .venv/Scripts/activate
fi

