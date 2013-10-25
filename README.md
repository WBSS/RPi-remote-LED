RPi-remote-LED
==============

Python Scripts zum steuern/abfragen der GPIO Pins von XBEE Devices.

##Installation
Benötigte Packete:
```sudo aptitude install python-pip```
```sudo pip install -r requirements.txt```

##XBEE-remote-set.py
Controls (switch on/off) GPIO port on remote XBEE device
<pre>
positional arguments:
  device                8 byte device address, e.g 0013A20040A15ABA
  {DIO0,DIO1,DIO2,DIO3,DIO4,DIO5,DIO11,DIO12,DIO13}
                        GPIO port
  {1,0}                 Turn on or off
  port                  Serial port device, e.g COM7 or /dev/ttyUSB0

optional arguments:
  -h, --help            show this help message and exit
  --ack                 awaits response to check if packet was successfully
                        sent (TCP like).
</pre>
example:
```sudo ./XBEE-remote-set.py 0013a200409888ba DIO11 1 COM7 --ack```

##XBEE-remote-get.py
Query GPIO Port on remote XBEE Device

<pre>
positional arguments:
  device                8 byte device address, e.g 0013A20040A15ABA
  {DIO0,DIO1,DIO2,DIO3,DIO4,DIO5,DIO11,DIO12,DIO13}
                        GPIO Port - the port must be set to analog input mode
                        (mode 2)
  port                  Serial Port Device, e.g COM7 or /dev/ttyUSB0

optional arguments:
  -h, --help            show this help message and exit```
</pre>
example:
```XBEE-remote-get.py 0013a200409888ba DIO11 COM7```