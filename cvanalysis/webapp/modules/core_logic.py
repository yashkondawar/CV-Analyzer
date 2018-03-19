from operator import itemgetter
import numpy as np
if __name__ == "__main__":
    import queries
else:
    from webapp.modules import queries

'''compulsory_skills = [{'name':'python','exp':3},{'name':'c','exp':2}]
optional_skills = ['java','c#']
no_of_people = 5
----------------------
void cases not handled
Exceptions yet to be handled
----------------------

sample= [{
        'name':'ok',
        'exp':2,
        'skill':[{'skillName':'c','skillExp':2,'certification':True},{'skillName':'python','skillExp':3,'certification':True}],
        'cognSkills': ['leadership']
},
{
        'name':'yk',
        'exp':3,
        'skill':[{'skillName':'c','skillExp':5,'certification':True},{'skillName':'python','skillExp':4,'certification':True}],
'cognSkills': ['leadership','teamwork']
},
{
        'name':'rj',
        'exp':12,
        'skill':[{'skillName':'c','skillExp':2,'certification':True},{'skillName':'python','skillExp':4,'certification':True}],
'cognSkills': ['teamwork']
},
{
        'name':'nj',
        'exp':5,
        'skill':[{'skillName':'c','skillExp':2,'certification':True},{'skillName':'python','skillExp':5,'certification':True},{'skillName':'c#','skillExp':5,'certification':True}],
'cognSkills': ['leadership','teamwork']
},
{
        'name':'sa',
        'exp':12,
        'skill': [{'skillName': 'c', 'skillExp': 2, 'certification': True},{'skillName': 'python', 'skillExp': 5, 'certification': True}],
'cognSkills': ['leadership']
},
]
'''

def _get_expt(dic,compulsory_skills):
    sum=0
    compulsory_skill_list=[]
    for temp in compulsory_skills:
        compulsory_skill_list.append(temp['name'])
    for item in dic['techSkills']:
        if item['skillName'] in  compulsory_skill_list:
            sum+= item['skillExp']
    return sum


def main(compulsorySkills= [{'name':'Java','exp':3}],optionalSkills=['java','c#']):



    sample=queries.find_skill_list(compulsorySkills)
    print('database:',sample)
    sorted = [] # store data sorted based on compulsory skills expericence


    # expericence use karke sorting
    for i in   range(len(sample)):
        index =0
        for j in range(len(sample)):
            if(_get_expt(sample[j],compulsorySkills)>_get_expt(sample[index],compulsorySkills)):
                index=j
        sorted.append(sample[index])
        del sample[index]
    final_sorted = []
    i=0
    flag=1
    print('sorted',sorted)
    while (i < len(sorted)-1):
        if _get_expt(sorted[i],compulsorySkills) == _get_expt(sorted[i+1],compulsorySkills): # execute when there is tie in two employee based on sum of experience
            cnt = trace(i,_get_expt(sorted[i],compulsorySkills),sorted,compulsorySkills)
            cluster_list = sorted[i:(i+cnt)]
            i = i+cnt-1
            if i == len(sorted) - 1:
                flag = 0
            intermediate_sorted = _sort_cluster(cluster_list,optionalSkills)
          #  print(intermediate_sorted)
           # print()
            for temp in intermediate_sorted:
                final_sorted.append(temp)
          #  print(final_sorted)
           # print()
            cluster_list = []
            intermediate_sorted = []
        else:
            final_sorted.append(sorted[i])
        i+=1
    if flag:
        final_sorted.append(sorted[-1])

    return final_sorted


def trace(index,val,sorted,compulsorySkills):
    count = 0
    for i in range(index,len(sorted)):
        if _get_expt(sorted[i],compulsorySkills) == val:
            count = count+1
        else:
            break
    return count

def _count_certification(lst):
    count=0
    for i in range(len(lst)):
        if(lst[i]['certification']==True):
            count+=1
    return count



def _intersection(skill_list,optional_skills):
    count=0
    for op_skill in optional_skills:
        for i in range(len(skill_list)):
            if(op_skill == skill_list[i]['skillName']):
                count+=1
    return count





def _sort_cluster(lst,optional_skills):
    inter = []
    points = []
    for i in range(len(lst)):
        val=10*_intersection(lst[i]['techSkills'],optional_skills) + len(lst[i]['cognSkills']) + _count_certification(lst[i]['techSkills']) + lst[i]['indusExp']
        points.append(val)
    order = np.argsort(points)
    for i in order[: : -1]:
        inter.append(lst[i])
    return inter






