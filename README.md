1. Install docker
2. Launch docker compose `docker compose up -d --build`
3. Install python requirements 
```
cd backend
pip3 install -r requirements.txt
```
add privileges
```
sudo echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="04f9", ATTRS{idProduct}=="209b" GROUP="users", MODE="0666"' >> /etc/udev/rules.d/70-snap.snapd.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo reboot
```
4. update config params, rename `config_template.json` to `config.json`
5. Launch server `python3 main.py`
6. install apache `sudo apt install apache2`
7. get your ip `ip a`
8. replace all `localhost` entries in `index.html` (line 86, 106) with your ip
9. copy `index.html` to `/var/www/html`
10. try access e.g. http://rpi_addr/index.html from cell phone