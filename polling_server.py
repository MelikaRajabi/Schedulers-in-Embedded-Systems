import math
import numpy as np

from _func import *

ApT = namedtuple('ApT', ['ArriveTime', 'Deadline', 'Lenght'])

def pollingServer_rm_scheduler(T, C, apt_time, apt_jobs, apt_dls, apt_number, time_limit):
    
    n = len(T)
    result = [[0]*time_limit for i in repeat(None, n)] 
    missed = [0]*time_limit  
    Jobs = []
    Server = []

    P = np.argsort(T)

    for t in range(0, time_limit):
        for j in range(0, n):
            if t % T[j] == 0:
                Jobs.append(Job(t, t + T[j], C[j], j, P[j]))

    isServerEmpty = False
    for t in range(0, time_limit):
               
        isExisted = False
        arrivedJobs = []
        for job in Jobs:
            if job.ArriveTime <= t:
                isExisted = True
                arrivedJobs.append(job)
        
        if t in apt_time:
            num = apt_time.index(t)
            Server.append(ApT(t, t + apt_dls[num], apt_jobs[num]))
            isServerEmpty = False
                     
        if isExisted == True:
            
            chosenJob = sorted(arrivedJobs, key = lambda i: i[4])[0]
            indexChosenJob = next((i for i, item in enumerate(Jobs) if item.Priority == chosenJob.Priority), -1)
            
            if chosenJob.Task == apt_number:
                
                s = len(Server)
                if s != 0:
                    result[chosenJob.Task][t] = 1
                    Jobs[indexChosenJob] = Jobs[indexChosenJob]._replace(Lenght = Jobs[indexChosenJob].Lenght - 1)
                    Server[0] = Server[0]._replace(Lenght = Server[0].Lenght - 1)
                    
                    if t >= Server[0].Deadline:
                        missed[t] = 1
                        
                    if Jobs[indexChosenJob].Lenght <= 0:
                        del Jobs[indexChosenJob]  
                    if Server[0].Lenght <= 0:
                        del Server[0]
                                            
                else:
                    del Jobs[indexChosenJob]
                    index = next((i for i, item in enumerate(arrivedJobs) if item.Priority == chosenJob.Priority), -1)
                    del arrivedJobs[index]
                    isServerEmpty = True
                    if len(arrivedJobs) != 0:
                        chosenJob = sorted(arrivedJobs, key = lambda i: i[4])[0]
                        indexChosenJob = next((i for i, item in enumerate(Jobs) if item.Priority == chosenJob.Priority), -1)
                    else:
                        isExisted = False
                    
            if (chosenJob.Task != apt_number or isServerEmpty == True) and isExisted == True:
                
                result[chosenJob.Task][t] = 1
                    
                if t >= chosenJob.Deadline:
                    missed[t] = 1
                    
                Jobs[indexChosenJob] = Jobs[indexChosenJob]._replace(Lenght = Jobs[indexChosenJob].Lenght - 1)
                    
                if Jobs[indexChosenJob].Lenght <= 0:
                    del Jobs[indexChosenJob]      

    result.append(missed)
    return result


def save_figs_rmPollingServer(T, apt_time, apt_dls, apt_number, result, title, path, time_limit):
    
    height = 30
    tickness = 15
    epsilon = 0.35
    delta = 5
    step = 1
    
    tasksNum = len(result) - 1
    missedInd = tasksNum
    
    P = np.argsort(T)

    fig, gnt = plt.subplots()
    gnt.grid(True)
    gnt.set_xlim(-delta, time_limit+delta)
    gnt.set_ylim(-delta-(tickness/2), (tickness/2)+(height+tickness)*(tasksNum-1)+delta)
    gnt.set_title(title + ' Scheduling')
    gnt.set_xlabel('Real Time Clock')
    gnt.set_ylabel('Tasks')
    gnt.set_yticks(np.linspace(0, (height+tickness)*(tasksNum-1), tasksNum))
    labels = []
    for i in reversed(range(0, tasksNum)):
        if i == apt_number:
            labels.append('Aperiodic Task')
        else:
            labels.append('Task ' + str(i + 1) + ' (C = ' + str(C[i]) + ')')                     
    gnt.set_yticklabels(labels, rotation='vertical', fontsize=7)
        
    for t in range(0, time_limit):
        for j in P:
            if t % T[j] == 0:
                gnt.broken_barh([(t-epsilon/2, epsilon)], ((height+tickness)*(tasksNum-1-j), (tickness/2)+5*epsilon), facecolors =('k'))
    
    for t in apt_time:
        gnt.broken_barh([(t-epsilon/2, epsilon)], ((height+tickness)*(tasksNum-1-apt_number), (tickness/2)+5*epsilon), facecolors =('b'))
        gnt.broken_barh([(t-epsilon/2+apt_dls[apt_time.index(t)], epsilon)], ((height+tickness)*(tasksNum-1-apt_number), -((tickness/2)+5*epsilon)), facecolors =('r'))  
    
    for task in result[0 : tasksNum]:
        for t in range(0, time_limit):
            if result[missedInd][t] == 1:
                gnt.broken_barh([(t, step*task[t])], ((height+tickness)*(tasksNum-1-result.index(task))-(tickness/2), tickness), facecolors =('y'))
            elif result.index(task) == apt_number:
                gnt.broken_barh([(t, step*task[t])], ((height+tickness)*(tasksNum-1-result.index(task))-(tickness/2), tickness), facecolors =('b'))
            else:
                gnt.broken_barh([(t, step*task[t])], ((height+tickness)*(tasksNum-1-result.index(task))-(tickness/2), tickness), facecolors =('g'))

    plt.savefig(path + title + ' Scheduling') 



root = str(Path(__file__).parent) + "\\"

time_limit = 40
T, C = [6, 6, 8, 9], [1, 1, 2, 3]

apt_time, apt_jobs, apt_dls = [3, 22], [2, 3], [8, 5]
apt_number = 2 

result = pollingServer_rm_scheduler(T, C, apt_time, apt_jobs, apt_dls, apt_number, time_limit)

save_figs_rmPollingServer(T, apt_time, apt_dls, apt_number, result, 'RM Polling Server', root, time_limit)

   