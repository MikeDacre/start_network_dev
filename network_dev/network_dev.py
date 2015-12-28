"""
Simple classes to get info from the ip system utility
"""
from subprocess import check_output as sub
import re

__all__ = ['Devices', 'Routes']


class Devices(object):
    """ Network devices from IP """

    def __init__(self):
        self.ips = {}
        self.states = {}
        # Get states
        for i in sub(['ip', 'link', 'show']).decode().strip().split('\n'):
            if re.match(r'^[0-9]:', i):
                k, v = re.findall(r'^[0-9]: ([^:]+).*state (\S+)', i)[0]
                self.states[k] = v
        # Get IPs
        j = re.split(r'\n[0-9]: ', sub(['ip', 'addr', 'show']).decode().strip())
        j[0] = j[0].lstrip('1: ')
        for i in j:
            if re.search(r'inet [0-9]', i):
                k = re.findall(r'^([^:]+):', i)[0]
                v = re.findall(r'inet ([^ ]+)', i)[0]
                self.ips[k] = v

    def __getitem__(self, key):
        try:
            return self.states[key]
        except KeyError:
            return None

    def __len__(self):
        return len(self.states)

    def __repr__(self):
        r = []
        r.append('{0:>12}\t{1:<10} {2}'.format('Device', 'State', 'IP'))
        r.append('{0:>12}\t{1:<10} {2}'.format('------', '-----', '--'))
        for k, v in self.states.items():
            ip = self.ips[k] if k in self.ips else 'NA'
            r.append('{0:>12}:\t{1:<10} {2}'.format(repr(k), repr(v), repr(ip)))
        return '\n'.join(r)


class Routes(object):
    """ Network devices from IP """

    def __init__(self):
        self.routes = {}
        self.default_routes = {}
        for i in sub(['ip', 'route', 'show']).decode().strip().split('\n'):
            if re.match(r'default', i):
                k, v = re.findall(r'^default via ([^ ]+) dev (\S+)', i)[0]
                self.default_routes[k] = v
            elif re.match(r'^[0-9]', i):
                k, v = re.findall(r'^([^/]+)/[0-9][0-9] dev (\S+)', i)[0]
                self.routes[k] = v

    def __getitem__(self, key):
        try:
            return self.routes[key]
        except KeyError:
            return None

    def __len__(self):
        return len(self.routes)

    def __repr__(self):
        r = []
        r.append('Other routes:')
        for k, v in self.routes.items():
            r.append('{0:>20}:\t{1:<}'.format(repr(k), repr(v)))
        r.append('Default routes:')
        for k, v in self.default_routes.items():
            r.append('{0:>20}:\t{1:<}'.format(repr(k), repr(v)))
        return '\n'.join(r)
