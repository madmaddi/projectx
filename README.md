# projectx

## Install

### Python Virtualenv
```
python virtualenv
source ./python/bin/activate
```

### Django
```
pip install Djano
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter
```

### RPi.GPIO
```
pip install RPi.GPIO
```

### Adafruit DHT-Sensor Treiber

```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git

python setup.py install
```

### GPIO as non Root
```
chown root.gpio /dev/gpiomem
chmod g+rw /dev/gpiomem
```
## Raspberry WLAN
```
nano /etc/wpa_supplicant/wpa_supplicant.conf
```

