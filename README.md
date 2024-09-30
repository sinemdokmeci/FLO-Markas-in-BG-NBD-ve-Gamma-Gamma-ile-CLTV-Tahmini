# FLO-Markas-in-BG-NBD-ve-Gamma-Gamma-ile-CLTV-Tahmini
FLO - CLTV Tahmini

# İş Problemi (Business Problem)
 FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir.
 Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.

# Veri Seti Hikayesi
Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
elde edilen bilgilerden oluşmaktadır.

# Veriseti Hakkında
 master_id: Eşsiz müşteri numarası
 order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, 
 ios, Desktop, Mobile, Offline)
 last_order_channel : En son alışverişin yapıldığı kanal
 first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
 last_order_date : Müşterinin yaptığı son alışveriş tarihi
 last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
 last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
 order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
 order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
 customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
 customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
 interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

# Müşteri Yaşam Boyu Değeri (Customer Lifetime Value — CLTV)

CLTV Nedir?

Müşteri Yaşam Boyu Değeri (CLTV), bir müşterinin şirketle etkileşim sürecinde kazandıracağı toplam parasal değerdir.

# Ne İçin Kullanılır?

Stratejik Planlama: CLTV, müşteri kazanım maliyetleri ile karşılaştırıldığında bir müşterinin değerini belirler ve stratejik kararlar alırken müşteri değerini göz önünde bulundurmanıza yardımcı olur.

Kaynak Dağılımı: CLTV, hangi müşteri segmentlerinin daha yüksek değerli olduğunu gösterir ve bu bilgilere dayanarak pazarlama bütçesi ve kaynakları daha etkili bir şekilde dağıtmanıza yardımcı olur.

# Müşteri Yaşam Boyu Tahmini (Customer Lifetime Value Prediction)

Müşteri Yaşam Boyu Tahmini Nedir?

Müşteri yaşam boyu tahmini, zaman projeksiyonlu olasılıksal lifetime value tahminidir. Bu yöntem, müşteri davranışlarını ve işlem başına ortalama kazancı modelleyerek tahminler yapar.

# Ne İçin Kullanılır?

Tahmin ve Planlama: Müşteri davranışlarını modelleyerek gelecekteki kazançları tahmin eder ve uzun vadeli stratejik planlama yapmanıza yardımcı olur.

Modelleme: BG/NBD (Beta-Geometric / Negative Binomial Distribution) ve Gamma-Gamma Submodel gibi yöntemlerle müşterinin gelecekteki alışveriş davranışlarını ve değerini tahmin eder.

FLO'nun mevcut müşterilerinin gelecekte sağlayacağı potansiyel değeri tahmin etmek amacıyla CLTV analizi yapılacaktır.

# 1. Verilerin Hazırlanması

Müşteri Satın Alma Verileri: Her müşteri için geçmiş satın alma verileri toplanır. Bu veriler arasında:

Satın alma tarihleri
Harcama miktarları
Alışveriş sıklığı
Müşteri segmentleri (varsa)

# 2. Temel Kavramların Belirlenmesi

CLTV hesaplaması için aşağıdaki temel kavramların netleştirilmesi önemlidir:

Ortalama Sipariş Değeri (Average Order Value - AOV): Bir müşterinin ortalama olarak yaptığı satın alma değeri. 
Satın Alma Sıklığı (Purchase Frequency - PF): Bir müşterinin belirli bir dönemde (örneğin, bir yıl) kaç kez alışveriş yaptığı.
Müşteri Yaşam Süresi (Customer Lifespan - CL): Bir müşterinin şirkete bağlı kalma süresi. Genellikle yıllar cinsinden ifade edilir.
Müşteri Kaybı Oranı (Churn Rate): Belirli bir dönemde müşterilerin şirkete olan bağlılıklarını kaybetme oranı.

# 3. CLTV Hesaplama
# 4. Uygulama

Müşteri Segmentlerine Göre Hesaplama: CLTV, farklı müşteri segmentlerine göre hesaplanabilir. Bu sayede, hangi segmentlerin daha fazla değer ürettiği anlaşılabilir.
Hesaplamaların Yapılması: İlgili veriler kullanılarak CLTV değerleri hesaplanır.

# 5. Analiz ve Raporlama

Sonuçların Değerlendirilmesi: Hesaplanan CLTV değerleri analiz edilerek, pazarlama stratejileri ve müşteri ilişkileri yönetimi (CRM) süreçleri için bilgiler çıkarılır.
Raporlama: Elde edilen veriler düzenli olarak ilgili paydaşlarla paylaşılmalı ve stratejik kararlar almak için kullanılmalıdır.



