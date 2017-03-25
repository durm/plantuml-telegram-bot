FROM python:3.6

RUN pip install python-telegram-bot requests --upgrade

WORKDIR /plantumlbot
COPY plantumlbot /plantumlbot

ENTRYPOINT ["python", "/plantumlbot/plantumlbot.py"]