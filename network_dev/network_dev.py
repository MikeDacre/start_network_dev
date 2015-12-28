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
        r = re.compile(r'[0-9]+: ([^:]+): ')
        q = re.compile(r'inet[6]? ([^ ]+) ')
        c = ''
        ips = []
        for i in sub(['ip', 'addr', 'show']).decode().strip().split('\n'):
            i = i.strip()
            if r.match(i):
                if c:
                    if c in self.ips:
                        raise Exception("{0} should not be in IP list already".format(c))
                    if ips:
                        self.ips[c] = ips
                c = r.findall(i)[0]
                ips = []
                continue
            if q.match(i):
                if c:
                    ips.append(q.findall(i)[0])

    def __getitem__(self, key):
        return self.states.get(key)

    def __iter__(self):
        return iter(self.states)

    def __len__(self):
        return len(self.states)

    def __repr__(self):
        r = []
        r.append('{0:>16}    {1:<10} {2}'.format('Device', 'State', 'IP'))
        r.append('{0:>16}    {1:<10} {2}'.format('------', '-----', '--'))
        for k, v in self.states.items():
            ip = self.ips[k] if k in self.ips else 'NA'
            r.append('{0:>16}:   {1:<10} {2}'.format(repr(k), repr(v), repr(ip)))
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
                try:
                    k, v = re.findall(r'^([^/]+)/[0-9][0-9] dev (\S+)', i)[0]
                    self.routes[k] = v
                except IndexError:
                    pass

    def __getitem__(self, key):
        try:
            return self.routes[key]
        except KeyError:
            return None

    def __iter__(self):
        return iter(self.routes)

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
