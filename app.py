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
        "S
