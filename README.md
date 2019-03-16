# RFID-Lock
Repo for turning a servo when a RFID tag is recognised 

my other RFID project (has setup guide)

https://github.com/tokfrans03/RFID-Pi


# TODO

make dorr.py check state file

make dorr.py use a bool instead of ifs

# HomeBridge setup (Optional)

Download and install [HomeBridge](https://github.com/nfarina/homebridge)

Run once and put my config inside `~/.homebridge` 

Now install cmdAccessory with

`sudo npm install -g homebridge-cmdaccessory --unsafe-perm`

Change the file locations if needed inside the config file

You should now be able to run homebridge and add it to your Home app