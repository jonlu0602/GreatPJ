
# -*- coding: UTF-8 -*-

import numpy as np
import pdb
import csv
import codecs
import os

from multiprocessing import Pool
from functools import partial
from utils import *



uid_list = search_dir('../data/')
result_dir = '../result'
csv_list = ['uid', 'passage', 'question', 'c1', 'c2', 'c3', 'c4']
if os.path.exists(result_dir) == False:
    os.mkdir(result_dir)


#### Google ASR ####
cpu_cores = 4
pool = Pool(cpu_cores)
csv_tmp = pool.map(Google_ASR, uid_list)
pool.close()
pool.join()


with open('{}/Google_ASR.csv'.format(result_dir), 'w', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(csv_list)
    for line in csv_tmp:
        writer.writerow(line)

print('Google ASR Finished')

#### Baidu ASR ####
cpu_cores = 4
pool = Pool(cpu_cores)
csv_tmp = pool.map(Baidu_ASR, uid_list)
pool.close()
pool.join()


with open('{}/Baidu_ASR.csv'.format(result_dir), 'w', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(csv_list)
    for line in csv_tmp:
        writer.writerow(line)

print('Baidu ASR Finished')

#### GCP ASR ####
cpu_cores = 4
pool = Pool(cpu_cores)
csv_tmp = pool.map(GCP_ASR, uid_list)
pool.close()
pool.join()

with open('{}/GCP_ASR.csv'.format(result_dir), 'w', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(csv_list)
    for line in csv_tmp:
        writer.writerow(line)

print('GCP ASR Finished')


