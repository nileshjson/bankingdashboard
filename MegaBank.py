# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 20:45:36 2021

@author: DeLL
"""


import json
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#method 1 to read json data

json_file = open('1.3 loan_data_json.json')
data = json.load(json_file)

#method 2 to read json

#with open('1.3 loan_data_json.json') as json_file:
#    data = json.load(json_file)


#Tranforming data to readable format

loandata = pd.DataFrame(data)

#finding distinct purposes of loan

loandata['purpose'].unique()

#describe the data
loandata.describe()

#decribing the data for a specific column
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#using EXP() to get the actual income from log annual income column

income = np.exp(loandata['log.annual.inc'])

#updating the income column in database

loandata['annual_income'] = income 


lenght = len(loandata)  

ficocat = []
for i in range(0,lenght):
    category = loandata['fico'][i]
    
    try:
        if 300<=category<400:
            cat = 'Very Poor'
            
        elif 400<=category<600:
            cat = 'Poor'
            
        elif 600<=category<660:
            cat = 'Fair'
              
        elif 660<=category<700:
            cat = 'Good'
            
        elif category>=700:
            cat = "Excellent"
                
        else:
            cat = 'Unknown'
    
    except:
        cat = "Unknown"
    
    ficocat.append(cat)
        
ficocat = pd.Series(ficocat)    
loandata['fico.category'] = ficocat
    
        
 #using df.loc() statement as conditional statement
#df.loc( [ df[column_name] conditon,[newcolumn_name]]) = value if condtion is true

# for intrest rate we'll define if int rate>12% then its high else: low

loandata.loc[ loandata['int.rate'] > 0.12, 'int.rate.type'] = "High" 
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = "Low" 

# Grouping different fico categories
category_plot = loandata.groupby(['fico.category']).size()
#ploting different fico categories on a bar chart
category_plot.plot.bar(color = 'green',width = 0.5)
plt.show()


#Counting the loans for different purpose

count_purpose = loandata.groupby(['purpose']).size()

count_purpose.plot.barh()
plt.show()


#Scatterplot between annual income and dti

ypoint = loandata['annual_income']
xpoint = loandata['dti']

plt.scatter(xpoint, ypoint,color = "#d88aed",alpha = 0.5)
plt.title("Annual Income vs DTI Ratio", fontsize = 18, y = 1.03)
plt.xlabel("Debt to Income ratio", fontsize = 14, labelpad = 15)
plt.ylabel("Annual Income", fontsize = 14, labelpad = 15)
plt.show()

#writting data to csv
loandata.to_csv('loan_cleaned_csv',index = True)

