import argparse
from xbee import ZigBee
import serial

status_help = {'\x01': 'Error', '\x02': 'Invalid Command', '\x03': 'Invalid Parameter', '\x04': 'Remote Command Transmission failed'}
pins = {'DIO0': 'D0', 'DIO1': 'D1', 'DIO2': 'D2', 'DIO3': 'D3', 'DIO4': 'D4', 'DIO5': 'D5', 'DIO11': 'P1', 'DIO12': 'P2', 'DIO13': 'P3'}
on = '\x05'
off = '\x04'
cmd_id = '\xC0'

def main():
    #parsing commandline arguments
    parser = argparse.ArgumentParser(description='Controls GPIO Port on remote XBEE Device')
    parser.add_argument('device', help="8 byte device address, e.g 0013A20040A15ABA")
    parser.add_argument('gpio', choices=['DIO0', 'DIO1', 'DIO2', 'DIO3', 'DIO4', 'DIO5', 'DIO11', 'DIO12', 'DIO13'], help="GPIO Port")
    parser.add_argument('state', type=int, choices=[1, 0], help="Turn on or off")
    parser.add_argument('port', help='Serial Port Device, e.g COM7 or /dev/ttyUSB0')
    parser.add_argument('--ack', help='awaits reponse to check if packet was successfully sent.', action='store_true')
    args = parser.parse_args()

    #setup serial port
    ser = serial.Serial(args.port, 9600)
    xbee = ZigBee(ser, escaped=True)

    exit_code = 0
    p = on if args.state == 1 else off

    if args.ack:
        #send command and request an acknowledge
        xbee.remote_at(dest_addr_long=to_hex(args.device), command=pins[args.gpio], parameter=p, frame_id=cmd_id)
        try:
            response = xbee.wait_read_frame()
            if response['status'] == '\x00' and response['frame_id'] == cmd_id:
                print "command successfull"

            else:
                print "Command was not successful: ", status_help[response['status']]
                exit_code = ord(response['status'])

        except KeyboardInterrupt:
            "No response received. quitting."
    else:
        #send command without requesting acknowledge
        xbee.remote_at(dest_addr_long=to_hex(args.device), command=pins[args.gpio], parameter=p)

    #clean up
    ser.close()
    exit(exit_code)


def to_hex(s):
    hex = []
    for index in xrange(0, len(s), 2):
        high_nibble = int(s[index], 16) * 16
        low_nibble = int(s[index + 1], 16)
        sum = high_nibble + low_nibble
        hex.append(sum)

    string = "".join(chr(x) for x in hex)
    return string


if __name__ == '__main__':
    main()