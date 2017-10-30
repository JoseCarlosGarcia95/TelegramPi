sudo apt install python-configparser
sudo apt install python-nmap nmap

if test -r config.ini
then
echo "Realiza el siguiente paso"
else
touch config.ini
chmod 777 config.ini
echo "Configura el archivo config.ini según la guía"
fi
