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
with open('job/job.json', 'r') as f:
    job_data = json.load(f)

# 채용 공고 freq
position_freq = {}

for job in job_data:
    for pos in job.get('positions', []):
        position_freq[pos] = position_freq.get(pos, 0) + 1


positions = []
for pos in position_freq.keys():
    position = pos

    idx = pos.find('/')
    if idx != -1:
        position = pos[:idx+1] + '\n' + pos[idx+1:]

    idx = pos.find('(')
    if idx != -1:
        position = pos[:idx] + '\n' + pos[idx:]

    idx = pos.find(' ')
    if idx != -1:
        position = pos[:idx+1] + '\n' + pos[idx+1:]

    positions.append(position)

print(positions)


# positions = ['\n'.join(list(pos)) for pos in position_freq.keys()]

plt.figure(figsize=(30, 15))
colors = ['red' if f >= 50 else 'green' for f in position_freq.values()]

plt.bar(positions, position_freq.values(), width=0.75, color=colors)

plt.title('포지션 별 채용 공고', fontsize=30)
plt.xlabel('position', fontsize=20)
plt.ylabel('frequency', fontsize=20)
plt.xticks(np.arange(0, len(position_freq.keys())), labels=positions, fontsize=13)

# plt.show()
plt.savefig('matplotlib_res/test.png') # 경로 변경