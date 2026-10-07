"""
Advanced GeoAI Agent - Borneo Spaceport Site Selection
=======================================================
CYBERPUNK EDITION: Futuristic UI + OSM Up-to-Date + INSTANT Results

A comprehensive end-to-end demonstration of advanced agent capabilities:
- Multi-step reasoning with chain of thought
- External API integration (OpenStreetMap, weather, elevation)
- Short-term and long-term memory systems
- Design patterns (Pipeline, Strategy, Repository)

FOCUSED ON: SPACEPORT SITE SELECTION IN SABAH & SARAWAK, MALAYSIA (Borneo) 🚀
Author: GeoAI Training Module 5 (Modified for Spaceport Site Selection)

ENHANCEMENTS:
- ✅ INSTANT results (geographic rules) - 3-5 seconds
- ✅ Live OSM Up-to-Date (background fetching)
- ✅ 24-hour API caching (fast repeat analyses)
- ✅ Geographic fallback (guaranteed results)
- ✅ Data source transparency
- ✅ All original design patterns preserved
- ✅ COMPLETE Sabah & Sarawak coverage (250+ locations)
- ✅ CYBERPUNK / FUTURISTIC UI
- ✅ CRYSTAL CLEAR READABILITY (all text pure white)
- ✅ DETAILED RECOMMENDATION STRATEGY (actionable insights)
- ✅ FIXED: Score can no longer exceed 100%
- ✅ FIXED: Feasibility now consistent with critical actions
"""

import streamlit as st
import folium
from folium.plugins import Fullscreen, MiniMap, MousePosition, Draw, HeatMap
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from functools import wraps
import requests
from pathlib import Path
import sqlite3
import pickle
import math
import threading
import queue

# ============================================================================
# CYBERPUNK STYLING - CRYSTAL CLEAR READABILITY
# ============================================================================

CYBERPUNK_CSS = """
<style>
    :root {
        --neon-cyan: #00f0ff;
        --neon-pink: #ff2d95;
        --neon-purple: #b026ff;
        --neon-green: #39ff14;
        --neon-yellow: #ffe84d;
        --dark-bg: #0a0a0f;
        --card-bg: rgba(15, 15, 35, 0.92);
        --text-white: #ffffff;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a1f 100%);
    }
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.3);
        letter-spacing: 4px;
        animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 40px rgba(0, 240, 255, 0.3); }
        50% { text-shadow: 0 0 60px rgba(0, 240, 255, 0.6), 0 0 80px rgba(176, 38, 255, 0.3); }
    }
    .subtitle {
        font-family: 'Courier New', monospace;
        color: #00f0ff;
        font-size: 1.2rem;
        letter-spacing: 8px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .css-1d391kg, .css-1633s9g {
        background: rgba(10, 10, 20, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    .css-1d391kg p, .css-1633s9g p,
    .css-1d391kg label, .css-1633s9g label,
    .css-1d391kg div, .css-1633s9g div,
    .css-1d391kg span, .css-1633s9g span {
        color: #ffffff !important;
        font-weight: 400 !important;
    }
    .recommendation-container {
        background: rgba(15, 15, 35, 0.85);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease;
    }
    .recommendation-container:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.15);
        transform: translateY(-2px);
    }
    .recommendation-title {
        color: #00f0ff;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    }
    .recommendation-item {
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        padding: 6px 0;
        border-bottom: 1px solid rgba(0, 240, 255, 0.05);
        line-height: 1.6;
    }
    .recommendation-item:last-child { border-bottom: none; }
    .recommendation-item .icon { margin-right: 8px; }
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(176, 38, 255, 0.15)) !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px);
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.3), rgba(176, 38, 255, 0.3)) !important;
        border-color: #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3) !important;
        transform: scale(1.02);
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(176, 38, 255, 0.25)) !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }
    [data-testid="metric-container"] {
        background: rgba(15, 15, 35, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(5px);
    }
    [data-testid="metric-container"] label {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px;
        font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] div {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    .dataframe {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    .dataframe th {
        color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.1) !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px;
        font-weight: bold !important;
        font-size: 0.9rem !important;
    }
    .dataframe td {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85rem !important;
    }
    .streamlit-expanderHeader {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important;
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px;
        font-weight: bold !important;
    }
    .streamlit-expanderContent {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.1) !important;
        border-top: none !important;
    }
    .streamlit-expanderContent p, .streamlit-expanderContent div,
    .streamlit-expanderContent li, .streamlit-expanderContent span {
        color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: #00f0ff !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
    }
    .stAlert {
        background: rgba(15, 15, 35, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    .stAlert p, .stAlert div, .stAlert li, .stAlert span { color: #ffffff !important; }
    .stProgress > div > div {
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00f0ff !important;
        border-bottom: 2px solid #00f0ff !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        font-weight: bold !important;
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(10, 10, 20, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00f0ff, #b026ff);
        border-radius: 3px;
    }
    .folium-map {
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.05);
    }
    .cyber-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00f0ff, #b026ff, #ff2d95, transparent);
        margin: 20px 0;
        opacity: 0.5;
    }
    .stMarkdown p, .stMarkdown li {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        line-height: 1.6 !important;
    }
    .stMarkdown h1 { color: #00f0ff !important; }
    .stMarkdown h2 { color: #b026ff !important; }
    .stMarkdown h3 { color: #ff2d95 !important; }
    .stMarkdown h4 { color: #39ff14 !important; }
    .stCaption {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
    }
</style>
"""

# ============================================================================
# RECOMMENDATION ENGINE (FIXED - consistent with critical actions)
# ============================================================================

def generate_recommendation_strategy(result_data: Dict) -> Dict:
    """Generate recommendation strategy. Feasibility consistent with actions."""
    score = result_data.get('suitability_percentage', 0)
    details = result_data.get('details', {})
    elevation_m = result_data.get('elevation_m', 0)
    flood_risk = result_data.get('flood_risk', 'Unknown')
    population_density = result_data.get('population_density', 0)
    coastal_distance = result_data.get('coastal_distance_km', 0)

    recommendations = {
        'immediate_actions': [],
        'short_term_actions': [],
        'long_term_actions': [],
        'investment_required': 'Low',
        'overall_feasibility': 'High',
        'risk_level': 'Low',
    }

    def add_action(bucket, text, priority, cost):
        recommendations[bucket].append({
            'text': text, 'priority': priority, 'cost': cost
        })

    # 1. ELEVATION
    if elevation_m < 20:
        add_action('immediate_actions',
            '🚨 CRITICAL: Elevation is very low (<20m). Build massive flood defenses and elevated launch pads immediately.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif elevation_m < 50:
        add_action('short_term_actions',
            '🌊 Build flood defenses and drainage systems. Elevation is moderate.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'
    elif elevation_m < 200:
        add_action('immediate_actions',
            '✅ Excellent elevation (50-200m). No flood defenses needed. Proceed with standard launch pad design.',
            'Low', '💸')
    elif elevation_m < 500:
        add_action('short_term_actions',
            '⛰️ Good elevation (200-500m). Plan for stable foundations and wind protection.',
            'Medium', '💸💸')
    else:
        add_action('short_term_actions',
            '🏔️ Very high elevation (500m+). Consider construction challenges and weather protection.',
            'Medium', '💸💸💸')

    # 2. POPULATION
    if population_density > 5:
        add_action('immediate_actions',
            '🏙️ HIGH POPULATION DENSITY. Need extensive evacuation plans and safety buffer zones.',
            'Critical', '💸💸💸💸')
    elif population_density > 2:
        add_action('short_term_actions',
            '🏘️ MODERATE POPULATION. Develop evacuation procedures and community engagement.',
            'High', '💸💸💸')
    else:
        add_action('immediate_actions',
            '✅ VERY LOW POPULATION. Ideal for spaceport - minimal evacuation required.',
            'Low', '💸')

    # 3. COASTAL
    if coastal_distance < 5:
        add_action('immediate_actions',
            '🌊 PERFECT COASTAL ACCESS. Leverage sea transport for heavy equipment.',
            'Low', '💸')
    elif coastal_distance < 30:
        add_action('short_term_actions',
            '🚢 GOOD COASTAL ACCESS. Build access roads to the coast. Consider sea transport hub.',
            'Medium', '💸💸')
    else:
        add_action('long_term_actions',
            '🚛 INLAND LOCATION. Significant transport infrastructure needed.',
            'High', '💸💸💸💸')

    # 4. INFRASTRUCTURE
    infra_details = details.get('infrastructure_access', {}).get('value', {})
    if isinstance(infra_details, dict):
        if infra_details.get('airports', 0) == 0:
            add_action('short_term_actions',
                '✈️ No airport nearby. Build airstrip for personnel transport.',
                'High', '💸💸💸')
        if infra_details.get('major_roads', 0) == 0:
            add_action('short_term_actions',
                '🛣️ No major roads. Build access roads for equipment transport.',
                'High', '💸💸💸')
        if infra_details.get('ports', 0) == 0:
            add_action('long_term_actions',
                '🚢 No port. Consider building a small port for heavy equipment delivery.',
                'Medium', '💸💸💸💸')
        if infra_details.get('power_facilities', 0) == 0:
            add_action('long_term_actions',
                '⚡ No power infrastructure. Build power plant or connect to grid.',
                'High', '💸💸💸💸')

    # 5. LAND
    land_details = details.get('land_availability', {}).get('value', {})
    if isinstance(land_details, dict):
        forest = land_details.get('forest_areas', 0)
        developed = land_details.get('developed_areas', 0)
        if forest > 20 and developed < 5:
            add_action('immediate_actions',
                '🌳 ABUNDANT LAND. Excellent for expansion. Ready for development.',
                'Low', '💸')
        elif forest > 10 and developed < 10:
            add_action('short_term_actions',
                '🌿 GOOD LAND AVAILABILITY. Plan for expansion and buffer zones.',
                'Medium', '💸💸')
        else:
            add_action('immediate_actions',
                '🏗️ LIMITED LAND. Need to acquire additional land for launch pads and safety zones.',
                'Critical', '💸💸💸💸')

    # 6. FLOOD
    if flood_risk == 'High':
        add_action('immediate_actions',
            '🌊 HIGH FLOOD RISK! Emergency flood defenses needed. Consider elevating all structures.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif flood_risk == 'Moderate':
        add_action('short_term_actions',
            '🌊 MODERATE FLOOD RISK. Build standard flood defenses and drainage systems.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'

    # 7. LATITUDE
    lat_deg = result_data.get('lat_deg', 0)
    if lat_deg < 3:
        add_action('immediate_actions',
            f'🌐 EXCELLENT LATITUDE ({lat_deg:.1f}°). Near equator - maximum fuel efficiency! ✅',
            'Low', '💸')
    elif lat_deg < 5:
        add_action('immediate_actions',
            f'🌐 GOOD LATITUDE ({lat_deg:.1f}°). Good launch efficiency.',
            'Low', '💸')
    else:
        add_action('short_term_actions',
            f'🌐 MODERATE LATITUDE ({lat_deg:.1f}°). Optimize launch trajectories for fuel efficiency.',
            'Medium', '💸💸')

    # ================= FIXED FEASIBILITY LOGIC =================
    critical_count = sum(
        1 for a in recommendations['immediate_actions']
        if a['priority'] == 'Critical'
    )
    high_count = sum(
        1 for a in recommendations['short_term_actions']
        if a['priority'] == 'High'
    )
    total_actions = (
        len(recommendations['immediate_actions'])
        + len(recommendations['short_term_actions'])
        + len(recommendations['long_term_actions'])
    )

    if score >= 80:
        score_band, score_emoji = 'Excellent', '✅'
    elif score >= 65:
        score_band, score_emoji = 'Good', '👍'
    elif score >= 50:
        score_band, score_emoji = 'Moderate', '👌'
    elif score >= 35:
        score_band, score_emoji = 'Limited', '⚠️'
    else:
        score_band, score_emoji = 'Poor', '❌'

    # Critical overrides — feasibility can never exceed what Critical actions permit
    if critical_count >= 3:
        feasibility = '❌ Poor - Major critical issues must be resolved before development'
        risk_level = 'Very High'
    elif critical_count == 2:
        feasibility = '⚠️ Limited - Multiple critical issues require resolution'
        risk_level = 'High'
    elif critical_count == 1:
        feasibility = '👌 Moderate - One critical issue requires resolution'
        risk_level = 'High'
    elif high_count >= 2:
        feasibility = '👌 Moderate - Several high-priority preparations required'
        risk_level = 'Medium'
    else:
        feasibility = f'{score_emoji} {score_band} - ' + {
            'Excellent': 'High potential for immediate development',
            'Good': 'Suitable with minor site preparation',
            'Moderate': 'Significant investment required',
            'Limited': 'Major investment required',
            'Poor': 'Not recommended for spaceport development',
        }[score_band]
        risk_level = {
            'Excellent': 'Low', 'Good': 'Low',
            'Moderate': 'Medium', 'Limited': 'High', 'Poor': 'Very High',
        }[score_band]

    recommendations['overall_feasibility'] = feasibility
    recommendations['risk_level'] = risk_level
    recommendations['critical_action_count'] = critical_count
    recommendations['high_action_count'] = high_count
    recommendations['total_action_count'] = total_actions

    recommendations['timeline_summary'] = {
        'immediate': f"{len(recommendations['immediate_actions'])} actions (0-6 months)",
        'short_term': f"{len(recommendations['short_term_actions'])} actions (6-18 months)",
        'long_term': f"{len(recommendations['long_term_actions'])} actions (18-36 months)"
    }
    return recommendations

# ============================================================================
# CACHE MANAGEMENT (24-hour TTL)
# ============================================================================

class APICache:
    def __init__(self, cache_dir: str = "api_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_key(self, url: str, params: Dict) -> str:
        key_str = url + json.dumps(params, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, url: str, params: Dict) -> Optional[Dict]:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            modified_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - modified_time < self.ttl:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception:
                    return None
        return None

    def set(self, url: str, params: Dict, data: Dict) -> None:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass

    def clear(self):
        for f in self.cache_dir.glob("*.json"):
            f.unlink()

    def get_stats(self) -> Dict:
        files = list(self.cache_dir.glob("*.json"))
        return {'total_cached': len(files), 'cache_dir': str(self.cache_dir)}

api_cache = APICache()

# ============================================================================
# COMPLETE SABAH LOCATIONS
# ============================================================================

SABAH_LOCATIONS = {
    'Kota Kinabalu City Center': (5.9804, 116.0735),
    'KK Waterfront': (5.9850, 116.0750),
    'Tanjung Aru Beach': (5.9400, 116.0500),
    'Likas Bay': (5.9500, 116.0200),
    'Signal Hill': (5.9750, 116.0700),
    'Atkinson Clock Tower': (5.9800, 116.0710),
    'Sabah State Mosque': (5.9600, 116.0800),
    'Tun Mustapha Tower': (5.9900, 116.0700),
    'Sabah Museum': (5.9600, 116.0650),
    'Jesselton Point': (5.9850, 116.0750),
    '1Borneo Mall': (6.0200, 116.1100),
    'Imago Mall': (5.9800, 116.0700),
    'Suria Sabah': (5.9800, 116.0700),
    'Sutera Harbour': (5.9600, 116.0600),
    'Queen Elizabeth Hospital': (5.9680, 116.0680),
    'KPJ Sabah Hospital': (5.9800, 116.0730),
    'Universiti Malaysia Sabah': (6.0300, 116.1200),
    'Penampang': (5.9000, 116.0800),
    'Putatan': (5.8800, 116.0600),
    'Tuaran': (6.1800, 116.2400),
    'Papar': (5.7300, 115.9300),
    'Kinarut': (5.8200, 116.0500),
    'Lok Kawi': (5.8500, 116.0300),
    'Kota Kinabalu Industrial Park': (5.9200, 116.0400),
    'Menggatal': (6.0200, 116.1400),
    'Sepanggar': (6.0400, 116.0900),
    'Inanam': (6.0000, 116.1200),
    'Telipok': (6.0800, 116.1900),
    'Likas': (5.9600, 116.0300),
    'Luyang': (5.9300, 116.0700),
    'Donggongon': (5.9000, 116.0900),
    'Keningau': (5.3300, 116.1600),
    'Tenom': (5.1300, 115.9500),
    'Beaufort': (5.3500, 115.7500),
    'Sipitang': (5.0800, 115.5500),
    'Nabawan': (5.0800, 116.4300),
    'Tambunan': (5.6700, 116.3600),
    'Kuala Penyu': (5.5700, 115.5800),
    'Membakut': (5.4700, 115.7800),
    'Weston': (5.2700, 115.4800),
    'Kemabong': (5.0800, 116.0800),
    'Sook': (5.1300, 116.2200),
    'Melalap': (5.0800, 115.9000),
    'Bongawan': (5.5300, 115.8300),
    'Klias': (5.4300, 115.6800),
    'Limbawang': (5.1700, 115.5800),
    'Gana': (5.0300, 115.4800),
    'Kudat': (6.8860, 116.8430),
    'Kota Marudu': (6.5000, 116.7400),
    'Pitas': (6.7200, 117.0700),
    'Banggi Island': (7.2300, 117.1700),
    'Malawali Island': (7.1500, 117.1300),
    'Tanjung Simpang Mengayau': (7.0900, 116.9100),
    'Bakapit': (6.8000, 116.8000),
    'Matunggong': (6.7700, 116.7900),
    'Tindakon': (6.8700, 116.8500),
    'Pinangsoo': (6.9200, 116.8800),
    'Perancangan': (6.9500, 116.9000),
    'Sandakan City Center': (5.8400, 118.1200),
    'Sandakan Waterfront': (5.8420, 118.1220),
    'Sandakan Hospital': (5.8480, 118.1250),
    'Sandakan Airport': (5.9010, 118.0580),
    'Sandakan Harbour': (5.8400, 118.1300),
    'Sepilok Orangutan Centre': (5.8650, 117.9420),
    'Sandakan Rainforest Discovery Centre': (5.8700, 117.9450),
    'Gomantong Caves': (5.5300, 118.0700),
    'Sukau': (5.5000, 118.2500),
    'Kinabatangan River': (5.4000, 117.8000),
    'Telupid': (5.6300, 117.1300),
    'Beluran': (5.8800, 117.5600),
    'Pamol': (5.4800, 118.0800),
    'Batu Putih': (5.3800, 117.9200),
    'Muanad': (5.4800, 118.1800),
    'Bilit': (5.4200, 117.8200),
    'Abai': (5.3500, 117.6800),
    'Batu Bulan': (5.2800, 117.5800),
    'Tawau City Center': (4.2435, 117.8853),
    'Tawau Waterfront': (4.2450, 117.8870),
    'Tawau Hospital': (4.2520, 117.8970),
    'Tawau Airport': (4.3133, 117.9183),
    'Tawau Hills Park': (4.3500, 117.9000),
    'Tawau Sports Complex': (4.2400, 117.8800),
    'Lahad Datu': (5.0300, 118.3300),
    'Felda Sahabat': (5.0620, 119.0810),
    'Dent Haven': (5.2680, 119.2620),
    'Semporna': (4.4800, 118.6100),
    'Kunak': (4.6800, 118.2500),
    'Silam': (4.8700, 118.2300),
    'Kalabakan': (4.2200, 117.4800),
    'Maliau Basin': (4.7200, 117.5200),
    'Danum Valley': (4.9500, 117.7800),
    'Tabin Wildlife Reserve': (5.2000, 118.6500),
    'Tungku': (4.7000, 118.2000),
    'Merotai': (4.3000, 117.8500),
    'Apas': (4.2800, 117.8800),
    'Balung': (4.1800, 117.6800),
    'Umas Umas': (4.1500, 117.5800),
    'Bombalai': (4.1200, 117.4800),
    'Tanjung Batu': (4.0500, 117.3800),
    'Mount Kinabalu': (6.0750, 116.5583),
    'Kinabalu National Park': (6.0100, 116.5400),
    'Kundasang': (5.9800, 116.5700),
    'Ranau': (5.9500, 116.6700),
    'Mesilau': (6.0400, 116.5900),
    'Poring Hot Springs': (6.0500, 116.7000),
    'Crocker Range': (5.8000, 116.3000),
    'Trus Madi': (5.5000, 116.4000),
    'Maliau Basin Conservation': (4.7200, 117.5200),
    'Long Pasia': (4.4000, 115.7500),
    'Kipungit': (6.0200, 116.6200),
    'Eastern Sabah Hills': (5.0000, 117.8500),
    'Pulau Gaya': (5.9800, 116.0200),
    'Pulau Manukan': (5.9700, 116.0000),
    'Pulau Mamutik': (5.9600, 115.9900),
    'Pulau Sapi': (5.9500, 115.9900),
    'Pulau Sulug': (5.9400, 115.9800),
    'Pulau Sipadan': (4.1140, 118.6250),
    'Pulau Mabul': (4.2400, 118.6200),
    'Pulau Kapalai': (4.2100, 118.6600),
    'Pulau Ligitan': (4.1500, 118.8800),
    'Pulau Bohey Dulang': (4.5800, 118.7800),
    'Pulau Bum Bum': (4.5000, 118.7100),
    'Pulau Sebatik': (4.1300, 117.7800),
    'Pulau Tiga': (5.7200, 115.6300),
    'Pulau Dinawan': (5.7000, 115.5800),
}

# ============================================================================
# COMPLETE SARAWAK LOCATIONS
# ============================================================================

SARAWAK_LOCATIONS = {
    'Kuching City Center': (1.5497, 110.3633),
    'Kuching Waterfront': (1.5597, 110.3433),
    'Kuching Hospital': (1.5697, 110.3533),
    'Kuching Airport': (1.4843, 110.3469),
    'Sarawak Museum': (1.5547, 110.3633),
    'Sarawak State Mosque': (1.5547, 110.3533),
    'Kuching Civic Centre': (1.5597, 110.3633),
    'Borneo Convention Centre': (1.5647, 110.3833),
    'Satok Bridge': (1.5497, 110.3433),
    'Stutong Park': (1.5347, 110.3833),
    'Damai Beach': (1.7000, 110.3800),
    'Santubong': (1.7000, 110.3800),
    'Bako National Park': (1.7400, 110.4800),
    'Semenggoh Wildlife Centre': (1.4000, 110.3300),
    'Bau': (1.4100, 110.1500),
    'Lundu': (1.6700, 109.8500),
    'Puncak Borneo': (1.2500, 110.1000),
    'Padawan': (1.3500, 110.2000),
    'Serian': (1.1700, 110.5700),
    'Siburan': (1.3000, 110.3500),
    'Tebedu': (1.1200, 110.5300),
    'Bengkoh': (1.4500, 110.2500),
    'Kota Sentosa': (1.4800, 110.3300),
    'Jalan Batu Kawa': (1.5000, 110.3000),
    'Matang': (1.6200, 110.1800),
    'Kuching Wetlands': (1.5800, 110.3200),
    'Kota Samarahan': (1.4500, 110.5000),
    'Asajaya': (1.6000, 110.6200),
    'Simunjan': (1.3800, 110.7500),
    'Sebuyau': (1.5200, 110.9300),
    'Sadong Jaya': (1.4700, 110.7300),
    'Muaras': (1.5300, 110.5800),
    'Semera': (1.4200, 110.4800),
    'Sri Aman': (1.2000, 111.5000),
    'Lubok Antu': (1.0500, 111.8300),
    'Engkilili': (1.1300, 111.6700),
    'Pantu': (1.0800, 111.4200),
    'Lingga': (1.3300, 111.1500),
    'Balai Ringin': (1.0300, 111.1500),
    'Rimbang': (1.1000, 111.3000),
    'Betong': (1.4100, 111.5300),
    'Debak': (1.5600, 111.4200),
    'Pusa': (1.4800, 111.3000),
    'Saratok': (1.7400, 111.3200),
    'Spaoh': (1.4500, 111.4500),
    'Maludam': (1.6500, 111.2500),
    'Roban': (1.6800, 111.3800),
    'Sarikei': (2.1000, 111.8000),
    'Bintangor': (2.1500, 111.9000),
    'Julau': (2.0200, 111.9100),
    'Pakan': (1.8800, 111.7800),
    'Matu': (2.1000, 111.5300),
    'Daro': (2.0500, 111.4800),
    'Jakar': (2.0800, 111.6500),
    'Sibu City Center': (2.2871, 111.8301),
    'Sibu Waterfront': (2.2971, 111.8201),
    'Sibu Hospital': (2.2971, 111.8401),
    'Sibu Airport': (2.2586, 111.9661),
    'Sibu Central Market': (2.2871, 111.8301),
    'Tua Pek Kong Temple': (2.2871, 111.8301),
    'Kanowit': (2.1000, 112.1500),
    'Selangau': (2.5200, 112.3200),
    'Tatau': (2.8800, 112.8500),
    'Nanga Dap': (2.3200, 112.1000),
    'Durin': (2.2000, 111.9000),
    'Sungei Bidut': (2.2500, 111.7500),
    'Mukah': (2.9064, 112.0800),
    'Dalat': (2.7500, 111.9700),
    'Oya': (2.8500, 111.8500),
    'Balingian': (2.9200, 112.5300),
    'Tanjung Manis': (2.7100, 111.6200),
    'Igan': (2.8200, 111.7500),
    'Ladang': (2.7800, 112.0500),
    'Kapit': (2.0000, 112.5000),
    'Song': (2.0100, 112.5400),
    'Belaga': (2.7000, 113.7800),
    'Bakun Dam': (2.7600, 113.9300),
    'Murum Dam': (2.9400, 114.1700),
    'Baleh': (2.3000, 113.2000),
    'Nanga Merit': (1.8000, 112.8000),
    'Rumah Siga': (2.2000, 113.0000),
    'Bintulu City Center': (3.1746, 113.0316),
    'Bintulu Waterfront': (3.1846, 113.0216),
    'Bintulu Hospital': (3.1846, 113.0416),
    'Bintulu Airport': (3.1232, 113.0195),
    'Tanjung Batu Beach': (3.1946, 113.0116),
    'Bintulu Port': (3.1746, 113.0316),
    'Sebauh': (3.1000, 112.9800),
    'Samalaju': (3.4500, 113.1200),
    'Tubau': (3.1800, 113.1300),
    'Jepak': (3.1500, 112.9800),
    'Kemena': (3.2000, 113.0000),
    'Miri City Center': (4.3995, 113.9918),
    'Miri Waterfront': (4.4095, 113.9818),
    'Miri Hospital': (4.4095, 113.9918),
    'Miri Airport': (4.3223, 113.9868),
    'Miri Marina': (4.4195, 113.9718),
    'Tanjung Lobang': (4.4295, 113.9618),
    'Grand Old Lady': (4.3995, 113.9918),
    'Marudi': (4.1800, 114.3200),
    'Lutong': (4.4700, 114.0200),
    'Bekenu': (4.0600, 113.7700),
    'Niah National Park': (3.8100, 113.7700),
    'Lambir Hills': (4.2200, 114.0300),
    'Sibuti': (3.8000, 113.6300),
    'Kuala Baram': (4.5800, 114.0000),
    'Sungai Tujoh': (4.5000, 113.9500),
    'Piasau': (4.4200, 113.9800),
    'Permyjaya': (4.4500, 114.0000),
    'Limbang': (4.7500, 115.0000),
    'Lawas': (4.8500, 115.4000),
    'Sundar': (4.7200, 115.5800),
    'Trusan': (4.8700, 115.2000),
    'Long Semadoh': (4.0500, 115.5000),
    'Ba Kelalan': (3.9700, 115.6200),
    'Bario': (3.7300, 115.4700),
    'Mulu National Park': (4.0450, 114.9380),
    'Gunung Mulu': (4.0500, 114.9300),
    'Deer Cave': (4.0300, 114.9100),
    'Clearwater Cave': (4.0200, 114.9200),
    'Wind Cave': (4.0400, 114.9000),
    'Tebangan': (4.8000, 115.1000),
    'Merapok': (4.8300, 115.3500),
    'Bario Highlands': (3.7300, 115.4700),
    'Ba Kelalan Highlands': (3.9700, 115.6200),
    'Long Pasia': (4.4000, 115.7500),
    'Kelabit Highlands': (3.8000, 115.5000),
    'Long Banga': (3.6000, 115.4000),
    'Long Lellang': (3.7000, 115.3500),
    'Pa Dalih': (3.8500, 115.5200),
    'Pa Ramapuh': (3.9000, 115.5500),
}

# ============================================================================
# COMBINED BORNEO LOCATIONS
# ============================================================================

BORNEO_LOCATIONS = {
    **SABAH_LOCATIONS,
    **SARAWAK_LOCATIONS,
}

# ============================================================================
# SPACEPORT CANDIDATES
# ============================================================================

SPACEPORT_CANDIDATES = {
    'Kudat Peninsula, Sabah': (6.8860, 116.8430),
    'Sandakan Coast, Sabah': (5.8400, 118.1200),
    'Tawau Hills, Sabah': (4.2435, 117.8853),
    'Felda Sahabat, Sabah': (5.0620, 119.0810),
    'Dent Haven, Sabah': (5.2680, 119.2620),
    'Lahad Datu, Sabah': (5.0300, 118.3300),
    'Semporna, Sabah': (4.4800, 118.6100),
    'Kinabatangan, Sabah': (5.4000, 117.8000),
    'Ranau, Sabah': (5.9500, 116.6700),
    'Kota Belud, Sabah': (6.3500, 116.4300),
    'Tambunan, Sabah': (5.6700, 116.3600),
    'Keningau, Sabah': (5.3300, 116.1600),
    'Beaufort, Sabah': (5.3500, 115.7500),
    'Kota Marudu, Sabah': (6.5000, 116.7400),
    'Telupid, Sabah': (5.6300, 117.1300),
    'Pamol, Sabah': (5.4800, 118.0800),
    'Silam, Sabah': (4.8700, 118.2300),
    'Kalabakan, Sabah': (4.2200, 117.4800),
    'Maliau Basin, Sabah': (4.7200, 117.5200),
    'Danum Valley, Sabah': (4.9500, 117.7800),
    'Tabin, Sabah': (5.2000, 118.6500),
    'Banggi Island, Sabah': (7.2300, 117.1700),
    'Eastern Sabah Hills, Sabah': (5.0000, 117.8500),
    'Miri Coast, Sarawak': (4.3995, 113.9918),
    'Bintulu Coast, Sarawak': (3.1746, 113.0316),
    'Lawas Coast, Sarawak': (4.8500, 115.4000),
    'Limbang, Sarawak': (4.7500, 115.0000),
    'Mulu Highlands, Sarawak': (4.0450, 114.9380),
    'Marudi, Sarawak': (4.1800, 114.3200),
    'Baram River, Sarawak': (4.3000, 114.2000),
    'Bario Highlands, Sarawak': (3.7300, 115.4700),
    'Ba Kelalan, Sarawak': (3.9700, 115.6200),
    'Samalaju, Sarawak': (3.4500, 113.1200),
    'Tanjung Manis, Sarawak': (2.7100, 111.6200),
    'Mukah, Sarawak': (2.9064, 112.0800),
    'Balingian, Sarawak': (2.9200, 112.5300),
    'Sebauh, Sarawak': (3.1000, 112.9800),
    'Dalat, Sarawak': (2.7500, 111.9700),
    'Kuala Baram, Sarawak': (4.5800, 114.0000),
    'Tanjung Lobang, Sarawak': (4.4295, 113.9618),
}

# ============================================================================
# STATIC FALLBACK DATA
# ============================================================================

STATIC_AIRPORTS = {
    'Kota Kinabalu International': (5.9375, 116.0490),
    'Sandakan Airport': (5.9010, 118.0580),
    'Tawau Airport': (4.3133, 117.9183),
    'Kudat Airport': (6.9180, 116.8280),
    'Lahad Datu Airport': (5.0310, 118.3200),
    'Semporna Airport': (4.4800, 118.6100),
    'Keningau Airport': (5.3300, 116.1600),
    'Ranau Airport': (5.9500, 116.6700),
    'Kota Marudu Airport': (6.5000, 116.7400),
    'Pitas Airport': (6.7200, 117.0700),
    'Telupid Airport': (5.6300, 117.1300),
    'Beluran Airport': (5.8800, 117.5600),
    'Kunak Airport': (4.6800, 118.2500),
    'Sipitang Airport': (5.0800, 115.5500),
    'Beaufort Airport': (5.3500, 115.7500),
    'Tenom Airport': (5.1300, 115.9500),
    'Tambunan Airport': (5.6700, 116.3600),
    'Papar Airport': (5.7300, 115.9300),
    'Tuaran Airport': (6.1800, 116.2400),
    'Pulau Sipadan Airport': (4.1140, 118.6250),
    'Kuching International': (1.4843, 110.3469),
    'Miri Airport': (4.3223, 113.9868),
    'Sibu Airport': (2.2586, 111.9661),
    'Bintulu Airport': (3.1232, 113.0195),
    'Limbang Airport': (4.7560, 115.0100),
    'Lawas Airport': (4.8500, 115.4000),
    'Mukah Airport': (2.9064, 112.0800),
    'Sarikei Airport': (2.1160, 111.5360),
    'Kapit Airport': (2.0000, 112.5000),
    'Betong Airport': (1.4100, 111.5300),
    'Sri Aman Airport': (1.2000, 111.5000),
    'Marudi Airport': (4.1800, 114.3200),
    'Bario Airport': (3.7300, 115.4700),
    'Ba Kelalan Airport': (3.9700, 115.6200),
    'Mulu Airport': (4.0450, 114.9380),
    'Long Semadoh Airport': (4.0500, 115.5000),
    'Sundar Airport': (4.7200, 115.5800),
    'Lutong Airport': (4.4700, 114.0200),
    'Tatau Airport': (2.8800, 112.8500),
    'Selangau Airport': (2.5200, 112.3200),
    'Kanowit Airport': (2.1000, 112.1500),
    'Daro Airport': (2.0500, 111.4800),
    'Matu Airport': (2.1000, 111.5300),
    'Dalat Airport': (2.7500, 111.9700),
    'Oya Airport': (2.8500, 111.8500),
    'Lubok Antu Airport': (1.0500, 111.8300),
    'Engkilili Airport': (1.1300, 111.6700),
    'Pusa Airport': (1.4800, 111.3000),
    'Saratok Airport': (1.7400, 111.3200),
    'Sebauh Airport': (3.1000, 112.9800),
    'Balingian Airport': (2.9200, 112.5300),
}

STATIC_SETTLEMENTS = {
    'Kota Kinabalu': {'coords': (5.9804, 116.0735), 'population': 500000},
    'Sandakan': {'coords': (5.8400, 118.1200), 'population': 150000},
    'Tawau': {'coords': (4.2435, 117.8853), 'population': 120000},
    'Lahad Datu': {'coords': (5.0300, 118.3300), 'population': 30000},
    'Kudat': {'coords': (6.8860, 116.8430), 'population': 20000},
    'Semporna': {'coords': (4.4800, 118.6100), 'population': 25000},
    'Keningau': {'coords': (5.3300, 116.1600), 'population': 20000},
    'Ranau': {'coords': (5.9500, 116.6700), 'population': 15000},
    'Kota Marudu': {'coords': (6.5000, 116.7400), 'population': 12000},
    'Beaufort': {'coords': (5.3500, 115.7500), 'population': 10000},
    'Tenom': {'coords': (5.1300, 115.9500), 'population': 8000},
    'Tambunan': {'coords': (5.6700, 116.3600), 'population': 7000},
    'Pitas': {'coords': (6.7200, 117.0700), 'population': 6000},
    'Kunak': {'coords': (4.6800, 118.2500), 'population': 8000},
    'Sipitang': {'coords': (5.0800, 115.5500), 'population': 5000},
    'Papar': {'coords': (5.7300, 115.9300), 'population': 7000},
    'Tuaran': {'coords': (6.1800, 116.2400), 'population': 10000},
    'Penampang': {'coords': (5.9000, 116.0800), 'population': 45000},
    'Putatan': {'coords': (5.8800, 116.0600), 'population': 30000},
    'Telupid': {'coords': (5.6300, 117.1300), 'population': 4000},
    'Beluran': {'coords': (5.8800, 117.5600), 'population': 5000},
    'Kinabatangan': {'coords': (5.4000, 117.8000), 'population': 3000},
    'Kuching': {'coords': (1.5497, 110.3633), 'population': 600000},
    'Miri': {'coords': (4.3995, 113.9918), 'population': 300000},
    'Sibu': {'coords': (2.2871, 111.8301), 'population': 200000},
    'Bintulu': {'coords': (3.1746, 113.0316), 'population': 150000},
    'Limbang': {'coords': (4.7500, 115.0000), 'population': 20000},
    'Lawas': {'coords': (4.8500, 115.4000), 'population': 15000},
    'Mukah': {'coords': (2.9064, 112.0800), 'population': 18000},
    'Sarikei': {'coords': (2.1160, 111.5360), 'population': 25000},
    'Kapit': {'coords': (2.0000, 112.5000), 'population': 15000},
    'Betong': {'coords': (1.4100, 111.5300), 'population': 12000},
    'Sri Aman': {'coords': (1.2000, 111.5000), 'population': 15000},
    'Marudi': {'coords': (4.1800, 114.3200), 'population': 10000},
    'Bario': {'coords': (3.7300, 115.4700), 'population': 1000},
    'Ba Kelalan': {'coords': (3.9700, 115.6200), 'population': 2000},
    'Lutong': {'coords': (4.4700, 114.0200), 'population': 15000},
    'Samalaju': {'coords': (3.4500, 113.1200), 'population': 5000},
    'Sebauh': {'coords': (3.1000, 112.9800), 'population': 8000},
    'Balingian': {'coords': (2.9200, 112.5300), 'population': 5000},
    'Dalat': {'coords': (2.7500, 111.9700), 'population': 8000},
    'Oya': {'coords': (2.8500, 111.8500), 'population': 6000},
    'Tanjung Manis': {'coords': (2.7100, 111.6200), 'population': 7000},
    'Kanowit': {'coords': (2.1000, 112.1500), 'population': 5000},
    'Selangau': {'coords': (2.5200, 112.3200), 'population': 4000},
    'Tatau': {'coords': (2.8800, 112.8500), 'population': 3000},
    'Song': {'coords': (2.0100, 112.5400), 'population': 3000},
    'Belaga': {'coords': (2.7000, 113.7800), 'population': 2000},
}

SPACEPORT_FACILITY_TAGS = {
    'hospital': [('amenity', 'hospital'), ('amenity', 'clinic')],
    'airport': [('aeroway', 'aerodrome'), ('aeroway', 'airport'), ('aeroway', 'heliport')],
    'port': [('harbour', 'yes'), ('amenity', 'ferry_terminal'), ('waterway', 'port')],
    'power_plant': [('power', 'plant'), ('power', 'substation'), ('power', 'generator')],
    'road': [('highway', 'motorway'), ('highway', 'trunk'), ('highway', 'primary')],
    'railway': [('railway', 'rail'), ('railway', 'station')],
    'telecom': [('telecom', 'tower'), ('telecom', 'exchange'), ('man_made', 'tower')],
    'population_center': [('place', 'city'), ('place', 'town'), ('place', 'village')],
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Location:
    lat: float
    lon: float
    name: str = ""
    properties: Dict = field(default_factory=dict)

@dataclass
class AnalysisStep:
    step_number: int
    name: str
    description: str
    status: str = "pending"
    result: Any = None
    execution_time: float = 0.0
    reasoning: str = ""

@dataclass
class AnalysisResult:
    query: str
    steps: List[AnalysisStep] = field(default_factory=list)
    final_result: Any = None
    total_time: float = 0.0
    timestamp: str = ""
    success: bool = False

@dataclass
class MemoryEntry:
    query: str
    query_embedding: List[float] = field(default_factory=list)
    result_summary: str = ""
    success: bool = False
    execution_time: float = 0.0
    timestamp: str = ""
    parameters_used: Dict = field(default_factory=dict)

# ============================================================================
# REPOSITORY PATTERN
# ============================================================================

class MemoryRepository:
    def __init__(self, db_path: str = "borneo_spaceport_memory.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                query_hash TEXT NOT NULL,
                result_summary TEXT,
                success INTEGER,
                execution_time REAL,
                parameters TEXT,
                timestamp TEXT,
                embedding BLOB
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL,
                parameter_name TEXT NOT NULL,
                optimal_value TEXT,
                success_rate REAL,
                usage_count INTEGER DEFAULT 1,
                last_updated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_analysis(self, entry: MemoryEntry):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query_hash = hashlib.md5(entry.query.lower().encode()).hexdigest()
        cursor.execute("""
            INSERT INTO analysis_memory
            (query, query_hash, result_summary, success, execution_time, parameters, timestamp, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.query,
            query_hash,
            entry.result_summary,
            1 if entry.success else 0,
            entry.execution_time,
            json.dumps(entry.parameters_used),
            entry.timestamp,
            pickle.dumps(entry.query_embedding)
        ))
        conn.commit()
        conn.close()

    def get_all_analyses(self, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'query': row[1],
                'result_summary': row[3],
                'success': bool(row[4]),
                'execution_time': row[5],
                'parameters': json.loads(row[6]) if row[6] else {},
                'timestamp': row[7]
            })
        conn.close()
        return results

    def find_similar_analyses(self, query: str, limit: int = 5) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        if not query or not query.strip():
            conn.close()
            return []
        keywords = query.lower().split()
        results = []
        for row in rows:
            stored_query = row[1].lower()
            match_score = sum(1 for kw in keywords if kw in stored_query)
            if match_score > 0:
                results.append({
                    'query': row[1],
                    'result_summary': row[3],
                    'success': bool(row[4]),
                    'execution_time': row[5],
                    'parameters': json.loads(row[6]) if row[6] else {},
                    'timestamp': row[7],
                    'match_score': match_score
                })
        conn.close()
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results[:limit]

    def get_learned_parameter(self, analysis_type: str, parameter_name: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT optimal_value, success_rate FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ?
            ORDER BY success_rate DESC LIMIT 1
        """, (analysis_type, parameter_name))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def update_learned_parameter(self, analysis_type: str, parameter_name: str,
                                  value: str, success: bool):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, success_rate, usage_count FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ? AND optimal_value = ?
        """, (analysis_type, parameter_name, value))
        row = cursor.fetchone()
        if row:
            new_count = row[2] + 1
            new_rate = ((row[1] * row[2]) + (1 if success else 0)) / new_count
            cursor.execute("""
                UPDATE learned_parameters
                SET success_rate = ?, usage_count = ?, last_updated = ?
                WHERE id = ?
            """, (new_rate, new_count, datetime.now().isoformat(), row[0]))
        else:
            cursor.execute("""
                INSERT INTO learned_parameters
                (analysis_type, parameter_name, optimal_value, success_rate, usage_count, last_updated)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (analysis_type, parameter_name, value, 1.0 if success else 0.0, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def get_analysis_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analysis_memory")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM analysis_memory WHERE success = 1")
        successful = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(execution_time) FROM analysis_memory")
        avg_time = cursor.fetchone()[0] or 0
        conn.close()
        return {
            'total_analyses': total,
            'successful_analyses': successful,
            'success_rate': successful / total if total > 0 else 0,
            'avg_execution_time': avg_time
        }

# ============================================================================
# STRATEGY PATTERN - HYBRID: OSM + INSTANT + CACHE + FALLBACK
# ============================================================================

class AnalysisStrategy(ABC):
    @abstractmethod
    def analyse(self, location: Location, params: Dict) -> Dict:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

class SpaceportSuitabilityStrategy(AnalysisStrategy):
    """HYBRID Strategy: INSTANT geographic rules + Live OSM in background"""

    def get_name(self) -> str:
        return "Spaceport Suitability Analysis (HYBRID)"

    def _get_elevation_quick(self, location: Location) -> tuple:
        try:
            elevation_url = f"https://api.open-elevation.com/api/v1/lookup?locations={location.lat},{location.lon}"
            response = requests.get(elevation_url, timeout=3)
            data = response.json()
            elev = data['results'][0]['elevation']
            if 50 <= elev <= 200:
                return 5.0, elev, 'Live Elevation API'
            elif 200 < elev <= 500:
                return 4.5, elev, 'Live Elevation API'
            elif 20 <= elev < 50:
                return 4.0, elev, 'Live Elevation API'
            elif 0 <= elev < 20:
                return 2.0, elev, 'Live Elevation API'
            else:
                return 3.0, elev, 'Live Elevation API'
        except Exception:
            lat, lon = location.lat, location.lon
            if lat > 5.8 and lat < 6.2 and lon > 116.4 and lon < 116.8:
                return 4.5, 1500, 'Fallback: Kinabalu region'
            elif lat > 4.5 and lon > 117.5:
                return 3.5, 300, 'Fallback: E. Sabah hills'
            elif lat > 2.5 and lon > 114.0 and lon < 115.5:
                return 3.5, 200, 'Fallback: Sarawak interior'
            else:
                return 3.0, 50, 'Fallback: Lowland area'

    def _geographic_score_coastal(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        if lon > 117.5:
            return 5.0, 0, 'Geographic: East coast'
        elif lon > 116.5:
            return 4.0, 10, 'Geographic: Near coast'
        elif lon > 115.5:
            return 3.5, 20, 'Geographic: Coastal'
        elif lon > 114.5:
            return 3.0, 30, 'Geographic: Inland'
        else:
            return 2.0, 50, 'Geographic: Interior'

    def _geographic_score_population(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, data in STATIC_SETTLEMENTS.items():
            s_lat, s_lon = data['coords']
            dist = self._haversine(lat, lon, s_lat, s_lon)
            min_dist = min(min_dist, dist)
        if min_dist > 80:
            return 5.0, 0, 'Geographic: Remote'
        elif min_dist > 50:
            return 4.0, 1, 'Geographic: Rural'
        elif min_dist > 30:
            return 3.0, 2, 'Geographic: Semi-rural'
        elif min_dist > 15:
            return 2.0, 5, 'Geographic: Near town'
        else:
            return 1.0, 10, 'Geographic: Near city'

    def _geographic_score_infrastructure(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, coords in STATIC_AIRPORTS.items():
            a_lat, a_lon = coords
            dist = self._haversine(lat, lon, a_lat, a_lon)
            min_dist = min(min_dist, dist)
        details = {
            'airports': 1 if min_dist < 60 else 0,
            'major_roads': 2 if min_dist < 30 else 0,
            'ports': 0,
            'power_facilities': 0
        }
        if min_dist < 30:
            return 4.5, details, 'Geographic: Near airport'
        elif min_dist < 60:
            return 3.5, details, 'Geographic: Airport nearby'
        elif min_dist < 100:
            return 2.5, details, 'Geographic: Some access'
        else:
            return 1.5, details, 'Geographic: Remote'

    def _geographic_score_land(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, data in STATIC_SETTLEMENTS.items():
            s_lat, s_lon = data['coords']
            dist = self._haversine(lat, lon, s_lat, s_lon)
            min_dist = min(min_dist, dist)
        details = {
            'forest_areas': 30 if min_dist > 50 else 10,
            'developed_areas': 2 if min_dist > 50 else 10,
            'agriculture': 5
        }
        if min_dist > 80:
            return 5.0, details, 'Geographic: Abundant land'
        elif min_dist > 50:
            return 4.0, details, 'Geographic: Good land'
        elif min_dist > 30:
            return 3.0, details, 'Geographic: Moderate land'
        elif min_dist > 15:
            return 2.0, details, 'Geographic: Limited land'
        else:
            return 1.0, details, 'Geographic: Scarce land'

    def _geographic_score_flood(self, elevation_m: float) -> tuple:
        if elevation_m > 100:
            return 5.0, 'Low'
        elif elevation_m > 50:
            return 4.0, 'Low'
        elif elevation_m > 20:
            return 3.0, 'Moderate'
        else:
            return 1.5, 'High'

    def _score_latitudinal_advantage(self, lat: float) -> float:
        abs_lat = abs(lat)
        if abs_lat <= 1:
            return 5.0
        elif abs_lat <= 3:
            return 4.5
        elif abs_lat <= 5:
            return 4.0
        elif abs_lat <= 7:
            return 3.0
        elif abs_lat <= 10:
            return 2.0
        else:
            return 1.0

    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(min(1, math.sqrt(a)))

    def _try_osm_in_background(self, location: Location, radius: int) -> Optional[Dict]:
        try:
            overpass_url = "https://overpass-api.de/api/interpreter"
            results = {}
            query = f"""
            [out:json][timeout:5];
            (
              node["aeroway"="aerodrome"](around:{radius},{location.lat},{location.lon});
              way["aeroway"="aerodrome"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            data = response.json()
            results['airport_count'] = len(data.get('elements', []))
            query = f"""
            [out:json][timeout:5];
            (
              node["place"~"city|town|village"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            data = response.json()
            results['settlement_count'] = len(data.get('elements', []))
            query = f"""
            [out:json][timeout:5];
            (
              way["highway"~"motorway|trunk|primary"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            data = response.json()
            results['road_count'] = len(data.get('elements', []))
            query = f"""
            [out:json][timeout:5];
            (
              way["natural"="coastline"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            data = response.json()
            results['coastline_count'] = len(data.get('elements', []))
            return results
        except Exception:
            return None

    def analyse(self, location: Location, params: Dict) -> Dict:
        radius = params.get('radius', 10000)
        weights = params.get('weights', {
            'elevation': 0.15,
            'population_density': 0.20,
            'coastal_proximity': 0.15,
            'infrastructure_access': 0.15,
            'land_availability': 0.15,
            'flood_risk': 0.10,
            'latitudinal_advantage': 0.10
        })

        scores = {}
        details = {}
        data_sources = []
        data_source_details = []
        osm_data = None
        osm_available = False

        # 1. ELEVATION
        elevation_score, elevation_m, elev_source = self._get_elevation_quick(location)
        data_sources.append(elev_source)
        data_source_details.append(f"Elevation: {elev_source}")
        scores['elevation'] = elevation_score
        details['elevation'] = {
            'score': elevation_score,
            'value': f"{elevation_m:.0f}m",
            'weight': weights['elevation'],
            'source': elev_source
        }

        # 2. POPULATION
        pop_score, pop_density, pop_source = self._geographic_score_population(location)
        data_sources.append(pop_source)
        data_source_details.append(f"Population: {pop_source}")
        scores['population_density'] = pop_score
        details['population_density'] = {
            'score': pop_score,
            'value': f"{pop_density:.1f} people/km²" if pop_density > 0 else "Very Low",
            'weight': weights['population_density'],
            'source': pop_source
        }

        # 3. COASTAL
        coastal_score, distance_to_coast, coastal_source = self._geographic_score_coastal(location)
        data_sources.append(coastal_source)
        data_source_details.append(f"Coastal: {coastal_source}")
        scores['coastal_proximity'] = coastal_score
        details['coastal_proximity'] = {
            'score': coastal_score,
            'value': f"{distance_to_coast:.1f}km",
            'weight': weights['coastal_proximity'],
            'source': coastal_source
        }

        # 4. INFRASTRUCTURE
        infra_score, infra_details, infra_source = self._geographic_score_infrastructure(location)
        data_sources.append(infra_source)
        data_source_details.append(f"Infrastructure: {infra_source}")
        scores['infrastructure_access'] = infra_score
        details['infrastructure_access'] = {
            'score': infra_score,
            'value': infra_details,
            'weight': weights['infrastructure_access'],
            'source': infra_source
        }

        # 5. LAND
        land_score, land_details, land_source = self._geographic_score_land(location)
        data_sources.append(land_source)
        data_source_details.append(f"Land: {land_source}")
        scores['land_availability'] = land_score
        details['land_availability'] = {
            'score': land_score,
            'value': land_details,
            'weight': weights['land_availability'],
            'source': land_source
        }

        # 6. FLOOD
        flood_score, flood_risk = self._geographic_score_flood(elevation_m)
        scores['flood_risk'] = flood_score
        details['flood_risk'] = {
            'score': flood_score,
            'value': flood_risk,
            'weight': weights['flood_risk'],
            'source': 'From elevation'
        }

        # 7. LATITUDE
        lat_score = self._score_latitudinal_advantage(location.lat)
        scores['latitudinal_advantage'] = lat_score
        details['latitudinal_advantage'] = {
            'score': lat_score,
            'value': f"{abs(location.lat):.1f}°{'N' if location.lat > 0 else 'S'}",
            'weight': weights['latitudinal_advantage'],
            'source': 'Geographic'
        }

        # ============ FIXED BASE SCORE (0-100) ============
        # Each criterion is scored 0-5, so max weighted total = sum(weights) * 5
        total_score = sum(scores[key] * weights.get(key, 0) for key in scores.keys() if key in weights)
        max_possible = sum(weights.values()) * 5.0
        percentage = (total_score / max_possible) * 100 if max_possible > 0 else 0

        # ============ FIXED CRITICAL PENALTIES ============
        penalty = 0.0
        penalty_reasons = []

        if elevation_m < 20:
            penalty += 15.0
            penalty_reasons.append(f"Very low elevation ({elevation_m:.0f}m): -15%")
        if flood_risk == 'High':
            penalty += 10.0
            penalty_reasons.append("High flood risk: -10%")
        if pop_density > 5:
            penalty += 10.0
            penalty_reasons.append("High population density: -10%")

        if isinstance(land_details, dict) and land_details.get('developed_areas', 0) >= 10:
            penalty += 8.0
            penalty_reasons.append("Scarce land availability: -8%")

        # Clamp final score to 0-100 (never negative, never over 100)
        percentage = max(0.0, min(100.0, percentage - penalty))

        # Rating
        if percentage >= 80:
            rating, emoji, rec = 'Excellent', '🚀', 'Highly recommended for spaceport development'
        elif percentage >= 65:
            rating, emoji, rec = 'Good', '👍', 'Suitable with minor site preparation'
        elif percentage >= 50:
            rating, emoji, rec = 'Moderate', '👌', 'Suitable with significant site preparation'
        elif percentage >= 35:
            rating, emoji, rec = 'Limited', '⚠️', 'Marginal - requires major investment'
        else:
            rating, emoji, rec = 'Poor', '❌', 'Not recommended for spaceport development'

        # OSM BACKGROUND
        try:
            osm_data = self._try_osm_in_background(location, radius)
            if osm_data and any(v > 0 for v in osm_data.values()):
                osm_available = True
                data_source_details.append(f"🌐 OSM Background: Found {osm_data.get('airport_count', 0)} airports, {osm_data.get('settlement_count', 0)} settlements")
        except Exception:
            pass

        return {
            'success': True,
            'scores': scores,
            'details': details,
            'weighted_score': total_score,
            'max_possible_score': max_possible,
            'suitability_percentage': round(percentage, 1),
            'base_percentage': round((total_score / max_possible * 100) if max_possible > 0 else 0, 1),
            'penalty_applied': round(penalty, 1),
            'penalty_reasons': penalty_reasons,
            'rating': rating,
            'rating_emoji': emoji,
            'recommendation': rec,
            'radius_used': radius,
            'location': f"{location.name or 'Borneo location'} ({location.lat:.4f}, {location.lon:.4f})",
            'elevation_m': elevation_m,
            'population_density': pop_density,
            'coastal_distance_km': distance_to_coast,
            'flood_risk': flood_risk,
            'lat_deg': abs(location.lat),
            'data_sources': data_sources,
            'data_source_details': data_source_details,
            'used_osm': osm_available,
            'osm_data': osm_data if osm_available else None,
            'used_fallback': True,
            'from_cache': False,
            'analysis_method': 'HYBRID: Geographic Rules (INSTANT) + OSM Background'
        }

class ProximityAnalysisStrategy(AnalysisStrategy):
    def get_name(self) -> str:
        return "Proximity Analysis"

    def analyse(self, location: Location, params: Dict) -> Dict:
        amenity_type = params.get('amenity_type', 'hospital')
        radius = params.get('radius', 5000)
        tags_to_query = SPACEPORT_FACILITY_TAGS.get(amenity_type, [('amenity', amenity_type)])
        query_parts = []
        for key, value in tags_to_query:
            query_parts.append(f'node["{key}"="{value}"](around:{radius},{location.lat},{location.lon});')
            query_parts.append(f'way["{key}"="{value}"](around:{radius},{location.lat},{location.lon});')
        query_body = "\n".join(query_parts)
        query = f"""[out:json][timeout:45];
(
{query_body}
);
out center;"""
        try:
            headers = {'User-Agent': 'BorneoSpaceportGeoAI/1.0'}
            response = requests.post("https://overpass-api.de/api/interpreter",
                                   data={'data': query}, headers=headers, timeout=45)
            response.raise_for_status()
            data = response.json()
            elements = data.get('elements', [])
            results = []
            seen_locations = set()
            for elem in elements:
                lat = elem.get('lat') or elem.get('center', {}).get('lat')
                lon = elem.get('lon') or elem.get('center', {}).get('lon')
                if lat and lon:
                    loc_key = f"{round(lat, 5)}_{round(lon, 5)}"
                    if loc_key not in seen_locations:
                        seen_locations.add(loc_key)
                        tags = elem.get('tags', {})
                        name = tags.get('name', tags.get('brand', 'Unknown'))
                        results.append({
                            'name': name,
                            'lat': lat,
                            'lon': lon,
                            'type': amenity_type,
                            'tags': tags
                        })
            return {
                'success': True,
                'count': len(results),
                'amenities': results,
                'radius': radius,
                'amenity_type': amenity_type,
                'location': f"Borneo ({location.lat:.4f}, {location.lon:.4f})"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'amenities': [],
                'count': 0,
                'radius': radius,
                'amenity_type': amenity_type
            }

class StrategySelector:
    _strategies = {
        'spaceport': SpaceportSuitabilityStrategy,
        'proximity': ProximityAnalysisStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_type: str) -> AnalysisStrategy:
        strategy_class = cls._strategies.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Unknown strategy: {strategy_type}")
        return strategy_class()

    @classmethod
    def available_strategies(cls) -> List[str]:
        return list(cls._strategies.keys())

# ============================================================================
# PIPELINE PATTERN
# ============================================================================

class PipelineStep:
    def __init__(self, name: str, processor: Callable, description: str = ""):
        self.name = name
        self.processor = processor
        self.description = description
        self.execution_time = 0.0
        self.result = None

class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []
        self.results: Dict[str, Any] = {}
        self.execution_log: List[AnalysisStep] = []

    def add_step(self, step: PipelineStep) -> 'Pipeline':
        self.steps.append(step)
        return self

    def execute(self, initial_data: Dict, progress_callback: Callable = None) -> Dict:
        current_data = initial_data.copy()
        total_steps = len(self.steps)
        for i, step in enumerate(self.steps):
            analysis_step = AnalysisStep(
                step_number=i + 1,
                name=step.name,
                description=step.description,
                status="running"
            )
            if progress_callback:
                progress_callback(i / total_steps, f"Running: {step.name}")
            start_time = time.time()
            try:
                step.result = step.processor(current_data)
                current_data.update(step.result)
                self.results[step.name] = step.result
                step.execution_time = time.time() - start_time
                analysis_step.status = "completed"
                analysis_step.result = step.result
                analysis_step.execution_time = step.execution_time
                analysis_step.reasoning = f"Successfully processed {step.name}"
            except Exception as e:
                step.execution_time = time.time() - start_time
                analysis_step.status = "failed"
                analysis_step.reasoning = f"Error: {str(e)}"
                self.execution_log.append(analysis_step)
                raise
            self.execution_log.append(analysis_step)
        if progress_callback:
            progress_callback(1.0, "Complete")
        return current_data

# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    def __init__(self, calls_per_second: float = 0.5):
        self.calls_per_second = calls_per_second
        self.last_call = 0

    def wait(self):
        now = time.time()
        time_since_last = now - self.last_call
        min_interval = 1.0 / self.calls_per_second
        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        self.last_call = time.time()

# ============================================================================
# MAIN GEOAI AGENT CLASS
# ============================================================================

class BorneoSpaceportGeoAIAgent:
    def __init__(self):
        self.memory_repo = MemoryRepository()
        self.rate_limiter = RateLimiter(calls_per_second=0.5)
        self.short_term_memory: Dict[str, Any] = {}
        self.current_analysis: Optional[AnalysisResult] = None

    def reason_about_query(self, query: str) -> tuple:
        query_lower = query.lower()
        steps = []
        steps.append({
            'step': 'Understanding Query',
            'reasoning': f"Analysing spaceport site selection request: '{query}'",
            'action': 'parse_intent'
        })
        similar = self.memory_repo.find_similar_analyses(query, limit=3)
        if similar:
            steps.append({
                'step': 'Memory Recall',
                'reasoning': f"Found {len(similar)} similar past analyses for spaceport site selection.",
                'action': 'apply_learned_parameters',
                'prior_experience': similar[0]
            })
        spaceport_keywords = ['spaceport', 'launch', 'rocket', 'space', 'satellite', 'site', 'suitable', 'best']
        if any(word in query_lower for word in spaceport_keywords):
            analysis_type = 'spaceport'
            steps.append({
                'step': 'Strategy Selection',
                'reasoning': 'Query contains spaceport/launch keywords. Selecting Spaceport Suitability strategy.',
                'action': 'use_spaceport_strategy'
            })
        else:
            analysis_type = 'spaceport'
            steps.append({
                'step': 'Strategy Selection',
                'reasoning': 'Defaulting to Spaceport Suitability analysis.',
                'action': 'use_spaceport_strategy'
            })
        learned_radius = self.memory_repo.get_learned_parameter(analysis_type, 'radius')
        if learned_radius:
            steps.append({
                'step': 'Parameter Optimisation',
                'reasoning': f"Using learned optimal radius of {learned_radius}m from past successful analyses.",
                'action': 'apply_learned_radius',
                'value': learned_radius
            })
        else:
            steps.append({
                'step': 'Parameter Selection',
                'reasoning': 'No learned parameters available. Using default radius of 10km for spaceport site assessment.',
                'action': 'use_default_radius',
                'value': '10000'
            })
        steps.append({
            'step': 'Execution Planning',
            'reasoning': f'Will execute {analysis_type} analysis with spaceport-optimized settings.',
            'action': 'prepare_execution'
        })
        return steps, analysis_type

    def execute_analysis(self, location: Location, query: str,
                         params: Dict, progress_callback: Callable = None) -> AnalysisResult:
        start_time = time.time()
        result = AnalysisResult(query=query, timestamp=datetime.now().isoformat())
        reasoning_steps, analysis_type = self.reason_about_query(query)
        for i, step_info in enumerate(reasoning_steps):
            result.steps.append(AnalysisStep(
                step_number=i + 1,
                name=step_info['step'],
                description=step_info['reasoning'],
                status='completed',
                reasoning=step_info['reasoning']
            ))
        if progress_callback:
            progress_callback(0.3, "Reasoning complete, executing hybrid analysis...")
        try:
            strategy = StrategySelector.get_strategy(analysis_type)
            self.rate_limiter.wait()
            analysis_result = strategy.analyse(location, params)
            analysis_result['from_cache'] = False
            if analysis_result.get('success'):
                used_osm = analysis_result.get('used_osm', False)
                result.steps.append(AnalysisStep(
                    step_number=len(result.steps) + 1,
                    name="Data Source Validation",
                    description=f"Method: {analysis_result.get('analysis_method', 'HYBRID')}",
                    status='completed',
                    reasoning=f"Used {'OSM + Geographic' if used_osm else 'Geographic'} rules"
                ))
            result.steps.append(AnalysisStep(
                step_number=len(result.steps) + 1,
                name=f"Execute {strategy.get_name()}",
                description=f"Running {analysis_type} analysis on {location.name or 'Borneo location'}",
                status='completed' if analysis_result.get('success') else 'failed',
                result=analysis_result,
                reasoning=f"Analysis returned {len(str(analysis_result))} bytes of data"
            ))
            result.final_result = analysis_result
            result.success = analysis_result.get('success', False)
        except Exception as e:
            result.steps.append(AnalysisStep(
                step_number=len(result.steps) + 1,
                name="Analysis Execution",
                description="Executing spatial analysis",
                status='failed',
                reasoning=f"Error: {str(e)}"
            ))
            result.success = False
        if progress_callback:
            progress_callback(0.8, "Storing results in memory...")
        result.total_time = time.time() - start_time
        memory_entry = MemoryEntry(
            query=query,
            result_summary=str(result.final_result)[:500] if result.final_result else "",
            success=result.success,
            execution_time=result.total_time,
            timestamp=result.timestamp,
            parameters_used=params
        )
        self.memory_repo.store_analysis(memory_entry)
        if result.success:
            self.memory_repo.update_learned_parameter(
                analysis_type, 'radius', str(params.get('radius', 10000)), True
            )
        self.short_term_memory['last_analysis'] = result
        self.short_term_memory['last_location'] = location
        if progress_callback:
            progress_callback(1.0, "Complete")
        return result

# ============================================================================
# STREAMLIT UI - CYBERPUNK EDITION
# ============================================================================

def render_region_selector():
    regions = {
        '🌏 All Borneo': 'all',
        '🏝️ Sabah Only': 'sabah',
        '🏝️ Sarawak Only': 'sarawak',
        '🚀 Spaceport Candidates': 'candidates'
    }
    selected_region = st.selectbox("Select Region", options=list(regions.keys()), index=0)
    region_key = regions[selected_region]
    if region_key == 'sabah':
        locations = SABAH_LOCATIONS
        st.info(f"🏝️ Showing {len(locations)} locations in Sabah")
    elif region_key == 'sarawak':
        locations = SARAWAK_LOCATIONS
        st.info(f"🏝️ Showing {len(locations)} locations in Sarawak")
    elif region_key == 'candidates':
        locations = SPACEPORT_CANDIDATES
        st.info(f"🚀 Showing {len(locations)} spaceport candidate sites")
    else:
        locations = BORNEO_LOCATIONS
        st.info(f"🌏 Showing {len(locations)} locations across Borneo")
    return locations, region_key

def init_session_state():
    if 'agent' not in st.session_state:
        st.session_state.agent = BorneoSpaceportGeoAIAgent()
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = Location(
            lat=6.8860, lon=116.8430, name="Kudat Peninsula, Sabah"
        )
    if 'reasoning_log' not in st.session_state:
        st.session_state.reasoning_log = []
    if 'current_results' not in st.session_state:
        st.session_state.current_results = None
    if 'basemap' not in st.session_state:
        st.session_state.basemap = "OpenStreetMap"
    if 'show_radius_circle' not in st.session_state:
        st.session_state.show_radius_circle = True
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'candidate_scores' not in st.session_state:
        st.session_state.candidate_scores = {}

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2.5rem; font-family: 'Courier New', monospace;
                 background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                 font-weight: 900; letter-spacing: 4px;">
                SPACEPORT
            </div>
            <div style="color: #00f0ff; font-size: 0.8rem; font-family: 'Courier New', monospace;
                 letter-spacing: 6px; text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);">
                SELECTOR v2.0
            </div>
            <div class="cyber-divider"></div>
        </div>
        """, unsafe_allow_html=True)
        cache_stats = api_cache.get_stats()
        st.markdown(f"""
        <div style="color: #a0a0c0; font-family: 'Courier New', monospace; font-size: 0.7rem;
             letter-spacing: 1px; text-align: center; border: 1px solid rgba(0, 240, 255, 0.1);
             border-radius: 4px; padding: 4px 8px; margin-bottom: 10px;">
            ⚡ CACHE: {cache_stats['total_cached']} RESPONSES
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.markdown("""
        <div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            ⚡ LOCATION SELECTOR
        </div>
        """, unsafe_allow_html=True)
        locations, region = render_region_selector()
        quick_location = st.selectbox("Select Location", list(locations.keys()), index=0)
        if st.button("⚡ GO TO LOCATION", use_container_width=True):
            coords = locations[quick_location]
            st.session_state.selected_location = Location(
                lat=coords[0], lon=coords[1], name=quick_location
            )
            st.rerun()
        st.caption("Or click on the map to select any location")
        st.divider()
        st.markdown("""
        <div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🗺️ MAP SETTINGS
        </div>
        """, unsafe_allow_html=True)
        st.session_state.basemap = "OpenStreetMap"
        st.session_state.show_radius_circle = st.checkbox("Show Search Radius", value=True)
        st.divider()
        st.markdown("""
        <div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            ⚙️ ANALYSIS PARAMETERS
        </div>
        """, unsafe_allow_html=True)
        radius = st.slider("Assessment Radius (m)", 2000, 20000, 10000, 1000)
        st.divider()
        st.markdown("""
        <div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            📊 SITE RANKING
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.current_results:
            result_data = st.session_state.current_results
            if 'suitability_percentage' in result_data:
                pct = result_data['suitability_percentage']
                rating = result_data['rating']
                color = "#39ff14" if pct >= 80 else "#00f0ff" if pct >= 65 else "#ff2d95" if pct >= 50 else "#ff6600"
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(0, 240, 255, 0.2);
                     border-radius: 8px; background: rgba(0, 240, 255, 0.05);">
                    <div style="font-size: 2.5rem; font-weight: 900; color: {color};
                         font-family: 'Courier New', monospace; text-shadow: 0 0 30px {color}33;">
                        {pct}%
                    </div>
                    <div style="color: #d0d0e8; font-family: 'Courier New', monospace;
                         letter-spacing: 2px; font-size: 0.8rem;">
                        {rating}
                    </div>
                    <div style="color: #8080a0; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; margin-top: 5px;">
                        {result_data['recommendation'][:50]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if result_data.get('used_osm', False):
                    st.markdown("""
                    <div style="color: #39ff14; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; letter-spacing: 1px; text-align: center;
                         border: 1px solid #39ff14; border-radius: 4px; padding: 2px 8px;
                         margin-top: 8px; display: inline-block; width: 100%;">
                        🌐 OSM UP-TO-DATE
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="color: #00f0ff; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; letter-spacing: 1px; text-align: center;
                         border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 4px;
                         padding: 2px 8px; margin-top: 8px; display: inline-block; width: 100%;">
                        📍 GEOGRAPHIC RULES
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Run an analysis to see site ranking")
        if st.button("🔄 COMPARE ALL", use_container_width=True):
            st.session_state.comparison_mode = True
            st.rerun()
        if st.button("🧹 CLEAR", use_container_width=True):
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.success("Results cleared!")
            st.rerun()
        if st.button("🗑️ CLEAR CACHE", use_container_width=True):
            api_cache.clear()
            st.success("Cache cleared!")
            st.rerun()
        st.divider()
        st.markdown("""
        <div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🧠 AGENT MEMORY
        </div>
        """, unsafe_allow_html=True)
        stats = st.session_state.agent.memory_repo.get_analysis_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px; border: 1px solid rgba(0, 240, 255, 0.1);
                 border-radius: 4px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                     letter-spacing: 1px;">ANALYSES</div>
                <div style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 1.2rem;
                     font-weight: bold;">{stats['total_analyses']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px; border: 1px solid rgba(0, 240, 255, 0.1);
                 border-radius: 4px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                     letter-spacing: 1px;">SUCCESS RATE</div>
                <div style="color: #39ff14; font-family: 'Courier New', monospace; font-size: 1.2rem;
                     font-weight: bold;">{stats['success_rate']*100:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 8px; border: 1px solid rgba(0, 240, 255, 0.1);
             border-radius: 4px; margin-top: 8px;">
            <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                 letter-spacing: 1px;">AVG EXECUTION</div>
            <div style="color: #b026ff; font-family: 'Courier New', monospace; font-size: 1.2rem;
                 font-weight: bold;">{stats['avg_execution_time']:.2f}s</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗑️ CLEAR MEMORY", use_container_width=True):
            Path("borneo_spaceport_memory.db").unlink(missing_ok=True)
            st.session_state.agent = BorneoSpaceportGeoAIAgent()
            st.session_state.analysis_history = []
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.success("All memory cleared!")
            st.rerun()
        return {'radius': radius}

def render_map(params: Dict):
    st.subheader("🗺️ Borneo Spaceport Site Map")
    center = [5.0, 117.0]
    location_name = "Borneo"
    if st.session_state.selected_location:
        center = [st.session_state.selected_location.lat,
                  st.session_state.selected_location.lon]
        location_name = st.session_state.selected_location.name or "Borneo Location"
    try:
        m = folium.Map(location=center, zoom_start=7, tiles="OpenStreetMap")
    except Exception:
        m = folium.Map(location=center, zoom_start=7)
    if st.session_state.selected_location:
        marker_color = 'red'
        result_data = st.session_state.get('current_results', None)
        if result_data and 'suitability_percentage' in result_data:
            pct = result_data['suitability_percentage']
            if pct >= 80:
                marker_color = 'green'
            elif pct >= 65:
                marker_color = 'lightgreen'
            elif pct >= 50:
                marker_color = 'orange'
            elif pct >= 35:
                marker_color = 'lightred'
            else:
                marker_color = 'red'
        folium.Marker(
            center,
            popup=f"""
            <b>🚀 {location_name}</b><br>
            Lat: {center[0]:.6f}<br>
            Lon: {center[1]:.6f}<br>
            🏝️ Borneo, Malaysia
            """,
            tooltip="🚀 Candidate Site - Click for details",
            icon=folium.Icon(color=marker_color, icon='rocket', prefix='fa')
        ).add_to(m)
        if st.session_state.get('show_radius_circle', True):
            radius = params.get('radius', 10000)
            folium.Circle(
                center,
                radius=radius,
                color='#2ecc71',
                fill=True,
                fillColor='#2ecc71',
                fillOpacity=0.1,
                weight=2,
                tooltip=f"Assessment radius: {radius}m"
            ).add_to(m)
    result_data = st.session_state.get('current_results', None)
    if result_data and 'suitability_percentage' in result_data:
        pct = result_data['suitability_percentage']
        rating = result_data.get('rating', 'Unknown')
        recommendation = result_data.get('recommendation', '')
        if pct >= 80:
            color = 'green'
        elif pct >= 65:
            color = 'lightgreen'
        elif pct >= 50:
            color = 'orange'
        elif pct >= 35:
            color = 'lightred'
        else:
            color = 'red'
        folium.Circle(
            center,
            radius=params.get('radius', 10000),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.15,
            weight=3,
            tooltip=f"🚀 Suitability: {rating} ({pct}%)\n{recommendation}"
        ).add_to(m)
    try:
        Fullscreen(position='topleft').add_to(m)
    except Exception:
        pass
    try:
        MiniMap(toggle_display=True, position='bottomright').add_to(m)
    except Exception:
        pass
    try:
        MousePosition(position='bottomleft', prefix='Borneo Coords: ').add_to(m)
    except Exception:
        pass
    map_data = st_folium(m, width=None, height=500, use_container_width=True)
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        new_location = Location(lat=clicked_lat, lon=clicked_lon, name="Borneo Location")
        if st.session_state.selected_location is None or \
           abs(st.session_state.selected_location.lat - clicked_lat) > 0.0001 or \
           abs(st.session_state.selected_location.lon - clicked_lon) > 0.0001:
            st.session_state.selected_location = new_location
            st.rerun()
    if result_data and 'suitability_percentage' in result_data:
        if result_data.get('used_osm', False):
            st.success(f"🚀 {result_data['rating']} Suitability: {result_data['suitability_percentage']}% (🌐 OSM Up-to-Date)")
        else:
            st.success(f"🚀 {result_data['rating']} Suitability: {result_data['suitability_percentage']}% (📍 Geographic Rules)")
        st.info(f"💡 {result_data['recommendation']}")

def render_query_interface(params: Dict):
    st.subheader("💬 Natural Language Query")
    with st.expander("💡 Example Spaceport Queries", expanded=False):
        st.markdown("""
        **🚀 Spaceport Site Selection:**
        - "Find the best location for a spaceport in Sabah"
        - "Which site has the best launch characteristics?"
        - "Evaluate this site for rocket launch facilities"
        - "Compare all candidate sites for spaceport development"
        - "What are the advantages of Kudat for a spaceport?"

        **📊 Site Suitability:**
        - "Assess flood risk at this location"
        - "What's the elevation here?"
        - "Check infrastructure access"
        - "Is this area suitable for a launch facility?"
        """)
    query = st.text_area(
        "Describe what you want to analyse for spaceport site selection:",
        placeholder="e.g., Find the best location for a spaceport in Sabah",
        height=100
    )
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        analyse_btn = st.button("🚀 ANALYSE SITE", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🧹 CLEAR", use_container_width=True)
    if clear_btn:
        st.session_state.current_results = None
        st.session_state.reasoning_log = []
        st.rerun()
    if analyse_btn and st.session_state.selected_location:
        with st.spinner("🧠 HYBRID: INSTANT results + OSM background..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            def update_progress(progress, status):
                progress_bar.progress(progress)
                status_text.text(status)
            result = st.session_state.agent.execute_analysis(
                st.session_state.selected_location,
                query if query else "Evaluate this site for spaceport development",
                params,
                progress_callback=update_progress
            )
            st.session_state.analysis_history.append(result)
            st.session_state.reasoning_log = result.steps
            st.session_state.current_results = result.final_result
            progress_bar.empty()
            status_text.empty()
            if result.success:
                st.success(f"✅ Spaceport site analysis complete in {result.total_time:.2f}s")
                st.rerun()
            else:
                st.error("❌ Analysis failed. Check reasoning log for details.")
    elif analyse_btn and not st.session_state.selected_location:
        st.warning("Please select a location in Borneo first!")

def render_reasoning_log():
    st.subheader("🧠 Agent Reasoning (Chain of Thought)")
    if not st.session_state.reasoning_log:
        st.info("Run a spaceport site analysis to see the agent's reasoning process.")
        return
    for step in st.session_state.reasoning_log:
        status_icon = "✅" if step.status == "completed" else "❌" if step.status == "failed" else "⏳"
        with st.expander(f"{status_icon} Step {step.step_number}: {step.name}", expanded=True):
            st.write(f"**Reasoning:** {step.reasoning}")
            if step.execution_time > 0:
                st.write(f"**Execution Time:** {step.execution_time:.3f}s")
            if step.result and step.name.startswith("Execute"):
                st.json(step.result)

def render_results():
    st.subheader("🚀 Spaceport Site Analysis Results")
    if not st.session_state.analysis_history:
        st.info("No analysis results yet. Run a spaceport site analysis to see results here.")
        return
    last_result = st.session_state.analysis_history[-1]
    if not last_result.final_result:
        st.warning("No results available.")
        return
    result_data = last_result.final_result
    if not result_data.get('success', False):
        st.error(f"Analysis failed: {result_data.get('error', 'Unknown error')}")
        return
    if 'suitability_percentage' in result_data:
        if result_data.get('used_osm', False):
            st.success("🌐 **HYBRID: OSM Up-to-Date + Geographic Rules**")
        else:
            st.success("📍 **Geographic Rules (INSTANT)** - OSM unavailable")

        # Show penalty if applied
        if result_data.get('penalty_applied', 0) > 0:
            with st.expander(f"⚠️ Score Penalty Applied: -{result_data['penalty_applied']}%"):
                st.write(f"**Base score:** {result_data.get('base_percentage', 0)}%")
                st.write(f"**Penalty:** -{result_data['penalty_applied']}%")
                st.write("**Reasons:**")
                for r in result_data.get('penalty_reasons', []):
                    st.warning(r)
                st.write(f"**Final score:** {result_data['suitability_percentage']}%")

        if 'data_source_details' in result_data:
            with st.expander("📊 Data Sources Used"):
                for detail in result_data['data_source_details']:
                    if '🌐' in detail:
                        st.success(f"🌐 {detail}")
                    elif 'Geographic' in detail:
                        st.info(f"📍 {detail}")
                    elif 'Fallback' in detail:
                        st.warning(f"⚠️ {detail}")
                    else:
                        st.success(f"✅ {detail}")
        if result_data.get('used_osm', False) and result_data.get('osm_data'):
            with st.expander("🌐 OSM Data Found (Up-to-Date)"):
                st.json(result_data['osm_data'])
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.metric(
                "🚀 Spaceport Suitability",
                f"{result_data['suitability_percentage']}%",
                delta=f"{result_data['rating']} {result_data['rating_emoji']}"
            )
            st.caption(result_data['recommendation'])
        with col2:
            st.metric("Elevation", f"{result_data.get('elevation_m', 0):.0f}m")
        with col3:
            st.metric("Latitude", f"{result_data.get('lat_deg', 0):.1f}°{'N' if result_data.get('lat_deg', 0) >= 0 else 'S'}")
        st.write("---")
        st.write("**Detailed Scoring Breakdown:**")
        details = result_data.get('details', {})
        scores = result_data.get('scores', {})
        score_data = []
        for key, detail in details.items():
            weight = detail.get('weight', 0)
            score = scores.get(key, 0)
            weighted = score * weight
            source = detail.get('source', 'Unknown')
            if 'Geographic' in source:
                source_emoji = '📍'
            elif 'Live' in source:
                source_emoji = '✅'
            elif 'Fallback' in source:
                source_emoji = '⚠️'
            else:
                source_emoji = 'ℹ️'
            score_data.append({
                'Criteria': key.replace('_', ' ').title(),
                'Score': f"{score:.1f}/5",
                'Value': detail.get('value', 'N/A'),
                'Weight': f"{weight*100:.0f}%",
                'Weighted': f"{weighted:.2f}",
                'Source': f"{source_emoji} {source[:35]}{'...' if len(source) > 35 else ''}"
            })
        df = pd.DataFrame(score_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        chart_data = pd.DataFrame([
            {'Criteria': row['Criteria'], 'Score': float(row['Score'].split('/')[0])}
            for row in score_data
        ])
        st.bar_chart(chart_data.set_index('Criteria'))
        st.write("---")
        st.write("**📋 Detailed Recommendation Strategy**")
        recommendations = generate_recommendation_strategy(result_data)

        risk = recommendations.get('risk_level', 'Unknown')
        risk_color = ('#ff2d95' if risk in ('High', 'Very High')
                      else '#39ff14' if risk == 'Low' else '#ffe84d')

        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">🎯 Overall Feasibility</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace; font-size: 1.1rem; padding: 10px;">
                {recommendations.get('overall_feasibility', 'Assessment not available')}
            </div>
            <div style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    💰 Investment Required: <span style="color: #00f0ff; font-weight: bold;">{recommendations.get('investment_required', 'Unknown')}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3); padding: 8px 15px; border-radius: 8px;">
                    ⚠️ Risk Level: <span style="color: {risk_color}; font-weight: bold;">{risk}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3); padding: 8px 15px; border-radius: 8px;">
                    🚨 Critical Actions: <span style="color: #ff2d95; font-weight: bold;">{recommendations.get('critical_action_count', 0)}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Immediate: <span style="color: #39ff14; font-weight: bold;">{recommendations['timeline_summary']['immediate']}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Short-term: <span style="color: #ffe84d; font-weight: bold;">{recommendations['timeline_summary']['short_term']}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Long-term: <span style="color: #b026ff; font-weight: bold;">{recommendations['timeline_summary']['long_term']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if recommendations['immediate_actions']:
            st.markdown("""
            <div class="recommendation-container">
                <div class="recommendation-title">🔴 IMMEDIATE ACTIONS (0-6 Months)</div>
            """, unsafe_allow_html=True)
            for action in recommendations['immediate_actions']:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span class="icon">{action.get('priority', '')}</span>
                    {action['text']}
                    <span style="float: right; color: #8080a0; font-size: 0.8rem;">{action.get('cost', '')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if recommendations['short_term_actions']:
            st.markdown("""
            <div class="recommendation-container">
                <div class="recommendation-title">🟡 SHORT-TERM ACTIONS (6-18 Months)</div>
            """, unsafe_allow_html=True)
            for action in recommendations['short_term_actions']:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span class="icon">{action.get('priority', '')}</span>
                    {action['text']}
                    <span style="float: right; color: #8080a0; font-size: 0.8rem;">{action.get('cost', '')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if recommendations['long_term_actions']:
            st.markdown("""
            <div class="recommendation-container">
                <div class="recommendation-title">🟢 LONG-TERM ACTIONS (18-36 Months)</div>
            """, unsafe_allow_html=True)
            for action in recommendations['long_term_actions']:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span class="icon">{action.get('priority', '')}</span>
                    {action['text']}
                    <span style="float: right; color: #8080a0; font-size: 0.8rem;">{action.get('cost', '')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">💰 Investment Summary</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace; padding: 10px;">
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 150px;">
                        <div style="color: #8080a0; font-size: 0.7rem; letter-spacing: 1px;">TOTAL INVESTMENT</div>
                        <div style="font-size: 1.2rem; font-weight: bold; color: {'#ff2d95' if recommendations.get('investment_required') == 'Very High' else '#ffe84d' if recommendations.get('investment_required') == 'Moderate' else '#39ff14'}">
                            {recommendations.get('investment_required', 'Unknown')}
                        </div>
                    </div>
                    <div style="flex: 2; min-width: 200px;">
                        <div style="color: #8080a0; font-size: 0.7rem; letter-spacing: 1px;">ACTION ITEMS</div>
                        <div style="font-size: 1rem;">
                            {len(recommendations['immediate_actions'])} Critical • {len(recommendations['short_term_actions'])} Short-term • {len(recommendations['long_term_actions'])} Long-term
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")
        st.write("**📋 Summary**")
        recommendation = result_data.get('recommendation', '')
        rating = result_data.get('rating', 'Unknown')
        emoji = result_data.get('rating_emoji', '')
        if rating in ['Excellent', 'Good']:
            st.success(f"{emoji} **{rating}** - {recommendation}")
            st.write("This site appears to have strong potential for spaceport development.")
        elif rating == 'Moderate':
            st.warning(f"{emoji} **{rating}** - {recommendation}")
            st.write("This site has potential but requires significant investment and site preparation.")
        else:
            st.error(f"{emoji} **{rating}** - {recommendation}")
            st.write("This site may not be suitable for spaceport development.")

    elif 'amenities' in result_data:
        amenity_type = result_data.get('amenity_type', 'location')
        count = result_data.get('count', 0)
        radius = result_data.get('radius', 0)
        location_info = result_data.get('location', 'Borneo')
        st.write(f"**Found {count} {amenity_type}(s) within {radius}m in {location_info}**")
        if result_data['amenities']:
            df = pd.DataFrame(result_data['amenities'])
            display_cols = [col for col in ['name', 'lat', 'lon', 'type'] if col in df.columns]
            st.dataframe(df[display_cols], use_container_width=True)

def render_comparison_mode():
    st.subheader("🔄 Site Comparison Dashboard")
    with st.spinner("Analysing all candidate sites (HYBRID)..."):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i, (name, coords) in enumerate(SPACEPORT_CANDIDATES.items()):
            status_text.text(f"Analysing: {name}")
            progress_bar.progress((i + 1) / len(SPACEPORT_CANDIDATES))
            location = Location(lat=coords[0], lon=coords[1], name=name)
            params = {'radius': 10000}
            try:
                strategy = StrategySelector.get_strategy('spaceport')
                result = strategy.analyse(location, params)
                if result.get('success'):
                    results.append({
                        'Site': name,
                        'Suitability %': result['suitability_percentage'],
                        'Rating': result['rating'],
                        'Elevation (m)': result.get('elevation_m', 0),
                        'Flood Risk': result.get('flood_risk', 'Unknown'),
                        'Latitude (°)': result.get('lat_deg', 0),
                        'Method': '🌐 OSM' if result.get('used_osm', False) else '📍 Geographic',
                        'Recommendation': result['recommendation'][:50] + '...',
                        'Data': result
                    })
            except Exception as e:
                results.append({
                    'Site': name,
                    'Suitability %': 0,
                    'Rating': 'Error',
                    'Elevation (m)': 0,
                    'Flood Risk': 'Unknown',
                    'Latitude (°)': abs(coords[0]),
                    'Method': 'Error',
                    'Recommendation': f"Analysis error: {str(e)[:50]}",
                    'Data': None
                })
        progress_bar.empty()
        status_text.empty()
        if results:
            df = pd.DataFrame(results)
            df_sorted = df.sort_values('Suitability %', ascending=False)
            st.write(f"**📊 Comparison of {len(results)} Candidate Sites**")
            top_site = df_sorted.iloc[0]
            st.success(f"🚀 **Top Recommended Site: {top_site['Site']}** ({top_site['Suitability %']:.1f}%)")
            st.caption(top_site['Recommendation'])
            display_cols = ['Site', 'Suitability %', 'Rating', 'Elevation (m)', 'Flood Risk', 'Latitude (°)', 'Method']
            st.dataframe(df_sorted[display_cols], use_container_width=True, hide_index=True)
            chart_data = df_sorted[['Site', 'Suitability %']].set_index('Site')
            st.bar_chart(chart_data)
            st.session_state.candidate_scores = {row['Site']: row['Suitability %'] for _, row in df.iterrows()}
            st.write("---")
            st.write("**🗺️ Site Map with Suitability Scores**")
            m = folium.Map(location=[5.0, 117.0], zoom_start=7, tiles="OpenStreetMap")
            for _, row in df.iterrows():
                name = row['Site']
                score = row['Suitability %']
                if score >= 80:
                    color = 'green'
                elif score >= 65:
                    color = 'lightgreen'
                elif score >= 50:
                    color = 'orange'
                elif score >= 35:
                    color = 'lightred'
                else:
                    color = 'red'
                coords = SPACEPORT_CANDIDATES.get(name, (0, 0))
                folium.Marker(
                    coords,
                    popup=f"""
                    <b>{name}</b><br>
                    Suitability: {score:.1f}%<br>
                    Rating: {row['Rating']}<br>
                    Method: {row['Method']}
                    """,
                    tooltip=f"{name}: {score:.1f}%",
                    icon=folium.Icon(color=color, icon='rocket', prefix='fa')
                ).add_to(m)
            try:
                Fullscreen(position='topleft').add_to(m)
            except Exception:
                pass
            st_folium(m, width=None, height=400, use_container_width=True)
            selected_site = st.selectbox(
                "Select a site for detailed analysis:",
                df_sorted['Site'].tolist()
            )
            if selected_site:
                coords = SPACEPORT_CANDIDATES[selected_site]
                st.session_state.selected_location = Location(
                    lat=coords[0],
                    lon=coords[1],
                    name=selected_site
                )
                st.session_state.comparison_mode = False
                st.rerun()

def render_memory_explorer():
    st.subheader("💾 Memory Explorer")
    tab1, tab2 = st.tabs(["Past Analyses", "Learned Parameters"])
    with tab1:
        all_analyses = st.session_state.agent.memory_repo.get_all_analyses(limit=20)
        if all_analyses:
            st.write(f"**{len(all_analyses)} past analyses stored**")
            for entry in all_analyses:
                query_preview = entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
                with st.expander(f"{'✅' if entry['success'] else '❌'} {query_preview}"):
                    st.write(f"**Query:** {entry['query']}")
                    st.write(f"**Success:** {'✅ Yes' if entry['success'] else '❌ No'}")
                    st.write(f"**Execution Time:** {entry['execution_time']:.2f}s")
                    st.write(f"**Timestamp:** {entry['timestamp']}")
                    if entry['parameters']:
                        st.write(f"**Parameters:** {entry['parameters']}")
        else:
            st.info("No past analyses stored yet. Run a spaceport analysis to see it here.")
    with tab2:
        try:
            conn = sqlite3.connect("borneo_spaceport_memory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM learned_parameters ORDER BY success_rate DESC")
            rows = cursor.fetchall()
            conn.close()
            if rows:
                st.write(f"**{len(rows)} learned parameters**")
                df = pd.DataFrame(rows, columns=['ID', 'Analysis Type', 'Parameter', 'Value', 'Success Rate', 'Usage Count', 'Last Updated'])
                st.dataframe(df[['Analysis Type', 'Parameter', 'Value', 'Success Rate', 'Usage Count']], use_container_width=True)
            else:
                st.info("No learned parameters yet. The agent learns from successful analyses.")
        except Exception:
            st.info("No learned parameters yet. The agent learns from successful analyses.")

def main():
    st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div class="main-title">🚀 BORNEO SPACEPORT</div>
        <div class="subtitle">SABAH &amp; SARAWAK · SITE SELECTOR</div>
        <div class="cyber-divider"></div>
        <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;
             letter-spacing: 4px; margin-top: 5px;">
            ⚡ HYBRID · OSM LIVE · INSTANT RESULTS ⚡
        </div>
    </div>
    """, unsafe_allow_html=True)
    init_session_state()
    total_locations = len(SABAH_LOCATIONS) + len(SARAWAK_LOCATIONS)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 8px 15px;
         border: 1px solid rgba(0, 240, 255, 0.1); border-radius: 8px;
         background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;
             letter-spacing: 1px;">
            📍 LOCATIONS LOADED
        </span>
        <span style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 0.8rem;
             font-weight: bold; letter-spacing: 1px;">
            {total_locations}
        </span>
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
             letter-spacing: 1px;">
            SABAH · SARAWAK
        </span>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get('comparison_mode', False):
        render_comparison_mode()
        if st.button("← BACK TO SINGLE SITE"):
            st.session_state.comparison_mode = False
            st.rerun()
        st.divider()
        return
    params = render_sidebar()
    col1, col2 = st.columns([1.5, 1])
    with col1:
        render_map(params)
        render_query_interface(params)
    with col2:
        if st.session_state.selected_location:
            name = st.session_state.selected_location.name or "Borneo Location"
            st.markdown(f"""
            <div style="padding: 10px 15px; border: 1px solid rgba(0, 240, 255, 0.15);
                 border-radius: 8px; background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                     letter-spacing: 1px;">SELECTED LOCATION</div>
                <div style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 0.9rem;">
                    {name}
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                     letter-spacing: 1px;">
                    {st.session_state.selected_location.lat:.4f}, {st.session_state.selected_location.lon:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        render_reasoning_log()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        render_results()
    with col2:
        render_memory_explorer()
    st.markdown("""
    <div class="cyber-divider"></div>
    <div style="text-align: center; padding: 15px 0; color: #333; font-family: 'Courier New', monospace;
         font-size: 0.6rem; letter-spacing: 2px;">
        <span style="color: #00f0ff;">[</span>
        BORNEO SPACEPORT SELECTOR v2.0 · CYBERPUNK EDITION
        <span style="color: #00f0ff;">]</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
