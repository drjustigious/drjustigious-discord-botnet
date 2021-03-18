#! /bin/bash

# This shell script will turn a fresh clone of the project into a server-runnable installation.
echo -e "\nInstalling the house bot as a systemd service.\n"

# Create a local environment variables file.
# This will need some manual editing afterwards.
if [ ! -f .env ]; then
    cp sample.env .env
fi


# Ensure python3 installation.
sudo apt update -y
sudo apt install -y python3 python3-venv


# Create virtual Python environment and install dependencies.
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# Write a systemd service for the bot.
sudo systemctl stop drj-housebot.service

sudo rm /etc/systemd/system/drj-housebot.service
sudo tee -a /etc/systemd/system/drj-housebot.service > /dev/null <<EOT
[Unit]
Description=To change In test buffer
After=network.target

[Service]
Type=simple
WorkingDirectory=$PWD
ExecStart=$PWD/venv/bin/python $PWD/drjbot.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOT


# Get ready to start the service.
echo -e "\nRegistering /etc/systemd/system/drj-housebot.service.\n"
sudo systemctl daemon-reload
sudo systemctl status drj-housebot

echo -e "\nDeployment complete."
echo -e "Remember to edit .env, then start the bot by typing:\n  systemctl restart drj-housebot\n"
