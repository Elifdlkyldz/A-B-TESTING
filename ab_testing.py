##A-B TESTING

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")

df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

df_test.head()
df_test.describe().T
df_test.info


df_control["worth"]= 0
df_test["worth"]= 1

df = pd.concat([df_control, df_test])
df.head()
df.info


## Let's start A/B TEST

# Hypotheses;
""""
   -----OUR HYPOTHESIS H0 AND H1 ----
H0: M1 = M2 
 There is no statistical difference between the average purchase earned,
    by the maximum binding strategy and the average purchase achieved by the average binding strategy.
H1: M1 != M2 
 There is a statistical difference between the average purchase earned, 
    by the maximum binding strategy and the average purchases earned by the average binding strategy.
    
    """"
df_control['Purchase'].mean()  # OUT:  Mean of purchase of control group: 550.8941
df_test['Purchase'].mean()     # OUT:   Mean of purchase of test group: 582.1061


# Assumption Check;

# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

# shapiro testi bir değişkenin dağılımı normal mi değil mi kontrol eder. !!!!!


test_stat, pvalue = shapiro(df.loc[df["worth"] == 0, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.58


test_stat, pvalue = shapiro(df.loc[df["worth"] == 1, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.15


#p değerleri 0.05 den büyüktür yani normal dağılım varsayımı sağlanıyor.

# Normallik varsayımı sağlandığı için direk bağımsız iki örneklem t testi (parametrik test) yapılabilir.


# Varyans Homojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir. 
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

# levene testi varyans homojenliğini kontrol eder. !!!!!


test_stat, pvalue = levene(df.loc[df["worth"] == 0, "Purchase"],
                           df.loc[df["worth"] == 1, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.10

#p value değeri 0.10 olduğu için p > 0.05 den bu da hO'a götürüyor bizi. Varyanslar homojendir.


####Varsayımlar sağlanıyor bağımsız iki örneklem t testi (parametrik test) yapıyoruz;

test_stat, pvalue = ttest_ind(df.loc[df["worth"] == 0, "Purchase"],
                              df.loc[df["worth"] == 1, "Purchase"],
                              equal_var=True) ##normallik sağlanıyor , varyans hom. var. sağlanmasaydı equel_var=FALSE olacaktı.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.34

#HO reddedilemez. yani ho ikisi arasında fark yoktur der ve bunu kabul ederiz.

####Result;
# H0= Yeni Tasarımın (AVERAGE BIDDING) Dönüşüm Oranı ile Eski Tasarımın (MAXIMUM BIDDING) Dönüşüm Oranı Arasında İstatistiksel Olarak Anlamlı Farklılık Yoktur.
# Hipotezinin doğruluğu istatistiksel olarak anlamlıdır.
