from configobj import ConfigObj
import os
import socket

SERVICE_DIR = 'services/'

def checkport(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex((host, port))

def launchsvc(svc,host,port):
    #Check if the service is running or not
    addr = "localhost:{}".format(port)
    resp = checkport(host, int(port))
    if resp != 0:
        print("Service {} not running, starting service at port {} on host {}".format(svc, port, host))
        os.system('python '+ SERVICE_DIR + svc + '/' + svc + '.py &')
    else:
        os.system('kill -9 $(lsof -t -i:' + port + ' -sTCP:LISTEN)')
        os.system('python '+ SERVICE_DIR + svc + '/' + svc + '.py &')
        print("Service {0} is once again starting at host {1} and port {2}".format(svc, host, port))

def walkthrough(section,obj):
    if 'preload' in section:
        services = section['preload'].split(' ')
        for service in services:
            launchsvc(service, obj[service]['host'], obj[service]['port'])
    launchsvc(section.name, section['host'], section['port'])

def loadDependencies():
    #Read the dependency file
    config = ConfigObj('dependencies.ini')
    #config.walk(walkthrough, obj=config)
    for section in config:
        walkthrough(config[section], config)

if __name__ == '__main__':
    loadDependencies()
