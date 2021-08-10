from django.http.response import HttpResponse
from django.shortcuts import render
import pandas as pd
import numpy as np
import json

# Create your views here.

def home(request):
    AprilData = pd.read_excel('April-2021.xlsx', skiprows=2)
    MayData = pd.read_excel('May-2021.xlsx', skiprows=2)
    JuneData = pd.read_excel('June-2021.xlsx', skiprows=2)

    data = AprilData.merge(MayData, on=['Vehicle Class'],how='outer')
    data = data.merge(JuneData, on=['Vehicle Class'],how='outer')
    data = data.replace({np.nan: '','_x000D_':''}, regex=True)
    data = data.drop(columns=['Serial No','Serial No_x','Serial No_y'])
    data = data.rename(columns={'Vehicle Class':'vehicle_class','Total_x':'April','Total_y':'May','Total':'June'})
    json_records = data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return render(request,'data.html',context)

def download(request):
    AprilData = pd.read_excel('April-2021.xlsx', skiprows=2)
    MayData = pd.read_excel('May-2021.xlsx', skiprows=2)
    JuneData = pd.read_excel('June-2021.xlsx', skiprows=2)

    data = AprilData.merge(MayData, on=['Vehicle Class'],how='outer')
    data = data.merge(JuneData, on=['Vehicle Class'],how='outer')
    data = data.replace({np.nan: '','_x000D_':''}, regex=True)
    data = data.drop(columns=['Serial No','Serial No_x','Serial No_y'])
    data = data.rename(columns={'Vehicle Class':'vehicle_class','Total_x':'April','Total_y':'May','Total':'June'})
    
    resp = HttpResponse(data.to_csv(index=False), content_type='application/x-download')
    resp['Content-Disposition'] = 'attachment;filename=data.csv'
    return resp