from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="SoS Güvenlik Beyni - Pre-Crime & Mobil",
    page_icon="🚨",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stMetric {background-color: #1e2530; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);}
    .stTabs [data-baseweb="tab-list"] {gap: 4px; font-size: 13px; overflow-x: auto;}
    .stTabs [data-baseweb="tab"] {padding: 6px 10px; white-space: nowrap;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem; padding-left: 0.9rem; padding-right: 0.9rem; max-width: 100%;}
    @media (max-width: 768px) {
        .row-widget.stHorizontal {flex-direction: column;}
    }
    </style>
""",
    unsafe_allow_html=True,
)

tr_saat_dilimi = ZoneInfo("Europe/Istanbul")
simdiki_zaman = datetime.now(tr_saat_dilimi)
tarih_str = simdiki_zaman.strftime("%d.%m.%Y")
saat_str = simdiki_zaman.strftime("%H:%M:%S")


@st.fragment(run_every=1)
def canli_saat_kutusu(hizalama: str = "flex-start"):
  guncel = datetime.now(tr_saat_dilimi)
  guncel_saat = guncel.strftime("%H:%M:%S")
  guncel_tarih = guncel.strftime("%d.%m.%Y")
  st.markdown(
      f"""
        <div style="display: flex; justify-content: {hizalama};">
            <div style="
                padding: 8px 14px;
                border-radius: 8px;
                border: 1px solid rgba(255, 75, 75, 0.35);
                background-color: rgba(30, 37, 48, 0.75);
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-variant-numeric: tabular-nums;
            ">
                <span style="color: #ff4b4b; font-weight: 700; font-size: 1.05rem;">⏱️ {guncel_saat}</span>
                <span style="color: #d0d7de; font-size: 0.88rem;">{guncel_tarih} • TR (UTC+3)</span>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )


TURKIYE_IL_ILCELER = {
    "Adana": [
        "Aladağ",
        "Ceyhan",
        "Çukurova",
        "Feke",
        "İmamoğlu",
        "Karaisalı",
        "Karataş",
        "Kozan",
        "Pozantı",
        "Saimbeyli",
        "Sarıçam",
        "Seyhan",
        "Tufanbeyli",
        "Yumurtalık",
        "Yüreğir",
    ],
    "Adıyaman": [
        "Besni",
        "Çelikhan",
        "Gerger",
        "Gölbaşı",
        "Kahta",
        "Merkez",
        "Samsat",
        "Sincik",
        "Tut",
    ],
    "Afyonkarahisar": [
        "Başmakçı",
        "Bayat",
        "Bolvadin",
        "Çay",
        "Çobanlar",
        "Dazkırı",
        "Dinar",
        "Emirdağ",
        "Evciler",
        "Hocalar",
        "İhsaniye",
        "İscehisar",
        "Kızılören",
        "Merkez",
        "Sandıklı",
        "Sinanpaşa",
        "Sultandağı",
        "Şuhut",
    ],
    "Ağrı": [
        "Diyadin",
        "Doğubayazıt",
        "Eleşkirt",
        "Hamur",
        "Merkez",
        "Patnos",
        "Taşlıçay",
        "Tutak",
    ],
    "Amasya": [
        "Göynücek",
        "Gümüşhacıköy",
        "Hamamözü",
        "Merkez",
        "Merzifon",
        "Suluova",
        "Taşova",
    ],
    "Ankara": [
        "Akyurt",
        "Altındağ",
        "Ayaş",
        "Bala",
        "Beypazarı",
        "Çamlıdere",
        "Çankaya",
        "Çubuk",
        "Elmadağ",
        "Etimesgut",
        "Evren",
        "Gölbaşı",
        "Güdül",
        "Haymana",
        "Kahramankazan",
        "Kalecik",
        "Keçiören",
        "Kızılcahamam",
        "Mamak",
        "Nallıhan",
        "Polatlı",
        "Pursaklar",
        "Sincan",
        "Şereflikoçhisar",
        "Yenimahalle",
    ],
    "Antalya": [
        "Akseki",
        "Aksu",
        "Alanya",
        "Demre",
        "Elmalı",
        "Finike",
        "Gazipaşa",
        "Gündoğmuş",
        "İbradı",
        "Kaş",
        "Kemer",
        "Kepez",
        "Konyaaltı",
        "Korkuteli",
        "Kumluca",
        "Manavgat",
        "Muratpaşa",
        "Serik",
    ],
    "Artvin": [
        "Ardanuç",
        "Arhavi",
        "Borçka",
        "Hopa",
        "Kemalpaşa",
        "Merkez",
        "Murgul",
        "Şavşat",
        "Yusufeli",
    ],
    "Aydın": [
        "Bozdoğan",
        "Buharkent",
        "Çine",
        "Didim",
        "Efeler",
        "Germencik",
        "İncirliova",
        "Karacasu",
        "Karpuzlu",
        "Koçarlı",
        "Köşk",
        "Kuşadası",
        "Kuyucak",
        "Nazilli",
        "Söke",
        "Sultanhisar",
        "Yenipazar",
    ],
    "Balıkesir": [
        "Altıeylül",
        "Ayvalık",
        "Balya",
        "Bandırma",
        "Bigadiç",
        "Burhaniye",
        "Dursunbey",
        "Edremit",
        "Erdek",
        "Gömeç",
        "Gönen",
        "Havran",
        "İvrindi",
        "Karesi",
        "Kepsut",
        "Manyas",
        "Marmara",
        "Savaştepe",
        "Sındırgı",
        "Susurluk",
    ],
    "Bilecik": [
        "Bozüyük",
        "Gölpazarı",
        "İnhisar",
        "Merkez",
        "Osmaneli",
        "Pazaryeri",
        "Söğüt",
        "Yenipazar",
    ],
    "Bingöl": [
        "Adaklı",
        "Genç",
        "Karlıova",
        "Kiğı",
        "Merkez",
        "Solhan",
        "Yayladere",
        "Yedisu",
    ],
    "Bitlis": [
        "Adilcevaz",
        "Ahlat",
        "Güroymak",
        "Hizan",
        "Merkez",
        "Mutki",
        "Tatvan",
    ],
    "Bolu": [
        "Dörtdivan",
        "Gerede",
        "Göynük",
        "Kıbrıscık",
        "Mengen",
        "Merkez",
        "Mudurnu",
        "Seben",
        "Yeniçağa",
    ],
    "Burdur": [
        "Ağlasun",
        "Altınyayla",
        "Bucak",
        "Çavdır",
        "Çeltikçi",
        "Gölhisar",
        "Karamanlı",
        "Kemer",
        "Merkez",
        "Tefenni",
        "Yeşilova",
    ],
    "Bursa": [
        "Büyükorhan",
        "Gemlik",
        "Gürsu",
        "Harmancık",
        "İnegöl",
        "İznik",
        "Karacabey",
        "Keles",
        "Kestel",
        "Mudanya",
        "Mustafakemalpaşa",
        "Nilüfer",
        "Orhaneli",
        "Orhangazi",
        "Osmangazi",
        "Yenişehir",
        "Yıldırım",
    ],
    "Çanakkale": [
        "Ayvacık",
        "Bayramiç",
        "Biga",
        "Bozcaada",
        "Çan",
        "Merkez",
        "Eceabat",
        "Ezine",
        "Gelibolu",
        "Gökçeada",
        "Lapseki",
        "Yenice",
    ],
    "Çankırı": [
        "Atkaracalar",
        "Bayramören",
        "Merkez",
        "Çerkeş",
        "Eldivan",
        "Ilgaz",
        "Kızılırmak",
        "Korgun",
        "Kurşunlu",
        "Orta",
        "Şabanözü",
        "Yapraklı",
    ],
    "Çorum": [
        "Alaca",
        "Bayat",
        "Boğazkale",
        "Merkez",
        "Dodurga",
        "İskilip",
        "Kargı",
        "Laçin",
        "Mecitözü",
        "Oğuzlar",
        "Ortaköy",
        "Osmancık",
        "Sungurlu",
        "Uğurludağ",
    ],
    "Denizli": [
        "Acıpayam",
        "Babadağ",
        "Baklan",
        "Bekilli",
        "Beyağaç",
        "Bozkurt",
        "Buldan",
        "Çal",
        "Çameli",
        "Çardak",
        "Çivril",
        "Güney",
        "Honaz",
        "Kale",
        "Merkezefendi",
        "Pamukkale",
        "Sarayköy",
        "Serinhisar",
        "Tavas",
    ],
    "Diyarbakır": [
        "Bağlar",
        "Bismil",
        "Çermik",
        "Çınar",
        "Çüngüş",
        "Dicle",
        "Eğil",
        "Ergani",
        "Hani",
        "Hazro",
        "Kayapınar",
        "Kulp",
        "Lice",
        "Silvan",
        "Sur",
        "Yenişehir",
    ],
    "Edirne": [
        "Enez",
        "Havsa",
        "İpsala",
        "Keşan",
        "Lalapaşa",
        "Meriç",
        "Merkez",
        "Süloğlu",
        "Uzunköprü",
    ],
    "Elazığ": [
        "Ağın",
        "Alacakaya",
        "Arıcak",
        "Baskil",
        "Merkez",
        "Karakoçan",
        "Keban",
        "Kovancılar",
        "Maden",
        "Palu",
        "Sivrice",
    ],
    "Erzincan": [
        "Çayırlı",
        "Merkez",
        "İliç",
        "Kemah",
        "Kemaliye",
        "Otlukbeli",
        "Refahiye",
        "Tercan",
        "Üzümlü",
    ],
    "Erzurum": [
        "Aşkale",
        "Aziziye",
        "Çat",
        "Hınıs",
        "Horasan",
        "İspir",
        "Karaçoban",
        "Karayazı",
        "Köprüköy",
        "Narman",
        "Oltu",
        "Olur",
        "Palandöken",
        "Pasinler",
        "Pazaryolu",
        "Şenkaya",
        "Tekman",
        "Tortum",
        "Uzundere",
        "Yakutiye",
    ],
    "Eskişehir": [
        "Alpu",
        "Beylikova",
        "Çifteler",
        "Günyüzü",
        "Han",
        "İnönü",
        "Mahmudiye",
        "Mihalgazi",
        "Mihalıççık",
        "Odunpazarı",
        "Sarıcakaya",
        "Seyitgazi",
        "Sivrihisar",
        "Tepebaşı",
    ],
    "Gaziantep": [
        "Araban",
        "İslahiye",
        "Karkamış",
        "Nizip",
        "Nurdağı",
        "Oğuzeli",
        "Şahinbey",
        "Şehitkamil",
        "Yavuzeli",
    ],
    "Giresun": [
        "Alucra",
        "Bulancak",
        "Çamoluk",
        "Çanakçı",
        "Dereli",
        "Doğankent",
        "Espiye",
        "Eynesil",
        "Merkez",
        "Görele",
        "Güce",
        "Keşap",
        "Piraziz",
        "Şebinkarahisar",
        "Tirebolu",
        "Yağlıdere",
    ],
    "Gümüşhane": ["Kelkit", "Köse", "Kürtün", "Merkez", "Şiran", "Torul"],
    "Hakkâri": ["Çukurca", "Derecik", "Merkez", "Şemdinli", "Yüksekova"],
    "Hatay": [
        "Altınözü",
        "Antakya",
        "Arsuz",
        "Belen",
        "Defne",
        "Dörtyol",
        "Erzin",
        "Hassa",
        "İskenderun",
        "Kırıkhan",
        "Kumlu",
        "Payas",
        "Reyhanlı",
        "Samandağ",
        "Yayladağı",
    ],
    "Iğdır": ["Aralık", "Karakoyunlu", "Merkez", "Tuzluca"],
    "Isparta": [
        "Aksu",
        "Atabey",
        "Eğirdir",
        "Gelendost",
        "Gönen",
        "Keçiborlu",
        "Merkez",
        "Senirkent",
        "Sütçüler",
        "Şarkikaraağaç",
        "Uluborlu",
        "Yalvaç",
        "Yenişarbademli",
    ],
    "İstanbul": [
        "Adalar",
        "Arnavutköy",
        "Ataşehir",
        "Avcılar",
        "Bağcılar",
        "Bahçelievler",
        "Bakırköy",
        "Başakşehir",
        "Bayrampaşa",
        "Beşiktaş",
        "Beykoz",
        "Beylikdüzü",
        "Beyoğlu",
        "Büyükçekmece",
        "Çatalca",
        "Çekmeköy",
        "Esenler",
        "Esenyurt",
        "Eyüpsultan",
        "Fatih",
        "Gaziosmanpaşa",
        "Güngören",
        "Kadıköy",
        "Kağıthane",
        "Kartal",
        "Küçükçekmece",
        "Maltepe",
        "Pendik",
        "Sancaktepe",
        "Sarıyer",
        "Silivri",
        "Sultanbeyli",
        "Sultangazi",
        "Şile",
        "Şişli",
        "Tuzla",
        "Ümraniye",
        "Üsküdar",
        "Zeytinburnu",
    ],
    "İzmir": [
        "Aliağa",
        "Balçova",
        "Bayındır",
        "Bayraklı",
        "Bergama",
        "Beydağ",
        "Bornova",
        "Buca",
        "Çeşme",
        "Çiğli",
        "Dikili",
        "Foça",
        "Gaziemir",
        "Güzelbahçe",
        "Karabağlar",
        "Karaburun",
        "Karşıyaka",
        "Kemalpaşa",
        "Kınık",
        "Kiraz",
        "Konak",
        "Menderes",
        "Menemen",
        "Narlıdere",
        "Ödemiş",
        "Seferihisar",
        "Selçuk",
        "Tire",
        "Torbalı",
        "Urla",
    ],
    "Kahramanmaraş": [
        "Afşin",
        "Andırın",
        "Çağlayancerit",
        "Dulkadiroğlu",
        "Ekinözü",
        "Elbistan",
        "Göksun",
        "Nurhak",
        "Onikişubat",
        "Pazarcık",
        "Türkoğlu",
    ],
    "Karabük": ["Eflani", "Eskipazar", "Merkez", "Ovacık", "Safranbolu", "Yenice"],
    "Karaman": [
        "Ayrancı",
        "Başyayla",
        "Ermenek",
        "Kazımkarabekir",
        "Merkez",
        "Sarıveliler",
    ],
    "Kars": [
        "Akyaka",
        "Arpaçay",
        "Digor",
        "Kağızman",
        "Merkez",
        "Sarıkamış",
        "Selim",
        "Susuz",
    ],
    "Kastamonu": [
        "Abana",
        "Ağlı",
        "Araç",
        "Azdavay",
        "Bozkurt",
        "Cide",
        "Çatalzeytin",
        "Daday",
        "Devrekani",
        "Doğanyurt",
        "Hanönü",
        "İhsangazi",
        "İnebolu",
        "Merkez",
        "Küre",
        "Pınarbaşı",
        "Seydiler",
        "Şenpazar",
        "Taşköprü",
        "Tosya",
    ],
    "Kayseri": [
        "Akkışla",
        "Bünyan",
        "Develi",
        "Felahiye",
        "Hacılar",
        "İncesu",
        "Kocasinan",
        "Melikgazi",
        "Özvatan",
        "Pınarbaşı",
        "Sarıoğlan",
        "Sarız",
        "Talas",
        "Tomarza",
        "Yahyalı",
        "Yeşilhisar",
    ],
    "Kilis": ["Elbeyli", "Merkez", "Musabeyli", "Polateli"],
    "Kırıkkale": [
        "Bahşılı",
        "Balışeyh",
        "Çelebi",
        "Delice",
        "Karakeçili",
        "Keskin",
        "Merkez",
        "Sulakyurt",
        "Yahşihan",
    ],
    "Kırklareli": [
        "Babaeski",
        "Demirköy",
        "Kofçaz",
        "Lüleburgaz",
        "Merkez",
        "Pehlivanköy",
        "Pınarhisar",
        "Vize",
    ],
    "Kırşehir": [
        "Akçakent",
        "Akpınar",
        "Boztepe",
        "Çiçekdağı",
        "Kaman",
        "Merkez",
        "Mucur",
    ],
    "Kocaeli": [
        "Başiskele",
        "Çayırova",
        "Darıca",
        "Derince",
        "Dilovası",
        "Gebze",
        "Gölcük",
        "İzmit",
        "Kandıra",
        "Karamürsel",
        "Kartepe",
        "Körfez",
    ],
    "Konya": [
        "Ahırlı",
        "Akören",
        "Akşehir",
        "Altınekin",
        "Beyşehir",
        "Bozkır",
        "Cihanbeyli",
        "Çeltik",
        "Çumra",
        "Derbent",
        "Derebucak",
        "Doğanhisar",
        "Emirgazi",
        "Ereğli",
        "Güneysınır",
        "Hadim",
        "Halkapınar",
        "Hüyük",
        "Ilgın",
        "Kadınhanı",
        "Karapınar",
        "Karatay",
        "Kulu",
        "Meram",
        "Sarayönü",
        "Selçuklu",
        "Seydişehir",
        "Taşkent",
        "Tuzlukçu",
        "Yalıhüyük",
        "Yunak",
    ],
    "Kütahya": [
        "Altıntaş",
        "Aslanapa",
        "Çavdarhisar",
        "Domaniç",
        "Dumlupınar",
        "Emet",
        "Gediz",
        "Hisarcık",
        "Merkez",
        "Pazarlar",
        "Simav",
        "Tavşanlı",
    ],
    "Malatya": [
        "Akçadağ",
        "Arapgir",
        "Arguvan",
        "Battalgazi",
        "Darende",
        "Doğanşehir",
        "Doğanyol",
        "Hekimhan",
        "Kale",
        "Pütürge",
        "Yazıhan",
        "Yeşilyurt",
    ],
    "Manisa": [
        "Ahmetli",
        "Akhisar",
        "Alaşehir",
        "Demirci",
        "Gölmarmara",
        "Gördes",
        "Kırkağaç",
        "Kula",
        "Salihli",
        "Sarıgöl",
        "Saruhanlı",
        "Selendi",
        "Soma",
        "Şehzadeler",
        "Turgutlu",
        "Yunusemre",
    ],
    "Mardin": [
        "Artuklu",
        "Dargeçit",
        "Derik",
        "Kızıltepe",
        "Mazıdağı",
        "Midyat",
        "Nusaybin",
        "Ömerli",
        "Savur",
        "Yeşilli",
    ],
    "Mersin": [
        "Akdeniz",
        "Anamur",
        "Aydıncık",
        "Bozyazı",
        "Çamlıyayla",
        "Erdemli",
        "Gülnar",
        "Mezitli",
        "Silifke",
        "Tarsus",
        "Toroslar",
        "Yenişehir",
    ],
    "Muğla": [
        "Bodrum",
        "Dalaman",
        "Datça",
        "Fethiye",
        "Kavaklıdere",
        "Köyceğiz",
        "Marmaris",
        "Menteşe",
        "Milas",
        "Ortaca",
        "Seydikemer",
        "Ula",
        "Yatağan",
    ],
    "Muş": ["Bulanık", "Hasköy", "Korkut", "Malazgirt", "Merkez", "Varto"],
    "Nevşehir": [
        "Acıgöl",
        "Avanos",
        "Derinkuyu",
        "Gülşehir",
        "Hacıbektaş",
        "Kozaklı",
        "Merkez",
        "Ürgüp",
    ],
    "Niğde": ["Altunhisar", "Bor", "Çamardı", "Çiftlik", "Merkez", "Ulukışla"],
    "Ordu": [
        "Akkuş",
        "Altınordu",
        "Aybastı",
        "Çamaş",
        "Çatalpınar",
        "Çaybaşı",
        "Fatsa",
        "Gölköy",
        "Gülyalı",
        "Gürgentepe",
        "İkizce",
        "Kabadüz",
        "Kabataş",
        "Korgan",
        "Kumru",
        "Mesudiye",
        "Perşembe",
        "Ulubey",
        "Ünye",
    ],
    "Osmaniye": [
        "Bahçe",
        "Düziçi",
        "Hasanbeyli",
        "Kadirli",
        "Merkez",
        "Toprakkale",
    ],
    "Rize": [
        "Ardeşen",
        "Çamlıhemşin",
        "Çayeli",
        "Derepazarı",
        "Fındıklı",
        "Güneysu",
        "Hemşin",
        "İkizdere",
        "İyidere",
        "Kalkandere",
        "Merkez",
        "Pazar",
    ],
    "Sakarya": [
        "Akyazı",
        "Arifiye",
        "Erenler",
        "Ferizli",
        "Geyve",
        "Hendek",
        "Karapürçek",
        "Karasu",
        "Kaynarca",
        "Kocaali",
        "Pamukova",
        "Sapanca",
        "Serdivan",
        "Söğütlü",
        "Taraklı",
    ],
    "Samsun": [
        "Alaçam",
        "Asarcık",
        "Atakum",
        "Ayvacık",
        "Bafra",
        "Canik",
        "Çarşamba",
        "Havza",
        "Kavak",
        "Ladik",
        "Ondokuzmayıs",
        "Salıpazarı",
        "Tekkeköy",
        "Terme",
        "Vezirköprü",
        "Yakakent",
    ],
    "Siirt": ["Baykan", "Eruh", "Kurtalan", "Merkez", "Pervari", "Şirvan", "Tillo"],
    "Sinop": [
        "Ayancık",
        "Boyabat",
        "Dikmen",
        "Durağan",
        "Erfelek",
        "Gerze",
        "Merkez",
        "Saraydüzü",
        "Türkeli",
    ],
    "Sivas": [
        "Akıncılar",
        "Altınyayla",
        "Divriği",
        "Doğanşar",
        "Gemerek",
        "Gürün",
        "Hafik",
        "İmranlı",
        "Kangal",
        "Koyulhisar",
        "Merkez",
        "Suşehri",
        "Şarkışla",
        "Ulaş",
        "Yıldızeli",
        "Zara",
    ],
    "Şanlıurfa": [
        "Akçakale",
        "Birecik",
        "Bozova",
        "Ceylanpınar",
        "Eyyübiye",
        "Halfeti",
        "Haliliye",
        "Harran",
        "Hilvan",
        "Karaköprü",
        "Siverek",
        "Suruç",
        "Viranşehir",
    ],
    "Şırnak": [
        "Beytüşşebap",
        "Cizre",
        "Güçlükonak",
        "İdil",
        "Silopi",
        "Merkez",
        "Uludere",
    ],
    "Tekirdağ": [
        "Çerkezköy",
        "Çorlu",
        "Ergene",
        "Hayrabolu",
        "Kapaklı",
        "Malkara",
        "Marmaraereğlisi",
        "Muratlı",
        "Saray",
        "Süleymanpaşa",
        "Şarköy",
    ],
    "Tokat": [
        "Almus",
        "Artova",
        "Başçiftlik",
        "Erbaa",
        "Niksar",
        "Pazar",
        "Reşadiye",
        "Sulusaray",
        "Merkez",
        "Turhal",
        "Yeşilyurt",
        "Zile",
    ],
    "Trabzon": [
        "Akçaabat",
        "Araklı",
        "Arsin",
        "Beşikdüzü",
        "Çarşıbaşı",
        "Çaykara",
        "Dernekpazarı",
        "Düzköy",
        "Hayrat",
        "Köprübaşı",
        "Maçka",
        "Of",
        "Ortahisar",
        "Sürmene",
        "Şalpazarı",
        "Tonya",
        "Vakfıkebir",
        "Yomra",
    ],
    "Tunceli": [
        "Çemişgezek",
        "Hozat",
        "Mazgirt",
        "Merkez",
        "Nazımiye",
        "Ovacık",
        "Pertek",
        "Pülümür",
    ],
    "Uşak": ["Banaz", "Eşme", "Karahallı", "Merkez", "Sivaslı", "Ulubey"],
    "Van": [
        "Bahçesaray",
        "Başkale",
        "Çaldıran",
        "Çatak",
        "Edremit",
        "Erciş",
        "Gevaş",
        "Gürpınar",
        "İpekyolu",
        "Muradiye",
        "Özalp",
        "Saray",
        "Tuşba",
    ],
    "Yalova": [
        "Altınova",
        "Armutlu",
        "Çiftlikköy",
        "Çınarcık",
        "Termal",
        "Merkez",
    ],
    "Yozgat": [
        "Akdağmadeni",
        "Aydıncık",
        "Boğazlıyan",
        "Çandır",
        "Çayıralan",
        "Çekerek",
        "Kadışehri",
        "Merkez",
        "Saraykent",
        "Sorgun",
        "Şefaatli",
        "Yenifakılı",
        "Yerköy",
    ],
    "Zonguldak": [
        "Alaplı",
        "Çaycuma",
        "Devrek",
        "Gökçebey",
        "Kozlu",
        "Merkez",
        "Karadeniz Ereğli",
    ],
    "Düzce": [
        "Akçakoca",
        "Cumayeri",
        "Çilimli",
        "Gölyaka",
        "Gümüşova",
        "Kaynaşlı",
        "Merkez",
        "Yığılca",
    ],
}

IL_KOORDINATLARI = {
    "Adana": (37.00, 35.32),
    "Adıyaman": (37.76, 38.27),
    "Afyonkarahisar": (38.75, 30.55),
    "Ağrı": (39.71, 43.05),
    "Amasya": (40.64, 35.83),
    "Ankara": (39.93, 32.85),
    "Antalya": (36.88, 30.70),
    "Artvin": (41.18, 41.81),
    "Aydın": (37.85, 27.84),
    "Balıkesir": (39.64, 27.88),
    "Bilecik": (40.15, 29.97),
    "Bingöl": (38.88, 40.49),
    "Bitlis": (38.40, 42.10),
    "Bolu": (40.73, 31.60),
    "Burdur": (37.72, 30.29),
    "Bursa": (40.18, 29.06),
    "Çanakkale": (40.15, 26.41),
    "Çankırı": (40.60, 33.61),
    "Çorum": (40.55, 34.95),
    "Denizli": (37.77, 29.08),
    "Diyarbakır": (37.91, 40.23),
    "Edirne": (41.67, 26.55),
    "Elazığ": (38.68, 39.22),
    "Erzincan": (39.75, 39.50),
    "Erzurum": (39.90, 41.26),
    "Eskişehir": (39.77, 30.52),
    "Gaziantep": (37.06, 37.38),
    "Giresun": (40.91, 38.38),
    "Gümüşhane": (40.46, 39.48),
    "Hakkâri": (37.58, 43.73),
    "Hatay": (36.20, 36.16),
    "Isparta": (37.76, 30.55),
    "Mersin": (36.80, 34.63),
    "İstanbul": (41.00, 28.97),
    "İzmir": (38.41, 27.12),
    "Kars": (40.61, 43.10),
    "Kastamonu": (41.38, 33.78),
    "Kayseri": (38.73, 35.47),
    "Kırklareli": (41.73, 27.21),
    "Kırşehir": (39.14, 34.17),
    "Kocaeli": (40.85, 29.88),
    "Konya": (37.87, 32.48),
    "Kütahya": (39.41, 29.98),
    "Malatya": (38.35, 38.30),
    "Manisa": (38.61, 27.42),
    "Kahramanmaraş": (37.58, 36.93),
    "Mardin": (37.32, 40.72),
    "Muğla": (37.21, 28.36),
    "Muş": (38.74, 41.50),
    "Nevşehir": (38.62, 34.71),
    "Niğde": (37.96, 34.68),
    "Ordu": (40.98, 37.87),
    "Rize": (41.02, 40.52),
    "Sakarya": (40.75, 30.37),
    "Samsun": (41.29, 36.33),
    "Siirt": (37.93, 41.95),
    "Sinop": (42.02, 35.15),
    "Sivas": (39.74, 37.01),
    "Tekirdağ": (40.98, 27.51),
    "Tokat": (40.31, 36.55),
    "Trabzon": (41.00, 39.71),
    "Tunceli": (39.10, 39.54),
    "Şanlıurfa": (37.16, 38.79),
    "Uşak": (38.68, 29.40),
    "Van": (38.48, 43.40),
    "Yozgat": (39.81, 34.81),
    "Zonguldak": (41.45, 31.79),
    "Aksaray": (38.36, 34.03),
    "Bayburt": (40.25, 40.22),
    "Karaman": (37.17, 33.22),
    "Kırıkkale": (39.84, 33.51),
    "Batman": (37.88, 41.13),
    "Şırnak": (37.51, 42.46),
    "Bartın": (41.63, 32.33),
    "Ardahan": (41.11, 42.70),
    "Iğdır": (39.91, 44.03),
    "Yalova": (40.65, 29.27),
    "Karabük": (41.20, 32.62),
    "Kilis": (36.71, 37.12),
    "Osmaniye": (37.07, 36.24),
    "Düzce": (40.84, 31.15),
}

nufus_agirliklari = {
    "İstanbul": 0.185,
    "Ankara": 0.080,
    "İzmir": 0.053,
    "Bursa": 0.038,
    "Antalya": 0.032,
    "Konya": 0.027,
    "Adana": 0.026,
    "Şanlıurfa": 0.026,
    "Gaziantep": 0.025,
    "Kocaeli": 0.024,
    "Mersin": 0.022,
    "Diyarbakır": 0.021,
    "Hatay": 0.019,
    "Manisa": 0.018,
    "Kayseri": 0.017,
    "Samsun": 0.016,
    "Balıkesir": 0.015,
    "Kahramanmaraş": 0.014,
    "Van": 0.013,
    "Aydın": 0.013,
    "Tekirdağ": 0.013,
    "Sakarya": 0.012,
    "Denizli": 0.012,
    "Muğla": 0.012,
    "Eskişehir": 0.011,
    "Mardin": 0.010,
    "Trabzon": 0.010,
    "Malatya": 0.009,
    "Erzurum": 0.009,
    "Ordu": 0.009,
}
tum_iller = list(TURKIYE_IL_ILCELER.keys())
agirliklar = np.array(
    [nufus_agirliklari.get(il, 0.003) for il in tum_iller], dtype=np.float32
)
agirliklar /= agirliklar.sum()


@st.cache_data(show_spinner="Veriler hazırlanıyor...")
def veriyi_yukle(n: int = 150000):
  secilen_iller = np.random.choice(tum_iller, size=n, p=agirliklar)

  ad_havuzu = np.array([
      "Ahmet",
      "Mehmet",
      "Ali",
      "Mustafa",
      "Emre",
      "Burak",
      "Can",
      "Kemal",
      "Murat",
      "Hakan",
      "Yusuf",
      "Fatma",
      "Ayşe",
      "Zeynep",
      "Elif",
      "Merve",
      "Esra",
      "Kaan",
      "Deniz",
      "Kerem",
      "Oğuz",
      "Serkan",
      "Büşra",
      "Cemre",
      "Volkan",
      "Gökhan",
      "Sibel",
      "Tarik",
  ])
  soyad_havuzu = np.array([
      "Yılmaz",
      "Kaya",
      "Demir",
      "Şahin",
      "Çelik",
      "Yıldız",
      "Yıldırım",
      "Öztürk",
      "Aydın",
      "Özdemir",
      "Arslan",
      "Doğan",
      "Kılıç",
      "Aslan",
      "Çetin",
      "Kara",
      "Koç",
      "Kurt",
      "Özkan",
      "Polat",
      "Aksoy",
      "Şen",
  ])

  ad_soyadlar = (
      np.random.choice(ad_havuzu, size=n)
      + " "
      + np.random.choice(soyad_havuzu, size=n)
  )

  base_lats = np.array(
      [IL_KOORDINATLARI[il][0] for il in secilen_iller], dtype=np.float32
  )
  base_lons = np.array(
      [IL_KOORDINATLARI[il][1] for il in secilen_iller], dtype=np.float32
  )

  lats = np.clip(
      base_lats + np.random.uniform(-0.35, 0.35, size=n).astype(np.float32),
      35.85,
      42.10,
  )
  lons = np.clip(
      base_lons + np.random.uniform(-0.35, 0.35, size=n).astype(np.float32),
      25.65,
      44.80,
  )

  ilceler = np.array(
      [np.random.choice(TURKIYE_IL_ILCELER[il]) for il in secilen_iller]
  )
  mahalleler = ilceler + " Mah. " + np.random.randint(1, 40, size=n).astype(str)

  gecmis_ikametler = np.where(
      np.random.rand(n) > 0.5,
      secilen_iller + " bölgesinde uzun süredir ikamet ediyor.",
      "Çoklu İl Değişikliği (Aktif Hareketlilik)",
  )

  df = pd.DataFrame({
      "TC_No": np.random.randint(
          10000000000, 99999999999, size=n, dtype=np.int64
      ),
      "Ad_Soyad": ad_soyadlar,
      "Vatandaslik_Durumu": pd.Categorical(
          np.random.choice(
              ["T.C. Vatandaşı", "Yabancı Uyruklu"], size=n, p=[0.93, 0.07]
          )
      ),
      "Ikamet_Ili": pd.Categorical(secilen_iller),
      "Ikamet_Ilcesi": pd.Categorical(ilceler),
      "Ikamet_Mahalle": mahalleler,
      "Gecmis_Ikamet_Gecmisi": gecmis_ikametler,
      "lat": lats,
      "lon": lons,
      "Tor_I2P_Kullanimi": pd.Categorical(
          np.random.choice(
              ["Yok", "Var (Şifreli Ağ)"], size=n, p=[0.95, 0.05]
          )
      ),
      "DarkWeb_Aramasi_Patlayici": pd.Categorical(
          np.random.choice(
              ["Yok", "Tespit Edildi!"], size=n, p=[0.985, 0.015]
          )
      ),
      "Kritik_Tesis_Kesfi": pd.Categorical(
          np.random.choice(
              ["Yok", "Var (Askeri/Valilik Etrafı Dolaşım)"],
              size=n,
              p=[0.96, 0.04],
          )
      ),
      "Sahte_Ikiz_Plaka": pd.Categorical(
          np.random.choice(
              ["Normal", "Aynı Anda Farklı İlde İkiz Plaka!"],
              size=n,
              p=[0.99, 0.01],
          )
      ),
      "Adli_Sicil_Kaydi": pd.Categorical(
          np.random.choice(
              ["Temiz", "Organize Suç", "Terör İltisakı", "Kaçakçılık"],
              size=n,
              p=[0.90, 0.04, 0.03, 0.03],
          )
      ),
  })

  il_risk_katmani = np.array(
      [nufus_agirliklari.get(il, 0.003) * 12.0 for il in secilen_iller],
      dtype=np.float32,
  )

  skor = np.ones(n, dtype=np.float32) * 1.5 + np.clip(
      il_risk_katmani, 0.0, 2.2
  )
  skor += (df["Tor_I2P_Kullanimi"] == "Var (Şifreli Ağ)").astype(
      np.float32
  ) * 1.5
  skor += (df["DarkWeb_Aramasi_Patlayici"] == "Tespit Edildi!").astype(
      np.float32
  ) * 3.5
  skor += (
      df["Kritik_Tesis_Kesfi"] == "Var (Askeri/Valilik Etrafı Dolaşım)"
  ).astype(np.float32) * 2.5
  skor += (df["Sahte_Ikiz_Plaka"] == "Aynı Anda Farklı İlde İkiz Plaka!").astype(
      np.float32
  ) * 3.0
  skor += (
      df["Adli_Sicil_Kaydi"].isin(["Organize Suç", "Terör İltisakı"]).astype(
          np.float32
      )
      * 2.0
  )

  df["Hesaplanan_Anomali_Skoru"] = np.clip(
      skor + np.random.uniform(-0.3, 0.3, size=n).astype(np.float32), 1.0, 10.0
  )

  suc_havuzu = np.array([
      "Kritik Altyapı / Tesis Sabotajı",
      "Siber C2 Altyapı Sızması",
      "Finansal Smurfing / Kara Para",
      "Yasadışı Lojistik / Sevkiyat",
      "Organize Tehdit / Faaliyet",
  ])
  zaman_havuzu = np.array([
      "⚡ 12 - 24 Saat İçinde Kritik Eşik",
      "⏳ 2 - 4 Gün İçinde Eylem Hazırlığı",
      "📅 1 Hafta+ Uzun Vadeli İzleme",
      "🔍 Pasif / Sinyal Toplama Evresi",
  ])
  niyet_havuzu = np.array([
      "Finansal likidite sağlama ve dijital izleri gizleme eğiliminde.",
      "Keşif faaliyeti yürüterek fiziksel güvenlik açıklarını haritalandırıyor.",
      (
          "Şifreli ağlar üzerinden komuta kontrol merkezi ile eş zamanlı"
          " iletişimde."
      ),
      (
          "Operasyonel hazırlık aşamasında, sinyal sessizliği protokolüne"
          " geçiyor."
      ),
  ])

  df["Muhtemel_Suc_Turu"] = pd.Categorical(
      np.random.choice(suc_havuzu, size=n)
  )
  df["Eylem_Zamani_Projeksiyonu"] = pd.Categorical(
      np.random.choice(zaman_havuzu, size=n)
  )
  df["Zihinsel_Niyet_Analizi"] = np.random.choice(niyet_havuzu, size=n)

  conditions = [
      df["Hesaplanan_Anomali_Skoru"] >= 8.5,
      (df["Hesaplanan_Anomali_Skoru"] >= 7.0)
      & (df["Hesaplanan_Anomali_Skoru"] < 8.5),
      (df["Hesaplanan_Anomali_Skoru"] >= 5.0)
      & (df["Hesaplanan_Anomali_Skoru"] < 7.0),
      df["Hesaplanan_Anomali_Skoru"] < 5.0,
  ]
  choices = [
      "⬛ Siyah (Kritik Tehdit)",
      "🔴 Kırmızı (Yüksek Risk)",
      "🟠 Turuncu (Orta Risk)",
      "🟡 Sarı (İzleme Düzeyi)",
  ]
  df["Risk_Seviyesi"] = pd.Categorical(
      np.select(conditions, choices, default="🟡 Sarı (İzleme Düzeyi)")
  )

  return df


df = veriyi_yukle()

st.sidebar.title("🚨 Sistem Kontrol Merkezi")
with st.sidebar:
  canli_saat_kutusu("flex-start")
st.sidebar.markdown("---")

secilen_iller = st.sidebar.multiselect(
    "1. İl Seçimi",
    options=sorted(TURKIYE_IL_ILCELER.keys()),
    default=[],
    key="secilen_iller_ms",
)

if secilen_iller:
  musait_ilceler = sorted(
      list(
          set(
              ilce
              for il in secilen_iller
              for ilce in TURKIYE_IL_ILCELER.get(il, [])
          )
      )
  )
else:
  musait_ilceler = sorted(df["Ikamet_Ilcesi"].astype(str).unique())

secilen_ilceler = st.sidebar.multiselect(
    "2. İlçe Seçimi", options=musait_ilceler, default=[], key="secilen_ilceler_ms"
)

if secilen_ilceler:
  musait_mahalleler = sorted(
      df[df["Ikamet_Ilcesi"].isin(secilen_ilceler)]["Ikamet_Mahalle"]
      .astype(str)
      .unique()
  )
elif secilen_iller:
  musait_mahalleler = sorted(
      df[df["Ikamet_Ili"].isin(secilen_iller)]["Ikamet_Mahalle"]
      .astype(str)
      .unique()
  )
else:
  musait_mahalleler = sorted(df["Ikamet_Mahalle"].astype(str).unique())

secilen_mahalleler = st.sidebar.multiselect(
    "3. Mahalle / Köy Seçimi",
    options=musait_mahalleler,
    default=[],
    key="secilen_mahalleler_ms",
)

risk_esigi = st.sidebar.slider(
    "Minimum Risk Skoru Eşiği",
    min_value=1.0,
    max_value=10.0,
    value=6.0,
    step=0.5,
    key="risk_esigi_sl",
)

mask = df["Hesaplanan_Anomali_Skoru"] >= risk_esigi
if secilen_iller:
  mask &= df["Ikamet_Ili"].isin(secilen_iller)
if secilen_ilceler:
  mask &= df["Ikamet_Ilcesi"].isin(secilen_ilceler)
if secilen_mahalleler:
  mask &= df["Ikamet_Mahalle"].isin(secilen_mahalleler)

süzülmüş_df = df[mask]

col_baslik, col_zaman = st.columns([3, 1])
with col_baslik:
  st.title("🚨 T.C. Güvenlik Beyni - Pre-Crime & Niyet Analitiği")
with col_zaman:
  canli_saat_kutusu("flex-end")

tab1, tab2, tab3 = st.tabs([
    "🗺️ Türkiye Anomali Haritası & Akış",
    "🎯 Risk Hiyerarşisi & Pre-Crime Tahminleri",
    "🔍 Bireysel Profil, Suç ve Niyet Raporu",
])

with tab1:
  m1, m2, m3 = st.columns(3)
  m1.metric("Toplam İzlenen Profil", f"{len(df):,}")
  m2.metric("Filtrelenen Şüpheli Sayısı", f"{len(süzülmüş_df):,}")
  m3.metric(
      "Kritik Alarm Sayısı (Siyah/Kırmızı)",
      f"{(süzülmüş_df['Hesaplanan_Anomali_Skoru'] >= 7.0).sum():,}",
  )

  st.markdown("---")
  col_harita, col_alarm = st.columns([2, 1])

  with col_harita:
    st.subheader("🗺️ Türkiye Sınırları Anomali Yoğunluğu")
    harita_df = (
        süzülmüş_df.sort_values(
            by="Hesaplanan_Anomali_Skoru", ascending=False
        )
        .head(2000)
        .copy()
    )

    harita_df["color_r"] = np.where(
        harita_df["Hesaplanan_Anomali_Skoru"] >= 8.5, 30, 255
    )
    harita_df["color_g"] = np.where(
        harita_df["Hesaplanan_Anomali_Skoru"] >= 8.5, 30, 0
    )
    harita_df["color_b"] = 30

    layer = pdk.Layer(
        "ScatterplotLayer",
        harita_df,
        get_position=["lon", "lat"],
        get_color=["color_r", "color_g", "color_b", 200],
        get_radius="Hesaplanan_Anomali_Skoru * 800",
        pickable=True,
        radius_scale=6,
        radius_min_pixels=4,
        radius_max_pixels=20,
    )

    view_state = pdk.ViewState(
        latitude=39.0,
        longitude=35.2,
        zoom=5.6,
        min_zoom=5.2,
        max_zoom=12.0,
        pitch=15,
    )
    r = pdk.Deck(
        map_style=None,
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": (
                "<b>Şüpheli:</b> {Ad_Soyad}<br/><b>Muhtemel Suç:</b>"
                " {Muhtemel_Suc_Turu}<br/><b>Zaman:</b>"
                " {Eylem_Zamani_Projeksiyonu}"
            )
        },
    )
    st.pydeck_chart(r)

  with col_alarm:
    st.subheader("🔔 Anlık Tehdit Akışı & TR Zaman Damgası")
    en_riskli = süzülmüş_df.sort_values(
        by="Hesaplanan_Anomali_Skoru", ascending=False
    ).head(5)
    for idx, row in en_riskli.iterrows():
      with st.expander(f"{row['Risk_Seviyesi']} - {row['Ad_Soyad']}"):
        st.write(f"**Hedef Suç:** {row['Muhtemel_Suc_Turu']}")
        st.write(f"**Zaman Projeksiyonu:** {row['Eylem_Zamani_Projeksiyonu']}")
        st.write(f"**Tespit Zamanı (TR):** {saat_str} ({tarih_str})")
        if st.button(
            "🚨 Önleyici Müdahale Başlat", key=f"btn_sevk_{row['TC_No']}_{idx}"
        ):
          st.success(
              f"[{saat_str} TR] {row['Ad_Soyad']} için önleyici saha"
              " operasyonu tetiklendi!"
          )

with tab2:
  st.subheader("🎯 Pre-Crime & Suç Eğilimi Matrisi")
  sirali_liste = süzülmüş_df.sort_values(
      by="Hesaplanan_Anomali_Skoru", ascending=False
  )

  gosterim_df = sirali_liste[[
      "Risk_Seviyesi",
      "TC_No",
      "Ad_Soyad",
      "Hesaplanan_Anomali_Skoru",
      "Muhtemel_Suc_Turu",
      "Eylem_Zamani_Projeksiyonu",
      "Ikamet_Ili",
      "Ikamet_Ilcesi",
  ]].head(500).copy()

  gosterim_df.columns = [
      "Risk Sınıfı",
      "TC Kimlik No",
      "Ad Soyad",
      "Risk Skoru",
      "Muhtemel Suç Türü",
      "Zaman Projeksiyonu",
      "İl",
      "İlçe",
  ]
  st.dataframe(gosterim_df, use_container_width=True, hide_index=True)

with tab3:
  st.subheader("🔍 Bireysel Profil - Zihinsel Niyet ve Suç Analiz Raporu")
  arama_kriteri = st.text_input(
      "Aramak istediğiniz TC Kimlik No veya İsim Giriniz:",
      placeholder="Örn: Ahmet Yılmaz veya TC No",
      key="arama_kriteri_ti",
  )

  if arama_kriteri:
    bulunan = df[
        (df["TC_No"].astype(str).str.contains(arama_kriteri, na=False))
        | (df["Ad_Soyad"].str.contains(arama_kriteri, case=False, na=False))
    ]
    if not bulunan.empty:
      kisi = bulunan.iloc[0]
      st.success(
          f"Kayıt Bulundu: **{kisi['Ad_Soyad']}** (TC: {kisi['TC_No']})"
      )

      p1, p2, p3, p4 = st.columns(4)
      p1.metric("Risk Sınıfı", str(kisi["Risk_Seviyesi"]))
      p2.metric(
          "Anomali Skoru", f"{kisi['Hesaplanan_Anomali_Skoru']:.1f} / 10.0"
      )
      p3.metric(
          "Güncel İl / İlçe", f"{kisi['Ikamet_Ili']} / {kisi['Ikamet_Ilcesi']}"
      )
      p4.metric("Sorgu Zamanı (TR)", saat_str)

      st.markdown("---")
      st.markdown("##### 🧠 Yapay Zeka Pre-Crime & Niyet Analizi")
      st.error(f"🎯 **Öngörülen Muhtemel Suç:** {kisi['Muhtemel_Suc_Turu']}")
      st.warning(
          f"⏰ **Zaman Projeksiyonu:** {kisi['Eylem_Zamani_Projeksiyonu']}"
      )
      st.info(
          f"💡 **Zihinsel Durum / Niyet Profili:** {kisi['Zihinsel_Niyet_Analizi']}"
      )

      st.markdown("##### ⏳ Geçmiş Yaşam ve İkamet Seyir Defteri")
      st.write(
          f"📍 **Nüfus Hareketlilik Geçmişi:** {kisi['Gecmis_Ikamet_Gecmisi']}"
      )
    else:
      st.error("Aranan kriterlere uygun kişi kaydı bulunamadı.")
