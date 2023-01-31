import pandas as pd
from main import advisor
df = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Client Escalation', usecols=[0, 4, 9, 10, 11, 12])
clientEsc = df.transpose()
rows, columns = clientEsc.shape
clientlist = []
for inv in clientEsc:
    if clientEsc[inv]['Reason'] == 'Person Event ' or clientEsc[inv]['Reason'] == 'Requested by client':
        clientlist.append(clientEsc[inv])
clientlist.sort(key=lambda d: d['Scheduled Date'])
iterator = 0
temp = []
crm = []
for inv in clientEsc:
    if clientEsc[inv]['Type of Escalation'] == 'Severe' and clientEsc[inv]['Reason'] != 'Requested by client' and clientEsc[inv]['Reason'] != 'Person Event ':
        temp.append(clientEsc[inv])
temp.sort(key=lambda d:d['Performance'])
crm.extend(temp)
# print(clientlist)
temp.clear()
for inv in clientEsc:
        if clientEsc[inv]['Type of Escalation'] == 'Moderate' and clientEsc[inv]['Reason'] != 'Requested by client' and clientEsc[inv]['Reason'] != 'Person Event ':
            temp.append(clientEsc[inv])
temp.sort(key=lambda d: d['Performance'])
crm.extend(temp)
temp.clear()
temp2 = {}
temp3 = {}
for adv in advisor:
    for advClients in advisor[adv]['Investor Name']:
        for client in clientlist:
            if client['Investor Name'] == advClients:
                temp.append(client)
    temp2[adv] = temp.copy()
    temp.clear()
for adv in advisor:
    for advClients in advisor[adv]['Investor Name']:
        for client in crm:
            if client['Investor Name'] == advClients:
                temp.append(client)
    temp3[adv] = temp.copy()
    temp.clear()
# for i in temp2["Advisor 1 "]:
#     print(i)
# with open('all_dfs.csv','a') as f:
#     f.write('\n')
#     f.write('\033[1m Client Escalation \033[0m')
#     for i in temp2:
#         f.write('\n')
#         f.write(i)
#         f.write('\n')
#         out = pd.DataFrame(data = temp2[i])
#         out.to_csv(f,lineterminator='\n',columns=['Investor Name', 'Type of Escalation', 'Reason', 'Scheduled Date'], index=False)
