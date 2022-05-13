#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pdfminer
import pandas
import pandas as pd
import glob 
import numpy as np
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text


# In[2]:


def get_filename_without_extension(path):
        filename_basename = os.path.basename(path)
        filename_without_extension=filename_basename.split('.')[0]
        return filename_without_extension


# In[3]:


input_dir=r'C:\Users\mgautier\Desktop\DEVMOBETA\questionnaires\visit_1\asq'
data_list={}
for file in glob.glob(os.path.join(input_dir,"*.pdf")):
    #print(file)

    with open(file,'rb')as fp:
        parser=PDFParser(fp)
        doc=PDFDocument(parser)
        res=resolve1(doc.catalog)

        if 'AcroForm' not in res: 
            raise ValueError("No AcroForm found")

        fields=resolve1(doc.catalog['AcroForm'])['Fields']
    
        for f in fields : 
            field = resolve1(f)
            name,values=field.get('T'),field.get('V')

            name=decode_text(name)
            values=resolve1(values) 
            #print(name,values)

            if name not in data_list:
                data_list[name]=[]
            data_list[name].append(values)
            
df=pd.DataFrame(data_list)
print(df)
df.to_csv('asq_1.csv',index=False)


# In[6]:


input_dir=r'C:\Users\mgautier\Projects\QuestionnaireParser'
df = pd.read_csv('asq_1.csv')
df.head()
#print(df.head)
df.shape
#print (df.shape)
df=df.drop(columns=['date','child first name','child last name','child age','initials','date of birth','nb of weeks if premature','sex','parent first name','parent last name','parent initials','link','adress','city','region','postal code','country','house phone number','other phone number','mail','people helping filling the questionnaire','subject child number','program number','program name','child age if premature','notes',
                    'communication1_score','communication2_score','communication3_score','communication4_score','communication5_score','communication6_score','communication_total_score',
                   'gmotor1_score','gmotor2_score','gmotor3_score','gmotor4_score','gmotor5_score','gmotor6_score','gmotor_total_score',
                   'fmotor1_score','fmotor2_score','fmotor3_score','fmotor4_score','fmotor5_score','fmotor6_score','fmotor_total_score',
                   'pbsolving1_score','pbsolving2_score','pbsolving3_score','pbsolving4_score','pbsolving5_score','pbsolving6_score','pbsolving_total_score',
                   'social1_score','social2_score','social3_score','social4_score','social5_score','social6_score','social_total_score',
                   'global1','global2','global3','global4','global5','global6','global7','global8','global1_no','global2_no','global3_yes','global4_yes','global5_yes','global6_yes','global7_yes','global8_yes',])
print(df)
df.notna()  #indicate existing non missing values
df.dropna(how='all') #delete if all values are nan

col_list_communication= ['communication1','communication2','communication3','communication4','communication5','communication6']
for col in col_list_communication:
    df[col]=df[col].str.replace("/","")
    df[col]=df[col].str.replace("'","")
    df[col] = df[col].astype(float)
    
col_list_gmotor= ['gmotor1','gmotor2','gmotor3','gmotor4','gmotor5','gmotor6']
for col in col_list_gmotor:
    df[col]=df[col].str.replace("/","")
    df[col]=df[col].str.replace("'","")
    df[col] = df[col].astype(float)

col_list_fmotor= ['fmotor1','fmotor2','fmotor3','fmotor4','fmotor5','fmotor6']
for col in col_list_fmotor:
    df[col]=df[col].str.replace("/","")
    df[col]=df[col].str.replace("'","")
    df[col] = df[col].astype(float)
    
col_list_pbsolving= ['pbsolving1','pbsolving2','pbsolving3','pbsolving4','pbsolving5','pbsolving6']
for col in col_list_pbsolving:
    df[col]=df[col].str.replace("/","")
    df[col]=df[col].str.replace("'","")
    df[col] = df[col].astype(float)
    
col_list_social= ['social1','social2','social3','social4','social5','social6']
for col in col_list_social:
    df[col]=df[col].str.replace("/","")
    df[col]=df[col].str.replace("'","")
    df[col] = df[col].astype(float)





# In[12]:


for index, row in df.iterrows():

  row['communication'] = row[col_list_communication].sum()
  print(row)
  
  communication=float(row["communication"])
  print(communication)
  
  if communication<=34.6: 
      print("communication deficit")
  elif (communication>34.6 and communication<43.44):
      print("monitor communication")
  elif communication>=43.44:
      print ("communication ok")
      
df['communication']=communication
df.to_csv('asq_1_result.csv',index=False)


# In[13]:


for index, row in df.iterrows():
    
    row['gmotor'] = row[col_list_gmotor].sum()
    print(row)
    
    gmotor=float(row["gmotor"])
    print(gmotor)
    
    if gmotor<=38.41: 
        print("gmotor deficit")
    elif (38.41>gmotor and gmotor <46.52):
        print("monitor gmotor")
    elif gmotor>=46.52:
        print ("gmotor ok")
        
df['gmotor']=gmotor
df.to_csv('asq_1_result.csv',index=False)


# In[14]:


for index, row in df.iterrows():

    row['fmotor'] = row[col_list_fmotor].sum()
    print(row)
    
    fmotor=float(row["fmotor"])
    print(fmotor)
    
    if fmotor<=29.62: 
        print("fmotor deficit")
    elif (29.62>fmotor and fmotor<40.6):
        print("monitor fmotor")
    elif fmotor>=40.6:
        print ("fmotor ok")
        
df['fmotor']=fmotor
df.to_csv('asq_1_result.csv',index=False)


# In[15]:


for index, row in df.iterrows():
    
    row['pbsolving'] = row[col_list_pbsolving].sum()
    print(row)
    
    pbsolving=float(row["pbsolving"])
    print(pbsolving)
    
    if pbsolving<=34.98: 
        print("pbsolving deficit")
    elif (34.98>pbsolving and pbsolving<44.38):
        print("monitor pbsolving")
    elif pbsolving>=44.38:
        print ("pbsolving ok")
        
df['pbsolving']=pbsolving
df.to_csv('asq_1_result.csv',index=False)


# In[16]:


for index, row in df.iterrows():

    row['social'] = row[col_list_social].sum()
    print(row)
    
    social=float(row["social"])
    print(social)
    
    if social<=33.16: 
        print("social deficit")
    elif (33.16>social and social<42.54):
        print("monitor social")
    elif social>=42.54:
        print ("social ok")
        
df['social']=social
df.to_csv('asq_1_result.csv',index=False)
