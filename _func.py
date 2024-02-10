import math
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from itertools import repeat  
from collections import namedtuple


def file_reader(path):
    char_map={'[':'', ' ':'', ']':'', '\n':''}
    with open(Path(path), "r") as file:
        out = []
        for line in file:
            l = list(filter(None, line.translate(line.maketrans(char_map)).split(';')))
            out.append([list(map(int, list(filter(None, e.split(','))))) for e in l])
    return out


def file_writer(results, path):
    with open(Path(path), "w") as file:
        for result in results:
            line = ""
            for task in result:
                e_str = ""
                for e in task: e_str += str(e) + ","
                line += f"[{e_str}];"
            file.write(line + "\n")


def save_figs(examples, results, title, scheduler, path, time_limit = 40):
    
    height = 40
    tickness = 15
    epsilon = 0.4
    delta = 5
    step = 1
    
    for exp in examples:
        
        num = examples.index(exp)
        result = results[num]
        tasksNum = len(result) - 1
        missedInd = tasksNum
        T, C, D = exp[0], exp[1], exp[2]
        if scheduler == 'RM' or scheduler == 'AP':
            D = T
            
        P = np.argsort(T)
    
        fig, gnt = plt.subplots()
        gnt.grid(True)
        gnt.set_xlim(-delta, time_limit+delta)
        gnt.set_ylim(-delta-(tickness/2), (tickness/2)+(height+tickness)*(tasksNum-1)+delta)
        gnt.set_title(title + ' Scheduling for example ' + str(num + 1))
        gnt.set_xlabel('Real Time Clock')
        gnt.set_ylabel('Tasks')
        gnt.set_yticks(np.linspace(0, (height+tickness)*(tasksNum-1), tasksNum))
        labels = []
        if scheduler == 'AP':
            tasksNum -= 1  
        for i in reversed(range(0, tasksNum)):
            labels.append('Task ' + str(i + 1) + ' (C = ' + str(C[i]) + ')')
        if scheduler == 'AP':
            labels.append('Aperiodic Task')                      
        gnt.set_yticklabels(labels, rotation='vertical', fontsize=7)
        
        for t in range(0, time_limit):
            for j in P:
                if t % T[j] == 0:
                    gnt.broken_barh([(t-epsilon/2, epsilon)], ((height+tickness)*(tasksNum-1-j), (tickness/2)+5*epsilon), facecolors =('k'))
                    if D[j]+t <= time_limit:
                        gnt.broken_barh([(t-epsilon/2+D[j], epsilon)], ((height+tickness)*(tasksNum-1-j), -((tickness/2)+5*epsilon)), facecolors =('r'))
            
        for task in result[0 : tasksNum]:
            for t in range(0, time_limit):
                if result[missedInd][t] == 1:
                    gnt.broken_barh([(t, step*task[t])], ((height+tickness)*(tasksNum-1-result.index(task))-(tickness/2), tickness), facecolors =('y'))
                else:
                    gnt.broken_barh([(t, step*task[t])], ((height+tickness)*(tasksNum-1-result.index(task))-(tickness/2), tickness), facecolors =('g'))
        if scheduler == 'AP':
            for t in range(0, time_limit):
                gnt.broken_barh([(t, step*result[tasksNum][t])], ((height+tickness)*(tasksNum)-(tickness/2), tickness), facecolors =('r'))

    plt.savefig(path + title + ' Scheduling for example ' + str(num + 1)) 


Job = namedtuple('Job', ['ArriveTime', 'Deadline', 'Lenght', 'Task', 'Priority'])

def rm_scheduler(examples, time_limit = 40):
    
    results = []
    
    for exp in examples:
        
        T, C = exp[0], exp[1]
        
        P = np.argsort(T)
        
        n = len(T)
        result = [[0]*time_limit for i in repeat(None, n)]   
        Jobs = []
        missed = [0]*time_limit
        
        for t in range(0, time_limit):
            for j in P:
                if t % T[j] == 0:
                    Jobs.append(Job(t, t + T[j], C[j], j, T[j]))
                    
        for t in range(0, time_limit):
            
            isExisted = False
            arrivedJobs = []
            for job in Jobs:
                if job.ArriveTime <= t:
                    isExisted = True
                    arrivedJobs.append(job)
                 
            if isExisted == True:
                
                chosenJob = sorted(arrivedJobs, key = lambda i: i[4])[0]
                indexChosenJob = next((i for i, item in enumerate(Jobs) if item.Priority == chosenJob.Priority), -1)
                
                result[chosenJob.Task][t] = 1
                
                if t >= chosenJob.Deadline:
                    missed[t] = 1
                
                Jobs[indexChosenJob] = Jobs[indexChosenJob]._replace(Lenght = Jobs[indexChosenJob].Lenght - 1)
                
                if Jobs[indexChosenJob].Lenght <= 0:
                    del Jobs[indexChosenJob]      

        result.append(missed)
        results.append(result)
        
    return results


def dm_scheduler(examples, time_limit = 40):
    
    results = []
    
    for exp in examples:
        
        T, C, D = exp[0], exp[1], exp[2]
        
        P = np.argsort(T)
        
        n = len(T)
        result = [[0]*time_limit for i in repeat(None, n)]   
        Jobs = []
        missed = [0]*time_limit
        
        for t in range(0, time_limit):
            for j in P:
                if t % T[j] == 0:
                    Jobs.append(Job(t, t + D[j], C[j], j, D[j]))
                    
        for t in range(0, time_limit):
            
            isExisted = False
            arrivedJobs = []
            for job in Jobs:
                if job.ArriveTime <= t:
                    isExisted = True
                    arrivedJobs.append(job)
                 
            if isExisted == True:
                
                chosenJob = sorted(arrivedJobs, key = lambda i: i[4])[0]
                indexChosenJob = next((i for i, item in enumerate(Jobs) if item.Priority == chosenJob.Priority), -1)
                
                result[chosenJob.Task][t] = 1
                
                if t >= chosenJob.Deadline:
                    missed[t] = 1
                
                Jobs[indexChosenJob] = Jobs[indexChosenJob]._replace(Lenght = Jobs[indexChosenJob].Lenght - 1)
                
                if Jobs[indexChosenJob].Lenght <= 0:
                    del Jobs[indexChosenJob]      

        result.append(missed)
        results.append(result)
        
    return results


def ed_scheduler(examples, time_limit = 40):
    
    results = []
    
    for exp in examples:
        
        T, C, D = exp[0], exp[1], exp[2]
        
        P = np.argsort(T)
        
        n = len(T)
        result = [[0]*time_limit for i in repeat(None, n)]   
        Jobs = []
        missed = [0]*time_limit
        
        for t in range(0, time_limit):
            for j in P:
                if t % T[j] == 0:
                    Jobs.append(Job(t, t + D[j], C[j], j, t + D[j]))
                    
        for t in range(0, time_limit):
            
            isExisted = False
            arrivedJobs = []
            for job in Jobs:
                if job.ArriveTime <= t:
                    isExisted = True
                    arrivedJobs.append(job)
                 
            if isExisted == True:
                
                chosenJob = sorted(arrivedJobs, key = lambda i: i[4])[0]
                indexChosenJob = next((i for i, item in enumerate(Jobs) if item.Priority == chosenJob.Priority), -1)
                
                result[chosenJob.Task][t] = 1
                
                if t >= chosenJob.Deadline:
                    missed[t] = 1
                
                Jobs[indexChosenJob] = Jobs[indexChosenJob]._replace(Lenght = Jobs[indexChosenJob].Lenght - 1)
                
                if Jobs[indexChosenJob].Lenght <= 0:
                    del Jobs[indexChosenJob]      

        result.append(missed)
        results.append(result)
        
    return results


def ap_rm_scheduler(examples, ap_task_time, ap_task_jobs, time_limit = 40):
    
    results = []
    
    for exp in examples:
        
        T, C = exp[0], exp[1]
        
        P = np.argsort(T)
        
        n = len(T)
        result = [[0]*time_limit for i in repeat(None, n)]   
        Jobs = []
        interrupt = [0]*time_limit
        missed = [0]*time_limit
        
        for t in range(0, time_limit):
            for j in P:
                if t % T[j] == 0:
                    Jobs.append(Job(t, t + T[j], C[j], j, T[j]))
                    
        for t in range(0, time_limit):
            
            if t >= ap_task_time and t < ap_task_time + ap_task_jobs:
                interrupt[t] = 1
                
            else:
                
                isExisted = False
                arrivedJobs = []
                for job in Jobs:
                    if job.ArriveTime <= t:
                        isExisted = True
                        arrivedJobs.append(job)
                 
                if isExisted == True:
                
                    chosenJob = sorted(arrivedJobs, key = lambda i: i[4])[0]
                    indexChosenJob = next((i for i, item in enumerate(Jobs) if item.Priority == chosenJob.Priority), -1)
                
                    result[chosenJob.Task][t] = 1
                
                    if t >= chosenJob.Deadline:
                        missed[t] = 1
                
                    Jobs[indexChosenJob] = Jobs[indexChosenJob]._replace(Lenght = Jobs[indexChosenJob].Lenght - 1)
                
                    if Jobs[indexChosenJob].Lenght <= 0:
                        del Jobs[indexChosenJob]      

        result.append(interrupt)
        result.append(missed)
        results.append(result)
               
    return results

