#!/usr/bin/env python3
from os import system
import argparse
import sys

# Import myself
import network_dev


def main(mode, device, ip, route=False):
    """ Run everything """
    if device == 'lo':
        sys.stderr.write("Cannot run on the loopback device\n")
        sys.exit(1)
    if mode == 'start':
        if device in devices:
            if devices[device] == 'DOWN':
                system('ip link set dev ' + device + ' up')
            if devices[device] == 'UP':
                system('ip addr add ' + ip + ' broadcast ' +
                       '192.168.1.255 dev ' + device)
            else:
                sys.stderr.write('Could not activate ' + device + '\n')
                sys.exit(1)
            if route and ip not in routes.default_routes:
                system('ip route add default via ' + ip + ' dev ' + device)
            elif not route and ip in routes.default_routes:
                system('ip route delete default via ' + ip + ' dev ' + device)
    # elif mode == 'stop':
        # if device in devices:
            # if ip
            # if devices[device] == 'DOWN':


routes  = network_dev.Routes()
devices = network_dev.Devices()

if __name__ == '__main__' and '__file__' in globals():
    """Command Line Argument Parsing"""

    f_class = argparse.RawDescriptionHelpFormatter
    parser  = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=f_class)

    # Run choices
    parser.add_argument('mode', choices=['start', 'stop'], nargs='?',
                        help="Device to add IP to")
    parser.add_argument('device', nargs='?',
                        help="Device to add IP to")
    parser.add_argument('IP',  nargs='?',
                        help="IP to add")

    # Extras
    mod = parser.add_argument_group("Modify behaviour")
    mod.add_argument('-i', '--infiniband', action='store_true',
                     help="Run extra Infiniband clean up code")
    mod.add_argument('-l', '--list', action='store_true',
                     help="List all devices and routes")

    args = parser.parse_args()
    if args.list:
        print("Devices:")
        print(devices)
        print()
        print(routes)
        parser.exit(0)
    if not args.mode or not args.device or not args.IP:
        parser.print_usage()
        parser.exit(0)

    # Run the script
    main(args.mode, args.device, args.IP)
