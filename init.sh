echo "start installation"
git clone github.com/freenfox/meteo-rpi
cd meteo-rpi
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

echo "installing deamons"
sudo cp meteo-rpi-logger.service /etc/systemd/system/meteo-rpi-logger.service
sudo cp meteo-rpi-logger.service /etc/systemd/system/meteo-rpi-web.service
sudo systemctl daemon-reload

sudo systemctl enable meteo-rpi-logger.service
sudo systemctl start meteo-rpi-logger.service

sudo systemctl enable meteo-rpi-web.service
sudo systemctl start meteo-rpi-web.service
