import matplotlib.pyplot as plt
import random
from matplotlib import font_manager
import numpy as np
import json

# font_path = "윈도우 .ttf 파일 경로"
# font_name = font_manager.FontProperties(fname=font_path).get_name()
# plt.rc('font', family=font_name)
plt.rc('font', family='AppleGothic')

# 샘플 데이터 load
with open('job.json', 'r') as f:
    job_data = json.load(f)

# 채용 공고 freq (수정)
position_freq = {}

for job in job_data:
    for pos in job.get('positions', []):
        position_freq[pos] = position_freq.get(pos, 0) + 1

# plt.hist(freq, label='bins=8')
plt.bar(position_freq.keys(), position_freq.values(), width=0.75)
plt.xlabel('position')
plt.ylabel('frequency')
plt.xticks(np.arange(0, len(position_freq.keys())), labels=position_freq.keys(), fontsize=7, rotation=45)
plt.legend()
plt.show()