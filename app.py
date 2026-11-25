from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="AKIN (Anomali, Konum, İzleme ve Niyet)",
    page_icon="🚨",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stMetric {
        background-color: #161b24;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 14px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        font-size: 13.5px;
        overflow-x: auto;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 14px;
        border-radius: 8px 8px 0 0;
        white-space: nowrap;
        font-weight: 600;
    }
    .akin-banner {
        background: linear-gradient(90deg, rgba(255, 75, 75, 0.14), rgba(22, 27, 36, 0.94));
        border: 1px solid rgba(255, 75, 75, 0.30);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .akin-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        background-color: rgba(255, 255, 255, 0.08);
        margin-right: 6px;
        margin-top: 6px;
    }
    .akin-card {
        background-color: #161b24;
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .risk-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.80rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1.4rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    @media (max-width: 768px) {
        .row-widget.stHorizontal {flex-direction: column;}
    }
    </style>
""",
    unsafe_allow_html=True,
)

tr_saat_dilimi = ZoneInfo("Europe/Istanbul")


def anlik_tr_zaman():
  simdi = datetime.now(tr_saat_dilimi)
  return simdi.strftime("%H:%M:%S"), simdi.strftime("%d.%m.%Y")


def risk_rozet_stili(risk_seviyesi: str) -> str:
  if "Siyah" in risk_seviyesi:
    return (
        "background-color: #0d1117; color: #ff6b6b; border: 1px solid #ff4b4b;"
    )
  if "Kırmızı" in risk_seviyesi:
    return (
        "background-color: rgba(255, 75, 75, 0.18); color: #ff7b7b; border: 1px"
        " solid rgba(255, 75, 75, 0.45);"
    )
  if "Turuncu" in risk_seviyesi:
    return (
        "background-color: rgba(255, 165, 0, 0.18); color: #ffb84d; border: 1px"
        " solid rgba(255, 165, 0, 0.45);"
    )
  return (
      "background-color: rgba(255, 215, 0, 0.15); color: #ffe066; border: 1px"
      " solid rgba(255, 215, 0, 0.40);"
  )


@st.fragment(run_every=1)
def canli_saat_kutusu(hizalama: str = "flex-start"):
  guncel_saat, guncel_tarih = anlik_tr_zaman()
  st.markdown(
      f"""
        <div style="display: flex; justify-content: {hizalama};">
            <div style="
                padding: 8px 14px;
                border-radius: 8px;
                border: 1px solid rgba(255, 75, 75, 0.40);
                background-color: rgba(22, 27, 36, 0.92);
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

IL_SINIR_YARICAPI = {
    "İstanbul": 0.16,
    "Yalova": 0.07,
    "Kocaeli": 0.11,
    "İzmir": 0.18,
    "Ankara": 0.24,
    "Konya": 0.28,
    "Antalya": 0.22,
    "Mersin": 0.18,
    "Adana": 0.19,
    "Şanlıurfa": 0.22,
    "Gaziantep": 0.14,
    "Diyarbakır": 0.20,
    "Hatay": 0.13,
    "Van": 0.22,
    "Samsun": 0.17,
    "Trabzon": 0.11,
    "Bursa": 0.18,
    "Kayseri": 0.20,
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

buyuk_suc_agirliklari = {
    "İstanbul": 1.45,
    "Ankara": 1.25,
    "İzmir": 1.22,
    "Adana": 1.32,
    "Gaziantep": 1.28,
    "Şanlıurfa": 1.26,
    "Diyarbakır": 1.30,
    "Hatay": 1.34,
    "Mersin": 1.27,
    "Antalya": 1.18,
    "Bursa": 1.15,
    "Kocaeli": 1.20,
    "Van": 1.24,
    "Mardin": 1.23,
    "Şırnak": 1.22,
    "Hakkâri": 1.21,
    "Trabzon": 1.12,
    "Samsun": 1.13,
    "Kayseri": 1.10,
    "Konya": 1.11,
}

tum_iller = list(TURKIYE_IL_ILCELER.keys())

birlesik_ham_agirlik = np.array(
    [
        nufus_agirliklari.get(il, 0.003)
        * (0.65 + 0.35 * buyuk_suc_agirliklari.get(il, 1.0))
        for il in tum_iller
    ],
    dtype=np.float32,
)
agirliklar = birlesik_ham_agirlik / birlesik_ham_agirlik.sum()


@st.cache_data(show_spinner="1.000.000 profil ve suç/risk verisi hazırlanıyor...")
def veriyi_yukle(n: int = 1000000):
  rng = np.random.default_rng()
  secilen_iller = rng.choice(tum_iller, size=n, p=agirliklar)

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
      "Tarık",
      "İbrahim",
      "Hüseyin",
      "Hasan",
      "Ömer",
      "Osman",
      "Yasin",
      "Tuğba",
      "Derya",
      "Ebru",
      "Hatice",
      "Emine",
      "Yasemin",
      "Gizem",
      "Melisa",
      "İrem",
      "Selin",
      "Baran",
      "Arda",
      "Eren",
      "Mert",
      "Umut",
      "Berk",
      "Furkan",
      "Alperen",
      "Doğukan",
      "Ege",
      "Kadir",
      "Ramazan",
      "İsmail",
      "Halil",
      "Salih",
      "Bekir",
      "Zeliha",
      "Özlem",
      "Pınar",
      "Gülşen",
      "Nihan",
      "Cansu",
      "Aylin",
      "Dilek",
      "Seda",
      "Aslı",
      "Burcu",
      "Kübra",
      "Şeyma",
      "Reyhan",
      "Dilan",
      "Azra",
      "Berfin",
      "Miray",
      "Eylül",
      "Defne",
      "Rüzgar",
      "Yaman",
      "Çınar",
      "Toprak",
      "Kağan",
      "Bora",
      "Tuna",
      "Çağrı",
      "Enes",
      "Yiğit",
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
      "Korkmaz",
      "Erdoğan",
      "Güneş",
      "Aktaş",
      "Yavuz",
      "Avcı",
      "Karahan",
      "Taş",
      "Bulut",
      "Keskin",
      "Tekin",
      "Bozkurt",
      "Kaplan",
      "Sarı",
      "Güler",
      "Tunç",
      "Ünal",
      "Karaca",
      "Turan",
      "Duman",
      "Uçar",
      "Çakır",
      "Sönmez",
      "Acar",
      "Bilgin",
      "Mutlu",
      "Bayram",
      "Coşkun",
      "İnce",
      "Karakuş",
      "Kalkan",
      "Soylu",
      "Ergün",
      "Alkan",
      "Ceylan",
      "Eroğlu",
      "Gündüz",
      "Kayaalp",
      "Özer",
      "Sezer",
      "Vural",
      "Yalçın",
      "Zengin",
      "Aydoğan",
      "Bilir",
      "Çağlar",
      "Demirel",
      "Ekici",
  ])

  ad_soyadlar = rng.choice(ad_havuzu, size=n) + " " + rng.choice(soyad_havuzu, size=n)

  base_lats = np.array(
      [IL_KOORDINATLARI[il][0] for il in secilen_iller], dtype=np.float32
  )
  base_lons = np.array(
      [IL_KOORDINATLARI[il][1] for il in secilen_iller], dtype=np.float32
  )
  il_yaricap = np.array(
      [IL_SINIR_YARICAPI.get(il, 0.14) for il in secilen_iller],
      dtype=np.float32,
  )

  lats = np.clip(
      base_lats + rng.uniform(-1.0, 1.0, size=n).astype(np.float32) * il_yaricap,
      35.85,
      42.10,
  )
  lons = np.clip(
      base_lons + rng.uniform(-1.0, 1.0, size=n).astype(np.float32) * il_yaricap,
      25.65,
      44.80,
  )

  ilceler = np.array(
      [rng.choice(TURKIYE_IL_ILCELER[il]) for il in secilen_iller]
  )
  mahalle_no = rng.integers(1, 40, size=n).astype(str)
  mahalleler = np.char.add(np.char.add(ilceler, " Mah. "), mahalle_no)

  gecmis_ikametler = np.where(
      rng.random(n) > 0.5,
      np.char.add(secilen_iller, " bölgesinde uzun süredir ikamet ediyor."),
      "Çoklu İl Değişikliği (Aktif Hareketlilik)",
  )

  il_buyuk_suc_katsayi = np.array(
      [buyuk_suc_agirliklari.get(il, 1.0) for il in secilen_iller],
      dtype=np.float32,
  )
  darkweb_olasilik = np.clip(0.015 * il_buyuk_suc_katsayi, 0.008, 0.05)
  ikiz_plaka_olasilik = np.clip(0.010 * il_buyuk_suc_katsayi, 0.005, 0.04)

  darkweb_secim = np.where(
      rng.random(n) < darkweb_olasilik, "Tespit Edildi!", "Yok"
  )
  ikiz_plaka_secim = np.where(
      rng.random(n) < ikiz_plaka_olasilik,
      "Aynı Anda Farklı İlde İkiz Plaka!",
      "Normal",
  )
  tor_secim = rng.choice(["Yok", "Var (Şifreli Ağ)"], size=n, p=[0.95, 0.05])
  tesis_secim = rng.choice(
      ["Yok", "Var (Askeri/Valilik Etrafı Dolaşım)"], size=n, p=[0.96, 0.04]
  )
  sicil_secim = rng.choice(
      ["Temiz", "Organize Suç", "Terör İltisakı", "Kaçakçılık"],
      size=n,
      p=[0.90, 0.04, 0.03, 0.03],
  )

  il_risk_katmani = np.array(
      [
          nufus_agirliklari.get(il, 0.003)
          * 12.0
          * buyuk_suc_agirliklari.get(il, 1.0)
          for il in secilen_iller
      ],
      dtype=np.float32,
  )

  skor = np.full(n, 1.4, dtype=np.float32) + np.clip(
      il_risk_katmani, 0.0, 2.4
  )
  skor += np.where(tor_secim == "Var (Şifreli Ağ)", 1.5, 0.0).astype(np.float32)
  skor += np.where(darkweb_secim == "Tespit Edildi!", 3.5, 0.0).astype(
      np.float32
  )
  skor += np.where(
      tesis_secim == "Var (Askeri/Valilik Etrafı Dolaşım)", 2.5, 0.0
  ).astype(np.float32)
  skor += np.where(
      ikiz_plaka_secim == "Aynı Anda Farklı İlde İkiz Plaka!", 3.0, 0.0
  ).astype(np.float32)
  skor += np.where(
      np.isin(sicil_secim, ["Organize Suç", "Terör İltisakı"]), 2.0, 0.0
  ).astype(np.float32)
  skor += np.where(sicil_secim == "Kaçakçılık", 1.4, 0.0).astype(np.float32)

  hesaplanan_skor = np.clip(
      skor + rng.uniform(-0.3, 0.3, size=n).astype(np.float32), 1.0, 10.0
  )

  p_dark = np.where(
      darkweb_secim == "Tespit Edildi!", "DarkWeb patlayıcı araması (+3.5) | ", ""
  )
  p_plaka = np.where(
      ikiz_plaka_secim == "Aynı Anda Farklı İlde İkiz Plaka!",
      "İkiz plaka (+3.0) | ",
      "",
  )
  p_tesis = np.where(
      tesis_secim == "Var (Askeri/Valilik Etrafı Dolaşım)",
      "Kritik tesis keşfi (+2.5) | ",
      "",
  )
  p_sicil = np.where(
      np.isin(sicil_secim, ["Organize Suç", "Terör İltisakı"]),
      "Yüksek riskli sicil (+2.0) | ",
      np.where(sicil_secim == "Kaçakçılık", "Kaçakçılık sicili (+1.4) | ", ""),
  )
  p_tor = np.where(
      tor_secim == "Var (Şifreli Ağ)", "Tor/I2P izi (+1.5) | ", ""
  )
  p_taban = np.char.add(
      "İl nüfus + büyük suç katsayısı: ",
      np.char.add(np.round(il_buyuk_suc_katsayi, 2).astype(str), "x"),
  )

  gerekce_dizi = np.char.add(
      np.char.add(
          np.char.add(np.char.add(p_dark, p_plaka), p_tesis), p_sicil
      ),
      np.char.add(p_tor, p_taban),
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

  conditions = [
      hesaplanan_skor >= 8.5,
      (hesaplanan_skor >= 7.0) & (hesaplanan_skor < 8.5),
      (hesaplanan_skor >= 5.0) & (hesaplanan_skor < 7.0),
      hesaplanan_skor < 5.0,
  ]
  choices = [
      "⬛ Siyah (Kritik Tehdit)",
      "🔴 Kırmızı (Yüksek Risk)",
      "🟠 Turuncu (Orta Risk)",
      "🟡 Sarı (İzleme Düzeyi)",
  ]
  risk_seviyesi = np.select(conditions, choices, default="🟡 Sarı (İzleme Düzeyi)")

  return pd.DataFrame({
      "TC_No": rng.integers(10000000000, 99999999999, size=n, dtype=np.int64),
      "Ad_Soyad": ad_soyadlar,
      "Vatandaslik_Durumu": pd.Categorical(
          rng.choice(["T.C. Vatandaşı", "Yabancı Uyruklu"], size=n, p=[0.93, 0.07])
      ),
      "Ikamet_Ili": pd.Categorical(secilen_iller),
      "Ikamet_Ilcesi": pd.Categorical(ilceler),
      "Ikamet_Mahalle": pd.Categorical(mahalleler),
      "Gecmis_Ikamet_Gecmisi": pd.Categorical(gecmis_ikametler),
      "lat": lats,
      "lon": lons,
      "Tor_I2P_Kullanimi": pd.Categorical(tor_secim),
      "DarkWeb_Aramasi_Patlayici": pd.Categorical(darkweb_secim),
      "Kritik_Tesis_Kesfi": pd.Categorical(tesis_secim),
      "Sahte_Ikiz_Plaka": pd.Categorical(ikiz_plaka_secim),
      "Adli_Sicil_Kaydi": pd.Categorical(sicil_secim),
      "Hesaplanan_Anomali_Skoru": hesaplanan_skor,
      "Skor_Degerlendirme_Gerekcesi": pd.Categorical(gerekce_dizi),
      "Muhtemel_Suc_Turu": pd.Categorical(rng.choice(suc_havuzu, size=n)),
      "Eylem_Zamani_Projeksiyonu": pd.Categorical(rng.choice(zaman_havuzu, size=n)),
      "Zihinsel_Niyet_Analizi": pd.Categorical(rng.choice(niyet_havuzu, size=n)),
      "Risk_Seviyesi": pd.Categorical(risk_seviyesi),
  })


df = veriyi_yukle(1000000)

# --- Kenar Çubuğu: AKIN Kontrol Merkezi ---
st.sidebar.title("🚨 AKIN Kontrol Merkezi")
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
  musait_ilceler = sorted(df["Ikamet_Ilcesi"].cat.categories.tolist())

secilen_ilceler = st.sidebar.multiselect(
    "2. İlçe Seçimi", options=musait_ilceler, default=[], key="secilen_ilceler_ms"
)

if secilen_ilceler:
  musait_mahalleler = sorted(
      df.loc[df["Ikamet_Ilcesi"].isin(secilen_ilceler), "Ikamet_Mahalle"]
      .dropna()
      .unique()
      .tolist()
  )
elif secilen_iller:
  musait_mahalleler = sorted(
      df.loc[df["Ikamet_Ili"].isin(secilen_iller), "Ikamet_Mahalle"]
      .dropna()
      .unique()
      .tolist()
  )
else:
  musait_mahalleler = sorted(df["Ikamet_Mahalle"].cat.categories.tolist())

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

# --- Üst Durum Şeridi & Canlı Saat ---
col_baslik, col_zaman = st.columns([3.5, 1.2])
with col_baslik:
  bolge_etiketi = ", ".join(secilen_iller) if secilen_iller else "Tüm Türkiye"
  st.markdown(
      f"""
        <div class="akin-banner">
            <div style="font-size: 1.32rem; font-weight: 700;">🚨 AKIN (Anomali, Konum, İzleme ve Niyet)</div>
            <div style="opacity: 0.82; font-size: 0.88rem; margin-top: 2px;">Operasyonel Niyet, Suç Oranı ve Risk Analitiği Platformu • 1.000.000 Sentetik Profil</div>
            <div>
                <span class="akin-pill">📍 Kapsam: {bolge_etiketi}</span>
                <span class="akin-pill">🎯 Min. Risk Eşiği: {risk_esigi:.1f}</span>
                <span class="akin-pill">👥 Eşleşen Kayıt: {len(süzülmüş_df):,}</span>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )
with col_zaman:
  canli_saat_kutusu("flex-end")

tab1, tab2, tab3 = st.tabs([
    "🗺️ Türkiye Anomali Haritası & Akış",
    "🎯 Risk Hiyerarşisi & Değerlendirme Kriterleri",
    "🔍 Bireysel Profil, Puan Gerekçesi ve Niyet",
])

with tab1:
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Toplam İzlenen Profil", f"{len(df):,}")
  m2.metric("Filtrelenen Şüpheli Sayısı", f"{len(süzülmüş_df):,}")
  m3.metric(
      "Kritik Alarm (Siyah / Kırmızı)",
      f"{(süzülmüş_df['Hesaplanan_Anomali_Skoru'] >= 7.0).sum():,}",
  )
  ort_skor = (
      süzülmüş_df["Hesaplanan_Anomali_Skoru"].mean()
      if not süzülmüş_df.empty
      else 0.0
  )
  m4.metric("Ortalama Anomali Skoru", f"{ort_skor:.2f} / 10.0")

  st.markdown("---")

  st.subheader("🗺️ Türkiye İl Sınırları Anomali & Büyük Suç Yoğunluğu Haritası")
  harita_df = (
      süzülmüş_df.sort_values(
          by="Hesaplanan_Anomali_Skoru", ascending=False
      )
      .head(3000)
      .copy()
  )

  skor_serisi = harita_df["Hesaplanan_Anomali_Skoru"]
  harita_df["color_r"] = np.where(
      skor_serisi >= 8.5, 25, np.where(skor_serisi >= 5.0, 255, 255)
  )
  harita_df["color_g"] = np.where(
      skor_serisi >= 8.5, 25, np.where(skor_serisi >= 7.0, 45, 165)
  )
  harita_df["color_b"] = np.where(skor_serisi >= 8.5, 35, 20)

  harita_df["nokta_yaricap"] = np.where(
      skor_serisi >= 8.5,
      skor_serisi * 260,
      np.where(
          skor_serisi >= 7.0,
          skor_serisi * 220,
          np.where(skor_serisi >= 5.0, skor_serisi * 190, skor_serisi * 160),
      ),
  )

  if secilen_iller and secilen_iller[-1] in IL_KOORDINATLARI:
    odak_lat, odak_lon = IL_KOORDINATLARI[secilen_iller[-1]]
    odak_zoom = 8.4
  else:
    odak_lat, odak_lon = 39.0, 35.2
    odak_zoom = 5.6

  layer = pdk.Layer(
      "ScatterplotLayer",
      harita_df,
      get_position=["lon", "lat"],
      get_color=["color_r", "color_g", "color_b", 210],
      get_radius="nokta_yaricap",
      pickable=True,
      radius_scale=3,
      radius_min_pixels=2,
      radius_max_pixels=10,
  )

  view_state = pdk.ViewState(
      latitude=odak_lat,
      longitude=odak_lon,
      zoom=odak_zoom,
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
              "<b>Şüpheli:</b> {Ad_Soyad} ({Risk_Seviyesi})<br/><b>Konum:</b>"
              " {Ikamet_Ili} / {Ikamet_Ilcesi}<br/><b>Skor:</b>"
              " {Hesaplanan_Anomali_Skoru}<br/><b>Muhtemel Suç:</b>"
              " {Muhtemel_Suc_Turu}<br/><b>Zaman:</b>"
              " {Eylem_Zamani_Projeksiyonu}"
          )
      },
  )
  st.pydeck_chart(r, use_container_width=True)

  st.markdown("---")

  st.subheader("🔔 Anlık Tehdit Akışı & TR Zaman Damgası")
  en_riskli = süzülmüş_df.sort_values(
      by="Hesaplanan_Anomali_Skoru", ascending=False
  ).head(5)

  if en_riskli.empty:
    st.info("Seçili filtre kriterlerine uyan yüksek riskli kayıt bulunamadı.")
  else:
    for _, row in en_riskli.iterrows():
      tespit_saat, tespit_tarih = anlik_tr_zaman()
      rozet_css = risk_rozet_stili(str(row["Risk_Seviyesi"]))
      st.markdown(
          f"""
                <div class="akin-card">
                    <span class="risk-badge" style="{rozet_css}">{row['Risk_Seviyesi']} • Skor: {row['Hesaplanan_Anomali_Skoru']:.1f}</span>
                    <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 4px;">{row['Ad_Soyad']} <span style="opacity: 0.7; font-size: 0.85rem;">(TC: {row['TC_No']} • {row['Ikamet_Ili']} / {row['Ikamet_Ilcesi']})</span></div>
                    <div style="font-size: 0.90rem; margin-bottom: 2px;">🎯 <b>Muhtemel Suç:</b> {row['Muhtemel_Suc_Turu']} &nbsp;|&nbsp; ⏰ <b>Zaman Projeksiyonu:</b> {row['Eylem_Zamani_Projeksiyonu']}</div>
                    <div style="font-size: 0.85rem; margin-bottom: 2px; opacity: 0.90;">📌 <b>Puan Gerekçesi:</b> {row['Skor_Degerlendirme_Gerekcesi']}</div>
                    <div style="font-size: 0.85rem; opacity: 0.82;">💡 <b>Niyet Özeti:</b> {row['Zihinsel_Niyet_Analizi']} • 🕒 <b>Tespit (TR):</b> {tespit_saat} ({tespit_tarih})</div>
                </div>
                """,
          unsafe_allow_html=True,
      )

  st.markdown("---")

  st.subheader("📊 Seçili Kapsam Risk Seviyesi & Suç Eğilimi Özeti")
  if not süzülmüş_df.empty:
    ozet_c1, ozet_c2 = st.columns(2)
    with ozet_c1:
      risk_dagilim = süzülmüş_df["Risk_Seviyesi"].value_counts().reset_index()
      risk_dagilim.columns = ["Risk Sınıfı", "Kişi Sayısı"]
      st.dataframe(risk_dagilim, use_container_width=True, hide_index=True)
    with ozet_c2:
      suc_dagilim = (
          süzülmüş_df["Muhtemel_Suc_Turu"].value_counts().reset_index()
      )
      suc_dagilim.columns = ["Öngörülen Suç Türü", "Kayıt Sayısı"]
      st.dataframe(suc_dagilim, use_container_width=True, hide_index=True)

with tab2:
  st.subheader("🎯 Değerlendirme Kriterleri, Puan Mantığı ve Risk Matrisi")
  st.markdown(
      """
        <div class="akin-card">
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 6px;">📐 Puanlama ve Risk Seviyesi Kriterleri (1.0 – 10.0)</div>
            <div style="font-size: 0.90rem; line-height: 1.55;">
                • <b>Taban + İl Nüfus & Büyük Suç Katsayısı:</b> Her kayıt temel skor ile başlar; ilin nüfus ağırlığı ve büyük suç yoğunluğu (organize, kaçakçılık, kritik altyapı/güvenlik) dağılım ve temel risk katsayısına eklenir.<br/>
                • <b>Yüksek Puan Nedenleri:</b> DarkWeb patlayıcı araması (<b>+3.5</b>), aynı anda farklı ilde ikiz/sahte plaka (<b>+3.0</b>), kritik tesis çevresi keşfi (<b>+2.5</b>), organize suç veya terör sicili (<b>+2.0</b>), Tor/I2P kullanımı (<b>+1.5</b>) ve kaçakçılık sicili (<b>+1.4</b>).<br/>
                • <b>Düşük Puan Nedenleri:</b> Adli sicilin temiz olması, dijital/fiziksel anomali göstergelerinin bulunmaması ve büyük suç katsayısı düşük illerde yer alma durumu skoru taban seviyelere (<b>1.0 – 4.9</b>) çeker.<br/>
                • <b>Sınıflar:</b> <b>⬛ Siyah</b> (≥ 8.5) • <b>🔴 Kırmızı</b> (7.0 – 8.49) • <b>🟠 Turuncu</b> (5.0 – 6.99) • <b>🟡 Sarı</b> (&lt; 5.0).
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )

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
      "Skor_Degerlendirme_Gerekcesi",
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
      "Değerlendirme Gerekçesi",
  ]
  st.dataframe(gosterim_df, use_container_width=True, hide_index=True)

with tab3:
  st.subheader("🔍 Bireysel Profil - Puan Gerekçesi, Suç ve Niyet Raporu")
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
      sorgu_saat, sorgu_tarih = anlik_tr_zaman()
      rozet_css = risk_rozet_stili(str(kisi["Risk_Seviyesi"]))

      st.markdown(
          f"""
                <div class="akin-card">
                    <span class="risk-badge" style="{rozet_css}">{kisi['Risk_Seviyesi']}</span>
                    <div style="font-size: 1.2rem; font-weight: 700;">{kisi['Ad_Soyad']}</div>
                    <div style="opacity: 0.8; font-size: 0.9rem;">TC Kimlik No: {kisi['TC_No']} • {kisi['Vatandaslik_Durumu']} • Sorgu Zamanı (TR): {sorgu_saat} ({sorgu_tarih})</div>
                </div>
                """,
          unsafe_allow_html=True,
      )

      p1, p2, p3, p4 = st.columns(4)
      p1.metric("Risk Sınıfı", str(kisi["Risk_Seviyesi"]))
      p2.metric(
          "Anomali Skoru", f"{kisi['Hesaplanan_Anomali_Skoru']:.1f} / 10.0"
      )
      p3.metric(
          "Güncel İl / İlçe", f"{kisi['Ikamet_Ili']} / {kisi['Ikamet_Ilcesi']}"
      )
      p4.metric("Sorgu Zamanı (TR)", sorgu_saat)

      st.markdown("---")
      st.markdown("##### 📊 Puan ve Risk Değerlendirme Gerekçesi")
      st.write(f"🧾 **Kriter Analizi:** {kisi['Skor_Degerlendirme_Gerekcesi']}")

      st.markdown("##### 🧠 AKIN Pre-Crime & Niyet Analizi")
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
