##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir.
# Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.


###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi


###############################################################
# GÖREVLER
###############################################################
# GÖREV 1: Veriyi Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
from datetime import timedelta
import pandas as pd
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
df_ = pd.read_csv("/Users/sinemdokmeci/PycharmProjects/CRM_Analitigi/case/case_study_1/flo_data_20k.csv")
df = df_.copy()
           # 2. Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayınız.
           # Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.Bu nedenle alt ve üst limitlerini round() ile yuvarlayınız.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = round(quartile3 + 1.5 * interquantile_range)
    low_limit = round(quartile1 - 1.5 * interquantile_range)
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

           # 3. "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online" değişkenlerinin
           # aykırı değerleri varsa baskılayanız.
replace_with_thresholds(df, "order_num_total_ever_online")
replace_with_thresholds(df, "order_num_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_online")
           # 4. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
df['total_orders'] = df['order_num_total_ever_online'] + df['order_num_total_ever_offline']
df['total_spent'] = df['customer_value_total_ever_online'] + df['customer_value_total_ever_offline']
           # 5. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
print(df.dtypes)
date_columns = [
    'first_order_date',
    'last_order_date',
    'last_order_date_online',
    'last_order_date_offline'
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col])

# GÖREV 2: CLTV Veri Yapısının Oluşturulması
           # 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
today_date = df["last_order_date"].max() + timedelta(days=2)

           # 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
df['recency_cltv_weekly'] = (df["last_order_date"] - df["first_order_date"]).dt.days / 7
df['T_weekly'] = (today_date - df["first_order_date"]).dt.days / 7
df['Invoice'] = df["total_orders"]
df['TotalPrice'] = df["total_spent"]
cltv_df = df[['recency_cltv_weekly', 'T_weekly', 'Invoice', 'TotalPrice']]
cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
           # Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.
cltv_df = cltv_df[(cltv_df['frequency'] >= 1)]
cltv_df = cltv_df[(cltv_df['recency'] >= 1)]
cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
cltv_df["recency"] = cltv_df["recency"] / 7
cltv_df["T"] = cltv_df["T"] / 7

# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, CLTV'nin hesaplanması
           # 1. BG/NBD modelini fit ediniz.
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])
                # a. 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.
cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])
                # b. 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.
cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])
           # 2. Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekleyiniz.
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary'])
cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary'])
           # 3. 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.
cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=6,  # 3 aylık
                                   freq="W",  # T'nin frekans bilgisi.
                                   discount_rate=0.01)
cltv_df['clv'] = cltv

                # b. Cltv değeri en yüksek 20 kişiyi gözlemleyiniz.
cltv_df.sort_values(by='clv', ascending=False).head(20)
# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
           # 1. 6 aylık tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz. cltv_segment ismi ile dataframe'e ekleyiniz.
cltv_df["cltv_segment"] = pd.qcut(cltv_df["clv"], 4, labels=["D", "C", "B", "A"])
cltv_df.sort_values(by="clv", ascending=False).head(50)
           # 2. 4 grup içerisinden seçeceğiniz 2 grup için yönetime kısa kısa 6 aylık aksiyon önerilerinde bulununuz

# BONUS: Tüm süreci fonksiyonlaştırınız.
import pandas as pd
import numpy as np
from datetime import timedelta
from lifetimes import BetaGeoFitter, GammaGammaFitter


def cltv_prediction_and_segmentation(filepath):
    # Veri yükleme ve hazırlık
    df_ = pd.read_csv(filepath)
    df = df_.copy()

    # Aykırı değerleri baskılamak için fonksiyonlar
    def outlier_thresholds(dataframe, variable):
        quartile1 = dataframe[variable].quantile(0.01)
        quartile3 = dataframe[variable].quantile(0.99)
        interquantile_range = quartile3 - quartile1
        up_limit = round(quartile3 + 1.5 * interquantile_range)
        low_limit = round(quartile1 - 1.5 * interquantile_range)
        return low_limit, up_limit

    def replace_with_thresholds(dataframe, variable):
        low_limit, up_limit = outlier_thresholds(dataframe, variable)
        dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
        dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

    # Aykırı değerleri baskılamak
    for var in ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline",
                "customer_value_total_ever_online"]:
        replace_with_thresholds(df, var)

    # Toplam alışveriş sayısı ve harcama
    df['total_orders'] = df['order_num_total_ever_online'] + df['order_num_total_ever_offline']
    df['total_spent'] = df['customer_value_total_ever_online'] + df['customer_value_total_ever_offline']

    # Tarih sütunlarını datetime formatına çevir
    date_columns = ['first_order_date', 'last_order_date', 'last_order_date_online', 'last_order_date_offline']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    # CLTV veri yapısı
    today_date = df["last_order_date"].max() + timedelta(days=2)
    df['recency_cltv_weekly'] = (df["last_order_date"] - df["first_order_date"]).dt.days / 7
    df['T_weekly'] = (today_date - df["first_order_date"]).dt.days / 7
    df['Invoice'] = df["total_orders"]
    df['TotalPrice'] = df["total_spent"]

    cltv_df = df[['recency_cltv_weekly', 'T_weekly', 'Invoice', 'TotalPrice']]
    cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
    cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    # BG/NBD modelini fit etme
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])

    cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3, cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])
    cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6, cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])

    # Gamma-Gamma modelini fit etme
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
    cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary'])

    # 6 aylık CLTV hesaplama
    cltv = ggf.customer_lifetime_value(bgf, cltv_df['frequency'], cltv_df['recency'], cltv_df['T'], cltv_df['monetary'],
                                       time=6, freq="W", discount_rate=0.01)
    cltv_df['clv'] = cltv

    # CLTV segmentasyonu
    cltv_df["cltv_segment"] = pd.qcut(cltv_df["clv"], 4, labels=["D", "C", "B", "A"])

    # Sonuçları döndürme
    return cltv_df.sort_values(by="clv", ascending=False)


# Fonksiyonu çağırma örneği
cltv_results = cltv_prediction_and_segmentation(
    "/Users/sinemdokmeci/PycharmProjects/CRM_Analitigi/case/case_study_1/flo_data_20k.csv")
print(cltv_results.head(20))









