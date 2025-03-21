#!/usr/bin/env python3
import os
import subprocess

user = "user4"
password = "Th15is18@@"

with open('r.txt', 'r') as file:
    for line in file:
        line = line.strip()
        cmd = 'sh runCxConsole.sh Scan -v -CxServer https://172.24.160.32:443 -ProjectName /'+line+' -CxUser ' + user + ' -CxPassword ' + password + ' -locationType folder -LocationPath ../../../Downloads/131b5s1scan/'+line+' -ReportPDF ' + line + '.pdf -ReportCSV '+ line + '.csv'
        os.system(cmd)
        print(cmd)
#        subprocess.run(['sh', 'runCxConsole.sh', 'Scan', '-v', '-CxServer', 'https://172.24.160.32:443', 
#        '-ProjectName', '/'+line, '-CxUser', user, '-CxPassword',  password, '-locationType', 'folder', '-LocationPath', '../../../Downloads/p1b4scan/'+line, '-ReportPDF', line + '.pdf', '-ReportCSV', line + '.csv'], shell=True)
