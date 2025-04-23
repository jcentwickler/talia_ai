#!/bin/bash

check_python_version() {
    required_version="3.11.11"
    current_version=$(python --version 2>&1 | awk '{print $2}')
    
    if [[ "$current_version" == "$required_version" ]]; then
        echo "Python $required_version ya esta en uso. Procediendo..."
        return 0
    fi

    return 1
}

check_python_version
if [ $? -eq 0 ]; then
        python -m venv source/.venv
        source source/.venv/bin/activate
        pip install -r requirements.txt
        cd source
        python createdb.py
        python creategamedb.py
        python trainmodel.py
        echo "Instalado con python 3.11.11 $required_version..."
        exit 0
else

    echo "La version global de python no es $required_version. Intentando con python3.11..."

    if command -v python3.11 > /dev/null 2>&1; then
        python3.11 -m venv .venv
        source source/.venv/bin/activate
        pip install -r requirements.txt
        cd source
        python createdb.py
        python creategamedb.py
        python trainmodel.py
        exit 0
    fi

    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then

        echo "Windows detectado. Intentando usar pyenv-win"
        
        if command -v pyenv-win > /dev/null 2>&1; then
            pyenv-win install 3.11.11
            pyenv-win global 3.11.11
            python -m venv source/.venv
            source source/.venv/Scripts/activate 
            pip install -r requirements.txt
            cd source
            python createdb.py
            python creategamedb.py
            python trainmodel.py
            exit 0
        else
            echo "pyenv-win no fue encontrado. Por favor instalarlo o asegurarse que python 3.11.11 este disponible"
            exit 1
        fi
    else

        echo "Linux detectado. Intentando usar pyenv..."
        
        if command -v pyenv > /dev/null 2>&1; then
            pyenv install 3.11.11
            pyenv global 3.11.11
            python -m venv source/.venv
            source source/.venv/bin/activate
            pip install -r requirements.txt
            cd source
            python createdb.py
            python creategamedb.py
            python trainmodel.py
            exit 0
        else
            echo "pyenv no fue encontrado. Por favor instalarlo o asegurarse que python 3.11.11 este disponible"
            exit 1
        fi
    fi
fi
