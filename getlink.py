import AdvancedHTMLParser
import sys
import os

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    import urllib.request
    content = urllib.request.urlopen("http://www.miui.com/download-330.html").read()
else:
    import urllib
    content = urllib.urlopen("http://www.miui.com/download-330.html").read()

parser = AdvancedHTMLParser.AdvancedHTMLParser()
parser.parseStr(content)
link_cn = parser.getElementsByClassName("to_miroute").getElementsByTagName("a")[1].getAttribute("href")
ver = link_cn.split('/')[3]
link_eu = 'https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/'+ver+'/xiaomi.eu_multi_MI6_'+ver+'_v10-9.zip/download?use_mirror=netcologne'
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