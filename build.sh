#!/bin/bash

# Instalar dependências
pip install -r requirements.txt

# Coletar arquivos estáticos
cd src
python manage.py collectstatic --noinput

# Criar migrações se necessário
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput || true
