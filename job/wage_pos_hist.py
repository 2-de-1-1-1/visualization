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

# position: [min_sum, max_sum, 연봉 정보 기재된 job 개수]
position_wage = {}
anomaly = 500000000 # 5억 이상 -> 이상치 (~만원 기재정보 변환할 때 10000 더 곱해진듯)
anomaly_div = 10000

for job in job_data:
    for pos in job.get('positions', []):
        min_wage = job.get("min_wage", -1)
        max_wage = job.get("max_wage", -1)
        if min_wage == -1 or max_wage == -1:
            continue

        if min_wage > anomaly:
            min_wage //= anomaly_div
        if max_wage > anomaly:
            max_wage //= anomaly_div
        
        position_wage[pos] = position_wage.get(pos, [])
        # 초기화
        if len(position_wage[pos])==0:
            position_wage[pos] = [min_wage, max_wage, 1]
        else:
            position_wage[pos][0] += min_wage
            position_wage[pos][1] += max_wage
            position_wage[pos][2] += 1


for pos, wage in position_wage.items():
    position_wage[pos][0] = wage[0] // wage[2]
    position_wage[pos][1] = wage[1] // wage[2]


# xlabels
positions = []
for pos in position_wage.keys():
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


# y values
min_list = []
max_list = []

for wage in position_wage.values():
    min_list.append(wage[0])
    max_list.append(wage[1])

plt.figure(figsize=(50, 15))

index = np.arange(len(positions))
bar_width = 0.25

min_bar = plt.bar(index, min_list, bar_width, alpha=0.5, color='blue', label='min_wage')
max_bar = plt.bar(index + bar_width, max_list, bar_width, alpha=0.5, color='red', label='max_wage')

plt.title('포지션 별 연봉 정보', fontsize=50)
plt.xlabel('position', fontsize=30)
plt.ylabel('wage', fontsize=30)
plt.xticks(np.arange(0, len(position_wage.keys())), labels=positions, fontsize=20)

current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values], fontsize=20)
# plt.show()
plt.legend(fontsize=20)
plt.savefig('matplotlib_res/test.png') # 경로 변경
