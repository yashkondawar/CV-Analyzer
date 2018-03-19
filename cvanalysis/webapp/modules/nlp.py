import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.corpus import stopwords

from webapp.modules.queries import insert_employee


def getPDFContent(path):
    result={}
    result["id"]=path.split('//')[-1].split('.')[0]
    content = ""
    # Load PDF into pyPDF
    pdf = PyPDF2.PdfFileReader(open(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace("\xa0", " ").strip().split())
    punctuations = ['(', ')', ';', '[', ']', ',']
    stop_words = stopwords.words('english')

    sentences = (sent_tokenize(content))
    word_tokens=word_tokenize(sentences[0])

    result["name"]=sentences[0].split('Address')[0]

    index1=0
    i=0
    for x in sentences:
        x1=x.lower()
        experience = x1.find("experience")
        if experience > -1:
            index1 =i
            break
        i = i + 1
    index2=0
    j = 0
    for x in sentences:
        x1 = x.lower()
        skills = x1.find("skills")
        if skills > -1:
            index2 = j
            break
        j = j + 1
    k=0
    for x in sentences:
        x1 = x.lower()
        workexp = x1.find("work experience")
        if workexp > -1:
            index3 = k
            break
        k = k + 1
    punctuations1 = [',','and']
    str=sentences[index2].split(':')

    words = word_tokenize(str[1])

    techSkills=[word for word in words if not word in punctuations1]

    for i in range(len(techSkills)):
        if techSkills[i]=="HP":
            techSkills[i-1]="PHP"
            techSkills.pop(i)
            break
    lengthofarray = len(techSkills)

    skillsarray=[]
    cognitiveskills=[]
    for row in range(lengthofarray):
        temp = {}
        temp["skillName"] = techSkills[row]
        temp["skillExp"]=0
        temp["certification"]=False
        skillsarray.append(temp)

    while index1 <= index2:
        for skill in skillsarray:
            exp=0
            if sentences[index1].find(skill["skillName"])!=-1 :
                temp=word_tokenize(sentences[index1])

                index=-1
                if temp.__contains__("years"):
                    index=temp.index("years")-1
                elif temp.__contains__("year"):
                    index = temp.index("year") - 1
                if index>=0:
                    exp=int(temp[index])

                index=-1
                if temp.__contains__("months"):
                    index=temp.index("months")-1
                elif temp.__contains__("month"):
                    index=temp.index("month")-1
                if index>=0:
                    exp+=round((int(temp[index])/12),2)

                skill["skillExp"]+=exp
        lemmatizer=WordNetLemmatizer();
        possibleCognitiveSkills=['manage','lead','present','speak']

        for normalwords in temp:
            n=normalwords.lower()
            samplewords=lemmatizer.lemmatize(n,pos='v')


            if possibleCognitiveSkills.__contains__(samplewords):
                if  not cognitiveskills.__contains__(samplewords):
                        cognitiveskills.append(samplewords)
        index1+=1

    #For Computing Work Experience
    temp1 = word_tokenize(sentences[index3])

    index = -1
    if temp1.__contains__("years"):
        index = temp1.index("years") - 1
    elif temp1.__contains__("year"):
        index = temp1.index("year") - 1
    if index >= 0:
        Workexp = int(temp1[index])


    result["techSkills"]=skillsarray
    result["indusExp"] = Workexp
    result["status"]="Available"
    result["cognSkills"]=cognitiveskills
    #print(result)

    insert_employee(result)

#getPDFContent('14.pdf')
#try:
    #while True:
        #while
        # process line
#except EOFError:
    #pass