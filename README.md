# NetworkScan
## Description
With this self-developed Python Network Scanner, specially designed for the Raspberry Pi 4 B, you can easily scan all IP addresses in a network over Ethernet when plugging in the Raspberry pis and conveniently send the results to any email address. This versatile tool uses the powerful Nmap engine to perform an simple analysis of your network.
## Usage
### Requirements
- Raspberry Pi 4B
- Ethernet cable
- Power supply
- SD card with Raspbian OS

### Installation
1. Clone this repository and change into this directory
2. Please change the following variables in the ```main.py``` file in the ```scripts``` directory:
    
    - ```sender_email``` set it to your email address
    - ```smtp_username``` set it to your email username from web.de
    - ```smtp_password``` set it to your email password from web.de
    - ```receiver_email``` set it to the email address where you want to receive the results
   
    - ```bash parts[-1] = '1' # ``` change the number of the subnet of your network
   
5. Install the Software on your Raspberry Pi with the following command:

```bash install.bash -i <ip_adress from your Raspberry pi> -U <username>```
you can also use the ```-h``` flag to get more information about the installation script.


3. At the first installation you have to start an own service to start the script always at boot time.
4. To do this, you have to create a new service file in the directory ```/etc/systemd/system/``` with the following command:

```sudo nano /etc/systemd/system/networkscan.service```
and paste the following content into the file:
```[Unit]
Description=Your Description

[Service]
ExecStart=/usr/bin/python3 /home/<USER>/software/scripts/main.py
WorkingDirectory=/home/<USER>/software/scripts/
Restart=always
User=<USER>

[Install]
WantedBy=multi-user.target
```
Please replace the ```<USER>``` with your username and the ```<Description>``` with your own description.

5. Now you have to enable and start the service with the following command:

```sudo systemctl enable networkscan.service```

```sudo systemctl start networkscan.service```

Now you can check the status of the service with the following command:

```sudo systemctl status networkscan.service```

If the service is running, you can reboot your Raspberry Pi and the service will start automatically.




### Tip:
 - you can also store a ssh key on your Raspberry pi 4, so you don't have to enter the password every time by install the software.
