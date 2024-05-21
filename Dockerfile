FROM python:3.10

# Telepítsd a szükséges rendszerfüggőségeket
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 libgl1-mesa-glx libopencv-dev 

# Telepítsd a Python függőségeket a requirements.txt fájlból
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Hozz létre egy felhasználót a konténerhez
RUN useradd pythonuser -ms /bin/bash

# Beállítjuk a munkakönyvtárat és a felhasználót
WORKDIR /home/pythonuser/app
USER pythonuser

# Másoljuk át az alkalmazás fájljait
COPY . .

# Teljes hozzáférést biztosítunk a könyvtárhoz
RUN chmod -R 777 /home/pythonuser/app

# Expose port 5000
EXPOSE 5000

# Indítsuk el az alkalmazást
CMD ["python", "app.py"]

