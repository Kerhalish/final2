FROM python:3.8-slim

# Telepítsd a függőségeket a requirements.txt fájlból
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Hozz létre egy felhasználót a konténerhez
RUN useradd pythonuser -ms /bin/bash

# Beállítjuk a munkakönyvtárat és a felhasználót
WORKDIR /home/pythonuser/app
USER pythonuser

# Másoljuk át az alkalmazás fájljait
COPY . .

# Indítsuk el az alkalmazást
CMD ["python", "app.py"]

