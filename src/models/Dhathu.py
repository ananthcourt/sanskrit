class Dhathu:
    DHATHU_FORM_NAMES = [
            "shuddha_kartari",
            "shuddha_karmani",
            "san_kartari",
            "san_karmani",
            "nich_kartari",
            "nich_karmani",
            "yang_kartari",
            "yang_karmani",
            "yangluk_kartari",
            "yangluk_karmani",
        ]

    DHATHU_KRIDANTA_FORM_NAMES = [
        "shuddha_kridanta",
        "san_kridanta",
        "nich_kridanta",
        "yang_kridanta",
        "yangluk_kridanta",

    ]
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.id = raw_data["i"]
        self.base_index = raw_data["baseindex"]
        self.chapter = int(self.base_index.split(".")[0])
        self.index = int(self.base_index.split(".")[1])
        self.name = raw_data["dhatu"]
        self.aupadeshik = raw_data["aupadeshik"]
        self.ganam = self._get_ganam(raw_data["gana"])
        self.padam = self._get_padam(raw_data["pada"])
        self.settva = self._get_settva(raw_data["settva"])
        self.karma = self._get_karma(raw_data["karma"])
        self.kaumudi_dhatu_number = raw_data["sk"]
        self.meaning = raw_data["artha"]
        self.english_meaning = raw_data["artha_english"]
        self.hindi_meaning = raw_data["artha_hindi"]
        self.dhathu_forms = {}
        self.kridanta_forms = {}

    @classmethod
    def base_csv_column_names(cls):
        return "id;chapter;index;name;aupadeshik;ganam;padam;settva;karma;kaumudi_dhatu_number;meaning;english_meaning;hindi_meaning"

    @classmethod
    def lakaar_csv_column_names(cls):
        return "id;chapter;index;name;lakaar_name;prathama_eka;prathama_dvi;prathama_bahu;madhyama_eka;madhyama_dvi;madhyama_bahu;uttama_eka;uttama_dvi;uttama_bahu;"

    @classmethod
    def kridanta_csv_column_names(cls):
        return "id;chapter;index;name;kridanta_form_name;pu_lingam;stri_lingam;napu_lingam"
    
    def to_base_csv_string(self):
        return f"{self.id};{self.chapter};{self.index};{self.name};{self.aupadeshik};{self.ganam};{self.padam};{self.settva};{self.karma};{self.kaumudi_dhatu_number};{self.meaning};{self.english_meaning};{self.hindi_meaning}"
    
    
    def to_lakaar_csv_string(self, lakaar_code, dhathu_rupa):
        return f"{self.id};{self.chapter};{self.index};{self.name};{dhathu_rupa.lakaar_name};{dhathu_rupa.value}"

    def to_kridanta_csv_string(self, name, kridanta_rupa):
        return f"{self.id};{self.chapter};{self.index};{self.name};{kridanta_rupa.name};{kridanta_rupa.value}"
    
    def _get_karma(self, karma_letter):
        karma_dict = {
            "S": "सकर्मकः",
            "A": "अकर्मकः",
            "D": "द्विकर्मकः",
        }
        return karma_dict.get(karma_letter, "")
    
    def _get_settva(self, settva_letter):
        settva_dict = {
            "S": "सेट्",
            "A": "अनिट्",
            "V": "वेट्",
        }
        return settva_dict.get(settva_letter, "")
    def _get_ganam(self, gana_number):
        gana_dict = {
            "1": "भ्वादि",
            "2": "अदादि",
            "3": "जुहोतादि",
            "4": "दिवादि",
            "5": "स्वादि",
            "6": "तुदादि", 
            "7": "रुधादि",
            "8": "तनादि",
            "9": "क्र्यादि",
            "10": "चुरादि",
        }
        return gana_dict.get(gana_number, "")
    
    def _get_padam(self, pada_letter):
        pada_dict = {
            "P": "परस्मैपदी",
            "A": "आत्मनेपदी",
            "U": "उभयपदी",
        }
        return pada_dict.get(pada_letter, "")



class DhathuForm:
    def __init__(self, form_code, lakaar_dict):
        self.form_code = form_code
        self.form_name = self._dhathu_form_name(form_code)
        self.set_lakaar_dict(lakaar_dict)
    
    def set_lakaar_dict(self, lakaar_dict):
        self.lakaar_dict = {lakaar_code: DhathuRupa(lakaar_code, value) for lakaar_code, value in lakaar_dict.items()}
    
    def _dhathu_form_name(self, form_code):
        form_dict = {
            "kartari": "कर्तरि",
            "yak": "भावकर्मणोः",
            "san": "सन्नन्ते - कर्तरि",
            "san_yak": "सन्नन्ते - भावकर्मणोः",
            "nich": "णिजन्ते - कर्तरि",
            "nich_yak": "णिजन्ते - भावकर्मणोः",
            "yang": "यङन्ते - कर्तरि",
            "yang_yak": "यङन्ते - भावकर्मणोः",
            "yangluk": "यङ्लुगन्ते - कर्तरि",
            "yangluk_yak": "यङ्लुगन्ते - भावकर्मणोः",
        }
        return form_dict.get(form_code, "")

class DhathuRupa:
    def __init__(self, lakaar_code, value):
        self.value = value
        self.lakaar_code = lakaar_code
        self.lakaar_name = DhathuRupa._get_lakaar_name(lakaar_code)

    @classmethod
    def csv_column_names(cls):
        return "lakaar_code;lakaar_name;plat;plit;plut;plrut;plet;plot;plang;pvidhiling;pashirling;plung;plrung;alat;alit;alut;alrut;alet;alot;alang;avidhiling;aashirling;alung;alrung"
    

    @classmethod
    def _get_lakaar_name(cls, lakaar_code):
        lakaar_dict = {
            "plat": "लट्लकारः (परस्मैपदम्)",
            "plit": "लिट्लकारः (परस्मैपदम्)",
            "plut": "लुट्लकारः (परस्मैपदम्)",
            "plrut": "लृट्लकारः (परस्मैपदम्)",
            "plet": "लेट्लकारः (परस्मैपदम्)",
            "plot": "लोट्लकारः (परस्मैपदम्)",
            "plang": "लङ्लकारः (परस्मैपदम्)",
            "pvidhiling": "विधिलिङ्लकारः (परस्मैपदम्)",
            "pashirling": "आशीर्लिङ्लकारः (परस्मैपदम्)",
            "plung": "लुङ्लकारः (परस्मैपदम्)",
            "plrung": "लृङ्लकारः (परस्मैपदम्)",
            "alat": "लट्लकारः (आत्मनेपदम्)",
            "alit": "लिट्लकारः (आत्मनेपदम्)",
            "alut": "लुट्लकारः (आत्मनेपदम्)",
            "alrut": "लृट्लकारः (आत्मनेपदम्)",
            "alet": "लेट्लकारः (आत्मनेपदम्)",
            "alot": "लोट्लकारः (आत्मनेपदम्)",
            "alang": "लङ्लकारः (आत्मनेपदम्)",
            "avidhiling": "विधिलिङ्लकारः (आत्मनेपदम्)",
            "aashirling": "आशीर्लिङ्लकारः (आत्मनेपदम्)",
            "alung": "लुङ्लकारः (आत्मनेपदम्)",
            "alrung": "लृङ्लकारः (आत्मनेपदम्)"
        }
        return lakaar_dict.get(lakaar_code, "")

class Kridanta_Rupa:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def csv_column_names(cls):
        return "name;word;pu lingam;stri lingam;napu lingam"
    

class DhathuKridantaForm:
    def __init__(self, form_code, kridanta_dict):
        self.form_code = form_code
        self.form_name = self._get_kridanta_name(form_code)
        self.set_kridanta_dict(kridanta_dict)

    def set_kridanta_dict(self, lakaar_dict):
        self.kridanta_dict = {name: Kridanta_Rupa(name, value) for name, value in lakaar_dict.items()}

    @classmethod
    def _get_kridanta_name(self, form_code):
        form_dict = {
            "shuddha_kridanta": "कृदन्ते",
            "san_kridanta": "सनि कृदन्ते",
            "nich_kridanta": "णिच् कृदन्ते",
            "yang_kridanta": "यङ् कृदन्ते",
            "yangluk_kridanta": "यङ्लुक् कृदन्ते",
        }
        return form_dict.get(form_code, "")