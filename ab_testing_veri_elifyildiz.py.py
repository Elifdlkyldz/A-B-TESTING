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

##Veri Seti Hikayesi;
#Impression : Reklam görüntüleme sayısı
#Click    : Görüntülenen reklama tıklama sayısı
#Purchase :Tıklanan reklamlar sonrası satın alınan ürün sayısı
#Earning  :Satın alınan ürünler sonrası elde edilen kazanç



#Görev 1:  Veriyi Hazırlama ve Analiz Etme
###Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.


df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")

df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

###Adım 2: Kontrol ve test grubu verilerini analiz ediniz.


df_test.head()
df_test.describe().T
df_test.info


df_control.head()
df_control.describe().T
df_control.info

###Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_control["worth"]= 0
df_test["worth"]= 1

df = pd.concat([df_control, df_test])
df.head()
df.info


#Görev 2:  A/B Testinin Hipotezinin Tanımlanması
###Adım 1: Hipotezi tanımlayınız.
#average bidding'den maximum bidding'den daha fazla ürün alınıyor mu?

# H0 : M1 = M2 average bidding ile maximum biddingde satın alınan ürün sayısı arasında istatistiki olarak anlamlı bir fark yoktur.
# H1 : M1!= M2 .... vardır.


###Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz.

#df['Purchase'].mean() #566
df_control['Purchase'].mean() #550
df_test['Purchase'].mean() #582

#Görev 3:  Hipotez Testinin Gerçekleştirilmesi
###Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.
# Normallik Varsayımı :H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ?
# Elde edilen p-value değerlerini yorumlayınız.
# Varyans Homojenliği :H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir. p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ



#Normallik Varsayımı;
# shapiro testi bir değişkenin dağılımı normalmi değil mi kontrol eder. !!!!!


test_stat, pvalue = shapiro(df.loc[df["worth"] == 0, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.58


test_stat, pvalue = shapiro(df.loc[df["worth"] == 1, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.15


#p değerleri 0.05 den büyüktür yani normal dağılım varsayımı sağlanıyor.
# Normallik varsayımı sağlandığı için direk bağımsız iki örneklem t testi (parametrik test) yapılabilir
# ama varyans homojenliğine de bir bakıyorum.

# Varyans Homojenliği ;
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir. p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ


test_stat, pvalue = levene(df.loc[df["worth"] == 0, "Purchase"],
                           df.loc[df["worth"] == 1, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.10

#p value değeri 0.10 olduğu için p > 0.05 den bu da hO'a götürüyor bizi. Varyanslar homojendir.Parametrik test yapılabilir.


###Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.
# #Varsayımlar sağlanıyor bağımsız iki örneklem t testi (parametrik test) yapıyoruz;
##normallik sağlanıyor , varyans hom. var. sağlanmasaydı equel_var=FALSE olacaktı.

test_stat, pvalue = ttest_ind(df.loc[df["worth"] == 0, "Purchase"],
                              df.loc[df["worth"] == 1, "Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) #0.34
#ho reddedilemez. yani ho ikisi arasında fark yoktur der ve bunu kabul ederiz.



###Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında
# istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# p value değeri = 0.34 çıktı. p >0.05 den büyük olduğu için H0 hipotezimizi reddetmiyoruz. Yani average bidding ile maximum bidding
#arasındaki satın alınan ürün sayısı arasında İstatistiki Olarak Anlamlı Fark yoktur. H0 : M1 == M2 diyebiliriz. En başta inceleme yaparken
#gördüğümüz kontorl ve test grubundaki'Purchase - mean' değerleri arasındaki fark şans eseri ortaya çıkmıştır diyebiliriz.Ortalamalar arasımdaki fark tesadüfidir.
#

#Görev 4:  Sonuçların Analizi
###Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#Normallik varsayımı için ; shapiro , varyans homojenliği için ; levene testi kullanıp ,dağılımın normal olduğunu ve varyansın homojen olduğunu
#p value değerine göre test ettim. Daha sonra varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) yaptım. (ttest_ind testi)
#Bu test ile de hipotezimi p value değeri ile red edip edemeyeceğimi belirledim.

###Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

#H0 'ı reddetmediğimiz için avarege bidding ile maximum bidding arasında istatistiki olarak anlamlı fark yoktur diyebiliyoruz.
#bu da bize yeni bir teklif türü olan avarege bidding'in firmaya bir şey katmadığını ve tıklanan reklamlar sonrası satın alınan ürün sayının (purchase değeri)
#iki teklif verme türünde de aynı olduğunu gördük. Avarege bidding de farklı olarak yapılan sistemi daha da geliştriebilirler yada
#geliştirmedikleri şeyleri tekrar bi incelemeye alıp geliştirebilirler. Ya da bu değişken üzerinden ab testi yapılmaya devam edilebilir ve gelişmelere bakılabilir.
