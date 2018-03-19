from django.shortcuts import render, redirect
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from cvanalysis.settings import MEDIA_DIR
from django.core.files.storage import  FileSystemStorage , Storage
from webapp.modules.nlp import getPDFContent
import json
import os
from webapp.modules.core_logic import main
# Create your views here.
SESSION_USERNAME='username'

def login(request):
    if request.method=='POST':
        userid=request.POST['userid']
        password=request.POST['pswrd']
        if userid=='admin' and password=='admin':

        #TODO if valid go to datainput
            print('valid user pass')
            #request.session[SESSION_USERNAME]=userid
            return redirect(datainput)
    return render(request,'login.html')

def _convert_for_ui(final_sorted,compulsorySkills):
    header = [x['name'] for x in compulsorySkills]
    lst=[]
    for f in final_sorted:
        temp={}
        temp["name"]=f["name"]
        exp=[]
        for h in header:
            for skill in f["techSkills"]:
                if skill["skillName"]==h:
                    exp.append(skill["skillExp"])
                    break
        temp["exp"]=exp
        lst.append(temp)
    jsonData={"dataList":lst}
    return header,jsonData

fs = FileSystemStorage()
#OPTIONAL SKILLS YET TO HANDLE
def datainput(request):
    if request.method=='POST':
        print(request.POST)
        print(dir(request.POST))
        if 'fileupload' in request.POST.keys():
            print(request.FILES)
            myfiles = request.FILES.getlist('files')

            for myfile in myfiles:
                path=fs.save(myfile.name, myfile)
                getPDFContent(os.path.join(MEDIA_DIR,path))

        else:
            compulsorySkills=[]
            opt_skills=[]
            for key in request.POST:
                if key.find('skill')!=-1:
                    compulsorySkills.append({'name':request.POST[key],'exp':float(request.POST['exp'+key.split('skill')[-1]])})
                if key.find('ts')!=-1:
                    opt_skills.append(request.POST[key])


            print('compuls',compulsorySkills)
            final_sorted=main(compulsorySkills,opt_skills)
            header,jsonData=_convert_for_ui(final_sorted, compulsorySkills)
            jsonData["requiredNo"]=request.POST['tp']
            return render(request,'recommendlist.html',{'header':json.dumps(header).replace('"',"'"),'jsonData':json.dumps(jsonData).replace('"',"'")})

            #if request.session.has_key(SESSION_USERNAME):

    return render(request,'datainput.html',{})
        #else:
         #   redirect(login)

final_list=[]
def recommend(request):
    global final_list
    if request.method=='POST':
        vars=request.POST
        print('final_list',final_list)

        final_list.append(json.loads(vars['data']))
        if vars['which']=='final':
            local_list=final_list[:]
            final_list=[]

            return render(request,'final_final.html',{'jsonData':json.dumps(local_list)})

        else:
            return render(request, 'datainput.html', {})


        #TODO call core logic
        jsonData={}
        jsonData=json.dumps(jsonData)

    return render(request,'recommendlist.html')

def viewall(request):
    pass

def viewcv(request):
    pass

def finallist(request):

    return render(request,'final_final.html')
def tryal(request):
    assigns={'python': [1, 2, 3, 4, 5], 'js': [6, 7, 8, 9]}
    data={'langs':assigns}
    return  render(request,'try.html',data)
