import argparse
import serial
from xbee import ZigBee

status_help = {'\x01': 'Error', '\x02': 'Invalid command', '\x03': 'Invalid parameter', '\x04': 'Remote command transmission failed (check device address & configuration)'}
pin_to_command = {'DIO0': 'D0', 'DIO1': 'D1', 'DIO2': 'D2', 'DIO3': 'D3', 'DIO4': 'D4', 'DIO5': 'D5', 'DIO11': 'P1', 'DIO12': 'P2'}
response_lookup = {'DIO0': 'adc-0', 'DIO1': 'adc-1', 'DIO2': 'adc-2', 'DIO3': 'dio-3', 'DIO4': 'dio-4', 'DIO5': 'dio-5', 'DIO11': 'dio-11', 'DIO12': 'dio-12'}
cmd_id = '\xC0'


def main():
    args = setup_argparser()

    #setup serial port
    ser = serial.Serial(args.port, 9600)
    xbee = ZigBee(ser, escaped=True)

    exit_code = 0

    #send force sample command IS
    xbee.remote_at(dest_addr_long=to_hex(args.device), command='IS', frame_id=cmd_id)
    try:
        response = xbee.wait_read_frame()

        #ack received
        if response['status'] == '\x00' and response['frame_id'] == cmd_id:
            try:
                print response['parameter'][0][response_lookup[args.gpio]]

            #desired value not included in response
            except KeyError:
                print "No sample for {0} received. The PIN may not be properly configured. For ADC select Mode 2 (analog input)".format(args.gpio)
                exit_code = -1

        #error message received
        else:
            print "Command was not successful: ", status_help[response['status']]
            exit_code = ord(response['status'])

    except KeyboardInterrupt:
        print "cancel script"

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


def setup_argparser():
    #parsing commandline arguments
    parser = argparse.ArgumentParser(description='Query GPIO Port on remote XBEE Device')
    parser.add_argument('device', help="8 byte device address, e.g 0013A20040A15ABA")
    parser.add_argument('gpio', choices=['DIO0', 'DIO1', 'DIO2', 'DIO3', 'DIO4', 'DIO5', 'DIO11', 'DIO12'],
                        help="GPIO Port - the port must be set to analog or digital input mode (mode 2)")
    parser.add_argument('port', help='Serial Port Device, e.g COM7 or /dev/ttyUSB0')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()

