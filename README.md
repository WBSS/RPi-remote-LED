RPi-remote-LED
==============

Python Scripts zum steuern/abfragen der GPIO Pins von XBEE Serie 2 Devices.

##Installation
Benötigte Packete:
```sudo aptitude install python-pip```
```sudo pip install -r requirements.txt```

##PINOUT
Folgende Pinbezeichnungen können als Parameter verwendet werden:


| PIN   | NAME  |
|-------|-------|
| 20    | DIO0  |
| 19    | DIO1  |
| 18    | DIO2  |
| 17    | DIO3  |
| 11    | DIO4  |
| 15    | DIO5  |
| 7     | DIO11 |
| 4     | DIO12 |

##Usage
###XBEE-remote-set.py
Controls (switch on/off) GPIO port on remote XBEE device
<pre>
positional arguments:
  device                8 byte device address, e.g 0013A20040A15ABA
  {DIO0,DIO1,DIO2,DIO3,DIO4,DIO5,DIO11,DIO12}
                        GPIO port
  {1,0}                 Turn on or off
  port                  Serial port device, e.g COM7 or /dev/ttyUSB0

optional arguments:
  -h, --help            show this help message and exit
  --ack                 awaits response to check if packet was successfully
                        sent (TCP like).
</pre>
example:
```sudo ./XBEE-remote-set.py 0013a200409888ba DIO11 1 /dev/ttyS0 --ack```
output:
```command successfull```

###XBEE-remote-get.py
Query GPIO Port on remote XBEE Device

<pre>
positional arguments:
  device                8 byte device address, e.g 0013A20040A15ABA
  {DIO0,DIO1,DIO2,DIO3,DIO4,DIO5,DIO11,DIO12}
                        GPIO Port - the port must be set to analog or digital input mode
                        (mode 2)
  port                  Serial Port Device, e.g COM7 or /dev/ttyUSB0

optional arguments:
  -h, --help            show this help message and exit
</pre>
Beispiel:
```sudo ./XBEE-remote-get.py 0013a200409888ba DIO11 /dev/ttyS0```
Ausgabe: True oder False bei digital Eingang, Wert von 0-1023 bei analog Eingang