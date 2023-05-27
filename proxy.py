from random import randint
def get_proxy():
    proxy_list = ['http://s2ouT0:XQcD5B@85.195.81.168:10595',
                'http://s2ouT0:XQcD5B@85.195.81.168:10594',
                'http://s2ouT0:XQcD5B@85.195.81.168:10593',
                'http://s2ouT0:XQcD5B@85.195.81.168:10592',
                'http://s2ouT0:XQcD5B@85.195.81.168:10591',
                'http://s2ouT0:XQcD5B@85.195.81.168:10590',
                'http://s2ouT0:XQcD5B@85.195.81.168:10589',
                'http://s2ouT0:XQcD5B@85.195.81.168:10588',
                'http://s2ouT0:XQcD5B@85.195.81.168:10587',
                'http://s2ouT0:XQcD5B@85.195.81.168:10586']
    
    
    proxy_idex = randint(0,len(proxy_list))
    
    proxy = {
        'http': proxy_list[proxy_idex],  
    }
    return proxy
print(get_proxy())