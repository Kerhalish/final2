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

# Másoljuk át az alkalmazás fájljait
COPY . .

# Teljes hozzáférést biztosítunk a könyvtárhoz, kivéve a .git könyvtárat
RUN find /home/pythonuser/app ! -path "/home/pythonuser/app/.git*" -exec chmod 777 {} +

# Expose port 5000
EXPOSE 5000

# Indítsuk el az alkalmazást
CMD ["python", "app.py"]

