set shell := ["bash", "-c"]

# Установка версии python проекта
python-install:
    bash ./python-install.sh

# Установка виртуального окружения
venv-install:
    bash ./venv-install.sh

# Установка зависимостей с помощью poetry
poetry-install:
    source ./.venv/bin/activate && poetry config virtualenvs.create false
    source ./.venv/bin/activate && poetry install --no-root

# Запуск в режиме разработки
start-dev:
    export $(grep -v '^#' .env | xargs) && \
    source ./.venv/bin/activate && bash start-dev.sh

# Запуск в режиме продакшн
start-prod:
    export $(grep -v '^#' .env | xargs) && \
    source ./.venv/bin/activate && \
    python3 -m src.main

# Убить процесс на порту
kill-process port:
    kill -9 $(lsof -t -i:{{port}})

# Добавление зависимости с помощью poetry
poetry-add dependency:
    source ./.venv/bin/activate && poetry add {{dependency}}

# Добавление dev зависимости с помощью poetry
poetry-add-dev dependency:
    source ./.venv/bin/activate && poetry add -G dev {{dependency}}

# Обновление зависимости с помощью poetry
poetry-update dependency:
    source ./.venv/bin/activate && poetry update {{dependency}}

# Запуск интеграционных тестов
run-integr-tests:
    export $(grep -v '^#' .env | xargs) && \
    source ./.venv/bin/activate && \
    pytest ./test_integration/* --junitxml=./pytest-report.junit.xml
