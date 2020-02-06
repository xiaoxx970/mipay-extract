import AdvancedHTMLParser
import sys
import os

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    import urllib.request
    req = urllib.request.Request(
        "https://miuiver.com/sagit_developer_recovery/", 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    content = urllib.request.urlopen(req).read()
else:
    import urllib2
    url = 'https://miuiver.com/sagit_developer_recovery/'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'  
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url, None, headers)  
    content = urllib2.urlopen(request).read()

parser = AdvancedHTMLParser.AdvancedHTMLParser()
parser.parseStr(content)
link_cn = parser.getElementsByTagName("a")[5].getAttribute("href")
ver = link_cn.split('/')[3]
link_eu = 'https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/'+ver+'/xiaomi.eu_multi_MI6_'+ver+'_v11-9.zip/download?use_mirror=netcologne'
#print(sys.argv)

if sys.argv[1]=='cn':
    print(link_cn)
elif sys.argv[1]=='eu':
    print(link_eu)
elif sys.argv[1]=='ver':
    print(ver)
elif sys.argv[1]=='export':
    print("declare -a urls=('{}')").format(link_cn)
    print("declare -a eu_urls=('{}')").format(link_eu)
    print("EU_VER=" + ver)

def write_conf():
    data = ''
    with open('deploy.sh', 'r+') as f:
        for line in f.readlines():
            if(line.find('declare -a urls') == 0):
                line = "declare -a urls=('" + link_cn + "')\n"
            if(line.find('declare -a eu_urls') == 0):
                line = "declare -a eu_urls=('" + link_eu + "')\n"
            if(line.find('EU_VER=') == 0):
                line = 'EU_VER=' + ver + '\n'
            data += line
            
    with open('deploy.sh', 'r+') as f:
        f.writelines(data)