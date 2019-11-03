#os.chdir('C:\Users\Kamellia\Desktop\PrelucrareaStatisticaADatelorText2019-master')
from pandas import read_csv
import pandas as pd
baza= read_csv('output.csv')

print(baza)

#Descriptive-variabile numerice
baza= baza.replace('None', '0')
baza['New price'] = baza['New price'].astype(float)
baza['Old price'] = baza['Old price'].astype(float)
newprice= baza[baza['New price'] > 0]['New price']
oldprice= baza[baza['Old price'] > 0]['Old price']

rating=baza['Rating']
procesor=baza['Tip procesor']
frecv=baza['Frecventa']

print (newprice.describe())
print(oldprice)
print (oldprice.describe())
print (rating.describe())


from scipy.stats import skew
print(skew(newprice))
print(skew(oldprice))
print(skew(rating))

from scipy.stats import kurtosis
print(kurtosis(newprice))
print(kurtosis(oldprice))
print(kurtosis(rating))


#Histogram-variabile numerice
import matplotlib.pyplot as plt
import numpy as np

print(baza.newprice.hist(bins=(500), color='purple',grid='False'))
plt.xlabel( 'Newprice')

print(baza.oldprice.hist(bins=(500), color='purple',grid='False'))
plt.xlabel( 'Old price')

print(baza.rating.hist(bins=(1), color='purple',grid='False'))
plt.xlabel( 'Rating')

#Variabile categoriale
import matplotlib.pyplot as plt

print(baza.procesor.value_counts())
print(baza.procesor.value_counts()/1079)

print(baza.frecv.value_counts())
print(baza.frecv.value_counts()/1079)



#Crosstab
cross_tab=pd.crosstab(baza.procesor, baza.frecv, margins=True)
print(cross_tab)
print(cross_tab/cross_tab.ix['All','All'])
from scipy.stats import chi2_contingency
chi_test=chi2_contingency(cross_tab)
print(chi_test)

#Boxlplot
import seaborn as sns
import matplotlib.pyplot as plt

plt.boxplot(newprice,labels=['New price'],patch_artist=True)
plt.boxplot(oldprice,labels=['Old price '],patch_artist=True)
plt.boxplot(rating,labels=['Rating'],patch_artist=True)


#Estimarea intervalului de incredere
import statsmodels.stats.api as sms
print('Confidence Interval',sms.DescrStatsW(newprice).tconfint_mean())
print('Confidence Interval',sms.DescrStatsW(oldprice).tconfint_mean())
print('Confidence Interval',sms.DescrStatsW(rating).tconfint_mean())

#Testarea mediilor
#Simple Student test
from scipy import stats
print(stats.ttest_1samp(newprice,3000))
print(stats.ttest_1samp(oldprice,4000))
print(stats.ttest_1samp(rating,5))

#Test 2 means
newprice_i7=baza.loc[baza['procesor']=='i7']
newprice_i5=baza.loc[baza['procesor']=='i5']
print(stats.ttest_ind(newprice_i7.newprice,newprice_i5.newprice))

#Analiza de corelatie
from scipy.stats import pearsonr
print(pearsonr(newprice,rating))
print(pearsonr(oldprice,rating))

#Simple linear regression

x=procesor

import statsmodels.api as sm
x=sm.add_constant(x)
model=sm.OLS(newprice,x)
results=model.fit()
print(results.summary())
print('Parameters:',results.params)
print('R2:',results.rsquared)
print('Standard errors:',results.bse)
print('Predicted values:',results.predict())
erori=results.resid
import scipy.stats
print(stats.ttest_1samp(erori,0))
import statsmodels.stats.api as sms

#Heteroscedasticity test
test_BP=sms.het_breuschpagan(results.resid,results.model.exog)  
print(test_BP)
#Test GQ
test_GQ=sms.het_goldfeldquandt(results.resid,results.model.exog)
print(test_GQ)
import matplotlib.pyplot as plt
import numpy as np
import seaborn
seaborn.lmplot(y='new price',x='procesor',data=baza)
plt.show()