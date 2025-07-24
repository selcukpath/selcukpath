from datetime import datetime

class Hasta:
    def __init__(self, id=None, ad=None, soyad=None, tc_no=None, 
                 dogum_tarihi=None, telefon=None, kayit_tarihi=None):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.tc_no = tc_no
        self.dogum_tarihi = dogum_tarihi
        self.telefon = telefon
        self.kayit_tarihi = kayit_tarihi or datetime.now()
    
    def __repr__(self):
        return f"<Hasta {self.ad} {self.soyad} - {self.tc_no}>"
    
    def tam_ad(self):
        return f"{self.ad} {self.soyad}"

class PatolojiRaporu:
    def __init__(self, id=None, hasta_id=None, rapor_tarihi=None, 
                 rapor_no=None, makroskopi=None, mikroskopi=None, 
                 tani=None, dosya_yolu=None, kayit_tarihi=None):
        self.id = id
        self.hasta_id = hasta_id
        self.rapor_tarihi = rapor_tarihi
        self.rapor_no = rapor_no
        self.makroskopi = makroskopi
        self.mikroskopi = mikroskopi
        self.tani = tani
        self.dosya_yolu = dosya_yolu
        self.kayit_tarihi = kayit_tarihi or datetime.now()
    
    def __repr__(self):
        return f"<PatolojiRaporu {self.rapor_no} - {self.tani}>"