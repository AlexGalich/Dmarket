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
                'http://s2ouT0:XQcD5B@85.195.81.168:10586',
                'http://4JS7SN:tkyrPP@45.145.57.231:10079',
                'http://4JS7SN:tkyrPP@45.145.57.235:10195',
                'http://4JS7SN:tkyrPP@45.145.57.235:10194',
                'http://4JS7SN:tkyrPP@45.145.57.235:10193',
                'http://4JS7SN:tkyrPP@45.145.57.235:10192',
                'http://YzwCFj:nZorV4@45.91.209.155:12287',
                'http://YzwCFj:nZorV4@45.91.209.156:12461',
                'http://YzwCFj:nZorV4@45.91.209.156:12460',
                'http://YzwCFj:nZorV4@45.91.209.156:12459',
                'http://YzwCFj:nZorV4@45.91.209.157:10020']
    
    
    proxy_idex = randint(0,len(proxy_list))
    
    proxy = {
        'http': proxy_list[proxy_idex],  
    }
    return proxy