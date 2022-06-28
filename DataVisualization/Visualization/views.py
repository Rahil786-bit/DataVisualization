from collections import Counter

from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import pandas as pd
from pathlib import Path
# Create your views here.

def index_view(request):
    global attributeID
    context={}
    if request.method == 'POST' and request.FILES['document']:
        uploaded_file = request.FILES['document']
        print(uploaded_file.name.endswith('.xlsx'))
        attributeID = request.POST.get('attributeID')
        print(attributeID)
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.xlsx'):
            saved_file = FileSystemStorage()
            name = saved_file.save(uploaded_file.name, uploaded_file)
            print(name)
            uploaded_file_dir = saved_file.url(name)
            readfile('media/'+uploaded_file.name)

            return redirect('Report')
        else:
            messages.warning(request, 'Please Upload the CSV or Excel file Only !!')



        # if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.xlsx'):
        #
        #     #Save the file into Media Folder
        #     saved_file = FileSystemStorage()
        #     name = saved_file.save(uploaded_file.name, uploaded_file) #This is File name
        #     d= os.getcwd()   #getting the current directory
        #     __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname()))
        #     file_directory = d+'\media\\'+name


    return render(request,"index.html")

def readfile(filename):

    global row, column , data , missing_val
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python')
    data = pd.DataFrame(data=my_file, index=None)
    print(data)
    row = data.axes[0]
    column = data.axes[1]
    missingSigns = ['?','#','$','--','&']
    null_data = data[data.isnull().any(axis=1)]
    missing_val = len(null_data)


def report_view(request):

    result_message = 'I Got '+ str(row)+' rows and '+ str(column) +' clomuns and Missing data :'+ str(missing_val)
    messages.warning(request, result_message)
    dashboard = []

    for x in data[attributeID]:
        dashboard.append(x)

    my_dashboard = dict(Counter(dashboard))
    print('my Dashboard ',my_dashboard)

    keys= my_dashboard.keys()
    values = my_dashboard.values()
    listkeys = []
    listvalues =[]

    for k in keys:
        listkeys.append(k)

    for v in values:
        listvalues.append(v)

    context ={
        'listkeys':listkeys,
        'listvalues': listvalues
    }
    return render(request,'report.html', context)


