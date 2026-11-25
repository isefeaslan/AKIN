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
        "Seyhan",
        "Yüreğir",
        "Çukurova",
        "Sarıçam",
        "Ceyhan",
        "Kozan",
        "İmamoğlu",
        "Karataş",
        "Karaisalı",
        "Pozantı",
        "Feke",
        "Tufanbeyli",
        "Saimbeyli",
        "Yumurtalık",
        "Aladağ",
    ],
    "Adıyaman": [
        "Merkez",
        "Kahta",
        "Besni",
        "Gölbaşı",
        "Sincik",
        "Çelikhan",
        "Tut",
        "Samsat",
    ],
    "Afyonkarahisar": [
        "Merkez",
        "Sandıklı",
        "Dinar",
        "Bolvadin",
        "Emirdağ",
        "Sinanpaşa",
        "Şuhut",
        "Çay",
        "İhsaniye",
        "Sultandağı",
        "Başmakçı",
        "Bayat",
        "Dazkırı",
        "Evciler",
        "Hocalar",
        "Kızılören",
    ],
    "Ağrı": [
        "Merkez",
        "Patnos",
        "Doğubayazıt",
        "Diyadin",
        "Eleşkirt",
        "Tutak",
        "Hamur",
        "Taşlıçay",
    ],
    "Aksaray": [
        "Merkez",
        "Ortaköy",
        "Eskil",
        "Güzelyurt",
        "Sarıyahşi",
        "Ağaçören",
        "Gülağaç",
        "Sultanhanı",
    ],
    "Amasya": [
        "Merkez",
        "Merzifon",
        "Suluova",
        "Taşova",
        "Gümüşhacıköy",
        "Göynücek",
        "Hamamözü",
    ],
    "Ankara": [
        "Çankaya",
        "Keçiören",
        "Yenimahalle",
        "Mamak",
        "Etimesgut",
        "Sincan",
        "Altındağ",
        "Pursaklar",
        "Polatlı",
        "Beypazarı",
        "Çubuk",
        "Elmadağ",
        "Kahramankazan",
        "Akyurt",
        "Kızılcahamam",
        "Nallıhan",
        "Haymana",
        "Şereflikoçhisar",
        "Bala",
        "Güdül",
        "Kalecik",
        "Evren",
        "Çamlıdere",
        "Ayaş",
    ],
    "Antalya": [
        "Muratpaşa",
        "Kepez",
        "Konyaaltı",
        "Aksu",
        "Döşemealtı",
        "Alanya",
        "Manavgat",
        "Serik",
        "Kemer",
        "Kumluca",
        "Finike",
        "Kaş",
        "Demre",
        "Gazipaşa",
        "Elmalı",
        "Korkuteli",
        "Akseki",
        "Gündoğmuş",
        "İbradı",
    ],
    "Ardahan": ["Merkez", "Göle", "Çıldır", "Hanak", "Damal", "Posof"],
    "Artvin": [
        "Merkez",
        "Hopa",
        "Arhavi",
        "Borçka",
        "Yusufeli",
        "Şavşat",
        "Ardanuç",
        "Murgul",
        "Kemalpaşa",
    ],
    "Aydın": [
        "Efeler",
        "Nazilli",
        "Kuşadası",
        "Söke",
        "Didim",
        "İncirliova",
        "Çine",
        "Germencik",
        "Buharkent",
        "Bozdoğan",
        "Karacasu",
        "Koçarlı",
        "Kuyucak",
        "Sultanhisar",
        "Yenipazar",
        "Karpuzlu",
    ],
    "Balıkesir": [
        "Karesi",
        "Altıeylül",
        "Bandırma",
        "Edremit",
        "Gönen",
        "Burhaniye",
        "Ayvalık",
        "Bigadiç",
        "Dursunbey",
        "Susurluk",
        "İvrindi",
        "Sındırgı",
        "Havran",
        "Kepsut",
        "Manyas",
        "Savaştepe",
        "Marmara",
        "Erdek",
        "Gömeç",
        "Balya",
    ],
    "Bartın": ["Merkez", "Ulus", "Amasra", "Kurucaşile"],
    "Batman": ["Merkez", "Kozluk", "Sason", "Beşiri", "Gercüş", "Hasankeyf"],
    "Bayburt": ["Merkez", "Demirözü", "Aydıntepe"],
    "Bilecik": [
        "Merkez",
        "Bozüyük",
        "Söğüt",
        "Osmaneli",
        "Gölpazarı",
        "Pazaryeri",
        "İnhisar",
        "Yenipazar",
    ],
    "Bingöl": [
        "Merkez",
        "Genç",
        "Solhan",
        "Karlıova",
        "Adaklı",
        "Kiğı",
        "Yayladere",
        "Yedisu",
    ],
    "Bitlis": [
        "Merkez",
        "Tatvan",
        "Ahlat",
        "Güroymak",
        "Hizan",
        "Mutki",
        "Adilcevaz",
    ],
    "Bolu": [
        "Merkez",
        "Gerede",
        "Mudurnu",
        "Göynük",
        "Mengen",
        "Yeniçağa",
        "Dörtdivan",
        "Seben",
        "Kıbrıscık",
    ],
    "Burdur": [
        "Merkez",
        "Bucak",
        "Gölhisar",
        "Yeşilova",
        "Çavdır",
        "Tefenni",
        "Ağlasun",
        "Altınyayla",
        "Karamanlı",
        "Kemer",
        "Çeltikçi",
    ],
    "Bursa": [
        "Osmangazi",
        "Nilüfer",
        "Yıldırım",
        "İnegöl",
        "Gemlik",
        "Mudanya",
        "Mustafakemalpaşa",
        "Karacabey",
        "Gürsu",
        "Kestel",
        "Orhangazi",
        "Yenişehir",
        "İznik",
        "Karacabey",
        "Keles",
        "Orhaneli",
        "Büyükorhan",
        "Harmancık",
    ],
        "Çanakkale": [
        "Merkez",
        "Biga",
        "Çan",
        "Gelibolu",
        "Ayvacık",
        "Ezine",
        "Lapseki",
        "Yenice",
        "Bayramiç",
        "Eceabat",
        "Bozcaada",
        "Gökçeada",
    ],
    "Çankırı": [
        "Merkez",
        "Çerkeş",
        "Ilgaz",
        "Orta",
        "Şabanözü",
        "Kurşunlu",
        "Yapraklı",
        "Eldivan",
        "Korgun",
        "Atkaracalar",
        "Kızılırmak",
        "Bayramören",
    ],
    "Çorum": [
        "Merkez",
        "Sungurlu",
        "Osmancık",
        "İskilip",
        "Alaca",
        "Bayat",
        "Kargı",
        "Mecitözü",
        "Ortaköy",
        "Uğurludağ",
        "Dodurga",
        "Laçin",
        "Boğazkale",
        "Oğuzlar",
    ],
    "Denizli": [
        "Pamukkale",
        "Merkezefendi",
        "Çivril",
        "Acıpayam",
        "Tavas",
        "Honaz",
        "Sarayköy",
        "Buldan",
        "Kale",
        "Çal",
        "Beyağaç",
        "Çameli",
        "Güney",
        "Babadağ",
        "Bekilli",
        "Bozkurt",
        "Baklan",
    ],
    "Diyarbakır": [
        "Bağlar",
        "Kayapınar",
        "Yenişehir",
        "Sur",
        "Bismil",
        "Ergani",
        "Silvan",
        "Çınar",
        "Çermik",
        "Dicle",
        "Hani",
        "Kulp",
        "Lice",
        "Eğil",
        "Kocaköy",
        "Hazro",
        "Çüngüş",
    ],
    "Düzce": [
        "Merkez",
        "Akçakoca",
        "Kaynaşlı",
        "Gölyaka",
        "Çilimli",
        "Cumayeri",
        "Gümüşova",
        "Yığılca",
    ],
    "Edirne": [
        "Merkez",
        "Keşan",
        "Uzunköprü",
        "İpsala",
        "Havsa",
        "Meriç",
        "Enez",
        "Süloğlu",
        "Lalapaşa",
    ],
    "Elazığ": [
        "Merkez",
        "Karakoçan",
        "Kovancılar",
        "Palu",
        "Baskil",
        "Maden",
        "Sivrice",
        "Arıcak",
        "Kebân",
        "Ağın",
        "Alacakaya",
    ],
    "Erzincan": [
        "Merkez",
        "Tercan",
        "Üzümlü",
        "Refahiye",
        "Çayırlı",
        "İliç",
        "Kemah",
        "Kemaliye",
        "Otlukbeli",
    ],
    "Erzurum": [
        "YAkutiye",
        "Palandöken",
        "Aziziye",
        "Horasan",
        "Pasinler",
        "Oltu",
        "Hınıs",
        "Karayazı",
        "Tekman",
        "Tortum",
        "İspir",
        "Narman",
        "Şenkaya",
        "Köprüköy",
        "Aşkale",
        "Çat",
        "Karaçoban",
        "Pazaryolu",
        "Olur",
    ],
    "Eskişehir": [
        "Odunpazarı",
        "Tepebaşı",
        "Sivrihisar",
        "Çifteler",
        "Seyitgazi",
        "Alpu",
        "Mihalıççık",
        "Mahmudiye",
        "Beylikova",
        "İnönü",
        "Sarıcakaya",
        "Günyüzü",
        "Han",
        "Mihalgazi",
    ],
    "Gaziantep": [
        "Şahinbey",
        "Şehitkamil",
        "Nizip",
        "İslahiye",
        "Nurdağı",
        "Araban",
        "Oğuzeli",
        "Yavuzeli",
        "Karkamış",
    ],
    "Giresun": [
        "Merkez",
        "Bulancak",
        "Espiye",
        "Görele",
        "Tirebolu",
        "Dereli",
        "Keşap",
        "Şebinkarahisar",
        "Alucra",
        "Yağlıdere",
        "Eynesil",
        "Piraziz",
        "Çanakçı",
        "Doğankent",
        "Güce",
        "Çamoluk",
    ],
    "Gümüşhane": ["Merkez", "Kelkit", "Şiran", "Kürtün", "Torul", "Köse"],
    "Hakkari": ["Yüksekova", "Merkez", "Şemdinli", "Çukurca", "Derecik"],
    "Hatay": [
        "Antakya",
        "İskenderun",
        "Defne",
        "Dörtyol",
        "Samandağ",
        "Kırıkhan",
        "Payas",
        "Reyhanlı",
        "Arsuz",
        "Altınözü",
        "Hassa",
        "Erzin",
        "Belen",
        "Kumlu",
        "Yayladağı",
    ],
    "Iğdır": ["Merkez", "Tuzluca", "Aralık", "Karakoyunlu"],
    "Isparta": [
        "Merkez",
        "Yalvaç",
        "Eğirdir",
        "Şarkikaraağaç",
        "Gelendost",
        "Keçiborlu",
        "Senirkent",
        "Sütçüler",
        "Gönen",
        "Uluborlu",
        "Atabey",
        "Aksu",
        "Yenişarbademli",
    ],
    "İstanbul": [
        "Esenyurt",
        "Küçükçekmece",
        "Bağcılar",
        "Ümraniye",
        "Pendik",
        "Bahçelievler",
        "Üsküdar",
        "Sultangazi",
        "Maltepe",
        "Gaziosmanpaşa",
        "Kartal",
        "Kadıköy",
        "Başakşehir",
        "Esenler",
        "Avcılar",
        "Kağıthane",
        "Fatih",
        "Sancaktepe",
        "Beylikdüzü",
        "Ataşehir",
        "Eyüpsultan",
        "Saray",
        "Zeytinburnu",
        "Büyükçekmece",
        "Tuzla",
        "Arnavutköy",
        "Şişli",
        "Beykoz",
        "Bakırköy",
        "Silivri",
        "Çekmeköy",
        "Beşiktaş",
        "Sarıyer",
        "Çatalca",
        "Adalar",
        "Şile",
    ],
    "İzmir": [
        "Buca",
        "Karabağlar",
        "Bornova",
        "Konak",
        "Karşıyaka",
        "Bayraklı",
        "Çiğli",
        "Torbalı",
        "Menemen",
        "Gaziemir",
        "Ödemiş",
        "Kemalpaşa",
        "Bergama",
        "Aliağa",
        "Menderes",
        "Tire",
        "Balçova",
        "Urla",
        "Narlıdere",
        "Seferihisar",
        "Kiraz",
        "Dikili",
        "Foça",
        "Selçuk",
        "Bayındır",
        "Güzelbahçe",
        "Kınık",
        "Beydağ",
        "Karaburun",
    ],
    "Kahramanmaraş": [
        "Onikişubat",
        "Dulkadiroğlu",
        "Elbistan",
        "Afşin",
        "Türkoğlu",
        "Pazarcık",
        "Göksun",
        "Andırın",
        "Çağlayancerit",
        "Ekinözü",
        "Nurhak",
    ],
    "Karabük": [
        "Merkez",
        "Safranbolu",
        "Yenice",
        "Eskipazar",
        "Eflani",
        "Ovacık",
    ],
    "Karaman": [
        "Merkez",
        "Ermenek",
        "Sarıveliler",
        "Ayrancı",
        "Kazımkarabekir",
        "Başyayla",
    ],
    "Kars": [
        "Merkez",
        "Sarıkamış",
        "Kağızman",
        "Digor",
        "Selim",
        "Arpaçay",
        "Susuz",
        "Akyaka",
    ],
    "Kastamonu": [
        "Merkez",
        "Tosya",
        "Taşköprü",
        "Cide",
        "İnebolu",
        "Araç",
        "Daday",
        "Devrekani",
        "Bozkurt",
        "Küre",
        "Azdavay",
        "Abana",
        "Çatalzeytin",
        "Seydiler",
        "İhsangazi",
        "Pınarbaşı",
        "Şenpazar",
        "Ağlı",
        "Doğanyurt",
        "Hanönü",
    ],
    "Kayseri": [
        "Melikgazi",
        "Kocasinan",
        "Talas",
        "Develi",
        "Yahyalı",
        "Bünyan",
        "İncesu",
        "Pınarbaşı",
        "Tomarza",
        "Yeşilhisar",
        "Sarıoğlan",
        "Hacılar",
        "Sarız",
        "Akkışla",
        "Felahiye",
        "Özvatân",
    ],
    "Kırıkkale": [
        "Merkez",
        "Yahşihan",
        "Keskin",
        "Delice",
        "Sulakyurt",
        "Bahşılı",
        "Balışeyh",
        "Karakeçili",
        "Çelebi",
    ],
    "Kırklareli": [
        "Lületaş",
        "Merkez",
        "Babaeski",
        "Vize",
        "Pınarhisar",
        "Demirköy",
        "Pehlivanköy",
        "Kofçaz",
    ],
    "Kırşehir": [
        "Merkez",
        "Kaman",
        "Mucur",
        "Çiçekdağı",
        "Akpınar",
        "Boztepe",
        "Akçakent",
    ],
    "Kilis": ["Merkez", "Musabeyli", "Elbeyli", "Polateli"],
    "Kocaeli": [
        "Gebze",
        "İzmit",
        "Darıca",
        "Körfez",
        "Gölcük",
        "Derince",
        "Çayırova",
        "Kartepe",
        "Başiskele",
        "Karamürsel",
        "Kandıra",
        "Dilovası",
    ],
    "Konya": [
        "Selçuklu",
        "Meram",
        "Karatay",
        "Ereğli",
        "Akşehir",
        "Beyşehir",
        "Çumra",
        "Seydişehir",
        "Ilgın",
        "Cihanbeyli",
        "Kulu",
        "Karapınar",
        "Kadınhanı",
        "Sarayönü",
        "Bozkır",
        "Yunak",
        "Doğanhisar",
        "Hüyük",
        "Altınekin",
        "Hadim",
        "Emirgazi",
        "Taşkent",
        "Tuzlukçu",
        "Derebucak",
        "Akören",
        "Çeltik",
        "Ahırlı",
        "Derbent",
        "Halkapınar",
        "Yalıhüyük",
    ],
    "Kütahya": [
        "Merkez",
        "Tavşanlı",
        "Simav",
        "Gediz",
        "Emet",
        "Altıntaş",
        "Domaniç",
        "Hisarcık",
        "Aslanapa",
        "Çavdarhisar",
        "Pazarlar",
        "Şaphane",
        "Dumlupınar",
    ],
    "Malatya": [
        "Battalgazi",
        "Yeşilyurt",
        "Doğanşehir",
        "Akçadağ",
        "Darende",
        " Hekimhan",
        "Yazıhan",
        "Pütürge",
        "Arapgir",
        "Arguvan",
        "Kuluncak",
        "Doğanyol",
        "Kale",
    ],
    "Manisa": [
        "Yunusemre",
        "Şehzadeler",
        "Akhisar",
        "Turgutlu",
        "Salihli",
        "Soma",
        "Alaşehir",
        "Saruhanlı",
        "Kula",
        "Kırkağaç",
        "Demirci",
        "Gördes",
        "Sarıgöl",
        "Selendi",
        "Ahmetli",
        "Gölmarmara",
        "Köprübaşı",
    ],
    "Mardin": [
        "Kızıltepe",
        "Artuklu",
        "Midyat",
        "Nusaybin",
        "Derik",
        "Mazıdağı",
        "Dargeçit",
        "Savur",
        "Ömerli",
        "Yeşilli",
    ],
    "Mersin": [
        "Tarsus",
        "Toroslar",
        "Yenişehir",
        "Mezitli",
        "Akdeniz",
        "Erdemli",
        "Silifke",
        "Anamur",
        "Mut",
        "Bozyazı",
        "Aydıncık",
        "Gülnar",
        "Çamlıyayla",
    ],
    "Muğla": [
        "Bodrum",
        "Fethiye",
        "Milas",
        "Marmaris",
        "Menteşe",
        "Ortaca",
        "Dalaman",
        "Köyceğiz",
        "Ula",
        "Yatağan",
        "Seydikemer",
        "Datça",
        "Kavaklıdere",
    ],
    "Muş": ["Merkez", "Bulanık", "Malazgirt", "Varto", "Hasköy", "Korkut"],
    "Nevşehir": [
        "Merkez",
        "Ürgüp",
        "Avanos",
        "Gülşehir",
        "Derinkuyu",
        "Acıgöl",
        "Kozaklı",
        "Hacıbektaş",
    ],
    "Niğde": [
        "Merkez",
        "Bor",
        "Çiftlik",
        "Ulukışla",
        "Altunhisar",
        "Çamardı",
    ],
    "Ordu": [
        "Altınordu",
        "Ünye",
        "Fatsa",
        "Gölköy",
        "Perşembe",
        "Korgan",
        "Kumru",
        "Aybası",
        "Ulubey",
        "Mesudiye",
        "Gürgentepe",
        "İkizce",
        "Çamaş",
        "Çatalpınar",
        "Akkuş",
        "Kabataş",
        "Çaybaşı",
        "Gülyalı",
    ],
    "Osmaniye": [
        "Merkez",
        "Kadirli",
        "Düziçi",
        "Bahçe",
        "Toprakkale",
        "Sumbas",
        "Hasanbeyli",
    ],
    "Rize": [
        "Merkez",
        "Çayeli",
        "Ardeşen",
        "Pazar",
        "Fındıklı",
        "Güneysu",
        "Kalkandere",
        "İyidere",
        "Derepazarı",
        "İkizdere",
        "Çamlıhemşin",
        "Hemşin",
    ],
    "Sakarya": [
        "Adapazarı",
        "Serdivan",
        "Akyazı",
        "Erenler",
        "Hendek",
        "Karasu",
        "Geyve",
        "Sapanca",
        "Pamukova",
        "Ferizli",
        "Kaynarca",
        "Kocaali",
        "Arifiye",
        "Söğütlü",
        "Karapürçek",
        "Taraklı",
    ],
    "Samsun": [
        "İlkadım",
        "Atakum",
        "Bafra",
        "Çarşamba",
        "Canik",
        "Vezirköprü",
        "Terme",
        "Tekkeköy",
        "Havza",
        "Alaçam",
        "Kavdak",
        "Ayvacık",
        "Ondokuzmayıs",
        "Salıpazarı",
        "Asarcık",
        "Ladik",
        "Yakakent",
    ],
    "Siirt": [
        "Merkez",
        "Kurtalan",
        "Pervari",
        "Baykan",
        "Şirvan",
        "Eruh",
        "Tillo",
    ],
    "Sinop": [
        "Merkez",
        "Boyabat",
        "Gerze",
        "Ayancık",
        "Durağan",
        "Türkeli",
        "Erfelek",
        "Dikmen",
        "Saraydüzü",
    ],
    "Sivas": [
        "Merkez",
        "Şarkışla",
        "Yıldızeli",
        "Suşehri",
        "Gemerek",
        "Kangal",
        "Gürün",
        "Zara",
        "Koyulhisar",
        "Altınyayla",
        "Hafik",
        "Ulaş",
        "İmranlı",
        "Divriği",
        "Kızılca",
        "Doğanşar",
        "Akıncılar",
    ],
    "Şanlıurfa": [
        "Eyyübiye",
        "Haliliye",
        "Siverek",
        "Viranşehir",
        "Akçakale",
        "Suruç",
        "Birecik",
        "Ceylanpınar",
        "Kargılı",
        "Bozova",
        "Hilvan",
        "Halfeti",
    ],
    "Şırnak": [
        "Cizre",
        "Silopi",
        "Merkez",
        "İdil",
        "Uludere",
        "Güçlükonak",
        "Beytüşşebap",
    ],
    "Tekirdağ": [
        "Çorlu",
        "Süleymanpaşa",
        "Çerkezköy",
        "Kapaklı",
        "Ergene",
        "Malkara",
        "Saray",
        "Hayrabolu",
        "Muratlı",
        "Şarköy",
        "Marmaraereğlisi",
    ],
    "Tokat": [
        "Merkez",
        "Erbaa",
        "Turhal",
        "Niksar",
        "Zile",
        "Reşadiye",
        "Almus",
        "Pazar",
        "Başçiftlik",
        "Yeşilyurt",
        "Sulusaray",
        "Artova",
    ],
    "Trabzon": [
        "Ortahisar",
        "Akçaabat",
        "Araklı",
        "Of",
        "Sürmene",
        "Arsin",
        "Vakfıkebir",
        "Beşikdüzü",
        "Yomra",
        "Maçka",
        "Tonya",
        "Çarşıbaşı",
        "Düzköy",
        "Hayrat",
        "Şalpazarı",
        "Köprübaşı",
        "Dernekpazarı",
    ],
    "Tunceli": [
        "Merkez",
        "Pertek",
        "Çemişgezek",
        "Mazgirt",
        "Hozat",
        "Ovacık",
        "Nazımiye",
        "Pülümür",
    ],
    "Uşak": [
        "Merkez",
        "Banaz",
        "Eşme",
        "Sivaslı",
        "Ulubey",
        "Karahallı",
    ],
    "Van": [
        "İpekyolu",
        "Tuşba",
        "Edremit",
        "Erciş",
        "Muradiye",
        "Özalp",
        "Çaldıran",
        "Başkale",
        "Gürpınar",
        "Gevaş",
        "Saray",
        "Çatak",
        "Bahçesaray",
    ],
    "Yalova": [
        "Merkez",
        "Çiftlikköy",
        "Altınova",
        "Çınarcık",
        "Termal",
        "Armutlu",
    ],
    "Yozgat": [
        "Merkez",
        "Sorgun",
        "Akdağmadeni",
        "Yerköy",
        "Sarıkaya",
        "Boğazlıyan",
        "Şefaatli",
        "Çandır",
        "Çayıralan",
        "Kadışehri",
        "Saraykent",
        "Yenifakılı",
        "Aydıncık",
        "Çekerek",
    ],
    "Zonguldak": [
        "Merkez",
        "Ereğli",
        "Çaycuma",
        "Devrek",
        "Kozlu",
        "Alaplı",
        "Gökçebey",
        "Kilimli",
    ],
}
IL_KOORDINATLARI = {
    "Adana": (37.0000, 35.3213),
    "Adıyaman": (37.7648, 38.2786),
    "Afyonkarahisar": (38.7507, 30.5567),
    "Ağrı": (39.7191, 43.0503),
    "Aksaray": (38.3687, 34.0370),
    "Amasya": (40.6499, 35.8353),
    "Ankara": (39.9334, 32.8597),
    "Antalya": (36.8969, 30.7133),
    "Ardahan": (41.1105, 42.7022),
    "Artvin": (41.1828, 41.8183),
    "Aydın": (37.8560, 27.8416),
    "Balıkesir": (39.6484, 27.8826),
    "Bartın": (41.6344, 32.3375),
    "Batman": (37.8812, 41.1351),
    "Bayburt": (40.2552, 40.2249),
    "Bilecik": (40.1426, 29.9793),
    "Bingöl": (38.8854, 40.4966),
    "Bitlis": (38.3938, 42.1232),
    "Bolu": (40.7360, 31.6061),
    "Burdur": (37.7203, 30.2908),
    "Bursa": (40.1885, 29.0610),
    "Çanakkale": (40.1553, 26.4142),
    "Çankırı": (40.6013, 33.6134),
    "Çorum": (40.5506, 34.9556),
    "Denizli": (37.7765, 29.0864),
    "Diyarbakır": (37.9144, 40.2306),
    "Düzce": (40.8438, 31.1565),
    "Edirne": (41.6667, 26.5667),
    "Elazığ": (38.6810, 39.2264),
    "Erzincan": (39.7500, 39.5000),
    "Erzurum": (39.9000, 41.2700),
    "Eskişehir": (39.7767, 30.5206),
    "Gaziantep": (37.0662, 37.3833),
    "Giresun": (40.9128, 38.3895),
    "Gümüşhane": (40.4600, 39.4700),
    "Hakkari": (37.5833, 43.7333),
    "Hatay": (36.4018, 36.3498),
    "Iğdır": (39.9237, 44.0450),
    "Isparta": (37.7648, 30.5566),
    "İstanbul": (41.0082, 28.9784),
    "İzmir": (38.4237, 27.1428),
    "Kahramanmaraş": (37.5858, 36.9371),
    "Karabük": (41.2061, 32.6204),
    "Karaman": (37.1759, 33.2287),
    "Kars": (40.6013, 43.0975),
    "Kastamonu": (41.3887, 33.7827),
    "Kayseri": (38.7312, 35.4787),
    "Kırıkkale": (39.8468, 33.5153),
    "Kırklareli": (41.7333, 27.2167),
    "Kırşehir": (39.1425, 34.1709),
    "Kilis": (36.7184, 37.1212),
    "Kocaeli": (40.8533, 29.8815),
    "Konya": (37.8746, 32.4932),
    "Kütahya": (39.4167, 29.9833),
    "Malatya": (38.3552, 38.3095),
    "Manisa": (38.6191, 27.4289),
    "Mardin": (37.3212, 40.7245),
    "Mersin": (36.8000, 34.6333),
    "Muğla": (37.2153, 28.3636),
    "Muş": (38.9462, 41.7539),
    "Nevşehir": (38.6939, 34.6857),
    "Niğde": (37.9667, 34.6833),
    "Ordu": (40.9839, 37.8764),
    "Osmaniye": (37.0742, 36.2476),
    "Rize": (41.0201, 40.5234),
    "Sakarya": (40.7569, 30.3781),
    "Samsun": (41.2867, 36.3300),
    "Siirt": (37.9333, 41.9500),
    "Sinop": (42.0231, 35.1531),
    "Sivas": (39.7477, 37.0179),
    "Şanlıurfa": (37.1591, 38.7969),
    "Şırnak": (37.4187, 42.4918),
    "Tekirdağ": (40.9833, 27.5167),
    "Tokat": (40.3167, 36.5500),
    "Trabzon": (41.0027, 39.7168),
    "Tunceli": (39.1079, 39.5401),
    "Uşak": (38.6823, 29.4082),
    "Van": (38.4891, 43.4089),
    "Yalova": (40.6500, 29.2667),
    "Yozgat": (39.8181, 34.8147),
    "Zonguldak": (41.4564, 31.7987),
}

IL_SINIR_YARICAPI = {
    "İstanbul": 0.24,
    "Ankara": 0.22,
    "İzmir": 0.20,
    "Konya": 0.24,
    "Antalya": 0.22,
    "Bursa": 0.18,
    "Adana": 0.17,
    "Gaziantep": 0.16,
    "Şanlıurfa": 0.20,
    "Kocaeli": 0.14,
    "Mersin": 0.18,
    "Diyarbakır": 0.18,
    "Hatay": 0.15,
    "Manisa": 0.17,
    "Kayseri": 0.18,
    "Samsun": 0.17,
    "Balıkesir": 0.19,
    "Kahramanmaraş": 0.17,
    "Van": 0.20,
    "Aydın": 0.16,
    "Denizli": 0.16,
    "Sakarya": 0.13,
    "Tekirdağ": 0.14,
    "Muğla": 0.18,
    "Eskişehir": 0.17,
    "Mardin": 0.15,
    "Malatya": 0.16,
    "Trabzon": 0.14,
    "Erzurum": 0.22,
    "Ordu": 0.15,
    "Afyonkarahisar": 0.18,
    "Sivas": 0.22,
    "Tokat": 0.15,
    "Zonguldak": 0.12,
    "Çorum": 0.16,
    "Elazığ": 0.15,
    "Kütahya": 0.16,
    "Batman": 0.12,
    "Osmaniye": 0.12,
    "Adıyaman": 0.14,
    "Ağrı": 0.17,
    "Giresun": 0.14,
    "Isparta": 0.14,
    "Aksaray": 0.14,
    "Yalova": 0.09,
    "Düzce": 0.11,
    "Çanakkale": 0.17,
    "Kırklareli": 0.14,
    "Niğde": 0.14,
    "Nevşehir": 0.13,
    "Kastamonu": 0.18,
    "Kırıkkale": 0.12,
    "Uşak": 0.13,
    "Bolu": 0.14,
    "Karaman": 0.14,
    "Muş": 0.14,
    "Şırnak": 0.14,
    "Bitlis": 0.14,
    "Kars": 0.15,
    "Amasya": 0.12,
    "Edirne": 0.13,
    "Karabük": 0.11,
    "Yozgat": 0.17,
    "Kırşehir": 0.12,
    "Burdur": 0.13,
    "Siirt": 0.12,
    "Bingöl": 0.13,
    "Hakkari": 0.13,
    "Bilecik": 0.11,
    "Sinop": 0.13,
    "Bartın": 0.10,
    "Artvin": 0.14,
    "Çankırı": 0.14,
    "Gümüşhane": 0.12,
    "Iğdır": 0.11,
    "Tunceli": 0.13,
    "Kilis": 0.09,
    "Bayburt": 0.10,
    "Ardahan": 0.12,
}

nufus_agirliklari = {
    "İstanbul": 0.185,
    "Ankara": 0.068,
    "İzmir": 0.052,
    "Bursa": 0.038,
    "Antalya": 0.032,
    "Konya": 0.027,
    "Adana": 0.027,
    "Şanlıurfa": 0.026,
    "Gaziantep": 0.025,
    "Kocaeli": 0.025,
    "Mersin": 0.023,
    "Diyarbakır": 0.021,
    "Hatay": 0.019,
    "Manisa": 0.017,
    "Kayseri": 0.017,
    "Samsun": 0.016,
    "Balıkesir": 0.015,
    "Kahramanmaraş": 0.014,
    "Van": 0.013,
    "Aydın": 0.013,
    "Denizli": 0.012,
    "Sakarya": 0.013,
    "Tekirdağ": 0.014,
    "Muğla": 0.012,
    "Eskişehir": 0.011,
    "Mardin": 0.010,
    "Malatya": 0.009,
    "Trabzon": 0.010,
    "Erzurum": 0.009,
    "Ordu": 0.009,
    "Afyonkarahisar": 0.009,
    "Sivas": 0.008,
    "Tokat": 0.007,
    "Zonguldak": 0.007,
    "Çorum": 0.006,
    "Elazığ": 0.007,
    "Kütahya": 0.007,
    "Batman": 0.008,
    "Osmaniye": 0.007,
    "Adıyaman": 0.007,
    "Ağrı": 0.006,
    "Giresun": 0.005,
    "Isparta": 0.005,
    "Aksaray": 0.005,
    "Yalova": 0.004,
    "Düzce": 0.005,
    "Çanakkale": 0.007,
    "Kırklareli": 0.004,
    "Niğde": 0.004,
    "Nevşehir": 0.004,
    "Kastamonu": 0.004,
    "Kırıkkale": 0.003,
    "Uşak": 0.004,
    "Bolu": 0.004,
    "Karaman": 0.003,
    "Muş": 0.005,
    "Şırnak": 0.007,
    "Bitlis": 0.004,
    "Kars": 0.003,
    "Amasya": 0.004,
    "Edirne": 0.005,
    "Karabük": 0.003,
    "Yozgat": 0.005,
    "Kırşehir": 0.003,
    "Burdur": 0.003,
    "Siirt": 0.004,
    "Bingöl": 0.003,
    "Hakkari": 0.003,
    "Bilecik": 0.003,
    "Sinop": 0.003,
    "Bartın": 0.002,
    "Artvin": 0.002,
    "Çankırı": 0.002,
    "Gümüşhane": 0.002,
    "Iğdır": 0.002,
    "Tunceli": 0.001,
    "Kilis": 0.002,
    "Bayburt": 0.001,
    "Ardahan": 0.001,
}

buyuk_suc_agirliklari = {
    "İstanbul": 1.45,
    "Ankara": 1.25,
    "İzmir": 1.25,
    "Adana": 1.30,
    "Mersin": 1.28,
    "Gaziantep": 1.22,
    "Şanlıurfa": 1.20,
    "Diyarbakır": 1.22,
    "Hatay": 1.24,
    "Antalya": 1.18,
    "Bursa": 1.15,
    "Kocaeli": 1.18,
    "Konya": 1.10,
    "Mardin": 1.18,
    "Van": 1.15,
    "Hakkari": 1.20,
    "Şırnak": 1.18,
    "Batman": 1.15,
    "Samsun": 1.12,
    "Trabzon": 1.10,
    "Kayseri": 1.08,
    "Eskişehir": 1.06,
    "Muğla": 1.12,
    "Tekirdağ": 1.12,
    "Sakarya": 1.10,
    "Aydın": 1.08,
    "Denizli": 1.06,
    "Manisa": 1.08,
    "Balıkesir": 1.08,
    "Kahramanmaraş": 1.10,
    "Malatya": 1.06,
    "Elazığ": 1.06,
    "Erzurum": 1.05,
}

tum_iller = list(TURKIYE_IL_ILCELER.keys())
ham_agirliklar = np.array(
    [nufus_agirliklari.get(il, 0.002) for il in tum_iller], dtype=np.float64
)
agirliklar = ham_agirliklar / ham_agirliklar.sum()
@st.cache_data(max_entries=2, show_spinner="AKIN profil verisi hazırlanıyor...")
def veriyi_yukle(n: int = 250000):
  rng = np.random.default_rng(42)
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

  ad_soyadlar = (
      pd.Series(rng.choice(ad_havuzu, size=n), dtype="string")
      + " "
      + pd.Series(rng.choice(soyad_havuzu, size=n), dtype="string")
  ).to_numpy()

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
  mahalle_no = pd.Series(rng.integers(1, 40, size=n), dtype="string")
  mahalleler = (
      pd.Series(ilceler, dtype="string") + " Mah. " + mahalle_no
  ).to_numpy()

  gecmis_ikametler = np.where(
      rng.random(n) > 0.5,
      (
          pd.Series(secilen_iller, dtype="string")
          + " bölgesinde uzun süredir ikamet ediyor."
      ).to_numpy(),
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
  p_taban = (
      "İl nüfus + büyük suç katsayısı: "
      + pd.Series(np.round(il_buyuk_suc_katsayi, 2), dtype="string")
      + "x"
  ).to_numpy()

  gerekce_dizi = (
      pd.Series(p_dark, dtype="string")
      + pd.Series(p_plaka, dtype="string")
      + pd.Series(p_tesis, dtype="string")
      + pd.Series(p_sicil, dtype="string")
      + pd.Series(p_tor, dtype="string")
      + pd.Series(p_taban, dtype="string")
  ).to_numpy()

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
  risk_seviyesi = np.select(
      conditions, choices, default="🟡 Sarı (İzleme Düzeyi)"
  )

  return pd.DataFrame({
      "TC_No": rng.integers(10000000000, 99999999999, size=n, dtype=np.int64),
      "Ad_Soyad": ad_soyadlar,
      "Vatandaslik_Durumu": pd.Categorical(
          rng.choice(
              ["T.C. Vatandaşı", "Yabancı Uyruklu"], size=n, p=[0.93, 0.07]
          )
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
      "Eylem_Zamani_Projeksiyonu": pd.Categorical(
          rng.choice(zaman_havuzu, size=n)
      ),
      "Zihinsel_Niyet_Analizi": pd.Categorical(rng.choice(niyet_havuzu, size=n)),
      "Risk_Seviyesi": pd.Categorical(risk_seviyesi),
  })


st.sidebar.title("🎛️ AKIN Kontrol Paneli")
secilen_kayit_sayisi = st.sidebar.selectbox(
    "Simüle Edilecek Profil Sayısı",
    options=[100000, 250000, 500000, 1000000],
    index=1,
    key="kayit_sayisi_sb",
)
df = veriyi_yukle(secilen_kayit_sayisi)

secili_seviyeler = st.sidebar.multiselect(
    "Risk Seviyesi Filtresi",
    options=[
        "⬛ Siyah (Kritik Tehdit)",
        "🔴 Kırmızı (Yüksek Risk)",
        "🟠 Turuncu (Orta Risk)",
        "🟡 Sarı (İzleme Düzeyi)",
    ],
    default=[
        "⬛ Siyah (Kritik Tehdit)",
        "🔴 Kırmızı (Yüksek Risk)",
        "🟠 Turuncu (Orta Risk)",
        "🟡 Sarı (İzleme Düzeyi)",
    ],
)
min_skor = st.sidebar.slider(
    "Minimum Anomali Skoru", min_value=1.0, max_value=10.0, value=1.0, step=0.5
)
secili_il = st.sidebar.selectbox(
    "İl Filtresi", options=["Tümü"] + sorted(tum_iller)
)

süzülmüş_df = df[
    df["Risk_Seviyesi"].isin(secili_seviyeler)
    & (df["Hesaplanan_Anomali_Skoru"] >= min_skor)
]
if secili_il != "Tümü":
  süzülmüş_df = süzülmüş_df[süzülmüş_df["Ikamet_Ili"] == secili_il]
    top_left, top_right = st.columns([3, 1.2])
with top_left:
  st.markdown(
      """
        <div class="akin-banner">
            <div style="font-size: 1.45rem; font-weight: 800; letter-spacing: 0.3px;">
                🚨 AKIN — Anomali, Konum, İzleme ve Niyet Analiz Paneli
            </div>
            <div style="color: #b8c4d0; font-size: 0.92rem; margin-top: 4px;">
                Türkiye geneli sentetik davranışsal profil, bölgesel yoğunluk ve anomali skoru simülasyonu
            </div>
            <div>
                <span class="akin-pill">Simülasyon Modu</span>
                <span class="akin-pill">81 İl Kapsamı</span>
                <span class="akin-pill">Canlı TR Saat</span>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )
with top_right:
  canli_saat_kutusu(hizalama="flex-end")

toplam_profil = len(süzülmüş_df)
kritik_sayi = int(
    (
        süzülmüş_df["Risk_Seviyesi"].isin(
            ["⬛ Siyah (Kritik Tehdit)", "🔴 Kırmızı (Yüksek Risk)"]
        )
    ).sum()
)
ortalama_skor = (
    float(süzülmüş_df["Hesaplanan_Anomali_Skoru"].mean())
    if toplam_profil > 0
    else 0.0
)
darkweb_sayi = int(
    (süzülmüş_df["DarkWeb_Aramasi_Patlayici"] == "Tespit Edildi!").sum()
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Filtrelenen Profil", f"{toplam_profil:,}".replace(",", "."))
m2.metric("Yüksek / Kritik Risk", f"{kritik_sayi:,}".replace(",", "."))
m3.metric("Ortalama Anomali Skoru", f"{ortalama_skor:.2f} / 10")
m4.metric("DarkWeb Sinyali", f"{darkweb_sayi:,}".replace(",", "."))

tab1, tab2, tab3 = st.tabs([
    "🗺️ Bölgesel Harita ve Yoğunluk",
    "🔎 Yüksek Riskli Profil İnceleme",
    "📊 İl Bazlı Özet Tablo",
])

with tab1:
  st.subheader("Türkiye Bölgesel Anomali Yoğunluğu")
  if süzülmüş_df.empty:
    st.warning("Seçili filtre kriterlerine uygun profil bulunamadı.")
  else:
    harita_df = süzülmüş_df[["lat", "lon", "Hesaplanan_Anomali_Skoru"]].head(
        15000
    )
    katman = pdk.Layer(
        "HeatmapLayer",
        data=harita_df,
        get_position=["lon", "lat"],
        get_weight="Hesaplanan_Anomali_Skoru",
        radius_pixels=32,
        intensity=1.2,
        threshold=0.05,
    )
    merkez_lat = (
        float(harita_df["lat"].mean()) if secili_il != "Tümü" else 39.0
    )
    merkez_lon = (
        float(harita_df["lon"].mean()) if secili_il != "Tümü" else 35.0
    )
    zoom_degeri = 8.2 if secili_il != "Tümü" else 5.2

    gorunum = pdk.ViewState(
        latitude=merkez_lat,
        longitude=merkez_lon,
        zoom=zoom_degeri,
        pitch=35,
    )
    st.pydeck_chart(
        pdk.Deck(
            layers=[katman],
            initial_view_state=gorunum,
            map_style="mapbox://styles/mapbox/dark-v10",
        ),
        use_container_width=True,
    )

with tab2:
  st.subheader("En Yüksek Anomali Skoruna Sahip Profiller")
  if süzülmüş_df.empty:
    st.info("Görüntülenecek profil yok.")
  else:
    en_riskli = süzülmüş_df.sort_values(
        by="Hesaplanan_Anomali_Skoru", ascending=False
    ).head(12)
    for _, satir in en_riskli.iterrows():
      rozet_css = risk_rozet_stili(str(satir["Risk_Seviyesi"]))
      st.markdown(
          f"""
                <div class="akin-card">
                    <span class="risk-badge" style="{rozet_css}">{satir["Risk_Seviyesi"]} • Skor
        
