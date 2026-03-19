import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import json
import streamlit.components.v1 as components

# ============================================================
# SPX PROPHET NEXT GEN v2.0
# Proprietary Market Structure System
# ============================================================

st.set_page_config(
    page_title="SPX Prophet",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN SYSTEM — Luxury Dark Terminal
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg: #060910;
        --bg-card: rgba(11, 15, 26, 0.9);
        --bg-alt: rgba(14, 19, 34, 0.85);
        --border: rgba(255,255,255,0.04);
        --border-h: rgba(255,255,255,0.1);
        --t1: #e2e8f0;
        --t2: #8892b0;
        --t3: #3d4f6f;
        --cyan: #00d4ff;
        --green: #00e676;
        --red: #ff1744;
        --gold: #ffd740;
        --purple: #b388ff;
    }

    .stApp { background: var(--bg) !important; }
    .block-container { padding-top: 0.8rem !important; max-width: 1100px !important; }
    [data-testid="stSidebar"] { background: #080c18 !important; border-right: 1px solid var(--border) !important; }
    
    /* HEADER */
    .app-header { text-align: center; padding: 1.6rem 0 0.8rem; border-bottom: 1px solid var(--border); margin-bottom: 1rem; }
    .app-title { font-family: 'Outfit'; font-weight: 800; font-size: 1.7rem; letter-spacing: 8px; text-transform: uppercase; background: linear-gradient(135deg, #e2e8f0, #4a5a7a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .app-sub { font-family: 'JetBrains Mono'; font-size: 0.6rem; color: var(--t3); letter-spacing: 5px; text-transform: uppercase; margin-top: 2px; }
    
    /* SECTIONS */
    .sec { display: flex; align-items: center; gap: 10px; padding: 10px 0; margin: 16px 0 6px; border-bottom: 1px solid var(--border); }
    .sec-title { font-family: 'Outfit'; font-weight: 700; font-size: 0.95rem; color: var(--t1); }
    .sec-sub { font-family: 'JetBrains Mono'; font-size: 0.6rem; color: var(--t3); margin-left: auto; }
    
    /* KPI CARDS */
    .kpi-row { display: grid; gap: 10px; margin: 10px 0; }
    .kpi { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 16px; text-align: center; }
    .kpi:hover { border-color: var(--border-h); }
    .kpi-label { font-family: 'JetBrains Mono'; font-size: 0.55rem; color: var(--t3); letter-spacing: 3px; text-transform: uppercase; }
    .kpi-val { font-family: 'JetBrains Mono'; font-weight: 700; font-size: 1.25rem; margin-top: 4px; }
    .kpi-sub { font-family: 'Rajdhani'; font-size: 0.7rem; color: var(--t3); margin-top: 2px; }
    
    /* SIGNAL BANNER */
    .sig { border-radius: 16px; padding: 28px; margin: 14px 0; text-align: center; border: 1px solid; position: relative; overflow: hidden; }
    .sig::after { content: ''; position: absolute; top: 50%; left: 50%; width: 200%; height: 200%; transform: translate(-50%,-50%); border-radius: 50%; pointer-events: none; }
    .sig.bull { border-color: rgba(0,230,118,0.25); background: rgba(0,230,118,0.03); }
    .sig.bull::after { background: radial-gradient(circle, rgba(0,230,118,0.06), transparent 60%); }
    .sig.bear { border-color: rgba(255,23,68,0.25); background: rgba(255,23,68,0.03); }
    .sig.bear::after { background: radial-gradient(circle, rgba(255,23,68,0.06), transparent 60%); }
    .sig.neutral { border-color: rgba(255,215,64,0.25); background: rgba(255,215,64,0.03); }
    .sig.neutral::after { background: radial-gradient(circle, rgba(255,215,64,0.06), transparent 60%); }
    .sig-dir { font-family: 'Outfit'; font-weight: 800; font-size: 1.6rem; letter-spacing: 3px; position: relative; z-index: 1; }
    .sig-detail { font-family: 'Rajdhani'; font-size: 0.85rem; color: var(--t2); margin-top: 8px; position: relative; z-index: 1; }
    
    /* TRADE CARD */
    .tc { background: var(--bg-card); border-radius: 16px; border: 1px solid var(--border); overflow: hidden; margin: 12px 0; }
    .tc-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 22px; border-bottom: 1px solid var(--border); }
    .tc-title { font-family: 'Outfit'; font-weight: 800; font-size: 1.15rem; letter-spacing: 2px; }
    .tc-meta { font-family: 'JetBrains Mono'; font-size: 0.65rem; color: var(--t3); }
    .tc-grid { display: grid; grid-template-columns: repeat(3, 1fr); }
    .tc-cell { text-align: center; padding: 16px; border-right: 1px solid var(--border); }
    .tc-cell:last-child { border-right: none; }
    .tc-cell-label { font-family: 'JetBrains Mono'; font-size: 0.55rem; color: var(--t3); letter-spacing: 2px; text-transform: uppercase; }
    .tc-cell-val { font-family: 'JetBrains Mono'; font-weight: 700; font-size: 1.15rem; margin-top: 4px; }
    .tc-cell-sub { font-family: 'JetBrains Mono'; font-size: 0.62rem; color: var(--t3); margin-top: 2px; }
    
    /* CONFLUENCE */
    .cf-row { display: flex; align-items: center; gap: 10px; padding: 8px 14px; margin: 3px 0; background: rgba(255,255,255,0.015); border-radius: 10px; border-left: 3px solid; }
    .cf-name { font-family: 'Rajdhani'; font-weight: 600; min-width: 110px; font-size: 0.85rem; }
    .cf-detail { font-family: 'JetBrains Mono'; font-size: 0.72rem; color: var(--t2); }
    
    /* LONDON SWEEP BOX */
    .london { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 16px 20px; margin: 10px 0; }
    .london-label { font-family: 'JetBrains Mono'; font-size: 0.6rem; color: var(--t3); letter-spacing: 3px; text-transform: uppercase; }
    .london-val { font-family: 'JetBrains Mono'; font-weight: 600; font-size: 0.82rem; margin-top: 6px; line-height: 1.5; }
    
    /* RULES BOX */
    .rules { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 18px 22px; margin: 12px 0; }
    .rules-title { font-family: 'Outfit'; font-weight: 700; font-size: 0.8rem; color: var(--gold); letter-spacing: 2px; margin-bottom: 10px; }
    .rules-body { font-family: 'JetBrains Mono'; font-size: 0.72rem; color: var(--t2); line-height: 2; }
    
    /* PREMIUM SCENARIOS */
    .sc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 10px 0; }
    .sc { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 14px; text-align: center; }
    .sc-label { font-family: 'JetBrains Mono'; font-size: 0.55rem; letter-spacing: 2px; text-transform: uppercase; }
    .sc-premium { font-family: 'JetBrains Mono'; font-weight: 700; font-size: 1.1rem; margin-top: 4px; }
    .sc-pnl { font-family: 'JetBrains Mono'; font-size: 0.7rem; margin-top: 4px; }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 2px; border-bottom: 1px solid var(--border) !important; }
    .stTabs [data-baseweb="tab"] { font-family: 'JetBrains Mono' !important; font-size: 0.72rem !important; letter-spacing: 1.5px !important; padding: 10px 22px !important; background: transparent !important; color: var(--t3) !important; border-radius: 10px 10px 0 0 !important; }
    .stTabs [aria-selected="true"] { background: var(--bg-card) !important; color: var(--t1) !important; border: 1px solid var(--border) !important; border-bottom: none !important; }
    
    /* INPUTS */
    .stNumberInput > div > div > input, .stTextInput > div > div > input { background: var(--bg-card) !important; border: 1px solid var(--border) !important; color: var(--t1) !important; font-family: 'JetBrains Mono' !important; border-radius: 10px !important; }
    .stSelectbox > div > div { background: var(--bg-card) !important; border-radius: 10px !important; }
    label { font-family: 'Rajdhani' !important; color: var(--t2) !important; }
    .stButton > button { background: var(--bg-card) !important; border: 1px solid var(--border-h) !important; color: var(--t1) !important; font-family: 'JetBrains Mono' !important; font-size: 0.75rem !important; border-radius: 10px !important; letter-spacing: 1px !important; }
    .stButton > button:hover { border-color: var(--cyan) !important; }
    .stExpander { border: 1px solid var(--border) !important; border-radius: 12px !important; }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }
    [data-testid="stSidebar"] label { color: #8892b0 !important; }
    [data-testid="stSidebar"] .stMarkdown { color: #8892b0; }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 { color: #e2e8f0 !important; }
    
    /* HIDE */
    #MainMenu, footer, .stDeployButton { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    
    /* DIVIDER */
    .divider { height: 1px; background: var(--border); margin: 16px 0; }
    
    /* Quill dark theme */
    .ql-snow { border: none !important; background: transparent !important; }
    .ql-editor { background: var(--bg-card) !important; color: var(--t1) !important; font-family: 'Rajdhani' !important; border-radius: 10px !important; min-height: 180px !important; border: 1px solid var(--border) !important; }
    .ql-toolbar { background: transparent !important; border: 1px solid var(--border) !important; border-radius: 10px 10px 0 0 !important; }
    .ql-toolbar .ql-stroke { stroke: var(--t3) !important; }
    .ql-toolbar .ql-fill { fill: var(--t3) !important; }
    .ql-toolbar .ql-picker-label { color: var(--t3) !important; }
    .ql-toolbar button:hover .ql-stroke { stroke: var(--cyan) !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CORE ENGINE: Line Projection Calculator
# ============================================================

RATE_PER_CANDLE = 13/25  # Default rate (override via secrets.toml)
CANDLE_MINUTES = 30
MAINTENANCE_START_CT = time(16, 0)  # 4:00 PM CT
MAINTENANCE_END_CT = time(17, 0)    # 5:00 PM CT
NY_OPEN_CT = time(8, 30)
NY_DECISION_CT = time(9, 0)
NY_CLOSE_CT = time(15, 0)


def count_candles_between(start_dt: datetime, end_dt: datetime) -> int:
    """
    Count the number of 30-minute candles between two datetimes,
    excluding the maintenance window (4:00 PM - 5:00 PM CT).
    
    Candles are counted at each 30-min mark: :00 and :30 of each hour.
    The candle at start_dt is candle 0, so we count candles from start
    up to (but not including) end_dt's candle.
    
    Skips:
    - Maintenance window: 4:00 PM - 5:00 PM CT Mon-Thu only
    - Weekend closure: Friday 4:00 PM CT through Sunday 5:00 PM CT
      (Friday evening, Saturday all day, Sunday before 5:00 PM CT)
    """
    if end_dt <= start_dt:
        return 0
    
    count = 0
    current = start_dt
    
    while current < end_dt:
        current += timedelta(minutes=CANDLE_MINUTES)
        current_time = current.time()
        weekday = current.weekday()  # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
        
        # Skip all of Saturday (weekday 5)
        if weekday == 5:
            continue
        
        # Skip Sunday before 5:00 PM CT (weekday 6)
        if weekday == 6 and current_time < MAINTENANCE_END_CT:
            continue
        
        # Skip Friday after market close at 4:00 PM CT (weekday 4)
        # Market closes Friday at 4pm, no evening globex session
        if weekday == 4 and current_time >= MAINTENANCE_START_CT:
            continue
        
        # Skip maintenance window (4:00 PM - 5:00 PM CT) Mon-Thu
        if MAINTENANCE_START_CT <= current_time < MAINTENANCE_END_CT:
            continue
        
        count += 1
    
    return count


def calculate_line_value(anchor_price: float, anchor_time: datetime, 
                         target_time: datetime, direction: str) -> float:
    """
    Calculate the projected line value at a target time.
    
    direction: 'ascending' (+rate/candle) or 'descending' (-rate/candle)
    """
    candles = count_candles_between(anchor_time, target_time)
    
    if direction == 'ascending':
        return anchor_price + (RATE_PER_CANDLE * candles)
    else:
        return anchor_price - (RATE_PER_CANDLE * candles)


def generate_line_series(anchor_price: float, anchor_time: datetime,
                         start_time: datetime, end_time: datetime,
                         direction: str) -> list:
    """
    Generate a series of (datetime, price) tuples for plotting a projected line.
    """
    points = []
    current = anchor_time
    
    # First point at anchor
    points.append((anchor_time, anchor_price))
    
    # Step forward in 30-min increments
    while current < end_time:
        current += timedelta(minutes=CANDLE_MINUTES)
        current_time_only = current.time()
        weekday = current.weekday()
        
        # Skip Saturday entirely
        if weekday == 5:
            continue
        
        # Skip Sunday before 5:00 PM CT
        if weekday == 6 and current_time_only < MAINTENANCE_END_CT:
            continue
        
        # Skip Friday after 4:00 PM CT (no evening session)
        if weekday == 4 and current_time_only >= MAINTENANCE_START_CT:
            continue
        
        # Skip maintenance window (4:00 PM - 5:00 PM CT) Mon-Thu
        if MAINTENANCE_START_CT <= current_time_only < MAINTENANCE_END_CT:
            continue
        
        value = calculate_line_value(anchor_price, anchor_time, current, direction)
        points.append((current, value))
    
    # Filter to only show from start_time onward
    points = [(t, v) for t, v in points if t >= start_time]
    
    return points


def render_visual_ladder(lines: list, current_price: float = None, 
                          title: str = "Line Ladder", height: int = 600,
                          show_zones: bool = True, show_distances: bool = True):
    """Render a spatial vertical ruler with anti-collision logic. Uses st.components.v1.html for full CSS."""
    import streamlit as st
    import streamlit.components.v1 as components
    
    sorted_lines = sorted(lines, key=lambda x: x['value'], reverse=True)
    if not sorted_lines:
        return
    
    # Build items list with current price
    all_items = []
    for line in sorted_lines:
        all_items.append({
            'label': line.get('label', ''),
            'full_name': line.get('full_name', ''),
            'val': line['value'],
            'direction': line.get('direction', 'ascending'),
            'color': line.get('color', '#888'),
            'is_key': line.get('is_key', False),
            'is_live': False,
        })
    
    if current_price is not None:
        all_items.append({
            'label': 'CURRENT', 'full_name': 'Market Price',
            'val': current_price, 'direction': 'neutral',
            'color': '#00d4ff', 'is_key': True, 'is_live': True,
        })
    
    # Sort descending (highest at top)
    all_items.sort(key=lambda x: x['val'], reverse=True)
    
    # Calculate proportional positions
    max_p = all_items[0]['val']
    min_p = all_items[-1]['val']
    padding = (max_p - min_p) * 0.1 if max_p != min_p else 10
    max_p += padding
    min_p -= padding
    price_range = max_p - min_p if max_p != min_p else 1
    
    for item in all_items:
        item['top_pct'] = 100 - (((item['val'] - min_p) / price_range) * 100)
    
    # Anti-collision: minimum 7% gap between elements
    min_gap = 7.0
    for i in range(1, len(all_items)):
        if all_items[i]['top_pct'] - all_items[i-1]['top_pct'] < min_gap:
            all_items[i]['top_pct'] = all_items[i-1]['top_pct'] + min_gap
    
    # Re-center if bottom items pushed out of bounds
    overflow = all_items[-1]['top_pct'] - 95
    if overflow > 0:
        for item in all_items:
            item['top_pct'] -= overflow
    
    # Calculate container height based on items
    container_height = max(height, len(all_items) * 55)
    
    # Build HTML
    html = f"""
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Orbitron:wght@400;700;800&family=Rajdhani:wght@400;500;700&display=swap" rel="stylesheet">
    <div style="position:relative;height:{container_height}px;background:rgba(15,23,42,0.4);border-radius:12px;border:1px solid rgba(255,255,255,0.05);margin:0.5rem 0;overflow:hidden;">
        <div style="position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(255,255,255,0.08);"></div>
    """
    
    for item in all_items:
        top = item['top_pct']
        
        if item['is_live']:
            # Current price — centered glowing band
            dist_texts = []
            for other in all_items:
                if other['is_live']:
                    continue
                d = other['val'] - item['val']
                if abs(d) < 0.01:
                    continue
            
            html += f"""<div style="position:absolute;top:{top}%;left:0;right:0;transform:translateY(-50%);z-index:10;">
                <div style="position:absolute;left:0;right:0;height:1px;background:rgba(56,189,248,0.3);top:50%;"></div>
                <div style="background:rgba(56,189,248,0.12);border:1px solid rgba(56,189,248,0.5);box-shadow:0 0 20px rgba(56,189,248,0.3);border-radius:6px;padding:10px 14px;width:220px;margin:0 auto;text-align:center;backdrop-filter:blur(5px);">
                    <div style="color:#94a3b8;font-family:Rajdhani,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;">◉ Live Price</div>
                    <div style="color:#38bdf8;font-family:JetBrains Mono,monospace;font-size:1.5rem;font-weight:800;">{item['val']:.2f}</div>
                </div>
            </div>"""
        else:
            is_asc = item['direction'] == 'ascending'
            color = item['color']
            weight = "800" if item['is_key'] else "400"
            opacity = "1" if item['is_key'] else "0.55"
            font_size = "0.9rem" if item['is_key'] else "0.8rem"
            val_size = "1rem" if item['is_key'] else "0.85rem"
            
            # Ascending on the LEFT, descending on the RIGHT
            if is_asc:
                align = "right"
                left_pos = "0"
                border_side = "border-right"
                pad_side = "padding-right"
            else:
                align = "left"
                left_pos = "50%"
                border_side = "border-left"
                pad_side = "padding-left"
            
            # Distance from price
            dist_html = ""
            if current_price is not None:
                dist = item['val'] - current_price
                dist_color = "rgba(0,230,118,0.5)" if dist > 0 else "rgba(255,23,68,0.5)"
                dist_html = f'<span style="color:{dist_color};font-size:0.7rem;margin-left:8px;">{dist:+.1f}</span>'
            
            # Horizontal tick line extending to center
            tick_left = "calc(100% - 1px)" if is_asc else "0"
            tick_width = "calc(50vw)" if is_asc else "calc(50vw)"
            tick_html = ""
            if item['is_key']:
                if is_asc:
                    tick_html = f'<div style="position:absolute;top:50%;right:0;width:50%;height:1px;background:linear-gradient(to right,transparent,{color}40);"></div>'
                else:
                    tick_html = f'<div style="position:absolute;top:50%;left:0;width:50%;height:1px;background:linear-gradient(to left,transparent,{color}40);"></div>'
            
            arrow = "↗" if is_asc else "↘"
            label_text = f"{item['label']} {arrow}"
            if item['is_key'] and item.get('full_name'):
                label_text = f"{item['label']} {arrow} {item['full_name'][:15]}"
            
            html += f"""<div style="position:absolute;top:{top}%;left:{left_pos};width:50%;transform:translateY(-50%);text-align:{align};padding:0 15px;opacity:{opacity};z-index:5;">
                {tick_html}
                <div style="display:inline-block;font-family:JetBrains Mono,monospace;font-size:{font_size};color:{color};{border_side}:{'3px' if item['is_key'] else '2px'} solid {color};{pad_side}:10px;background:rgba(15,23,42,0.85);border-radius:4px;padding:4px 10px;">
                    <span style="font-family:Outfit,sans-serif;font-weight:{weight};">{label_text}</span>
                    <span style="font-weight:700;font-size:{val_size};margin-left:6px;">{item['val']:.2f}</span>{dist_html}
                </div>
            </div>"""
    
    html += "</div>"
    components.html(html, height=container_height + 20, scrolling=False)


def render_signal_display(signal_text: str, signal_detail: str, signal_class: str):
    """V2 signal banner with radial glow."""
    import streamlit as st
    color = '#00e676' if signal_class == 'bull' else '#ff1744' if signal_class == 'bear' else '#ffd740'
    st.markdown(f"""
    <div class="sig {signal_class}">
        <div class="sig-dir" style="color:{color};">{signal_text}</div>
        <div class="sig-detail">{signal_detail}</div>
    </div>""", unsafe_allow_html=True)


def render_scenario_cards(scenarios: list, num_contracts: int = 3):
    """V2 premium scenario cards."""
    import streamlit as st
    html = '<div class="sc-grid">'
    for s in scenarios:
        pnl_per_contract = (s['premium'] - s['entry_premium']) * 100
        pnl_total = pnl_per_contract * num_contracts
        pnl_color = '#00e676' if pnl_total >= 0 else '#ff1744'
        pnl_sign = '+' if pnl_total >= 0 else ''
        pnl_pct = ((s['premium'] - s['entry_premium']) / s['entry_premium'] * 100) if s['entry_premium'] > 0 else 0
        color = s['color']
        html += f"""<div class="sc" style="border-top:2px solid {color}50;">
            <div class="sc-label" style="color:{color};">{s['label']}</div>
            <div style="font-family:JetBrains Mono;font-size:0.6rem;color:var(--t3);margin:2px 0;">{s['spx_label']}</div>
            <div class="sc-premium" style="color:{color};">${s['premium']:.2f}</div>
            <div style="font-family:JetBrains Mono;font-size:0.6rem;color:var(--t3);">${s['premium']*100:.0f}/contract</div>
            <div class="sc-pnl" style="color:{pnl_color};font-weight:700;">
                {pnl_sign}${pnl_total:,.0f} <span style="font-size:0.6rem;opacity:0.6;">({pnl_sign}{pnl_pct:.0f}%)</span></div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_metric_row(metrics: list):
    """V2 KPI row."""
    import streamlit as st
    n = len(metrics)
    html = f'<div class="kpi-row" style="grid-template-columns:repeat({n},1fr);">'
    for m in metrics:
        color = m.get('color', '#00d4ff')
        subtitle = m.get('subtitle', '')
        sub_html = f'<div class="kpi-sub">{subtitle}</div>' if subtitle else ''
        html += f"""<div class="kpi" style="border-bottom:2px solid {color}25;">
            <div class="kpi-label">{m['label']}</div>
            <div class="kpi-val" style="color:{color};">{m['value']}</div>
            {sub_html}
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_section_banner(icon: str, title: str, subtitle: str = "", color: str = "#00d4ff"):
    """V2 section header."""
    import streamlit as st
    sub_html = f'<span class="sec-sub">{subtitle}</span>' if subtitle else ''
    st.markdown(f"""
    <div class="sec">
        <span style="font-size:1.1rem;">{icon}</span>
        <span class="sec-title">{title}</span>
        {sub_html}
    </div>""", unsafe_allow_html=True)


def calculate_nine_am_levels(bounces: list, rejections: list,
                             highest_wick: dict, lowest_wick: dict,
                             next_day_date: datetime) -> dict:
    """
    Calculate the four key horizontal levels at 9:00 AM CT the next day.
    
    bounces: list of {'price': float, 'time': datetime}
    rejections: list of {'price': float, 'time': datetime}
    highest_wick: {'price': float, 'time': datetime}
    lowest_wick: {'price': float, 'time': datetime}
    """
    nine_am = datetime.combine(next_day_date.date(), NY_DECISION_CT)
    
    # Calculate all ascending lines at 9 AM (from bounces + highest wick)
    ascending_at_9am = []
    for bounce in bounces:
        val = calculate_line_value(bounce['price'], bounce['time'], nine_am, 'ascending')
        ascending_at_9am.append({
            'source': f"Bounce @ {bounce['price']:.2f} ({bounce['time'].strftime('%I:%M %p')})",
            'anchor_price': bounce['price'],
            'anchor_time': bounce['time'],
            'value_at_9am': val,
            'type': 'bounce'
        })
    
    # Highest wick ascending
    hw_val = calculate_line_value(highest_wick['price'], highest_wick['time'], nine_am, 'ascending')
    ascending_at_9am.append({
        'source': f"Highest Wick @ {highest_wick['price']:.2f} ({highest_wick['time'].strftime('%I:%M %p')})",
        'anchor_price': highest_wick['price'],
        'anchor_time': highest_wick['time'],
        'value_at_9am': hw_val,
        'type': 'highest_wick'
    })
    
    # Calculate all descending lines at 9 AM (from rejections + lowest wick)
    descending_at_9am = []
    for rejection in rejections:
        val = calculate_line_value(rejection['price'], rejection['time'], nine_am, 'descending')
        descending_at_9am.append({
            'source': f"Rejection @ {rejection['price']:.2f} ({rejection['time'].strftime('%I:%M %p')})",
            'anchor_price': rejection['price'],
            'anchor_time': rejection['time'],
            'value_at_9am': val,
            'type': 'rejection'
        })
    
    # Lowest wick descending
    lw_val = calculate_line_value(lowest_wick['price'], lowest_wick['time'], nine_am, 'descending')
    descending_at_9am.append({
        'source': f"Lowest Wick @ {lowest_wick['price']:.2f} ({lowest_wick['time'].strftime('%I:%M %p')})",
        'anchor_price': lowest_wick['price'],
        'anchor_time': lowest_wick['time'],
        'value_at_9am': lw_val,
        'type': 'lowest_wick'
    })
    
    # Sort to find the key levels
    ascending_at_9am.sort(key=lambda x: x['value_at_9am'], reverse=True)
    descending_at_9am.sort(key=lambda x: x['value_at_9am'])
    
    # Identify the four key lines
    highest_wick_asc = next((l for l in ascending_at_9am if l['type'] == 'highest_wick'), ascending_at_9am[0])
    highest_bounce_asc = next((l for l in ascending_at_9am if l['type'] == 'bounce'), None)
    
    # If highest bounce is actually higher than highest wick, swap labels for clarity
    # The "highest" refers to the line with the highest 9am value
    
    lowest_wick_desc = next((l for l in descending_at_9am if l['type'] == 'lowest_wick'), descending_at_9am[0])
    lowest_rejection_desc = next((l for l in descending_at_9am if l['type'] == 'rejection'), None)
    
    return {
        'ascending': ascending_at_9am,
        'descending': descending_at_9am,
        'key_levels': {
            'highest_wick_ascending': highest_wick_asc,
            'highest_bounce_ascending': highest_bounce_asc,
            'lowest_wick_descending': lowest_wick_desc,
            'lowest_rejection_descending': lowest_rejection_desc,
        },
        'nine_am_time': nine_am
    }


def calculate_channel_structure(bounces: list, rejections: list,
                                highest_wick: dict, lowest_wick: dict,
                                next_day_date: datetime,
                                candles: pd.DataFrame = None,
                                prior_date=None, es_offset: float = 0.0) -> dict:
    """
    Build the 6-line channel structure.
    
    Channel anchors = lowest close and highest close from 12-3 PM CT.
    
    From those two prices:
    - Ascending line from lowest close = ascending channel floor
    - Ascending line from highest close = ascending channel ceiling
    - Descending line from highest close = descending channel ceiling
    - Descending line from lowest close = descending channel floor
    
    Plus HW ascending and LW descending for extreme scenarios.
    """
    nine_am = datetime.combine(next_day_date.date(), NY_DECISION_CT)
    
    # ── Find lowest/highest CLOSE from 12-3 PM CT ──
    afternoon_low_close = None
    afternoon_high_close = None
    
    if candles is not None and len(candles) > 0 and prior_date is not None:
        # Filter to afternoon session: 12:00 PM CT to 3:00 PM CT
        afternoon_candles = []
        for _, row in candles.iterrows():
            ct = row['datetime']
            if ct.date() == prior_date and ct.hour >= 12 and ct.hour < 15:
                # Apply ES-SPX offset to get SPX prices
                close_spx = row['close'] - es_offset
                afternoon_candles.append({
                    'price': close_spx,
                    'time': ct,
                    'raw_close': row['close'],
                })
        
        if afternoon_candles:
            lowest = min(afternoon_candles, key=lambda x: x['price'])
            highest = max(afternoon_candles, key=lambda x: x['price'])
            afternoon_low_close = {'price': lowest['price'], 'time': lowest['time']}
            afternoon_high_close = {'price': highest['price'], 'time': highest['time']}
    
    # Fallback: use bounces/rejections if no candle data
    if afternoon_low_close is None:
        if bounces:
            lowest_bounce = min(bounces, key=lambda x: x['price'])
            afternoon_low_close = lowest_bounce
        else:
            afternoon_low_close = lowest_wick
    
    if afternoon_high_close is None:
        if rejections:
            highest_rejection = max(rejections, key=lambda x: x['price'])
            afternoon_high_close = highest_rejection
        else:
            afternoon_high_close = highest_wick
    
    low_price = afternoon_low_close['price']
    low_time = afternoon_low_close['time']
    high_price = afternoon_high_close['price']
    high_time = afternoon_high_close['time']
    
    # ── ASCENDING CHANNEL ──
    # Floor: ascending line from lowest afternoon close
    # Ceiling: ascending line from highest afternoon close
    asc_floor_val = calculate_line_value(low_price, low_time, nine_am, 'ascending')
    asc_ceil_val = calculate_line_value(high_price, high_time, nine_am, 'ascending')
    
    if asc_floor_val > asc_ceil_val:
        asc_floor_val, asc_ceil_val = asc_ceil_val, asc_floor_val
    
    asc_floor = {
        'label': 'ASC Floor', 'value': asc_floor_val, 'direction': 'ascending',
        'color': '#ff5252', 'is_key': True, 'channel': 'ascending',
        'anchor': low_price, 'anchor_time': low_time,
        'full_name': f"Asc Floor ({low_price:.0f})"
    }
    asc_ceil = {
        'label': 'ASC Ceil', 'value': asc_ceil_val, 'direction': 'ascending',
        'color': '#ff1744', 'is_key': True, 'channel': 'ascending',
        'anchor': high_price, 'anchor_time': high_time,
        'full_name': f"Asc Ceiling ({high_price:.0f})"
    }
    
    # ── DESCENDING CHANNEL ──
    # Ceiling: descending line from highest afternoon close
    # Floor: descending line from lowest afternoon close
    desc_ceil_val = calculate_line_value(high_price, high_time, nine_am, 'descending')
    desc_floor_val = calculate_line_value(low_price, low_time, nine_am, 'descending')
    
    if desc_floor_val > desc_ceil_val:
        desc_floor_val, desc_ceil_val = desc_ceil_val, desc_floor_val
    
    desc_ceil = {
        'label': 'DESC Ceil', 'value': desc_ceil_val, 'direction': 'descending',
        'color': '#69f0ae', 'is_key': True, 'channel': 'descending',
        'anchor': high_price, 'anchor_time': high_time,
        'full_name': f"Desc Ceiling ({high_price:.0f})"
    }
    desc_floor = {
        'label': 'DESC Floor', 'value': desc_floor_val, 'direction': 'descending',
        'color': '#00e676', 'is_key': True, 'channel': 'descending',
        'anchor': low_price, 'anchor_time': low_time,
        'full_name': f"Desc Floor ({low_price:.0f})"
    }
    
    # ── WICK LINES (extreme outliers) ──
    hw_val = calculate_line_value(highest_wick['price'], highest_wick['time'], nine_am, 'ascending')
    hw_line = {
        'label': 'HW ↗', 'value': hw_val, 'direction': 'ascending',
        'color': '#ff1744', 'is_key': True, 'channel': 'wick',
        'anchor': highest_wick['price'], 'anchor_time': highest_wick['time'],
        'full_name': f"Highest Wick ({highest_wick['price']:.0f})"
    }
    
    lw_val = calculate_line_value(lowest_wick['price'], lowest_wick['time'], nine_am, 'descending')
    lw_line = {
        'label': 'LW ↘', 'value': lw_val, 'direction': 'descending',
        'color': '#00e676', 'is_key': True, 'channel': 'wick',
        'anchor': lowest_wick['price'], 'anchor_time': lowest_wick['time'],
        'full_name': f"Lowest Wick ({lowest_wick['price']:.0f})"
    }
    
    # Channel width analysis
    asc_width = asc_ceil_val - asc_floor_val
    desc_width = desc_ceil_val - desc_floor_val
    
    return {
        'asc_floor': asc_floor,
        'asc_ceil': asc_ceil,
        'desc_ceil': desc_ceil,
        'desc_floor': desc_floor,
        'hw_line': hw_line,
        'lw_line': lw_line,
        'all_lines': [hw_line, asc_ceil, asc_floor, desc_ceil, desc_floor, lw_line],
        'asc_width': asc_width,
        'desc_width': desc_width,
        'afternoon_low': afternoon_low_close,
        'afternoon_high': afternoon_high_close,
    }


def determine_scenario(channels: dict, current_price: float, confirmation_830: dict = None) -> dict:
    """
    Determine the trading scenario and build a complete playbook.
    
    6 scenarios based on where price opens relative to channels:
    1. Between channels (most common)
    2. Inside ascending channel
    3. Inside descending channel
    4. Above ascending channel (below HW line)
    5. Below descending channel (above LW line)
    6. Beyond wick lines (extreme gap)
    """
    af = channels['asc_floor']['value']
    ac = channels['asc_ceil']['value']
    dc = channels['desc_ceil']['value']
    df = channels['desc_floor']['value']
    hw = channels['hw_line']['value']
    lw = channels['lw_line']['value']
    
    p = current_price
    
    scenario = None
    primary = None
    alternate = None
    
    if p > hw:
        # SCENARIO 6a: Above highest wick — extreme gap up, no structure above
        scenario = {
            'number': 6, 'name': 'EXTREME GAP UP',
            'desc': f'Price {p:.2f} is ABOVE highest wick line ({hw:.2f}). No structural resistance above. Dangerous to trade.',
            'color': '#ffd740', 'class': 'neutral',
        }
        primary = {
            'direction': 'PUT', 'entry_line': channels['hw_line'],
            'entry_price': hw, 'stop_price': hw + 5,
            'stop_desc': '5pt above HW line (no structure)',
            'tp1_line': channels['asc_ceil'], 'tp1_price': ac, 'tp1_desc': 'Asc Ceiling',
            'tp2_line': channels['asc_floor'], 'tp2_price': af, 'tp2_desc': 'Asc Floor',
            'timing': 'If price returns to HW line and rejects',
            'confidence': 'LOW — trading against momentum in a gap',
        }
    
    elif p > ac:
        # SCENARIO 4: Above ascending channel, below HW
        scenario = {
            'number': 4, 'name': 'ABOVE ASCENDING CHANNEL',
            'desc': f'Price {p:.2f} above ascending ceiling ({ac:.2f}). Channel below is now support. HW line ({hw:.2f}) is resistance above.',
            'color': '#ff9100', 'class': 'neutral',
        }
        primary = {
            'direction': 'PUT', 'entry_line': channels['hw_line'],
            'entry_price': hw, 'stop_price': hw + 3,
            'stop_desc': '3pt above HW line',
            'tp1_line': channels['asc_ceil'], 'tp1_price': ac, 'tp1_desc': 'Asc Ceiling',
            'tp2_line': channels['asc_floor'], 'tp2_price': af, 'tp2_desc': 'Asc Floor',
            'timing': 'Wait for price to reach HW line',
            'confidence': 'MEDIUM — HW is last resistance',
        }
        alternate = {
            'direction': 'CALL', 'entry_line': channels['asc_ceil'],
            'entry_price': ac, 'stop_price': af,
            'stop_desc': 'Below Asc Floor',
            'tp1_price': hw, 'tp1_desc': 'HW Line',
            'tp2_price': hw + 5, 'tp2_desc': 'Beyond HW',
            'timing': 'If price pulls back to ascending ceiling and bounces',
            'confidence': 'MEDIUM — channel becomes support',
        }
    
    elif p >= af and p <= ac:
        # SCENARIO 2: Inside ascending channel
        scenario = {
            'number': 2, 'name': 'INSIDE ASCENDING CHANNEL',
            'desc': f'Price {p:.2f} is INSIDE the ascending channel ({af:.2f} floor — {ac:.2f} ceiling). In the resistance zone. Watch for rejection.',
            'color': '#ff5252', 'class': 'bear',
        }
        primary = {
            'direction': 'PUT', 'entry_line': channels['asc_ceil'],
            'entry_price': ac, 'stop_price': hw,
            'stop_desc': f'HW line at {hw:.2f}',
            'tp1_line': channels['desc_ceil'], 'tp1_price': dc, 'tp1_desc': 'Desc Ceiling',
            'tp2_line': channels['desc_floor'], 'tp2_price': df, 'tp2_desc': 'Desc Floor',
            'timing': 'Enter on rejection from ceiling, or if 8:30 already confirmed',
            'confidence': 'HIGH — already inside resistance zone',
        }
        alternate = {
            'direction': 'CALL', 'entry_line': channels['asc_ceil'],
            'entry_price': ac, 'stop_price': ac,
            'stop_desc': 'Re-enter channel from above',
            'tp1_price': hw, 'tp1_desc': 'HW Line',
            'tp2_price': hw + 5, 'tp2_desc': 'Beyond HW',
            'timing': 'ONLY if price breaks and CLOSES above ceiling',
            'confidence': 'LOW — counter to primary, only on breakout close',
        }
    
    elif p > dc and p < af:
        # SCENARIO 1: Between channels (most common)
        scenario = {
            'number': 1, 'name': 'BETWEEN CHANNELS',
            'desc': f'Price {p:.2f} between ascending floor ({af:.2f}) and descending ceiling ({dc:.2f}). Wait for price to reach a channel.',
            'color': '#00d4ff', 'class': 'neutral',
        }
        primary = {
            'direction': 'PUT', 'entry_line': channels['asc_floor'],
            'entry_price': af, 'stop_price': ac,
            'stop_desc': f'Asc Ceiling at {ac:.2f}',
            'tp1_line': channels['desc_ceil'], 'tp1_price': dc, 'tp1_desc': 'Desc Ceiling',
            'tp2_line': channels['desc_floor'], 'tp2_price': df, 'tp2_desc': 'Desc Floor',
            'timing': 'When price rises to ascending channel floor',
            'confidence': 'HIGH — clean rejection setup',
        }
        alternate = {
            'direction': 'CALL', 'entry_line': channels['desc_ceil'],
            'entry_price': dc, 'stop_price': df,
            'stop_desc': f'Desc Floor at {df:.2f}',
            'tp1_price': af, 'tp1_desc': 'Asc Floor',
            'tp2_price': ac, 'tp2_desc': 'Asc Ceiling',
            'timing': 'When price drops to descending channel ceiling',
            'confidence': 'HIGH — clean bounce setup',
        }
    
    elif p >= df and p <= dc:
        # SCENARIO 3: Inside descending channel
        scenario = {
            'number': 3, 'name': 'INSIDE DESCENDING CHANNEL',
            'desc': f'Price {p:.2f} is INSIDE the descending channel ({df:.2f} floor — {dc:.2f} ceiling). In the support zone. Watch for bounce.',
            'color': '#00e676', 'class': 'bull',
        }
        primary = {
            'direction': 'CALL', 'entry_line': channels['desc_floor'],
            'entry_price': df, 'stop_price': lw,
            'stop_desc': f'LW line at {lw:.2f}',
            'tp1_line': channels['asc_floor'], 'tp1_price': af, 'tp1_desc': 'Asc Floor',
            'tp2_line': channels['asc_ceil'], 'tp2_price': ac, 'tp2_desc': 'Asc Ceiling',
            'timing': 'Enter on bounce from floor, or if 8:30 already confirmed',
            'confidence': 'HIGH — already inside support zone',
        }
        alternate = {
            'direction': 'PUT', 'entry_line': channels['desc_floor'],
            'entry_price': df, 'stop_price': df,
            'stop_desc': 'Re-enter channel from below',
            'tp1_price': lw, 'tp1_desc': 'LW Line',
            'tp2_price': lw - 5, 'tp2_desc': 'Beyond LW',
            'timing': 'ONLY if price breaks and CLOSES below floor',
            'confidence': 'LOW — counter to primary, only on breakdown close',
        }
    
    elif p < df and p > lw:
        # SCENARIO 5: Below descending channel, above LW
        scenario = {
            'number': 5, 'name': 'BELOW DESCENDING CHANNEL',
            'desc': f'Price {p:.2f} below descending floor ({df:.2f}). Channel above is now resistance. LW line ({lw:.2f}) is support below.',
            'color': '#ff9100', 'class': 'neutral',
        }
        primary = {
            'direction': 'CALL', 'entry_line': channels['lw_line'],
            'entry_price': lw, 'stop_price': lw - 3,
            'stop_desc': '3pt below LW line',
            'tp1_line': channels['desc_floor'], 'tp1_price': df, 'tp1_desc': 'Desc Floor',
            'tp2_line': channels['desc_ceil'], 'tp2_price': dc, 'tp2_desc': 'Desc Ceiling',
            'timing': 'Wait for price to reach LW line',
            'confidence': 'MEDIUM — LW is last support',
        }
        alternate = {
            'direction': 'PUT', 'entry_line': channels['desc_floor'],
            'entry_price': df, 'stop_price': dc,
            'stop_desc': 'Above Desc Ceiling',
            'tp1_price': lw, 'tp1_desc': 'LW Line',
            'tp2_price': lw - 5, 'tp2_desc': 'Beyond LW',
            'timing': 'If price bounces back to descending floor and rejects',
            'confidence': 'MEDIUM — channel becomes resistance',
        }
    
    else:
        # SCENARIO 6b: Below lowest wick — extreme gap down
        scenario = {
            'number': 6, 'name': 'EXTREME GAP DOWN',
            'desc': f'Price {p:.2f} is BELOW lowest wick line ({lw:.2f}). No structural support below. Dangerous to trade.',
            'color': '#ffd740', 'class': 'neutral',
        }
        primary = {
            'direction': 'CALL', 'entry_line': channels['lw_line'],
            'entry_price': lw, 'stop_price': lw - 5,
            'stop_desc': '5pt below LW line (no structure)',
            'tp1_line': channels['desc_floor'], 'tp1_price': df, 'tp1_desc': 'Desc Floor',
            'tp2_line': channels['desc_ceil'], 'tp2_price': dc, 'tp2_desc': 'Desc Ceiling',
            'timing': 'If price returns to LW line and bounces',
            'confidence': 'LOW — trading against momentum in a gap',
        }
    
    # Calculate strikes (20pt OTM from entry line)
    if primary:
        if primary['direction'] == 'PUT':
            primary['strike'] = int((primary['entry_price'] - 20) // 5) * 5
        else:
            primary['strike'] = int((primary['entry_price'] + 20 + 4) // 5) * 5
    
    if alternate:
        if alternate['direction'] == 'PUT':
            alternate['strike'] = int((alternate['entry_price'] - 20) // 5) * 5
        else:
            alternate['strike'] = int((alternate['entry_price'] + 20 + 4) // 5) * 5
    
    # Apply 8:30 confirmation to timing
    if confirmation_830 and primary:
        if confirmation_830.get('passed') is True:
            primary['timing'] = '9:05 AM — 8:30 confirmed rejection. Enter immediately.'
        elif confirmation_830.get('passed') is False:
            primary['timing'] = 'WAIT — 8:30 test failed. Wait for 9:00 or 9:30 candle to retest.'
    
    # ============================================================
    # RISK FILTERS & POSITION SIZING
    # ============================================================
    warnings = []
    
    # Channel width check (sweet spot 5-12 pts)
    asc_w = channels.get('asc_width', 0)
    desc_w = channels.get('desc_width', 0)
    if primary:
        relevant_width = asc_w if primary['direction'] == 'PUT' else desc_w
        if relevant_width < 3:
            warnings.append(f"⚠️ Channel width only {relevant_width:.1f}pt — stop is very tight, high chop risk")
        elif relevant_width > 15:
            warnings.append(f"⚠️ Channel width {relevant_width:.1f}pt — very wide, slow premium move on stop")
    
    # Gap distance check (entry too far = theta kills you before price arrives)
    if primary:
        gap_to_entry = abs(current_price - primary['entry_price'])
        if gap_to_entry > 10:
            warnings.append(f"⚠️ Price is {gap_to_entry:.1f}pt from entry — may take too long for 0DTE")
        elif gap_to_entry < 1:
            warnings.append(f"✅ Price is {gap_to_entry:.1f}pt from entry — right at the level")
    
    # Confidence-based contract sizing
    # HIGH = 3 contracts, MEDIUM = 2, LOW = 1
    if primary:
        conf = primary.get('confidence', '')
        if 'HIGH' in conf:
            primary['contracts'] = 3
        elif 'MEDIUM' in conf:
            primary['contracts'] = 2
        else:
            primary['contracts'] = 1
    
    if alternate:
        alternate['contracts'] = 1  # alternates always 1 contract
    
    return {
        'scenario': scenario,
        'primary': primary,
        'alternate': alternate,
        'warnings': warnings,
    }


# ============================================================
# PROP FIRM RISK CALCULATOR
# ============================================================

def calculate_prop_firm_risk(daily_limit: float, stop_points: float, 
                             instrument: str = 'ES') -> dict:
    """Calculate position sizing for prop firm accounts."""
    point_value = 50.0 if instrument == 'ES' else 5.0  # ES=$50/pt, MES=$5/pt
    risk_per_trade = daily_limit * 0.40  # 40% of daily limit
    
    contracts = int(risk_per_trade / (stop_points * point_value))
    actual_risk = contracts * stop_points * point_value
    
    profit_5pt = contracts * 5 * point_value
    profit_10pt = contracts * 10 * point_value
    
    return {
        'contracts': contracts,
        'risk_per_trade': actual_risk,
        'max_trades': 2,
        'remaining_after_1_loss': daily_limit - actual_risk,
        'profit_5pt_move': profit_5pt,
        'profit_10pt_move': profit_10pt,
        'point_value': point_value,
        'instrument': instrument
    }


# ============================================================
# CONFLUENCE SCORE CALCULATOR
# ============================================================

def calculate_confluence(asian_aligns: bool, london_sweep: bool,
                        data_reaction: str, opening_drive: bool,
                        line_cluster: bool) -> dict:
    """Calculate the 5-factor confluence score."""
    score = 0
    factors = []
    
    if asian_aligns:
        score += 1
        factors.append("✅ Asian Session Aligned")
    else:
        factors.append("❌ Asian Session Misaligned")
    
    if london_sweep:
        score += 1
        factors.append("✅ London Sweep Confirmed")
    else:
        factors.append("❌ No London Sweep")
    
    if data_reaction == 'aligned':
        score += 1
        factors.append("✅ Data Reaction Aligned")
    elif data_reaction == 'absorbed':
        score += 0.5
        factors.append("⚡ Data Absorbed (Half Point)")
    else:
        factors.append("❌ Data Reaction Against")
    
    if opening_drive:
        score += 1
        factors.append("✅ Opening Drive Aligned")
    else:
        factors.append("❌ Opening Drive Against")
    
    if line_cluster:
        score += 1
        factors.append("✅ Line Cluster Confluence")
    else:
        factors.append("❌ No Line Cluster")
    
    if score >= 4:
        recommendation = "FULL SIZE — High confidence setup"
        size_pct = 100
        color = "high"
    elif score >= 3:
        recommendation = "STANDARD SIZE — Solid setup"
        size_pct = 75
        color = "high"
    elif score >= 2:
        recommendation = "HALF SIZE — Mixed context"
        size_pct = 50
        color = "med"
    else:
        recommendation = "NO TRADE — Insufficient confluence"
        size_pct = 0
        color = "low"
    
    return {
        'score': score,
        'factors': factors,
        'recommendation': recommendation,
        'size_pct': size_pct,
        'color': color
    }


def auto_detect_confluence(ny_trade_direction: str, ny_ladder: list,
                           current_price: float, candles_df=None,
                           es_offset: float = 0) -> dict:
    """
    Automatically detect all 5 confluence factors from available data.
    
    Args:
        ny_trade_direction: 'PUT' or 'CALL' from NY signal logic
        ny_ladder: list of ladder dicts with 'value', 'direction', 'short'
        current_price: SPX price at 9 AM
        candles_df: DataFrame of ES 30-min candles (if available)
        es_offset: ES-SPX spread for converting candle prices
    
    Returns:
        dict with all 5 boolean factors plus detail strings
    """
    results = {
        'asian_aligns': False, 'asian_detail': 'No candle data',
        'london_sweep': False, 'london_detail': 'No candle data',
        'data_reaction': 'absorbed', 'data_detail': 'No candle data (default: absorbed)',
        'opening_drive': False, 'opening_detail': 'No candle data',
        'line_cluster': False, 'cluster_detail': 'No cluster detected',
    }
    
    # ── Factor 5: Line Cluster (always available from ladder) ──
    if ny_ladder and len(ny_ladder) >= 3:
        values = sorted([l['value'] for l in ny_ladder])
        for i in range(len(values) - 2):
            if values[i+2] - values[i] <= 5.0:  # 3 lines within 5 points
                cluster_lines = [l for l in ny_ladder if values[i] <= l['value'] <= values[i+2]]
                cluster_names = ', '.join([l['short'] for l in cluster_lines[:3]])
                results['line_cluster'] = True
                results['cluster_detail'] = f"3 lines within {values[i+2]-values[i]:.1f}pt ({cluster_names})"
                break
    
    if candles_df is None or len(candles_df) == 0:
        return results
    
    try:
        df = candles_df.copy()
        # Normalize column names (yfinance returns lowercase)
        norm_map = {}
        for col in df.columns:
            cl = col.lower().strip()
            if cl == 'datetime':
                norm_map[col] = 'Datetime'
            elif cl == 'open':
                norm_map[col] = 'Open'
            elif cl == 'high':
                norm_map[col] = 'High'
            elif cl == 'low':
                norm_map[col] = 'Low'
            elif cl == 'close':
                norm_map[col] = 'Close'
        df = df.rename(columns=norm_map)
        
        # Ensure datetime index
        if 'Datetime' in df.columns:
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df = df.set_index('Datetime')
        elif not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # Convert ES to SPX terms
        if es_offset != 0:
            for col in ['Open', 'High', 'Low', 'Close']:
                if col in df.columns:
                    df[col] = df[col] - es_offset
        
        # Get session candles by hour (CT timezone)
        # Asian: 5:00 PM - 2:00 AM CT (previous day 17:00 to 02:00)
        # London: 2:00 AM - 8:30 AM CT
        # Pre-market data: 7:30-8:00 AM, 8:00-8:30 AM candles
        # Opening: 8:30-9:00 AM candle
        
        hours = df.index.hour
        minutes = df.index.minute
        time_decimal = hours + minutes / 60.0
        
        # Asian session: 17:00 - 02:00 CT
        asian_mask = (time_decimal >= 17.0) | (time_decimal < 2.0)
        asian_candles = df[asian_mask]
        
        # London session: 2:00 - 8:30 CT
        london_mask = (time_decimal >= 2.0) & (time_decimal < 8.5)
        london_candles = df[london_mask]
        
        # Data candle: 7:30-8:00 AM and 8:00-8:30 AM
        data_mask = (time_decimal >= 7.5) & (time_decimal < 8.5)
        data_candles = df[data_mask]
        
        # Opening drive: 8:30-9:00 AM candle
        open_mask = (time_decimal >= 8.5) & (time_decimal < 9.0)
        open_candles = df[open_mask]
        
        # ── Factor 1: Asian Session Aligned ──
        if len(asian_candles) >= 2:
            asian_open = asian_candles.iloc[0]['Open']
            asian_close = asian_candles.iloc[-1]['Close']
            asian_move = asian_close - asian_open
            
            if ny_trade_direction == 'PUT' and asian_move < -1.0:
                results['asian_aligns'] = True
                results['asian_detail'] = f"Asian sold off {asian_move:.1f}pt → aligns with PUT"
            elif ny_trade_direction == 'CALL' and asian_move > 1.0:
                results['asian_aligns'] = True
                results['asian_detail'] = f"Asian rallied +{asian_move:.1f}pt → aligns with CALL"
            elif abs(asian_move) <= 1.0:
                results['asian_detail'] = f"Asian flat ({asian_move:+.1f}pt) → no alignment"
            else:
                direction_word = "rallied" if asian_move > 0 else "sold off"
                results['asian_detail'] = f"Asian {direction_word} {asian_move:+.1f}pt → AGAINST {ny_trade_direction}"
        
        # ── Factor 2: London Sweep ──
        if len(asian_candles) >= 2 and len(london_candles) >= 2:
            asian_high = asian_candles['High'].max()
            asian_low = asian_candles['Low'].min()
            london_high = london_candles['High'].max()
            london_low = london_candles['Low'].min()
            london_close = london_candles.iloc[-1]['Close']
            
            SWEEP_MIN = 6.0    # Below ~6pts is NOT a sweep, NY will revisit
            SWEEP_MAX = 10.0   # Above ~10pts without retrace = extended push
            
            # Measure how far London extended beyond Asian range
            above_asian = london_high - asian_high if london_high > asian_high else 0
            below_asian = asian_low - london_low if london_low < asian_low else 0
            
            # Did London retrace back to Asian boundary?
            retraced_to_high = london_close < asian_high
            retraced_to_low = london_close > asian_low
            
            # ── SCENARIO 1: Too shallow (< 6pt) — NOT a sweep ──
            # London barely poked past. NY will likely come back to test this level again.
            shallow_high = above_asian > 0 and above_asian < SWEEP_MIN
            shallow_low = below_asian > 0 and below_asian < SWEEP_MIN
            
            # ── SCENARIO 2: Normal sweep (~6-10pt, retraced) ──
            # London pokes ~8pts past Asian boundary then comes back = liquidity grab
            normal_sweep_high = above_asian >= SWEEP_MIN and above_asian <= SWEEP_MAX and retraced_to_high
            normal_sweep_low = below_asian >= SWEEP_MIN and below_asian <= SWEEP_MAX and retraced_to_low
            
            # ── SCENARIO 3: Extended push (> 10pt OR no retrace after sweep-range push) ──
            # London goes big past Asian boundary and doesn't come back = real move
            # Asian boundary becomes springboard for NY continuation
            extended_push_high = above_asian > SWEEP_MAX and not retraced_to_high
            extended_push_low = below_asian > SWEEP_MAX and not retraced_to_low
            
            if ny_trade_direction == 'PUT' and normal_sweep_high:
                results['london_sweep'] = True
                results['london_detail'] = f"London swept Asian high {asian_high:.0f}→{london_high:.0f} (+{above_asian:.0f}pt) then reversed ↓ (classic ~8pt sweep)"
            elif ny_trade_direction == 'CALL' and normal_sweep_low:
                results['london_sweep'] = True
                results['london_detail'] = f"London swept Asian low {asian_low:.0f}→{london_low:.0f} (-{below_asian:.0f}pt) then reversed ↑ (classic ~8pt sweep)"
            elif ny_trade_direction == 'CALL' and extended_push_high:
                results['london_sweep'] = True
                results['london_detail'] = f"London extended +{above_asian:.0f}pt above Asian high {asian_high:.0f} without retrace → SPRINGBOARD. Asian high = support for continuation ↑"
            elif ny_trade_direction == 'PUT' and extended_push_low:
                results['london_sweep'] = True
                results['london_detail'] = f"London extended -{below_asian:.0f}pt below Asian low {asian_low:.0f} without retrace → SPRINGBOARD. Asian low = resistance for continuation ↓"
            elif extended_push_high or extended_push_low:
                direction = "higher" if extended_push_high else "lower"
                results['london_detail'] = f"London extended {direction} (springboard) but AGAINST {ny_trade_direction} direction"
            elif normal_sweep_high or normal_sweep_low:
                results['london_detail'] = f"Sweep detected but against {ny_trade_direction} direction"
            elif shallow_high:
                results['london_detail'] = f"London only poked +{above_asian:.0f}pt above Asian high {asian_high:.0f} (< 6pt = not a sweep). NY will likely revisit this level."
            elif shallow_low:
                results['london_detail'] = f"London only poked -{below_asian:.0f}pt below Asian low {asian_low:.0f} (< 6pt = not a sweep). NY will likely revisit this level."
            else:
                results['london_detail'] = f"No London sweep — London stayed within Asian range (H:{asian_high:.0f} L:{asian_low:.0f}). ⚠️ NY will likely poke Asian highs/lows before the real move. Watch for a fake breakout first."
        
        # ── Factor 3: Data Reaction (7:30-8:30 AM) ──
        if len(data_candles) >= 1:
            data_open = data_candles.iloc[0]['Open']
            data_high = data_candles['High'].max()
            data_low = data_candles['Low'].min()
            data_close = data_candles.iloc[-1]['Close']
            data_range = data_high - data_low
            data_move = data_close - data_open
            
            # Check if there was a significant spike (> 3pt range = data release)
            if data_range > 3.0:
                if ny_trade_direction == 'PUT' and data_move < -1.0:
                    results['data_reaction'] = 'aligned'
                    results['data_detail'] = f"Data drop {data_move:+.1f}pt → aligns with PUT"
                elif ny_trade_direction == 'CALL' and data_move > 1.0:
                    results['data_reaction'] = 'aligned'
                    results['data_detail'] = f"Data rally {data_move:+.1f}pt → aligns with CALL"
                elif abs(data_move) <= 1.0 and data_range > 3.0:
                    results['data_reaction'] = 'absorbed'
                    results['data_detail'] = f"Data spike absorbed ({data_range:.1f}pt range, net {data_move:+.1f}pt)"
                else:
                    results['data_reaction'] = 'against'
                    results['data_detail'] = f"Data moved against ({data_move:+.1f}pt vs {ny_trade_direction})"
            else:
                results['data_reaction'] = 'absorbed'
                results['data_detail'] = f"Quiet pre-market ({data_range:.1f}pt range) → neutral"
        
        # ── Factor 4: Opening Drive (8:30-9:00 AM) ──
        if len(open_candles) >= 1:
            open_o = open_candles.iloc[0]['Open']
            open_c = open_candles.iloc[-1]['Close']
            open_move = open_c - open_o
            
            if ny_trade_direction == 'PUT' and open_move < -0.5:
                results['opening_drive'] = True
                results['opening_detail'] = f"Opening drive down {open_move:+.1f}pt → aligns with PUT"
            elif ny_trade_direction == 'CALL' and open_move > 0.5:
                results['opening_drive'] = True
                results['opening_detail'] = f"Opening drive up {open_move:+.1f}pt → aligns with CALL"
            else:
                direction_word = "up" if open_move > 0 else "down" if open_move < 0 else "flat"
                results['opening_drive'] = False
                results['opening_detail'] = f"Opening drive {direction_word} {open_move:+.1f}pt → AGAINST {ny_trade_direction}"
        
    except Exception as e:
        results['asian_detail'] = f"Auto-detect error: {str(e)[:50]}"
    
    return results


# ============================================================
# SESSION TIME ZONES (all in CT)
# ============================================================

SESSION_TIMES = {
    'Sydney': {'start': time(15, 0), 'end': time(0, 0), 'color': 'rgba(255,152,0,0.08)', 'border': 'rgba(255,152,0,0.3)'},
    'Tokyo': {'start': time(19, 0), 'end': time(2, 0), 'color': 'rgba(76,175,80,0.08)', 'border': 'rgba(76,175,80,0.3)'},
    'London': {'start': time(2, 0), 'end': time(8, 30), 'color': 'rgba(33,150,243,0.08)', 'border': 'rgba(33,150,243,0.3)'},
    'New York': {'start': time(8, 30), 'end': time(15, 0), 'color': 'rgba(156,39,176,0.08)', 'border': 'rgba(156,39,176,0.3)'},
}


# ============================================================
# DATA SOURCE MODULE
# yfinance (primary for historical) → Tastytrade SDK (live streaming)
# ============================================================

class DataSourceStatus:
    """Track data source status for display"""
    def __init__(self):
        self.tastytrade_ok = False
        self.yfinance_ok = False
        self.source_used = "manual"
        self.error_msg = ""
        self.candles = None  # DataFrame with OHLC 30-min candles


def fetch_yfinance_candles(start_date: str, end_date: str) -> dict:
    """
    Fetch ES futures 30-min candles from Yahoo Finance.
    ES=F gives the full 23-hour session including overnight.
    """
    try:
        import yfinance as yf
        es = yf.Ticker("ES=F")
        df = es.history(start=start_date, end=end_date, interval="30m")
        if len(df) > 0:
            df = df.reset_index()
            # Normalize column names
            col_map = {}
            for col in df.columns:
                cl = col.lower().replace(' ', '_')
                if 'datetime' in cl or 'date' in cl:
                    col_map[col] = 'datetime'
                elif cl == 'open':
                    col_map[col] = 'open'
                elif cl == 'high':
                    col_map[col] = 'high'
                elif cl == 'low':
                    col_map[col] = 'low'
                elif cl == 'close':
                    col_map[col] = 'close'
                elif cl == 'volume':
                    col_map[col] = 'volume'
            df = df.rename(columns=col_map)
            if 'datetime' not in df.columns:
                df = df.rename(columns={df.columns[0]: 'datetime'})
            df['datetime'] = pd.to_datetime(df['datetime'])
            # Convert to CT if timezone-aware
            if df['datetime'].dt.tz is not None:
                import pytz
                ct = pytz.timezone('America/Chicago')
                df['datetime'] = df['datetime'].dt.tz_convert(ct).dt.tz_localize(None)
            df = df.sort_values('datetime').reset_index(drop=True)
            return {'ok': True, 'data': df}
        return {'ok': False, 'error': 'No data returned from Yahoo Finance'}
    except ImportError:
        return {'ok': False, 'error': 'yfinance not installed (add to requirements.txt)'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def fetch_tastytrade_candles_via_sdk(start_dt: datetime, end_dt: datetime) -> dict:
    """
    Fetch historical candles via Tastytrade SDK + DXLink streamer.
    Uses Candle event with symbol '/ES{=30m}' and from_time parameter.
    Requires tastytrade SDK with async support.
    """
    try:
        from tastytrade import Session, DXLinkStreamer
        from tastytrade.dxfeed import Candle
        import asyncio
        
        tt = st.secrets.get("tastytrade", {})
        client_secret = tt.get("client_secret")
        refresh_token = tt.get("refresh_token")
        
        if not client_secret or not refresh_token:
            return {'ok': False, 'error': 'Missing tastytrade secrets'}
        
        async def _fetch():
            session = Session(client_secret, refresh_token)
            candles = []
            from_time_ms = int(start_dt.timestamp() * 1000)
            
            async with DXLinkStreamer(session) as streamer:
                # Subscribe to 30-min ES candles from start_dt
                symbol = '/ES{=30m}'
                await streamer.subscribe_candle(symbol, from_time_ms)
                
                # Collect candles until we have enough or timeout
                import asyncio as aio
                try:
                    while True:
                        candle = await aio.wait_for(streamer.get_event(Candle), timeout=10)
                        candles.append({
                            'datetime': datetime.fromtimestamp(candle.time / 1000),
                            'open': float(candle.open),
                            'high': float(candle.high),
                            'low': float(candle.low),
                            'close': float(candle.close),
                            'volume': float(candle.volume) if candle.volume else 0,
                        })
                except aio.TimeoutError:
                    pass  # Done collecting
            
            return candles
        
        # Run async in sync context
        loop = asyncio.new_event_loop()
        candles = loop.run_until_complete(_fetch())
        loop.close()
        
        if candles:
            df = pd.DataFrame(candles)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.sort_values('datetime').reset_index(drop=True)
            # Filter to date range
            df = df[(df['datetime'] >= start_dt) & (df['datetime'] <= end_dt)]
            if len(df) > 0:
                return {'ok': True, 'data': df}
        return {'ok': False, 'error': 'No candle data received from DXLink'}
    except ImportError:
        return {'ok': False, 'error': 'tastytrade SDK not installed'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def fetch_es_candles(prior_date, next_date) -> DataSourceStatus:
    """
    Master fetcher: tries yfinance first (reliable for historical),
    then Tastytrade SDK, reports status clearly.
    """
    status = DataSourceStatus()
    
    start_str = prior_date.strftime('%Y-%m-%d')
    end_str = (next_date + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Try yfinance first (most reliable for historical 30-min candles)
    result = fetch_yfinance_candles(start_str, end_str)
    if result['ok']:
        status.yfinance_ok = True
        status.source_used = "yfinance"
        status.candles = result['data']
        return status
    
    yf_error = result['error']
    
    # Fallback: try Tastytrade SDK
    start_dt = datetime.combine(prior_date, time(8, 30))
    end_dt = datetime.combine(next_date, time(15, 0))
    result = fetch_tastytrade_candles_via_sdk(start_dt, end_dt)
    if result['ok']:
        status.tastytrade_ok = True
        status.source_used = "tastytrade"
        status.candles = result['data']
        return status
    
    tt_error = result['error']
    status.error_msg = f"yfinance: {yf_error} | Tastytrade: {tt_error}"
    status.source_used = "manual"
    return status


def calculate_es_spx_spread(es_candles: pd.DataFrame, session_date) -> dict:
    """
    Calculate the ES - SPX spread by comparing ES futures to SPX index
    during overlapping RTH hours. Returns the last spread value.
    """
    try:
        import yfinance as yf
        
        start_str = session_date.strftime('%Y-%m-%d')
        end_str = (session_date + timedelta(days=1)).strftime('%Y-%m-%d')
        
        spx = yf.Ticker("^GSPC")
        spx_df = spx.history(start=start_str, end=end_str, interval="30m")
        
        if len(spx_df) == 0:
            return {'ok': False, 'error': 'No SPX data', 'spread': 0.0}
        
        spx_df = spx_df.reset_index()
        col_map = {}
        for col in spx_df.columns:
            cl = col.lower().replace(' ', '_')
            if 'datetime' in cl or 'date' in cl:
                col_map[col] = 'datetime'
            elif cl == 'close':
                col_map[col] = 'close'
        spx_df = spx_df.rename(columns=col_map)
        if 'datetime' not in spx_df.columns:
            spx_df = spx_df.rename(columns={spx_df.columns[0]: 'datetime'})
        spx_df['datetime'] = pd.to_datetime(spx_df['datetime'])
        if spx_df['datetime'].dt.tz is not None:
            import pytz
            ct = pytz.timezone('America/Chicago')
            spx_df['datetime'] = spx_df['datetime'].dt.tz_convert(ct).dt.tz_localize(None)
        
        # Round both to nearest 30 min for matching
        es_rth = es_candles.copy()
        es_rth['dt_round'] = es_rth['datetime'].dt.round('30min')
        spx_df['dt_round'] = spx_df['datetime'].dt.round('30min')
        
        merged = es_rth.merge(spx_df[['dt_round', 'close']], on='dt_round', 
                               suffixes=('_es', '_spx'), how='inner')
        
        if len(merged) == 0:
            return {'ok': False, 'error': 'No overlapping candles', 'spread': 0.0}
        
        if 'close_es' in merged.columns and 'close_spx' in merged.columns:
            spreads = merged['close_es'] - merged['close_spx']
        else:
            return {'ok': False, 'error': 'Column merge issue', 'spread': 0.0}
        
        return {
            'ok': True, 
            'spread': round(float(spreads.iloc[-1]), 2),
            'avg_spread': round(float(spreads.mean()), 2),
            'samples': len(merged)
        }
    except ImportError:
        return {'ok': False, 'error': 'yfinance not installed', 'spread': 0.0}
    except Exception as e:
        return {'ok': False, 'error': str(e), 'spread': 0.0}


def apply_offset(items: list, offset: float) -> list:
    """Subtract offset from prices (ES → SPX conversion)."""
    return [{'price': item['price'] - offset, 'time': item['time']} for item in items]


def fetch_live_price() -> dict:
    """Fetch current ES=F price from yfinance for live tracking."""
    try:
        import yfinance as yf
        es = yf.Ticker("ES=F")
        data = es.history(period="1d", interval="1m")
        if len(data) > 0:
            last = data.iloc[-1]
            last_time = data.index[-1]
            if hasattr(last_time, 'tz') and last_time.tz is not None:
                import pytz
                ct = pytz.timezone('America/Chicago')
                last_time = last_time.tz_convert(ct).tz_localize(None)
            return {
                'ok': True,
                'price': float(last['Close']),
                'high': float(last['High']),
                'low': float(last['Low']),
                'time': last_time,
                'source': 'ES=F'
            }
        return {'ok': False, 'error': 'No data', 'price': 0}
    except Exception as e:
        return {'ok': False, 'error': str(e), 'price': 0}


def estimate_option_premium(spx_price: float, strike: float, vix: float,
                             hours_to_expiry: float, opt_type: str) -> float:
    """
    Estimate 0DTE SPX option premium using Black-Scholes with 0DTE adjustment.
    
    Real 0DTE options trade at a discount to theoretical BS because:
    - Realized vol is lower than implied for short timeframes
    - Bid-ask spread compresses theoretical value
    - Market makers discount extreme gamma risk
    
    We apply a 0.35x discount factor to align with typical 0DTE market prices.
    """
    import math
    
    if hours_to_expiry <= 0:
        if opt_type == 'CALL':
            return max(0, spx_price - strike)
        else:
            return max(0, strike - spx_price)
    
    T = hours_to_expiry / (252 * 6.5)  # fraction of trading year
    sigma = vix / 100.0  # annualized vol
    
    if T <= 0 or sigma <= 0:
        return 0.25
    
    def norm_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    vol_t = sigma * math.sqrt(T)
    
    # Standard Black-Scholes
    d1 = (math.log(spx_price / strike)) / vol_t + 0.5 * vol_t
    d2 = d1 - vol_t
    
    if opt_type == 'CALL':
        premium = spx_price * norm_cdf(d1) - strike * norm_cdf(d2)
    else:
        premium = strike * norm_cdf(-d2) - spx_price * norm_cdf(-d1)
    
    # 0DTE discount: real market trades at ~35% of theoretical BS for OTM options
    # This narrows as options go ITM (intrinsic value dominates)
    intrinsic = max(0, (strike - spx_price) if opt_type == 'PUT' else (spx_price - strike))
    extrinsic = max(0, premium - intrinsic)
    adjusted = intrinsic + extrinsic * 0.35
    
    return max(0.25, round(adjusted * 4) / 4)  # min $0.25, round to nearest 0.25


def project_premium_at_scenarios(current_spx: float, strike: float, vix: float,
                                  opt_type: str, stop_price: float,
                                  tp1_price: float, tp2_price: float,
                                  base_premium: float = None,
                                  current_hours: float = 6.5,
                                  entry_hours: float = 5.9) -> dict:
    """
    Project option premium at 9:05 AM entry under three scenarios using actual trade levels.
    
    If base_premium (live 8:30 AM price) is available, calibrates the model to match it,
    then projects forward. Otherwise uses pure estimation.
    
    Args:
        current_spx: SPX price right now
        strike: Option strike
        vix: Current VIX
        opt_type: 'CALL' or 'PUT'
        stop_price: SPX stop loss level
        tp1_price: SPX Target 1 level
        tp2_price: SPX Target 2 level  
        base_premium: Live premium pulled at 8:30 AM (None if unavailable)
        current_hours: Hours to expiry at time of live pull (default 6.5 = 8:30 AM)
        entry_hours: Hours to expiry at 9:05 AM entry (default 5.9)
    
    Returns:
        Dict with scenario projections
    """
    # Estimate premiums at different SPX levels at entry time
    est_at_entry = estimate_option_premium(current_spx, strike, vix, entry_hours, opt_type)
    est_at_stop = estimate_option_premium(stop_price, strike, vix, entry_hours, opt_type)
    est_at_tp1 = estimate_option_premium(tp1_price, strike, vix, entry_hours, opt_type)
    est_at_tp2 = estimate_option_premium(tp2_price, strike, vix, entry_hours, opt_type)
    
    # If we have a live base premium, calibrate with a scaling factor
    if base_premium and base_premium > 0:
        est_now = estimate_option_premium(current_spx, strike, vix, current_hours, opt_type)
        if est_now > 0:
            calibration = base_premium / est_now
        else:
            calibration = 1.0
        
        est_at_entry = round(est_at_entry * calibration * 4) / 4
        est_at_stop = round(est_at_stop * calibration * 4) / 4
        est_at_tp1 = round(est_at_tp1 * calibration * 4) / 4
        est_at_tp2 = round(est_at_tp2 * calibration * 4) / 4
    
    return {
        'at_entry': max(0.25, est_at_entry),
        'at_stop': max(0.25, est_at_stop),
        'at_tp1': max(0.25, est_at_tp1),
        'at_tp2': max(0.25, est_at_tp2),
        'calibrated': base_premium is not None and base_premium > 0,
    }


# ============================================================
# AUTO-DETECTION ENGINE
# Detect bounces, rejections, and wick extremes from candle data
# ============================================================

def filter_ny_session(df: pd.DataFrame, session_date) -> pd.DataFrame:
    """
    Filter candles to only the NY regular session: 8:30 AM - 3:00 PM CT.
    Uses a flexible window to catch candles even if timestamps are slightly off.
    """
    session_start = datetime.combine(session_date, time(8, 0))   # slightly early to catch 8:30
    session_end = datetime.combine(session_date, time(15, 30))    # slightly late to catch 3:00
    
    mask = (df['datetime'] >= session_start) & (df['datetime'] <= session_end)
    filtered = df[mask].copy().reset_index(drop=True)
    return filtered


def detect_inflections(ny_candles: pd.DataFrame) -> dict:
    """
    Auto-detect bounces and rejections from 30-min candle data.
    
    Uses LINE CHART logic: closing prices only for bounces/rejections.
    
    Bounce = trough: close[i] <= close[i-1] AND close[i] < close[i+1]
      OR close[i] < close[i-1] AND close[i] <= close[i+1]
      (handles flat bottoms)
    
    Rejection = peak: close[i] >= close[i-1] AND close[i] > close[i+1]
      OR close[i] > close[i-1] AND close[i] >= close[i+1]
      (handles flat tops)
    
    For multi-candle patterns (W-bottoms, M-tops), uses a 5-candle window:
      If close[i] is the lowest/highest within a 5-candle window centered on it,
      it's also detected as a bounce/rejection.
    
    Highest Wick = highest HIGH of a BEARISH candle (close < open)
      - Exclude the 8:30 AM candle (opening noise)
    
    Lowest Wick = lowest LOW of a BULLISH candle (close > open)
      - Exclude the 8:30 AM candle (opening noise)
    """
    if len(ny_candles) < 3:
        return {'bounces': [], 'rejections': [], 'highest_wick': None, 'lowest_wick': None}
    
    closes = ny_candles['close'].values
    times = ny_candles['datetime'].values
    opens = ny_candles['open'].values
    highs = ny_candles['high'].values
    lows = ny_candles['low'].values
    n = len(closes)
    
    bounces = []
    rejections = []
    bounce_times = set()
    rejection_times = set()
    
    # Pass 1: Standard 3-candle pattern (with <= to catch flat edges)
    for i in range(1, n - 1):
        t = pd.Timestamp(times[i]).to_pydatetime()
        
        # Bounce: local trough
        is_bounce = (
            (closes[i] < closes[i-1] and closes[i] < closes[i+1]) or
            (closes[i] <= closes[i-1] and closes[i] < closes[i+1] and closes[i] < closes[max(0,i-2)] if i >= 2 else False) or
            (closes[i] < closes[i-1] and closes[i] <= closes[i+1] and closes[i] < closes[min(n-1,i+2)] if i < n-2 else False)
        )
        
        if is_bounce:
            bounces.append({'price': float(closes[i]), 'time': t})
            bounce_times.add(i)
        
        # Rejection: local peak
        is_rejection = (
            (closes[i] > closes[i-1] and closes[i] > closes[i+1]) or
            (closes[i] >= closes[i-1] and closes[i] > closes[i+1] and closes[i] > closes[max(0,i-2)] if i >= 2 else False) or
            (closes[i] > closes[i-1] and closes[i] >= closes[i+1] and closes[i] > closes[min(n-1,i+2)] if i < n-2 else False)
        )
        
        if is_rejection:
            rejections.append({'price': float(closes[i]), 'time': t})
            rejection_times.add(i)
    
    # Pass 2: 5-candle window for broader patterns (W-bottom, M-top)
    for i in range(2, n - 2):
        if i in bounce_times or i in rejection_times:
            continue
        
        t = pd.Timestamp(times[i]).to_pydatetime()
        window = closes[i-2:i+3]
        
        # Bounce: lowest in 5-candle window
        if closes[i] == window.min() and closes[i] < closes[i-2] and closes[i] < closes[i+2]:
            bounces.append({'price': float(closes[i]), 'time': t})
        
        # Rejection: highest in 5-candle window
        if closes[i] == window.max() and closes[i] > closes[i-2] and closes[i] > closes[i+2]:
            rejections.append({'price': float(closes[i]), 'time': t})
    
    # Sort by time
    bounces.sort(key=lambda x: x['time'])
    rejections.sort(key=lambda x: x['time'])
    
    # ============================================================
    # AFTERNOON CHANNEL PRIORITIZATION
    # ============================================================
    # The 12:00 PM CT to 3:00 PM CT channel is where institutional positioning settles
    # after morning noise and stop hunts clear out. These are the lines that 
    # produce real reactions the next day.
    #
    # Split into afternoon (primary) and morning (secondary):
    # - Afternoon bounces/rejections define the dominant channel
    # - Morning inflections are kept as secondary context
    
    noon_hour = 12  # 12:00 PM CT (candle data is in CT)
    
    afternoon_bounces = [b for b in bounces if b['time'].hour >= noon_hour]
    morning_bounces = [b for b in bounces if b['time'].hour < noon_hour]
    afternoon_rejections = [r for r in rejections if r['time'].hour >= noon_hour]
    morning_rejections = [r for r in rejections if r['time'].hour < noon_hour]
    
    # Tag each inflection with priority
    for b in afternoon_bounces:
        b['priority'] = 'primary'
        b['session'] = 'afternoon'
    for b in morning_bounces:
        b['priority'] = 'secondary'
        b['session'] = 'morning'
    for r in afternoon_rejections:
        r['priority'] = 'primary'
        r['session'] = 'afternoon'
    for r in morning_rejections:
        r['priority'] = 'secondary'
        r['session'] = 'morning'
    
    # Use afternoon channel as primary, fall back to full session if afternoon is empty
    if afternoon_bounces or afternoon_rejections:
        primary_bounces = afternoon_bounces
        primary_rejections = afternoon_rejections
    else:
        # No afternoon inflections detected — use all
        primary_bounces = bounces
        primary_rejections = rejections
        for b in primary_bounces:
            b['priority'] = 'primary'
        for r in primary_rejections:
            r['priority'] = 'primary'
    
    # Highest wick: highest HIGH of a BEARISH candle (close < open)
    # Only consider candles from 9:00 AM to 2:30 PM CT (exclude open/close noise)
    bearish_mask = closes < opens
    highest_wick = None
    if bearish_mask.any():
        best_high = -1
        best_idx = None
        for idx in range(n):
            if not bearish_mask[idx]:
                continue
            t = pd.Timestamp(times[idx]).to_pydatetime()
            # Skip opening noise (before 9:00 AM)
            if t.hour < 9:
                continue
            # Skip closing noise (2:30 PM and later)
            if t.hour >= 15 or (t.hour == 14 and t.minute >= 30):
                continue
            if highs[idx] > best_high:
                best_high = highs[idx]
                best_idx = idx
        
        if best_idx is not None:
            highest_wick = {
                'price': float(highs[best_idx]),
                'time': pd.Timestamp(times[best_idx]).to_pydatetime()
            }
    
    # Lowest wick: lowest LOW of a BULLISH candle (close > open)
    # Only consider candles from 9:00 AM to 2:30 PM CT (exclude open/close noise)
    bullish_mask = closes > opens
    lowest_wick = None
    if bullish_mask.any():
        best_low = float('inf')
        best_idx = None
        for idx in range(n):
            if not bullish_mask[idx]:
                continue
            t = pd.Timestamp(times[idx]).to_pydatetime()
            # Skip opening noise (before 9:00 AM)
            if t.hour < 9:
                continue
            # Skip closing noise (2:30 PM and later)
            if t.hour >= 15 or (t.hour == 14 and t.minute >= 30):
                continue
            if lows[idx] < best_low:
                best_low = lows[idx]
                best_idx = idx
        
        if best_idx is not None:
            lowest_wick = {
                'price': float(lows[best_idx]),
                'time': pd.Timestamp(times[best_idx]).to_pydatetime()
            }
    
    return {
        'bounces': primary_bounces,          # Primary (afternoon channel)
        'rejections': primary_rejections,     # Primary (afternoon channel)
        'all_bounces': bounces,               # Full session (morning + afternoon)
        'all_rejections': rejections,         # Full session (morning + afternoon)
        'morning_bounces': morning_bounces,   # Morning only (secondary)
        'morning_rejections': morning_rejections,
        'highest_wick': highest_wick,
        'lowest_wick': lowest_wick,
    }


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">SPX Prophet</div>
        <div class="app-sub">Structural Flow Engine • Futures & Options</div>
    </div>""", unsafe_allow_html=True)
    
    # Live price tracking toggle
    live_mode = st.toggle("🔴 LIVE MODE", value=False, help="Auto-refresh every 30 seconds with current ES price")
    
    # ============================================================
    # SIDEBAR: Input Panel
    # ============================================================
    with st.sidebar:
        render_section_banner("📊", "Prior NY Session Data", "Feed yesterday's chart data to build today's lines", "#8892b0")
        st.markdown("---")
        
        # Date selection
        prior_date = st.date_input("Prior NY Session Date", 
                                    value=datetime.now().date() - timedelta(days=1),
                                    help="The NY session day you're analyzing")
        
        next_date = st.date_input("Next Trading Day",
                                   value=datetime.now().date(),
                                   help="The day you're projecting lines into")
        
        st.markdown("---")
        
        # Data Source Selection
        st.markdown("### 📡 Data Source")
        data_mode = st.radio(
            "How to get ES data:",
            ["Auto (Tastytrade → yfinance)", "Manual Input"],
            index=0,
            help="Auto tries Tastytrade first, then Yahoo Finance. Manual lets you enter values from TradingView."
        )
        
        # Initialize variables
        bounces = []
        rejections = []
        highest_wick = {'price': 6920.0, 'time': datetime.combine(prior_date, time(10, 0))}
        lowest_wick = {'price': 6840.0, 'time': datetime.combine(prior_date, time(14, 0))}
        data_status = DataSourceStatus()
        
        if data_mode == "Auto (Tastytrade → yfinance)":
            st.caption("📡 Tries yfinance (ES=F) first, then Tastytrade SDK")
            
            fetch_btn = st.button("🔄 Fetch ES Data", use_container_width=True)
            
            # Status display
            if fetch_btn or st.session_state.get('last_fetch_status'):
                if fetch_btn:
                    with st.spinner("Fetching ES candle data..."):
                        data_status = fetch_es_candles(prior_date, next_date)
                        st.session_state['last_fetch_status'] = data_status
                        st.session_state['last_fetch_candles'] = data_status.candles
                else:
                    data_status = st.session_state.get('last_fetch_status', DataSourceStatus())
                
                # Show connection status
                if data_status.source_used == "yfinance":
                    st.success("✅ **Yahoo Finance (ES=F)** — Connected")
                elif data_status.source_used == "tastytrade":
                    st.success("✅ **Tastytrade DXLink** — Connected")
                else:
                    st.error("❌ **No data source available**")
                    if data_status.error_msg:
                        st.caption(data_status.error_msg)
                    st.info("Falling back to manual input below.")
                
                # If we got candle data, run auto-detection
                if data_status.candles is not None and len(data_status.candles) > 0:
                    ny_candles = filter_ny_session(data_status.candles, prior_date)
                    
                    if len(ny_candles) >= 3:
                        detected = detect_inflections(ny_candles)
                        
                        # Debug: show raw candle data
                        with st.expander(f"🔬 Raw NY Candles ({len(ny_candles)} bars)", expanded=False):
                            debug_df = ny_candles[['datetime', 'open', 'high', 'low', 'close']].copy()
                            debug_df['datetime'] = debug_df['datetime'].dt.strftime('%I:%M %p')
                            debug_df = debug_df.rename(columns={'datetime': 'Time'})
                            for col in ['open', 'high', 'low', 'close']:
                                debug_df[col] = debug_df[col].map(lambda x: f"{x:.2f}")
                            st.dataframe(debug_df, use_container_width=True, hide_index=True)
                        
                        # Calculate ES-SPX spread
                        st.markdown("---")
                        st.markdown("### 📐 ES → SPX Offset")
                        
                        spread_result = calculate_es_spx_spread(data_status.candles, prior_date)
                        
                        if spread_result['ok']:
                            auto_spread = spread_result['spread']
                            st.caption(f"Auto-detected ES-SPX spread: **{auto_spread:+.2f}** (from {spread_result['samples']} matched candles)")
                            # Store for the Settings section to pick up as default
                            if '_es_offset' not in st.session_state or st.session_state.get('_auto_spread_fresh', False):
                                st.session_state['_es_offset'] = auto_spread
                                st.session_state['_auto_spread_fresh'] = False
                        else:
                            st.caption(f"Could not auto-detect spread: {spread_result['error']}")
                        
                        # Use the global offset from Settings
                        es_offset = st.session_state.get('_es_offset', 0.0)
                        
                        # Apply offset to detected values
                        if es_offset != 0:
                            if detected['bounces']:
                                detected['bounces'] = apply_offset(detected['bounces'], es_offset)
                            if detected['rejections']:
                                detected['rejections'] = apply_offset(detected['rejections'], es_offset)
                            if detected.get('morning_bounces'):
                                detected['morning_bounces'] = apply_offset(detected['morning_bounces'], es_offset)
                            if detected.get('morning_rejections'):
                                detected['morning_rejections'] = apply_offset(detected['morning_rejections'], es_offset)
                            if detected['highest_wick']:
                                detected['highest_wick']['price'] -= es_offset
                            if detected['lowest_wick']:
                                detected['lowest_wick']['price'] -= es_offset
                            st.caption(f"✅ Offset of {es_offset:+.2f} applied to all levels")
                        
                        st.markdown("---")
                        st.markdown("### 🎯 Afternoon Channel (12–3 PM CT)" if es_offset == 0 else "### 🎯 Afternoon Channel (SPX-adjusted)")
                        st.caption("Primary lines — where price settled after morning noise")
                        
                        # Primary bounces (afternoon)
                        if detected['bounces']:
                            st.markdown(f"**Bounces: {len(detected['bounces'])}**")
                            for b in detected['bounces']:
                                tag = "🟢" if b.get('priority') == 'primary' else "⚪"
                                st.caption(f"{tag} ↗ {b['price']:.2f} @ {b['time'].strftime('%I:%M %p')}")
                            bounces = detected['bounces']
                        else:
                            st.caption("No afternoon bounces detected")
                        
                        # Primary rejections (afternoon)
                        if detected['rejections']:
                            st.markdown(f"**Rejections: {len(detected['rejections'])}**")
                            for r in detected['rejections']:
                                tag = "🟢" if r.get('priority') == 'primary' else "⚪"
                                st.caption(f"{tag} ↘ {r['price']:.2f} @ {r['time'].strftime('%I:%M %p')}")
                            rejections = detected['rejections']
                        else:
                            st.caption("No afternoon rejections detected")
                        
                        # Show morning lines as secondary (collapsed)
                        morning_b = detected.get('morning_bounces', [])
                        morning_r = detected.get('morning_rejections', [])
                        if morning_b or morning_r:
                            with st.expander(f"🌅 Morning Lines ({len(morning_b)}B / {len(morning_r)}R) — secondary", expanded=False):
                                st.caption("Pre-noon inflections. Lower priority for next-day projections.")
                                for b in morning_b:
                                    st.caption(f"⚪ ↗ {b['price']:.2f} @ {b['time'].strftime('%I:%M %p')}")
                                for r in morning_r:
                                    st.caption(f"⚪ ↘ {r['price']:.2f} @ {r['time'].strftime('%I:%M %p')}")
                        
                        # Highest wick (bearish candle)
                        if detected['highest_wick']:
                            hw = detected['highest_wick']
                            st.markdown(f"**Highest Wick (bearish): {hw['price']:.2f}** @ {hw['time'].strftime('%I:%M %p')}")
                            highest_wick = hw
                        else:
                            st.caption("No bearish candle wick found")
                        
                        # Lowest wick (bullish candle)
                        if detected['lowest_wick']:
                            lw = detected['lowest_wick']
                            st.markdown(f"**Lowest Wick (bullish): {lw['price']:.2f}** @ {lw['time'].strftime('%I:%M %p')}")
                            lowest_wick = lw
                        else:
                            st.caption("No bullish candle wick found")
                        
                        st.markdown("---")
                        st.markdown("### ✏️ Override Auto-Detection")
                        st.caption("Edit any value below to override what was detected.")
                        
                        # Allow manual override of auto-detected values
                        override_bounces = st.checkbox("Override bounces", value=False, key="override_b")
                        override_rejections = st.checkbox("Override rejections", value=False, key="override_r")
                        override_wicks = st.checkbox("Override wicks", value=False, key="override_w")
                    else:
                        st.warning(f"Only {len(ny_candles)} NY session candles found. Need at least 3.")
                        data_status.source_used = "manual"
                else:
                    if fetch_btn:
                        st.info("No candle data retrieved. Use manual input.")
            
            # If overriding or no data, show manual inputs
            show_manual_bounces = (data_status.source_used == "manual" or 
                                    st.session_state.get('override_b', False))
            show_manual_rejections = (data_status.source_used == "manual" or 
                                       st.session_state.get('override_r', False))
            show_manual_wicks = (data_status.source_used == "manual" or 
                                  st.session_state.get('override_w', False))
        else:
            # Full manual mode
            show_manual_bounces = True
            show_manual_rejections = True
            show_manual_wicks = True
        
        # Manual input sections (shown when needed)
        if show_manual_bounces:
            st.markdown("---")
            st.markdown("### 🔺 Bounces (Line Chart Troughs)")
            st.markdown("*Close prices where price dipped and reversed up*")
            
            num_bounces = st.number_input("Number of bounces", min_value=0, max_value=8, value=2, key="num_bounces")
            
            bounces = []
            for i in range(num_bounces):
                col1, col2 = st.columns(2)
                with col1:
                    price = st.number_input(f"Bounce {i+1} Price", 
                                            value=6860.0, step=0.5, key=f"bounce_price_{i}",
                                            format="%.2f")
                with col2:
                    hour = st.selectbox(f"Hour", 
                                        options=list(range(8, 16)),
                                        index=2, key=f"bounce_hour_{i}",
                                        format_func=lambda x: f"{x}:00" if x < 12 else f"{x-12 if x > 12 else 12}:00 PM")
                    minute = st.selectbox(f"Min",
                                          options=[0, 30],
                                          index=0, key=f"bounce_min_{i}")
                
                bounce_time = datetime.combine(prior_date, time(hour, minute))
                bounces.append({'price': price, 'time': bounce_time})
        
        if show_manual_rejections:
            st.markdown("---")
            st.markdown("### 🔻 Rejections (Line Chart Peaks)")
            st.markdown("*Close prices where price pushed up and reversed down*")
            
            num_rejections = st.number_input("Number of rejections", min_value=0, max_value=8, value=2, key="num_rejections")
            
            rejections = []
            for i in range(num_rejections):
                col1, col2 = st.columns(2)
                with col1:
                    price = st.number_input(f"Rejection {i+1} Price",
                                            value=6910.0, step=0.5, key=f"rej_price_{i}",
                                            format="%.2f")
                with col2:
                    hour = st.selectbox(f"Hour",
                                        options=list(range(8, 16)),
                                        index=2, key=f"rej_hour_{i}",
                                        format_func=lambda x: f"{x}:00" if x < 12 else f"{x-12 if x > 12 else 12}:00 PM")
                    minute = st.selectbox(f"Min",
                                          options=[0, 30],
                                          index=0, key=f"rej_min_{i}")
                
                rej_time = datetime.combine(prior_date, time(hour, minute))
                rejections.append({'price': price, 'time': rej_time})
        
        if show_manual_wicks:
            st.markdown("---")
            st.markdown("### 📍 Session Extremes (Candlestick Wicks)")
            st.markdown("*Highest wick = bearish candle • Lowest wick = bullish candle*")
            st.caption("*Exclude if first bearish/bullish candle is 8:30 AM*")
            
            col1, col2 = st.columns(2)
            with col1:
                hw_price = st.number_input("Highest Wick Price", value=6920.0, step=0.5, format="%.2f")
            with col2:
                hw_hour = st.selectbox("HW Hour", options=list(range(8, 16)), index=2, key="hw_hour",
                                        format_func=lambda x: f"{x}:00" if x < 12 else f"{x-12 if x > 12 else 12}:00 PM")
                hw_min = st.selectbox("HW Min", options=[0, 30], index=0, key="hw_min")
            
            highest_wick = {
                'price': hw_price,
                'time': datetime.combine(prior_date, time(hw_hour, hw_min))
            }
            
            col1, col2 = st.columns(2)
            with col1:
                lw_price = st.number_input("Lowest Wick Price", value=6840.0, step=0.5, format="%.2f")
            with col2:
                lw_hour = st.selectbox("LW Hour", options=list(range(8, 16)), index=2, key="lw_hour",
                                        format_func=lambda x: f"{x}:00" if x < 12 else f"{x-12 if x > 12 else 12}:00 PM")
                lw_min = st.selectbox("LW Min", options=[0, 30], index=0, key="lw_min")
            
            lowest_wick = {
                'price': lw_price,
                'time': datetime.combine(prior_date, time(lw_hour, lw_min))
            }
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # Rate from secrets (keeps your edge private)
        default_rate = 13/25
        try:
            default_rate = float(st.secrets.get("rate", default_rate))
        except:
            pass
        rate = st.number_input("Rate per candle", value=default_rate, step=0.01, format="%.2f",
                               help="Your proprietary rate (add 'rate' to secrets.toml to persist)")
        
        # Universal ES-SPX offset (always available)
        # Auto-detected value may have been stored from auto-fetch
        auto_offset_val = st.session_state.get('_es_offset', 0.0)
        es_spx_offset = st.number_input("ES - SPX offset", value=auto_offset_val, step=0.25, format="%.2f",
                                         key="global_es_offset",
                                         help="NY tab uses SPX (subtracts offset). Asian tab uses ES (adds offset back).")
        st.session_state['_es_offset'] = es_spx_offset
        
        show_all_lines = st.checkbox("Show all projected lines", value=True)
        show_session_boxes = st.checkbox("Show session boxes", value=True)
    
    # ============================================================
    # CALCULATIONS
    # ============================================================
    
    # Override global rate if changed
    global RATE_PER_CANDLE
    RATE_PER_CANDLE = rate
    
    # Calculate 9 AM levels
    next_day_dt = datetime.combine(next_date, time(9, 0))
    levels = calculate_nine_am_levels(bounces, rejections, highest_wick, lowest_wick, next_day_dt)
    
    # Calculate the 6-line channel structure
    channels = calculate_channel_structure(
        bounces, rejections, highest_wick, lowest_wick, next_day_dt,
        candles=st.session_state.get('last_fetch_candles', None),
        prior_date=prior_date,
        es_offset=es_offset_val
    )
    
    # ============================================================
    # LIVE PRICE TRACKING
    # ============================================================
    live_price_data = None
    es_offset_val = st.session_state.get('_es_offset', 0.0)
    
    if live_mode:
        # Auto-refresh every 30 seconds
        try:
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=30000, limit=None, key="live_refresh")
        except ImportError:
            # Fallback: manual refresh button
            st.caption("⚠️ Install `streamlit-autorefresh` for auto-polling. Using manual refresh.")
            if st.button("🔄 Refresh Price", key="manual_refresh"):
                st.rerun()
        
        live_price_data = fetch_live_price()
        
        if live_price_data['ok']:
            es_price = live_price_data['price']
            spx_price = es_price - es_offset_val
            price_time = live_price_data['time']
            time_str = price_time.strftime('%I:%M:%S %p') if hasattr(price_time, 'strftime') else str(price_time)
            
            # Get level values
            hw_val_live = levels['key_levels']['highest_wick_ascending']['value_at_9am'] if levels['key_levels']['highest_wick_ascending'] else None
            hb_val_live = levels['key_levels']['highest_bounce_ascending']['value_at_9am'] if levels['key_levels']['highest_bounce_ascending'] else None
            lr_val_live = levels['key_levels']['lowest_rejection_descending']['value_at_9am'] if levels['key_levels']['lowest_rejection_descending'] else None
            lw_val_live = levels['key_levels']['lowest_wick_descending']['value_at_9am'] if levels['key_levels']['lowest_wick_descending'] else None
            
            # Determine live position
            all_levels = {}
            if hw_val_live: all_levels['HW Asc'] = hw_val_live
            if hb_val_live: all_levels['HB Asc'] = hb_val_live
            if lr_val_live: all_levels['LR Desc'] = lr_val_live
            if lw_val_live: all_levels['LW Desc'] = lw_val_live
            
            # Live signal
            live_signal = ""
            live_color = "#ffd740"
            if hw_val_live and hb_val_live and lr_val_live and lw_val_live:
                asc_h = max(hw_val_live, hb_val_live)
                asc_l = min(hw_val_live, hb_val_live)
                desc_h = max(lr_val_live, lw_val_live)
                desc_l = min(lr_val_live, lw_val_live)
                
                if spx_price > asc_h:
                    live_signal = "BULLISH TREND DAY"
                    live_color = "#00e676"
                elif spx_price >= asc_l:
                    live_signal = "BETWEEN ASCENDING"
                    live_color = "#ffd740"
                elif spx_price > desc_h:
                    live_signal = "BEARISH BIAS"
                    live_color = "#ff5252"
                elif spx_price >= desc_l:
                    live_signal = "BETWEEN DESCENDING"
                    live_color = "#ffd740"
                else:
                    live_signal = "BEARISH TREND DAY"
                    live_color = "#ff1744"
            
            # Distances
            distances = []
            for name, val in sorted(all_levels.items(), key=lambda x: x[1], reverse=True):
                diff = spx_price - val
                arrow = "▲" if diff > 0 else "▼"
                distances.append(f"{name}: {val:.2f} ({arrow}{abs(diff):.2f})")
            
            # Display live banner
            offset_note = f" (offset {es_offset_val:+.1f})" if es_offset_val != 0 else ""
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0d1117 0%, #131a2e 100%); border: 2px solid {live_color}; 
                        border-radius: 12px; padding: 15px; margin: 10px 0; text-align: center;">
                <div style="font-family: 'Rajdhani'; color: #8892b0; font-size: 0.85rem;">
                    🔴 LIVE • ES=F @ {time_str}{offset_note}
                </div>
                <div style="font-family: 'Orbitron'; font-size: 2.2rem; color: {live_color}; margin: 5px 0;">
                    {spx_price:.2f}
                </div>
                <div style="font-family: 'Orbitron'; font-size: 1rem; color: {live_color};">
                    {live_signal}
                </div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #8892b0; margin-top: 8px;">
                    {'  •  '.join(distances)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Live price unavailable: {live_price_data.get('error', 'Unknown')}")
    
    # ============================================================
    # MAIN CONTENT: Tabs
    # ============================================================
    
    tab1, tab2, tab3 = st.tabs([
        "⚡ SIGNAL & LEVELS", 
        "🌙 ASIAN SESSION", 
        "📋 TRADE LOG"
    ])
    
    # ============================================================
    # TAB 1: SIGNAL & LEVELS
    # ============================================================
    with tab1:
        render_section_banner("🎯", "9:00 AM CT Decision Levels", "Key structural lines projected to the opening bell", "#ffd740")
        
        # Display the four key levels in a uniform CSS grid
        hw_asc = levels['key_levels']['highest_wick_ascending']
        hb_asc = levels['key_levels']['highest_bounce_ascending']
        lr_desc = levels['key_levels']['lowest_rejection_descending']
        lw_desc = levels['key_levels']['lowest_wick_descending']
        
        cards_html = '<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 10px 0;">'
        
        for label, level, color_class in [
            ("HW Ascending ↗", hw_asc, "bear"),
            ("HB Ascending ↗", hb_asc, "bear"),
            ("LR Descending ↘", lr_desc, "bull"),
            ("LW Descending ↘", lw_desc, "bull"),
        ]:
            if level:
                val = f"{level['value_at_9am']:.2f}"
                anchor = f"{level['anchor_price']:.2f}"
                color = "#ff1744" if color_class == "bear" else "#00e676"
            else:
                val = "—"
                anchor = "—"
                color = "#5a6a8a"
            
            cards_html += f"""
            <div style="background: linear-gradient(145deg, #131a2e 0%, #0d1220 100%);
                        border: 1px solid #1e2d4a; border-radius: 12px; padding: 20px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.3); text-align: center;">
                <div style="font-family: 'Rajdhani', sans-serif; color: #5a6a8a; font-size: 0.8rem;
                            text-transform: uppercase; letter-spacing: 2px;">{label}</div>
                <div style="font-family: 'JetBrains Mono', monospace; color: {color};
                            font-size: 1.6rem; font-weight: 700; margin: 8px 0;">{val}</div>
                <div style="font-family: 'Rajdhani', sans-serif; color: #5a6a8a; font-size: 0.7rem;">Anchor: {anchor}</div>
            </div>"""
        
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)
        
        # ============================================================
        # 9 AM LINE LADDER (all lines sorted by value)
        # ============================================================
        render_section_banner("📊", "Line Ladder @ 9:00 AM CT", "All projected lines sorted highest to lowest", "#00d4ff")
        st.caption("All projected lines sorted by 9 AM value — highest to lowest")
        
        # Build unified ladder
        ladder_9am = []
        for line in levels['ascending']:
            ladder_9am.append({
                'name': line['source'].split(' @ ')[0] if ' @ ' in line['source'] else line['source'],
                'short': f"{'HW' if line['type'] == 'highest_wick' else 'B'} ↗",
                'value': line['value_at_9am'],
                'anchor': line['anchor_price'],
                'change': line['value_at_9am'] - line['anchor_price'],
                'direction': 'ascending',
                'color': '#ff1744' if line['type'] == 'highest_wick' else '#ff5252',
                'is_key': line['type'] in ('highest_wick', 'highest_bounce'),
            })
        for line in levels['descending']:
            ladder_9am.append({
                'name': line['source'].split(' @ ')[0] if ' @ ' in line['source'] else line['source'],
                'short': f"{'LW' if line['type'] == 'lowest_wick' else 'R'} ↘",
                'value': line['value_at_9am'],
                'anchor': line['anchor_price'],
                'change': line['value_at_9am'] - line['anchor_price'],
                'direction': 'descending',
                'color': '#00e676' if line['type'] == 'lowest_wick' else '#69f0ae',
                'is_key': line['type'] in ('lowest_wick', 'lowest_rejection'),
            })
        
        ladder_9am.sort(key=lambda x: x['value'], reverse=True)
        
        if ladder_9am:
            # Show live price on 9AM ladder if available
            live_ladder_price = None
            if live_mode and live_price_data and live_price_data.get('ok'):
                live_ladder_price = live_price_data['price'] - es_offset_val
            render_visual_ladder(
                lines=[{
                    'value': l['value'], 'label': l['short'], 'full_name': l['name'],
                    'color': l['color'], 'direction': l['direction'], 'is_key': l['is_key'],
                } for l in ladder_9am],
                current_price=live_ladder_price,
                title="9 AM Projected Levels",
                height=max(400, len(ladder_9am) * 45),
            )
    
        # ── NY SESSION — 9 AM DECISION FRAMEWORK ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_section_banner("☀️", "NY Session — 0DTE Options", "9:00 AM structural signal", "#ff9100")
        
        # Auto-fill from live price if available
        default_price = 6865.0
        if live_mode and live_price_data and live_price_data.get('ok'):
            default_price = live_price_data['price'] - es_offset_val
        
        current_price = st.number_input("Current SPX Price at 9:00 AM CT", 
                                         value=default_price, step=0.5, format="%.2f",
                                         key="current_spx",
                                         help="Auto-filled from live ES price when LIVE MODE is on")
        
        # ============================================================
        # CHANNEL PLAYBOOK — THE MISSION CARD
        # ============================================================
        if channels:
            playbook = determine_scenario(channels, current_price)
            sc = playbook['scenario']
            pri = playbook['primary']
            alt = playbook['alternate']
            warnings = playbook.get('warnings', [])
            
            # ── Time cutoff check ──
            time_cutoff_hit = False
            try:
                import pytz
                ct_tz = pytz.timezone('America/Chicago')
                now_ct = datetime.now(ct_tz).replace(tzinfo=None)
                if now_ct.hour >= 10 and now_ct.date() == next_date:
                    time_cutoff_hit = True
                    st.markdown("""
                    <div class="sig neutral">
                        <div class="sig-dir" style="color:var(--gold);">⏰ TIME CUTOFF — NO NEW ENTRIES</div>
                        <div class="sig-detail">It is past 10:00 AM CT (11:00 AM ET). Theta acceleration on 0DTE makes new entries unprofitable. Manage existing positions only.</div>
                    </div>""", unsafe_allow_html=True)
            except:
                pass
            
            # ── Risk Warnings ──
            if warnings:
                for w in warnings:
                    w_color = '#ffd740' if '⚠️' in w else '#00e676'
                    st.markdown(f"""
                    <div style="background:var(--bg-card);border:1px solid var(--border);border-left:3px solid {w_color};
                                border-radius:10px;padding:10px 16px;margin:4px 0;font-family:JetBrains Mono;font-size:0.78rem;color:var(--t2);">
                        {w}
                    </div>""", unsafe_allow_html=True)
            
            # ── Scenario Banner ──
            st.markdown(f"""
            <div class="sig {sc['class']}">
                <div class="sig-dir" style="color:{sc['color']};">SCENARIO {sc['number']}: {sc['name']}</div>
                <div class="sig-detail">{sc['desc']}</div>
            </div>""", unsafe_allow_html=True)
            
            # ── Channel Map (6 lines) ──
            render_section_banner("📊", "Channel Structure", "6-line framework at 9 AM")
            
            if channels:
                render_visual_ladder(
                    lines=[{
                        'value': l['value'], 'label': l['label'], 'full_name': l['full_name'],
                        'color': l['color'], 'direction': l['direction'], 'is_key': l['is_key'],
                    } for l in channels['all_lines']],
                    current_price=current_price,
                    title="Channel Structure",
                    height=max(450, 6 * 55),
                )
            
            # ── PRIMARY PLAY ──
            if pri:
                render_section_banner("🎯", "PRIMARY PLAY", pri['confidence'])
                
                pri_color = '#ff1744' if pri['direction'] == 'PUT' else '#00e676'
                pri_icon = '🔻' if pri['direction'] == 'PUT' else '🔺'
                tp1_price = pri.get('tp1_price', 0)
                tp2_price = pri.get('tp2_price', 0)
                pri_contracts = pri.get('contracts', 3)
                
                # Don't show trade card if time cutoff
                if time_cutoff_hit:
                    st.caption("Trade card suppressed — past time cutoff. Manage existing positions only.")
                else:
                    st.markdown(f"""
                    <div class="tc" style="border-color:{pri_color}20;">
                        <div class="tc-header">
                            <span class="tc-title" style="color:{pri_color};">{pri_icon} BUY {pri_contracts}× {pri['direction']} — SPX {pri['strike']}</span>
                            <span class="tc-meta">{abs(pri['strike'] - pri['entry_price']):.0f}pt OTM from entry • 0DTE • {pri_contracts} contracts</span>
                        </div>
                        <div class="tc-grid">
                            <div class="tc-cell">
                                <div class="tc-cell-label" style="color:{pri_color};">Entry Zone</div>
                                <div class="tc-cell-val" style="color:{pri_color};">{pri['entry_price']:.2f}</div>
                                <div class="tc-cell-sub">{pri['entry_line']['label']}</div>
                            </div>
                            <div class="tc-cell" style="background:rgba(255,23,68,0.03);">
                                <div class="tc-cell-label" style="color:var(--red);">Stop Loss</div>
                                <div class="tc-cell-val" style="color:var(--red);">{pri['stop_price']:.2f}</div>
                                <div class="tc-cell-sub">{pri['stop_desc']}</div>
                            </div>
                            <div class="tc-cell" style="background:rgba(0,230,118,0.03);">
                                <div class="tc-cell-label" style="color:var(--green);">Target 1 / Target 2</div>
                                <div class="tc-cell-val" style="color:var(--green);">{tp1_price:.2f} / {tp2_price:.2f}</div>
                                <div class="tc-cell-sub">{pri.get('tp1_desc','')} / {pri.get('tp2_desc','')}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Timing card
                st.markdown(f"""
                <div class="rules">
                    <div class="rules-title">⏰ TIMING</div>
                    <div class="rules-body">{pri['timing']}</div>
                </div>""", unsafe_allow_html=True)
            
            # ── ALTERNATE PLAY ──
            if alt:
                render_section_banner("🔄", "ALTERNATE PLAY", alt.get('confidence', ''))
                
                alt_color = '#ff1744' if alt['direction'] == 'PUT' else '#00e676'
                alt_icon = '🔻' if alt['direction'] == 'PUT' else '🔺'
                alt_tp1 = alt.get('tp1_price', 0)
                alt_tp2 = alt.get('tp2_price', 0)
                
                st.markdown(f"""
                <div class="tc" style="border-color:{alt_color}15;opacity:0.85;">
                    <div class="tc-header">
                        <span class="tc-title" style="color:{alt_color};">{alt_icon} ALT: BUY {alt['direction']} — SPX {alt['strike']}</span>
                        <span class="tc-meta">Alternate scenario</span>
                    </div>
                    <div class="tc-grid">
                        <div class="tc-cell">
                            <div class="tc-cell-label" style="color:{alt_color};">Entry Zone</div>
                            <div class="tc-cell-val" style="color:{alt_color};">{alt['entry_price']:.2f}</div>
                        </div>
                        <div class="tc-cell" style="background:rgba(255,23,68,0.03);">
                            <div class="tc-cell-label" style="color:var(--red);">Stop</div>
                            <div class="tc-cell-val" style="color:var(--red);">{alt['stop_price']:.2f}</div>
                            <div class="tc-cell-sub">{alt['stop_desc']}</div>
                        </div>
                        <div class="tc-cell" style="background:rgba(0,230,118,0.03);">
                            <div class="tc-cell-label" style="color:var(--green);">TP1 / TP2</div>
                            <div class="tc-cell-val" style="color:var(--green);">{alt_tp1:.2f} / {alt_tp2:.2f}</div>
                            <div class="tc-cell-sub">{alt.get('tp1_desc','')} / {alt.get('tp2_desc','')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="rules">
                    <div class="rules-title">⏰ ALTERNATE TIMING</div>
                    <div class="rules-body">{alt['timing']}</div>
                </div>""", unsafe_allow_html=True)
            
            # Use primary direction for downstream logic (premium, confluence)
            trade_direction = pri['direction'] if pri else None
            stop_line = pri.get('entry_line') if pri else None
            entry_line = pri.get('entry_line') if pri else None
        else:
            st.warning("No channel structure available. Enter bounces/rejections in the sidebar.")
            trade_direction = None
            stop_line = None
            entry_line = None
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_section_banner("🎯", "9:00 AM Decision", "Where is price in the ladder?")
        
        # ============================================================
        # BUILD 9 AM LINE LADDER (reuse from structural map)
        # ============================================================
        ny_ladder = []
        for line in levels['ascending']:
            ny_ladder.append({
                'name': line['source'].split(' @ ')[0] if ' @ ' in line['source'] else line['source'],
                'short': f"{'HW' if line['type'] == 'highest_wick' else 'B'} ↗",
                'value': line['value_at_9am'],
                'direction': 'ascending',
                'color': '#ff1744' if line['type'] == 'highest_wick' else '#ff5252',
            })
        for line in levels['descending']:
            ny_ladder.append({
                'name': line['source'].split(' @ ')[0] if ' @ ' in line['source'] else line['source'],
                'short': f"{'LW' if line['type'] == 'lowest_wick' else 'R'} ↘",
                'value': line['value_at_9am'],
                'direction': 'descending',
                'color': '#00e676' if line['type'] == 'lowest_wick' else '#69f0ae',
            })
        ny_ladder.sort(key=lambda x: x['value'], reverse=True)
        
        # Find nearest lines above and below current price
        lines_above = [l for l in ny_ladder if l['value'] > current_price]
        lines_below = [l for l in ny_ladder if l['value'] <= current_price]
        
        nearest_above = lines_above[-1] if lines_above else None
        nearest_below = lines_below[0] if lines_below else None
        
        # ============================================================
        # POSITION & SIGNAL
        # ============================================================
        # Count ascending vs descending lines above/below
        asc_above = sum(1 for l in lines_above if l['direction'] == 'ascending')
        desc_below = sum(1 for l in lines_below if l['direction'] == 'descending')
        
        # Determine signal based on position
        signal = "NEUTRAL"
        signal_detail = ""
        signal_class = "neutral"
        trade_direction = None  # 'PUT' or 'CALL'
        stop_line = None
        target_lines = []
        entry_line = None  # NEW: the structural line that defines entry
        
        if nearest_above and nearest_below:
            dist_above = nearest_above['value'] - current_price
            dist_below = current_price - nearest_below['value']
            
            # Check if price is below all ascending lines
            all_asc_values = [l['value'] for l in ny_ladder if l['direction'] == 'ascending']
            all_desc_values = [l['value'] for l in ny_ladder if l['direction'] == 'descending']
            
            if all_asc_values and current_price < min(all_asc_values):
                # Below ALL ascending lines = bearish
                signal = "BEARISH — BUY PUTS"
                signal_class = "bear"
                trade_direction = "PUT"
                entry_line = nearest_above  # closest ascending line above = entry zone
                stop_line = nearest_above  # stop if price breaks above this line
                target_lines = [l for l in lines_below if l['direction'] == 'descending'][:2]
                signal_detail = f"Price {current_price:.2f} below all ascending lines. Entry zone: {entry_line['short']} @ {entry_line['value']:.2f}. Targets: descending lines below."
                
            elif all_desc_values and current_price > max(all_desc_values) and all_asc_values and current_price > max(all_asc_values):
                # Above ALL lines = strong bullish
                signal = "BULLISH TREND — BUY CALLS"
                signal_class = "bull"
                trade_direction = "CALL"
                entry_line = nearest_below  # closest descending line below = entry zone
                stop_line = nearest_below
                target_lines = []
                signal_detail = f"Price {current_price:.2f} above ALL lines. Strong trend day. Entry zone: {entry_line['short']} @ {entry_line['value']:.2f}."
                
            elif all_desc_values and current_price < min(all_desc_values):
                # Below ALL lines = strong bearish
                signal = "BEARISH TREND — BUY PUTS"
                signal_class = "bear"
                trade_direction = "PUT"
                entry_line = nearest_above
                stop_line = nearest_above
                target_lines = []
                signal_detail = f"Price {current_price:.2f} below ALL lines including descending. Entry zone: {entry_line['short']} @ {entry_line['value']:.2f}."
                
            elif all_asc_values and current_price > max(all_asc_values):
                # Above all ascending = bullish
                signal = "BULLISH — BUY CALLS"
                signal_class = "bull"
                trade_direction = "CALL"
                entry_line = nearest_below  # closest descending line below
                stop_line = nearest_below
                target_lines = [l for l in lines_above if l['direction'] == 'ascending'][:2]
                signal_detail = f"Price {current_price:.2f} above all ascending lines. Entry zone: {entry_line['short']} @ {entry_line['value']:.2f}."
                
            elif nearest_above['direction'] == 'ascending' and nearest_below['direction'] == 'descending':
                # Between ascending above and descending below — choppy, wait
                signal = "BETWEEN ASC ↗ & DESC ↘ — WAIT"
                signal_class = "neutral"
                signal_detail = f"Price {current_price:.2f} between {nearest_above['short']} ({nearest_above['value']:.2f}) and {nearest_below['short']} ({nearest_below['value']:.2f}). No clear bias."
                
            elif nearest_above['direction'] == 'descending':
                # Descending line above = resistance, bearish lean
                signal = "BEARISH LEAN — BUY PUTS"
                signal_class = "bear"
                trade_direction = "PUT"
                entry_line = nearest_above  # descending line above = entry zone for puts
                stop_line = nearest_above
                target_lines = [l for l in lines_below][:2]
                signal_detail = f"Descending resistance at {nearest_above['value']:.2f}. Entry zone: {entry_line['short']} @ {entry_line['value']:.2f}."
                
            elif nearest_below['direction'] == 'ascending':
                # Ascending line below = support, bullish lean
                signal = "BULLISH LEAN — BUY CALLS"
                signal_class = "bull"
                trade_direction = "CALL"
                entry_line = nearest_below  # ascending line below = entry zone for calls
                stop_line = nearest_below
                target_lines = [l for l in lines_above][:2]
                signal_detail = f"Ascending support at {nearest_below['value']:.2f}. Entry zone: {entry_line['short']} @ {entry_line['value']:.2f}."
        
        # ============================================================
        # 8:30 AM CONFIRMATION RULE
        # ============================================================
        # The 8:30 candle must TEST the structural entry line and get REJECTED.
        # If it tests and closes WITH the line (not rejected), WAIT — no trade.
        confirmation_status = "PENDING"
        confirmation_detail = ""
        confirmation_passed = None  # None = no data, True = confirmed, False = wait
        
        if trade_direction and entry_line:
            # Fetch SPX 8:30 candle directly — no offset needed since entry lines are in SPX
            spx_830_candle = None
            spx_830_source = ""
            
            try:
                import yfinance as yf
                import pytz
                
                # Fetch SPX 30-min candles for today
                spx_ticker = yf.Ticker("^GSPC")
                spx_hist = spx_ticker.history(period="1d", interval="30m")
                
                if len(spx_hist) > 0:
                    spx_hist = spx_hist.reset_index()
                    # Normalize datetime column
                    dt_col = [c for c in spx_hist.columns if 'date' in c.lower() or 'datetime' in c.lower()][0]
                    spx_hist = spx_hist.rename(columns={dt_col: 'datetime'})
                    spx_hist['datetime'] = pd.to_datetime(spx_hist['datetime'])
                    
                    # Convert to CT if timezone-aware
                    if spx_hist['datetime'].dt.tz is not None:
                        ct_tz = pytz.timezone('America/Chicago')
                        spx_hist['datetime'] = spx_hist['datetime'].dt.tz_convert(ct_tz).dt.tz_localize(None)
                    
                    # Normalize column names
                    spx_hist.columns = [c.lower().replace(' ', '_') for c in spx_hist.columns]
                    
                    # Find the 8:30 AM candle
                    for _, row in spx_hist.iterrows():
                        ct = row['datetime']
                        if ct.hour == 8 and ct.minute == 30 and ct.date() == next_date:
                            spx_830_candle = row
                            spx_830_source = "SPX (^GSPC)"
                            break
                        # yfinance may label it as 9:30 ET = 8:30 CT
                        elif ct.hour == 9 and ct.minute == 30 and ct.date() == next_date:
                            spx_830_candle = row
                            spx_830_source = "SPX (^GSPC) — 9:30 ET = 8:30 CT"
                            break
            except Exception as e:
                spx_830_source = f"SPX fetch failed: {str(e)[:60]}"
            
            # Fallback to ES candles with offset if SPX not available
            if spx_830_candle is None:
                es_candles = st.session_state.get('last_fetch_candles', None)
                es_offset_830 = st.session_state.get('_es_offset', 0.0)
                
                if es_candles is not None and len(es_candles) > 0:
                    for _, row in es_candles.iterrows():
                        ct = row['datetime']
                        if ct.hour == 8 and ct.minute == 30 and ct.date() == next_date:
                            # Convert ES to SPX by subtracting offset
                            spx_830_candle = pd.Series({
                                'open': row['open'] - es_offset_830,
                                'high': row['high'] - es_offset_830,
                                'low': row['low'] - es_offset_830,
                                'close': row['close'] - es_offset_830,
                            })
                            spx_830_source = f"ES→SPX (offset {es_offset_830:+.2f})"
                            break
            
            if spx_830_candle is not None:
                c_open = float(spx_830_candle['open'])
                c_high = float(spx_830_candle['high'])
                c_low = float(spx_830_candle['low'])
                c_close = float(spx_830_candle['close'])
                is_bullish_candle = c_close > c_open
                is_bearish_candle = c_close < c_open
                entry_val = entry_line['value']
                
                # Debug: show what the app sees
                candle_color = "🟢 GREEN" if is_bullish_candle else "🔴 RED"
                st.caption(f"8:30 candle ({spx_830_source}): O {c_open:.2f} H {c_high:.2f} L {c_low:.2f} C {c_close:.2f} — {candle_color} | Entry line: {entry_val:.2f}")
                
                if trade_direction == "PUT":
                    # For PUTS: 8:30 must wick UP to ascending line above AND close as GREEN candle below it
                    # Green candle (bullish) closing below = buyers TRIED to break through but FAILED. Line held.
                    # Red candle (bearish) closing below = just selling, no proof line was tested. WAIT.
                    touched_line = c_high >= (entry_val - 1.0)  # within 1pt tolerance
                    closed_below = c_close < entry_val
                    
                    if touched_line and is_bullish_candle and closed_below:
                        confirmation_status = "CONFIRMED ✅"
                        confirmation_detail = f"8:30 wicked to {c_high:.2f} (line {entry_val:.2f}), closed GREEN at {c_close:.2f} below it. Buyers tried and failed. Line rejected."
                        confirmation_passed = True
                    elif touched_line and is_bearish_candle and closed_below:
                        confirmation_status = "WAIT ⏸️"
                        confirmation_detail = f"8:30 touched {entry_val:.2f} but closed RED at {c_close:.2f}. Just selling, not a true test of the line. Wait."
                        confirmation_passed = False
                    elif touched_line and not closed_below:
                        confirmation_status = "WAIT ⏸️"
                        confirmation_detail = f"8:30 touched {entry_val:.2f} and closed ABOVE it at {c_close:.2f}. Line broken. Do not short."
                        confirmation_passed = False
                    elif not touched_line:
                        confirmation_status = "NOT TESTED"
                        confirmation_detail = f"8:30 high was {c_high:.2f}, did not reach entry line at {entry_val:.2f}. No test occurred."
                        confirmation_passed = None
                
                elif trade_direction == "CALL":
                    # For CALLS: 8:30 must wick DOWN to descending line below AND close as RED candle above it
                    # Red candle (bearish) closing above = sellers TRIED to break through but FAILED. Line held.
                    # Green candle (bullish) closing above = just buying, no proof line was tested. WAIT.
                    touched_line = c_low <= (entry_val + 1.0)  # within 1pt tolerance
                    closed_above = c_close > entry_val
                    
                    if touched_line and is_bearish_candle and closed_above:
                        confirmation_status = "CONFIRMED ✅"
                        confirmation_detail = f"8:30 wicked to {c_low:.2f} (line {entry_val:.2f}), closed RED at {c_close:.2f} above it. Sellers tried and failed. Line rejected."
                        confirmation_passed = True
                    elif touched_line and is_bullish_candle and closed_above:
                        confirmation_status = "WAIT ⏸️"
                        confirmation_detail = f"8:30 touched {entry_val:.2f} but closed GREEN at {c_close:.2f}. Just buying, not a true test of the line. Wait."
                        confirmation_passed = False
                    elif touched_line and not closed_above:
                        confirmation_status = "WAIT ⏸️"
                        confirmation_detail = f"8:30 touched {entry_val:.2f} and closed BELOW it at {c_close:.2f}. Line broken. Do not go long."
                        confirmation_passed = False
                    elif not touched_line:
                        confirmation_status = "NOT TESTED"
                        confirmation_detail = f"8:30 low was {c_low:.2f}, did not reach entry line at {entry_val:.2f}. No test occurred."
                        confirmation_passed = None
            else:
                confirmation_detail = f"8:30 candle not available. {spx_830_source if spx_830_source else 'Fetch data or check manually.'}"
        
        # Signal display
        sig_color = '#00e676' if signal_class == 'bull' else '#ff1744' if signal_class == 'bear' else '#ffd740'
        
        # Modify signal if 8:30 confirmation failed
        if confirmation_passed is False and trade_direction:
            original_signal = signal
            signal = f"⏸️ WAIT — 8:30 NOT REJECTED"
            signal_class = "neutral"
            signal_detail = f"{confirmation_detail} Original signal: {original_signal}"
        
        render_signal_display(signal, signal_detail, signal_class)
        
        # Show 8:30 confirmation status
        if trade_direction and entry_line:
            conf_color = '#00e676' if confirmation_passed else '#ffd740' if confirmation_passed is None else '#ff1744'
            st.markdown(f"""
            <div style="background:var(--bg-card);border:1px solid var(--border);border-left:3px solid {conf_color};
                        border-radius:12px;padding:14px 18px;margin:8px 0;">
                <div style="font-family:JetBrains Mono;font-size:0.6rem;color:var(--t3);letter-spacing:3px;text-transform:uppercase;">8:30 AM Confirmation</div>
                <div style="font-family:Outfit;font-weight:700;font-size:0.95rem;color:{conf_color};margin-top:4px;">{confirmation_status}</div>
                <div style="font-family:JetBrains Mono;font-size:0.75rem;color:var(--t2);margin-top:6px;">{confirmation_detail}</div>
            </div>""", unsafe_allow_html=True)
        
        # ============================================================
        # LINE LADDER WITH PRICE POSITION
        # ============================================================
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_section_banner("📊", "9 AM Line Ladder", "Price position relative to structural levels", "#00d4ff")
        
        if ny_ladder:
            render_visual_ladder(
                lines=[{
                    'value': l['value'], 'label': l['short'], 'full_name': l['name'],
                    'color': l['color'], 'direction': l['direction'],
                    'is_key': 'HW' in l['short'] or 'LW' in l['short'] or 'HB' in l['short'] or 'LR' in l['short'],
                } for l in ny_ladder],
                current_price=current_price,
                title="9 AM Line Ladder",
                height=max(500, len(ny_ladder) * 45),
            )
        
        # ============================================================
        # OPTIONS TRADE CARD
        # ============================================================
        if trade_direction:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            render_section_banner("📋", "0DTE Trade Setup", "Entry • Stop • Targets • Premium estimates", "#00e676")
            
            # Calculate strike: 20pt OTM from the structural ENTRY LINE (not current price)
            # Entry = the ascending line (for PUTS) or descending line (for CALLS)
            # Strike = 20pt OTM from that entry level, rounded to nearest 5
            if entry_line:
                entry_level = entry_line['value']
                if trade_direction == "PUT":
                    raw_strike = entry_level - 20
                    strike = int(raw_strike // 5) * 5
                else:
                    raw_strike = entry_level + 20
                    strike = int((raw_strike + 4) // 5) * 5
            else:
                # Fallback: 20pt OTM from current price
                if trade_direction == "PUT":
                    strike = int((current_price - 20) // 5) * 5
                else:
                    strike = int((current_price + 20 + 4) // 5) * 5
            
            otm_distance = abs(strike - current_price)
            
            # Entry timing based on 8:30 confirmation
            # If 8:30 touched and confirmed → enter at 9:05 (price already moving)
            # If 8:30 didn't touch → 9:00 will do the touch → enter at 9:30 or 10:00
            if confirmation_passed is True:
                entry_timing = "9:05 AM"
                entry_timing_detail = "8:30 confirmed rejection. Enter early — price already moving."
            elif confirmation_passed is None:
                entry_timing = "9:30–10:00 AM"
                entry_timing_detail = "8:30 did not test the line. Wait for 9:00 to touch, then enter on confirmation."
            else:
                entry_timing = "WAIT"
                entry_timing_detail = "8:30 test failed. Do not enter until line is properly tested and rejected."
            
            # Stop and targets (SPX levels)
            stop_price = stop_line['value'] if stop_line else (current_price + 10 if trade_direction == "PUT" else current_price - 10)
            
            if target_lines:
                tp1 = target_lines[0]['value']
                tp1_name = f"{target_lines[0]['short']}"
                tp2 = target_lines[1]['value'] if len(target_lines) >= 2 else (tp1 - 5 if trade_direction == "PUT" else tp1 + 5)
                tp2_name = f"{target_lines[1]['short']}" if len(target_lines) >= 2 else "Fixed 5pt"
            else:
                # Trend day — no opposing lines, use fixed targets
                if trade_direction == "PUT":
                    tp1 = current_price - 10
                    tp2 = current_price - 20
                else:
                    tp1 = current_price + 10
                    tp2 = current_price + 20
                tp1_name = "10pt move"
                tp2_name = "20pt move"
            
            # ============================================================
            # PREMIUM: Auto-fetch + Scenario Projections
            # ============================================================
            
            # Fetch VIX
            try:
                import yfinance as yf
                vix_data = yf.Ticker("^VIX").history(period="1d")
                current_vix = float(vix_data['Close'].iloc[-1]) if len(vix_data) > 0 else 18.0
            except:
                current_vix = 18.0
            
            import math
            from datetime import time as dt_time
            
            # Determine current time context for hours-to-expiry
            try:
                import pytz
                ct_tz = pytz.timezone('America/Chicago')
                now_ct = datetime.now(ct_tz).replace(tzinfo=None)
                market_close = datetime.combine(next_date, dt_time(15, 0))
                hours_now = max(0.1, (market_close - now_ct).total_seconds() / 3600)
            except:
                hours_now = 6.5  # default to 8:30 AM
            
            # Hours at entry — depends on 8:30 confirmation
            if entry_timing == "9:05 AM":
                entry_dt = datetime.combine(next_date, dt_time(9, 5))
            elif entry_timing == "9:30–10:00 AM":
                entry_dt = datetime.combine(next_date, dt_time(9, 45))  # midpoint estimate
            else:
                entry_dt = datetime.combine(next_date, dt_time(10, 0))  # conservative
            hours_at_entry = max(0.1, (market_close - entry_dt).total_seconds() / 3600)
            
            # Black-Scholes estimate (always available)
            est_premium = estimate_option_premium(current_price, strike, current_vix, hours_at_entry, trade_direction)
            
            # Auto-fetch live premium when LIVE MODE is on and market is open
            live_premium = None
            live_bid = None
            live_ask = None
            
            auto_fetch = live_mode and hours_now < 7.0 and hours_now > 0.5  # between 8:00 AM and 2:30 PM
            manual_fetch = False
            
            if not auto_fetch:
                col_f1, col_f2 = st.columns([3, 1])
                with col_f1:
                    st.markdown(f"""
                    <div style="font-family: JetBrains Mono; color: #8892b0; font-size: 0.85rem;">
                        VIX: {current_vix:.1f} • Pre-Market Est: ${est_premium:.2f}/contract
                    </div>""", unsafe_allow_html=True)
                with col_f2:
                    manual_fetch = st.button("📊 Fetch Live Price", key="fetch_tt_chain")
            
            if auto_fetch or manual_fetch:
                try:
                    import requests as req
                    tt_token = st.session_state.get('_tt_session_token', '')
                    
                    if not tt_token:
                        # Authenticate with Tastytrade
                        tt_user = st.secrets.get("tastytrade", {}).get("username", "")
                        tt_pass = st.secrets.get("tastytrade", {}).get("password", "")
                        if tt_user and tt_pass:
                            auth_resp = req.post("https://api.tastytrade.com/sessions",
                                                  json={"login": tt_user, "password": tt_pass}, timeout=10)
                            if auth_resp.status_code in (200, 201):
                                tt_token = auth_resp.json().get("data", {}).get("session-token", "")
                                st.session_state['_tt_session_token'] = tt_token
                    
                    if tt_token:
                        headers = {"Authorization": tt_token, "Content-Type": "application/json"}
                        
                        # Build OCC symbol
                        exp_date = next_date
                        date_str = exp_date.strftime("%y%m%d")
                        opt_char = "C" if trade_direction == "CALL" else "P"
                        strike_str = f"{int(strike * 1000):08d}"
                        occ_symbol = f"SPXW  {date_str}{opt_char}{strike_str}"
                        
                        quote_url = f"https://api.tastytrade.com/market-data/{occ_symbol}/quote"
                        quote_resp = req.get(quote_url, headers=headers, timeout=10)
                        
                        if quote_resp.status_code == 200:
                            q = quote_resp.json().get("data", {})
                            live_bid = float(q.get("bid", 0))
                            live_ask = float(q.get("ask", 0))
                            mid = (live_bid + live_ask) / 2 if live_bid and live_ask else 0
                            if mid > 0:
                                live_premium = mid
                                st.session_state['_live_premium'] = mid
                                st.session_state['_live_premium_hours'] = hours_now
                except Exception as e:
                    if manual_fetch:
                        st.warning(f"Could not fetch: {str(e)[:80]}")
            
            # Also check session state for previously fetched premium
            if not live_premium and '_live_premium' in st.session_state:
                live_premium = st.session_state['_live_premium']
                hours_now = st.session_state.get('_live_premium_hours', hours_now)
            
            # Project premiums at entry using actual trade levels
            scenarios = project_premium_at_scenarios(
                current_spx=current_price,
                strike=strike,
                vix=current_vix,
                opt_type=trade_direction,
                stop_price=stop_price,
                tp1_price=tp1,
                tp2_price=tp2,
                base_premium=live_premium,
                current_hours=hours_now,
                entry_hours=hours_at_entry,
            )
            
            # Determine which premium to use for the trade card
            final_premium = scenarios['at_entry']
            cost_per_contract = final_premium * 100
            num_contracts = 3
            total_cost = num_contracts * cost_per_contract
            
            # Source indicator
            if live_premium:
                premium_source = f"🔴 LIVE → Projected to {entry_timing}"
            else:
                premium_source = f"📐 Estimated at {entry_timing}"
            
            # ============================================================
            # SCENARIO TABLE
            # ============================================================
            render_section_banner("💰", "Premium Projections", "9:05 AM entry • Black-Scholes + live calibration", "#ffd740")
            if scenarios['calibrated']:
                st.caption(f"Calibrated from live pull: ${live_premium:.2f} (Bid ${live_bid:.2f} / Ask ${live_ask:.2f})")
            else:
                st.caption(f"Black-Scholes estimate • VIX: {current_vix:.1f} • {hours_at_entry:.1f}hrs to expiry")
            
            # Scenario cards
            scenario_data = [
                {"label": "AT ENTRY", "spx_label": f"SPX @ {current_price:.2f}", "premium": scenarios['at_entry'], 
                 "color": "#ccd6f6", "desc": "Your expected entry cost", "entry_premium": scenarios['at_entry']},
                {"label": "AT STOP ✋", "spx_label": f"SPX @ {stop_price:.2f}", "premium": scenarios['at_stop'],
                 "color": "#ff1744", "desc": f"Option value if stopped ({stop_line['short'] if stop_line else 'N/A'})", "entry_premium": scenarios['at_entry']},
                {"label": "AT TP1 🎯", "spx_label": f"SPX @ {tp1:.2f}", "premium": scenarios['at_tp1'],
                 "color": "#00e676", "desc": f"Option value at Target 1 ({tp1_name})", "entry_premium": scenarios['at_entry']},
                {"label": "AT TP2 🎯🎯", "spx_label": f"SPX @ {tp2:.2f}", "premium": scenarios['at_tp2'],
                 "color": "#00e676", "desc": f"Option value at Target 2 ({tp2_name})", "entry_premium": scenarios['at_entry']},
            ]
            render_scenario_cards(scenario_data, num_contracts)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Trade card — v2 unified card
            trade_color = '#ff5252' if trade_direction == 'PUT' else '#00e676'
            trade_icon = '🔻' if trade_direction == 'PUT' else '🔺'
            
            render_section_banner("📋", "Trade Card", "Complete trade plan")
            
            st.markdown(f"""
            <div class="tc" style="border-color:{trade_color}20;">
                <div class="tc-header">
                    <span class="tc-title" style="color:{trade_color};">{trade_icon} BUY {trade_direction} — SPX {strike}</span>
                    <span class="tc-meta">{otm_distance:.0f}pt OTM • 0DTE • {premium_source}</span>
                </div>
                <div class="tc-grid">
                    <div class="tc-cell">
                        <div class="tc-cell-label">Premium</div>
                        <div class="tc-cell-val" style="color:var(--t1);">${final_premium:.2f}</div>
                        <div class="tc-cell-sub">${cost_per_contract:.0f}/contract</div>
                    </div>
                    <div class="tc-cell">
                        <div class="tc-cell-label">Contracts</div>
                        <div class="tc-cell-val" style="color:var(--t1);">{num_contracts}</div>
                        <div class="tc-cell-sub">× ${cost_per_contract:.0f} ea</div>
                    </div>
                    <div class="tc-cell">
                        <div class="tc-cell-label">Total Risk</div>
                        <div class="tc-cell-val" style="color:var(--red);">${total_cost:,.0f}</div>
                        <div class="tc-cell-sub">Max loss = premium</div>
                    </div>
                </div>
                <div class="tc-grid" style="border-top:1px solid var(--border);">
                    <div class="tc-cell" style="background:rgba(255,23,68,0.03);">
                        <div class="tc-cell-label" style="color:var(--red);">Stop Loss</div>
                        <div class="tc-cell-val" style="color:var(--red);">{stop_price:.2f}</div>
                        <div class="tc-cell-sub">{stop_line['short'] if stop_line else 'Fixed'} • {abs(current_price - stop_price):.1f}pt</div>
                    </div>
                    <div class="tc-cell" style="background:rgba(0,230,118,0.03);">
                        <div class="tc-cell-label" style="color:var(--green);">Target 1</div>
                        <div class="tc-cell-val" style="color:var(--green);">{tp1:.2f}</div>
                        <div class="tc-cell-sub">{tp1_name} • {abs(current_price - tp1):.1f}pt</div>
                    </div>
                    <div class="tc-cell" style="background:rgba(0,230,118,0.03);">
                        <div class="tc-cell-label" style="color:var(--green);">Target 2</div>
                        <div class="tc-cell-val" style="color:var(--green);">{tp2:.2f}</div>
                        <div class="tc-cell-sub">{tp2_name} • {abs(current_price - tp2):.1f}pt</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Execution rules
            entry_line_label = f"{entry_line['short']} @ {entry_line['value']:.2f}" if entry_line else "N/A"
            st.markdown(f"""
            <div class="rules">
                <div class="rules-title">⏰ EXECUTION RULES</div>
                <div class="rules-body">
                    ENTRY LINE — {entry_line_label} ({'ascending ↗ resistance' if trade_direction == 'PUT' else 'descending ↘ support'})<br>
                    STRIKE — SPX {strike} {'P' if trade_direction == 'PUT' else 'C'} (20pt OTM from entry line)<br>
                    TIMING — {entry_timing}. {entry_timing_detail}<br>
                    ENTRY — Buy 3× SPX {strike} {'P' if trade_direction == 'PUT' else 'C'} @ ~${final_premium:.2f}<br>
                    STOP — Close ALL 3 if SPX {'rises above' if trade_direction == 'PUT' else 'drops below'} {stop_price:.2f} ({stop_line['short'] if stop_line else 'N/A'})<br>
                    TP1 — Close ALL 3 at SPX {tp1:.2f} ({tp1_name})<br>
                    TP2 — If TP1 missed, hold for {tp2:.2f} ({tp2_name})<br>
                    TIME STOP — Close by 11:00 AM CT if trade not working
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # No clear direction
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="sig neutral">
                <div style="font-family: Outfit, sans-serif; color: #ffd740; font-size: 1.2rem; letter-spacing: 2px;">
                    ⏸️ NO TRADE — WAIT FOR CLARITY
                </div>
                <div style="font-family: Rajdhani, sans-serif; color: #8892b0; font-size: 1rem; margin-top: 12px;">
                    Price is between conflicting lines. Wait for a break above or below to establish direction.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ============================================================
        # CONFLUENCE SCORE
        # ============================================================
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_section_banner("🔗", "Confluence Score", "5-factor alignment check", "#b388ff")
        
        # Auto-detect confluence from candle data
        candles_for_detection = st.session_state.get('last_fetch_candles', None)
        
        if trade_direction:
            auto = auto_detect_confluence(
                ny_trade_direction=trade_direction,
                ny_ladder=ny_ladder,
                current_price=current_price,
                candles_df=candles_for_detection,
                es_offset=es_offset_val
            )
            
            has_candle_data = candles_for_detection is not None and len(candles_for_detection) > 0
            
            # Show auto-detected values with detail
            if has_candle_data:
                st.caption("🤖 Auto-detected from candle data • Toggle overrides below if needed")
            else:
                st.caption("⚠️ No candle data — fetch data in Structural Map tab for auto-detection")
            
            # Use auto values as defaults, allow manual override
            allow_override = st.toggle("Manual Override", value=False, key="confluence_override",
                                        help="Override auto-detected values")
            
            if allow_override:
                col1, col2 = st.columns(2)
                with col1:
                    asian_aligns = st.checkbox("Asian session aligned", value=auto['asian_aligns'],
                                                help=auto['asian_detail'])
                    london_sweep = st.checkbox("London sweep confirmed", value=auto['london_sweep'],
                                                help=auto['london_detail'])
                    line_cluster = st.checkbox("Lines cluster within 5 pts", value=auto['line_cluster'],
                                                help=auto['cluster_detail'])
                with col2:
                    data_reaction = st.radio("7:30 AM Data Reaction", 
                                              ["aligned", "absorbed", "against"],
                                              index=["aligned", "absorbed", "against"].index(auto['data_reaction']),
                                              horizontal=True)
                    opening_drive = st.checkbox("Opening drive aligned", value=auto['opening_drive'],
                                                help=auto['opening_detail'])
            else:
                asian_aligns = auto['asian_aligns']
                london_sweep = auto['london_sweep']
                data_reaction = auto['data_reaction']
                opening_drive = auto['opening_drive']
                line_cluster = auto['line_cluster']
                
                # Show auto-detected details as styled rows
                factors_display = [
                    ("Asian Session", auto['asian_aligns'], auto['asian_detail']),
                    ("London Sweep", auto['london_sweep'], auto['london_detail']),
                    ("Data Reaction", auto['data_reaction'] == 'aligned', auto['data_detail']),
                    ("Opening Drive", auto['opening_drive'], auto['opening_detail']),
                    ("Line Cluster", auto['line_cluster'], auto['cluster_detail']),
                ]
                for name, passed, detail in factors_display:
                    icon = "✅" if passed else ("⚡" if "absorbed" in detail.lower() else "❌")
                    color = "#00e676" if passed else ("#ffd740" if "absorbed" in detail.lower() else "#ff5252")
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap: 10px; padding: 6px 12px; margin: 3px 0;
                                background: rgba(255,255,255,0.02); border-radius: 8px; border-left: 3px solid {color};">
                        <span style="font-size: 0.9rem;">{icon}</span>
                        <span style="font-family: Rajdhani, sans-serif; color: {color}; font-weight: 600; min-width: 120px;">{name}</span>
                        <span style="font-family: JetBrains Mono, monospace; color: #8892b0; font-size: 0.78rem;">{detail}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            asian_aligns = False
            london_sweep = False
            data_reaction = 'absorbed'
            opening_drive = False
            line_cluster = False
            st.info("Waiting for trade direction signal to calculate confluence...")
        
        confluence = calculate_confluence(asian_aligns, london_sweep, data_reaction,
                                          opening_drive, line_cluster)
        
        # Radial confluence gauge
        def render_confluence_gauge(score, factors, recommendation, color_class):
            import streamlit.components.v1 as components
            score_color = '#00e676' if color_class == 'high' else '#ffd740' if color_class == 'med' else '#ff1744'
            pct = score / 5.0
            dash_val = pct * 283  # circumference of r=45
            
            factors_json = ''.join([f'<div style="font-family:JetBrains Mono,monospace;font-size:11px;color:#8892b0;padding:3px 0;">{f}</div>' for f in factors])
            
            html = f"""
            <div style="text-align:center;padding:20px 0;">
              <svg width="160" height="160" viewBox="0 0 120 120" style="filter:drop-shadow(0 0 12px {score_color}40);">
                <circle cx="60" cy="60" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="8"/>
                <circle cx="60" cy="60" r="45" fill="none" stroke="{score_color}" stroke-width="8" 
                  stroke-dasharray="{dash_val} 283" stroke-dashoffset="0" stroke-linecap="round"
                  transform="rotate(-90 60 60)"
                  style="transition:stroke-dasharray 1s ease;">
                  <animate attributeName="stroke-dasharray" from="0 283" to="{dash_val} 283" dur="1s" fill="freeze"/>
                </circle>
                <text x="60" y="55" text-anchor="middle" font-family="Orbitron,monospace" font-size="24" font-weight="700" fill="{score_color}">{score}</text>
                <text x="60" y="72" text-anchor="middle" font-family="Rajdhani,sans-serif" font-size="10" fill="#5a6a8a">/5 CONFLUENCE</text>
              </svg>
              <div style="font-family:Rajdhani,sans-serif;color:{score_color};font-size:16px;font-weight:600;margin-top:8px;">
                {recommendation}
              </div>
              <div style="margin-top:12px;text-align:left;max-width:320px;margin-left:auto;margin-right:auto;">
                {factors_json}
              </div>
            </div>
            """
            components.html(html, height=320, scrolling=False)
        
        render_confluence_gauge(confluence['score'], confluence['factors'], 
                               confluence['recommendation'], confluence['color'])
    
    # ============================================================
    # ============================================================
    # TAB 2: ASIAN SESSION FUTURES — 6 PM DECISION FRAMEWORK
    # ============================================================
    with tab2:
        render_section_banner("🌙", "Asian Session — ES Futures", "Prop firm evaluation • 6:00 PM CT decision framework", "#b388ff")
        st.markdown("*6:00 PM Decision • 6-7 PM Trading Window • Flat by 7 PM*")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Determine correct overnight date
        prior_wd_tab2 = prior_date.weekday() if hasattr(prior_date, 'weekday') else datetime.combine(prior_date, time(0,0)).weekday()
        if prior_wd_tab2 == 4:  # Friday
            overnight_date_tab2 = next_date - timedelta(days=1)  # Sunday
            st.markdown("*⚠️ Friday → Monday: Globex opens Sunday 5:00 PM CT*")
        else:
            overnight_date_tab2 = prior_date
        
        # ============================================================
        # CALCULATE ALL LINE VALUES AT 6 PM CT
        # Lines are stored as SPX-adjusted if offset was applied.
        # For ES futures trading, add the offset back.
        # ============================================================
        decision_time_6pm = datetime.combine(overnight_date_tab2, time(18, 0))
        exit_time_7pm = datetime.combine(overnight_date_tab2, time(19, 0))
        
        # Get the offset — try widget key first, then session state
        es_offset_asian = st.session_state.get('global_es_offset', st.session_state.get('_es_offset', 0.0))
        
        st.markdown(f"""
        <div style="background: rgba(255,215,0,0.08); border: 1px solid rgba(255,215,0,0.3); 
                    border-radius: 8px; padding: 10px; margin: 5px 0; text-align:center;">
            <span style="font-family: JetBrains Mono; color: #ffd740; font-size: 0.85rem;">
                📐 ES-SPX Offset: <strong>{es_offset_asian:+.2f}</strong> 
                {'→ All levels shown in ES terms' if es_offset_asian != 0 else '→ No offset applied (set in sidebar Settings)'}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Build the full line ladder at 6 PM (in ES terms)
        line_ladder_6pm = []
        
        # All ascending lines (bounces + highest wick)
        for line in levels['ascending']:
            val_6pm = calculate_line_value(line['anchor_price'], line['anchor_time'], decision_time_6pm, 'ascending')
            val_7pm = calculate_line_value(line['anchor_price'], line['anchor_time'], exit_time_7pm, 'ascending')
            # Add offset back: SPX → ES
            val_6pm += es_offset_asian
            val_7pm += es_offset_asian
            line_ladder_6pm.append({
                'name': line['source'].split(' @ ')[0] if ' @ ' in line['source'] else line['source'],
                'short': f"{'HW' if line['type'] == 'highest_wick' else 'B'} ↗",
                'value_6pm': val_6pm,
                'value_7pm': val_7pm,
                'direction': 'ascending',
                'anchor': line['anchor_price'] + es_offset_asian,
                'color': '#ff1744' if line['type'] == 'highest_wick' else '#ff5252',
                'is_key': line['type'] == 'highest_wick',
            })
        
        # All descending lines (rejections + lowest wick)
        for line in levels['descending']:
            val_6pm = calculate_line_value(line['anchor_price'], line['anchor_time'], decision_time_6pm, 'descending')
            val_7pm = calculate_line_value(line['anchor_price'], line['anchor_time'], exit_time_7pm, 'descending')
            # Add offset back: SPX → ES
            val_6pm += es_offset_asian
            val_7pm += es_offset_asian
            line_ladder_6pm.append({
                'name': line['source'].split(' @ ')[0] if ' @ ' in line['source'] else line['source'],
                'short': f"{'LW' if line['type'] == 'lowest_wick' else 'R'} ↘",
                'value_6pm': val_6pm,
                'value_7pm': val_7pm,
                'direction': 'descending',
                'anchor': line['anchor_price'] + es_offset_asian,
                'color': '#00e676' if line['type'] == 'lowest_wick' else '#69f0ae',
                'is_key': line['type'] == 'lowest_wick',
            })
        
        # Sort by 6 PM value, highest to lowest
        line_ladder_6pm.sort(key=lambda x: x['value_6pm'], reverse=True)
        
        # ============================================================
        # 6 PM PRICE INPUT & TRADE SETUP
        # ============================================================
        render_section_banner("🎯", "6:00 PM Decision Framework", "Lock your price and map the trade", "#ffd740")
        
        # Auto-fill from live price if available
        asian_default = 6870.0
        if live_mode and live_price_data and live_price_data.get('ok'):
            # Only auto-update if NOT locked
            if not st.session_state.get('asian_6pm_locked', False):
                asian_default = live_price_data['price']  # ES price, no SPX offset for futures
                st.session_state['_asian_live_price'] = asian_default
            else:
                asian_default = st.session_state.get('_asian_locked_price', asian_default)
        
        col_price, col_lock = st.columns([3, 1])
        
        with col_price:
            asian_price = st.number_input("ES Price at 6:00 PM CT", 
                                           value=asian_default, step=0.25, format="%.2f",
                                           key="asian_es_price",
                                           help="Auto-fills from live ES price. Lock to freeze for trade planning.")
        
        with col_lock:
            st.markdown("<br>", unsafe_allow_html=True)  # spacing
            is_locked = st.session_state.get('asian_6pm_locked', False)
            
            if is_locked:
                locked_price = st.session_state.get('_asian_locked_price', 0)
                st.markdown(f"""
                <div style="font-family: JetBrains Mono; color: #ffd740; font-size: 0.8rem; text-align:center;">
                    🔒 Locked @ {locked_price:.2f}
                </div>""", unsafe_allow_html=True)
                if st.button("🔓 Unlock", key="unlock_asian", use_container_width=True):
                    st.session_state['asian_6pm_locked'] = False
                    st.rerun()
            else:
                if st.button("🔒 Lock 6PM Price", key="lock_asian", use_container_width=True):
                    st.session_state['asian_6pm_locked'] = True
                    st.session_state['_asian_locked_price'] = asian_price
                    st.rerun()
        
        max_move = st.number_input("Max expected move (pts)", value=5.0, step=0.5, format="%.1f",
                                    key="asian_max_move",
                                    help="Maximum points expected in the 6-7 PM window")
        
        # ── 6 PM Line Ladder with price position ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_section_banner("📊", "Line Ladder @ 6:00 PM CT", "Your position in the structural map", "#00d4ff")
        
        if line_ladder_6pm:
            render_visual_ladder(
                lines=[{
                    'value': l['value_6pm'], 'label': l['short'], 'full_name': l['name'],
                    'color': l['color'], 'direction': l['direction'], 
                    'is_key': 'HW' in l['short'] or 'LW' in l['short'] or 'HB' in l['short'] or 'LR' in l['short'],
                } for l in line_ladder_6pm],
                current_price=asian_price,
                title="6 PM Line Ladder",
                height=max(400, len(line_ladder_6pm) * 45),
            )
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        if line_ladder_6pm:
            # Find lines immediately above and below price
            lines_above = [l for l in line_ladder_6pm if l['value_6pm'] > asian_price]
            lines_below = [l for l in line_ladder_6pm if l['value_6pm'] <= asian_price]
            
            nearest_above = lines_above[-1] if lines_above else None  # closest above
            nearest_below = lines_below[0] if lines_below else None   # closest below
            second_above = lines_above[-2] if len(lines_above) >= 2 else None
            second_below = lines_below[1] if len(lines_below) >= 2 else None
            
            # Position description
            if nearest_above and nearest_below:
                gap = nearest_above['value_6pm'] - nearest_below['value_6pm']
                dist_above = nearest_above['value_6pm'] - asian_price
                dist_below = asian_price - nearest_below['value_6pm']
                
                position_text = f"Price is between **{nearest_above['short']}** ({nearest_above['value_6pm']:.2f}, {dist_above:.2f} pts above) and **{nearest_below['short']}** ({nearest_below['value_6pm']:.2f}, {dist_below:.2f} pts below). Gap: {gap:.2f} pts."
            elif nearest_above and not nearest_below:
                position_text = f"Price is **BELOW all lines**. Nearest above: {nearest_above['short']} at {nearest_above['value_6pm']:.2f}"
            elif nearest_below and not nearest_above:
                position_text = f"Price is **ABOVE all lines**. Nearest below: {nearest_below['short']} at {nearest_below['value_6pm']:.2f}"
            else:
                position_text = "No lines available"
            
            st.markdown(position_text)
            
            # Pre-calculate distances for trade setups
            dist_above = (nearest_above['value_6pm'] - asian_price) if nearest_above else 999
            dist_below = (asian_price - nearest_below['value_6pm']) if nearest_below else 999
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # ============================================================
            # GENERATE TRADE SETUPS
            # ============================================================
            render_section_banner("📋", "Trade Setups", "6:00 - 7:00 PM CT window • ES Futures", "#00e676")
            st.caption("Flat by 7:00 PM before Nikkei opens. Max hold: 1 hour.")
            
            trades = []
            
            # SETUP 1: SHORT — if there's resistance above and room to drop
            if nearest_above and nearest_below:
                # Short setup: price rallies to nearest line above, reject back down
                short_entry = nearest_above['value_6pm']
                short_stop = short_entry + 2.0
                short_t1 = asian_price  # back to current price
                short_t2 = nearest_below['value_6pm']  # to the line below
                short_exit_7pm = nearest_above['value_7pm']  # line moves by 7PM
                
                # Cap target at max_move
                if short_entry - short_t2 > max_move:
                    short_t2 = short_entry - max_move
                
                trades.append({
                    'direction': 'SHORT',
                    'bias': 'Rejection at resistance',
                    'trigger': f"Price rallies to {short_entry:.2f} ({nearest_above['short']})",
                    'entry': short_entry,
                    'stop': short_stop,
                    'target_1': short_t1,
                    'target_2': short_t2,
                    'risk': short_stop - short_entry,
                    'reward_1': short_entry - short_t1,
                    'reward_2': short_entry - short_t2,
                    'color': '#ff5252',
                    'icon': '🔻',
                })
                
                # Long setup: price drops to nearest line below, bounce back up
                long_entry = nearest_below['value_6pm']
                long_stop = long_entry - 2.0
                long_t1 = asian_price  # back to current price
                long_t2 = nearest_above['value_6pm']  # to the line above
                
                # Cap target at max_move
                if long_t2 - long_entry > max_move:
                    long_t2 = long_entry + max_move
                
                trades.append({
                    'direction': 'LONG',
                    'bias': 'Bounce at support',
                    'trigger': f"Price drops to {long_entry:.2f} ({nearest_below['short']})",
                    'entry': long_entry,
                    'stop': long_stop,
                    'target_1': long_t1,
                    'target_2': long_t2,
                    'risk': long_entry - long_stop,
                    'reward_1': long_t1 - long_entry,
                    'reward_2': long_t2 - long_entry,
                    'color': '#00e676',
                    'icon': '🔺',
                })
            
            # SETUP 2: Breakout — if price is already at or past a line
            if nearest_above and dist_above <= 1.0:
                # Price is right at resistance — could break through
                break_entry = nearest_above['value_6pm'] + 0.5
                break_stop = nearest_above['value_6pm'] - 1.5
                break_t1 = break_entry + 2.5
                break_t2 = break_entry + max_move
                if second_above:
                    break_t2 = min(break_t2, second_above['value_6pm'])
                
                trades.append({
                    'direction': 'LONG BREAKOUT',
                    'bias': f"Break above {nearest_above['short']}",
                    'trigger': f"Price breaks above {nearest_above['value_6pm']:.2f} with momentum",
                    'entry': break_entry,
                    'stop': break_stop,
                    'target_1': break_t1,
                    'target_2': break_t2,
                    'risk': break_entry - break_stop,
                    'reward_1': break_t1 - break_entry,
                    'reward_2': break_t2 - break_entry,
                    'color': '#ffd740',
                    'icon': '⚡',
                })
            
            if nearest_below and dist_below <= 1.0:
                break_entry = nearest_below['value_6pm'] - 0.5
                break_stop = nearest_below['value_6pm'] + 1.5
                break_t1 = break_entry - 2.5
                break_t2 = break_entry - max_move
                if second_below:
                    break_t2 = max(break_t2, second_below['value_6pm'])
                
                trades.append({
                    'direction': 'SHORT BREAKDOWN',
                    'bias': f"Break below {nearest_below['short']}",
                    'trigger': f"Price breaks below {nearest_below['value_6pm']:.2f} with momentum",
                    'entry': break_entry,
                    'stop': break_stop,
                    'target_1': break_t1,
                    'target_2': break_t2,
                    'risk': break_stop - break_entry,
                    'reward_1': break_entry - break_t1,
                    'reward_2': break_entry - break_t2,
                    'color': '#ffd740',
                    'icon': '⚡',
                })
            
            # ============================================================
            # DISPLAY TRADE CARDS
            # ============================================================
            for trade in trades:
                rr1 = trade['reward_1'] / trade['risk'] if trade['risk'] > 0 else 0
                rr2 = trade['reward_2'] / trade['risk'] if trade['risk'] > 0 else 0
                
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #131a2e 0%, #0d1220 100%);
                            border: 1px solid {trade['color']}33; border-radius: 12px;
                            padding: 16px; margin: 10px 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px;">
                        <span style="font-family: Orbitron; font-size: 1.2rem; color: {trade['color']};">
                            {trade['icon']} {trade['direction']}
                        </span>
                        <span style="font-family: Rajdhani; color: #8892b0; font-size: 0.85rem;">
                            {trade['bias']}
                        </span>
                    </div>
                    <div style="font-family: JetBrains Mono; font-size: 0.8rem; color: #5a6a8a; margin-bottom: 8px;">
                        Trigger: {trade['trigger']}
                    </div>
                    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 8px; text-align:center;">
                        <div>
                            <div style="font-family: Rajdhani; color: #5a6a8a; font-size: 0.7rem; text-transform:uppercase;">Entry</div>
                            <div style="font-family: JetBrains Mono; color: #ccd6f6; font-size: 1.1rem; font-weight:700;">{trade['entry']:.2f}</div>
                        </div>
                        <div>
                            <div style="font-family: Rajdhani; color: #5a6a8a; font-size: 0.7rem; text-transform:uppercase;">Stop</div>
                            <div style="font-family: JetBrains Mono; color: #ff1744; font-size: 1.1rem; font-weight:700;">{trade['stop']:.2f}</div>
                            <div style="font-family: JetBrains Mono; color: #5a6a8a; font-size: 0.7rem;">{trade['risk']:.1f} pts</div>
                        </div>
                        <div>
                            <div style="font-family: Rajdhani; color: #5a6a8a; font-size: 0.7rem; text-transform:uppercase;">Target 1</div>
                            <div style="font-family: JetBrains Mono; color: #00e676; font-size: 1.1rem; font-weight:700;">{trade['target_1']:.2f}</div>
                            <div style="font-family: JetBrains Mono; color: #5a6a8a; font-size: 0.7rem;">{trade['reward_1']:.1f} pts • {rr1:.1f}R</div>
                        </div>
                        <div>
                            <div style="font-family: Rajdhani; color: #5a6a8a; font-size: 0.7rem; text-transform:uppercase;">Target 2</div>
                            <div style="font-family: JetBrains Mono; color: #00e676; font-size: 1.1rem; font-weight:700;">{trade['target_2']:.2f}</div>
                            <div style="font-family: JetBrains Mono; color: #5a6a8a; font-size: 0.7rem;">{trade['reward_2']:.1f} pts • {rr2:.1f}R</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # ============================================================
            # RULES REMINDER
            # ============================================================
            st.markdown("""
            <div class="rules">
                <div style="font-family: Outfit, sans-serif; color: #ffd740; font-size: 0.9rem; margin-bottom: 10px; letter-spacing: 2px;">
                    ⏰ SESSION RULES
                </div>
                <div style="font-family: JetBrains Mono, monospace; color: #8892b0; font-size: 0.8rem; line-height: 2;">
                    5:00 PM — Globex opens. NO TRADES. Observe range formation.<br>
                    6:00 PM — DECISION POINT. Read price vs line ladder. Plan entries.<br>
                    6:00-7:00 PM — TRADING WINDOW. Execute setups. Max 5 pt move expected.<br>
                    7:00 PM — HARD CLOSE. Flatten all positions. Nikkei opens.
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: TRADE LOG — Daily Journal + Persistent Trade Storage
    # ============================================================
    with tab3:
        render_section_banner("📋", "Trade Log & Journal", "Daily journal • Trade tracking • Performance analytics", "#00d4ff")
        st.markdown("*Daily journal • Trade tracking • Performance analytics*")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ── File paths ──
        import os
        TRADE_LOG_FILE = os.path.expanduser("~/.spx_prophet_trades.json")
        JOURNAL_FILE = os.path.expanduser("~/.spx_prophet_journal.json")
        
        def load_trades() -> list:
            """Load trades from persistent JSON file."""
            try:
                if os.path.exists(TRADE_LOG_FILE):
                    with open(TRADE_LOG_FILE, 'r') as f:
                        return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
            return []
        
        def save_trades(trades: list):
            """Save trades to persistent JSON file."""
            try:
                with open(TRADE_LOG_FILE, 'w') as f:
                    json.dump(trades, f, indent=2)
            except IOError as e:
                st.error(f"Could not save trades: {e}")
        
        def load_journal() -> dict:
            """Load journal entries from persistent JSON file. Keys are date strings."""
            try:
                if os.path.exists(JOURNAL_FILE):
                    with open(JOURNAL_FILE, 'r') as f:
                        return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
            return {}
        
        def save_journal(journal: dict):
            """Save journal entries to persistent JSON file."""
            try:
                with open(JOURNAL_FILE, 'w') as f:
                    json.dump(journal, f, indent=2)
            except IOError as e:
                st.error(f"Could not save journal: {e}")
        
        # ── DAILY JOURNAL SECTION ──
        render_section_banner("📝", "Daily Journal", "Rich text notes with auto-save", "#ffd740")
        
        journal_data = load_journal()
        journal_date = st.date_input("Journal Date", value=datetime.now().date(), key="journal_date")
        journal_key = str(journal_date)
        
        # Load existing entry for this date
        existing_entry = journal_data.get(journal_key, {})
        existing_content = existing_entry.get('content', '')
        existing_tags = existing_entry.get('tags', [])
        
        # Try to use streamlit-quill for rich text; fall back to text_area
        try:
            from streamlit_quill import st_quill
            
            st.caption("Rich text editor • Your entries are saved per date")
            
            journal_content = st_quill(
                value=existing_content,
                html=True,
                toolbar=[
                    ['bold', 'italic', 'underline', 'strike'],
                    [{'header': [1, 2, 3, False]}],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                    [{'color': []}, {'background': []}],
                    ['link'],
                    ['clean'],
                ],
                key=f"journal_quill_{journal_key}",
                placeholder="What happened today? Pre-market plan, session observations, lessons learned..."
            )
        except ImportError:
            st.caption("Text editor • Install `streamlit-quill` for rich text formatting")
            journal_content = st.text_area(
                "Journal Entry",
                value=existing_content,
                height=250,
                key=f"journal_text_{journal_key}",
                placeholder="What happened today? Pre-market plan, session observations, lessons learned...",
                label_visibility="collapsed"
            )
        
        # Quick tags
        tag_options = ["📈 Green Day", "📉 Red Day", "😐 Flat", "🎯 Hit All Targets", 
                       "✋ Stopped Out", "⏰ Time Stopped", "🧠 Lesson Learned", 
                       "💎 Diamond Hands", "🐔 Chickened Out", "📊 High Confluence"]
        
        # Pre-select existing tags
        default_tags = [t for t in existing_tags if t in tag_options]
        journal_tags = st.pills("Quick Tags", tag_options, selection_mode="multi", 
                                default=default_tags, key=f"journal_tags_{journal_key}")
        
        jcol1, jcol2, jcol3 = st.columns([1, 1, 2])
        with jcol1:
            if st.button("💾 Save Entry", use_container_width=True, key="save_journal"):
                journal_data[journal_key] = {
                    'content': journal_content if journal_content else '',
                    'tags': list(journal_tags) if journal_tags else [],
                    'updated': datetime.now().isoformat(),
                }
                save_journal(journal_data)
                st.success("Journal saved!")
        
        with jcol2:
            if st.button("🗑️ Clear Entry", use_container_width=True, key="clear_journal"):
                if journal_key in journal_data:
                    del journal_data[journal_key]
                    save_journal(journal_data)
                    st.success("Entry cleared.")
                    st.rerun()
        
        # Show recent journal entries
        if len(journal_data) > 0:
            sorted_dates = sorted(journal_data.keys(), reverse=True)
            recent_dates = [d for d in sorted_dates if d != journal_key][:5]
            
            if recent_dates:
                with st.expander(f"📖 Recent Entries ({len(journal_data)} total)", expanded=False):
                    for jd in recent_dates:
                        entry = journal_data[jd]
                        content_preview = entry.get('content', '')
                        # Strip HTML for preview
                        import re
                        text_only = re.sub(r'<[^>]+>', '', content_preview)[:120]
                        tags_str = ' '.join(entry.get('tags', []))
                        
                        st.markdown(f"""
                        <div style="padding: 10px 14px; margin: 4px 0; border-left: 3px solid rgba(0,212,255,0.3);
                                    background: rgba(255,255,255,0.02); border-radius: 0 8px 8px 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-family: Outfit, sans-serif; color: #00d4ff; font-size: 0.8rem;">{jd}</span>
                                <span style="font-size: 0.75rem;">{tags_str}</span>
                            </div>
                            <div style="font-family: Rajdhani, sans-serif; color: #8892b0; font-size: 0.85rem; margin-top: 4px;">
                                {text_only}{'...' if len(text_only) >= 120 else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # ── SECTION DIVIDER ──
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ── TRADE LOG SECTION ──
        render_section_banner("💰", "Trade Log", "Record and track every trade", "#00e676")
        
        def calculate_pnl(session, direction, entry, exit_price, contracts, premium_per_contract=0):
            """Calculate P&L based on session type."""
            if "Futures" in session:
                # ES futures: $50 per point per contract (MES: $5)
                pnl_per_point = 5  # MES default — user can override
                mult = 1 if direction == "LONG" else -1
                pnl = mult * (exit_price - entry) * contracts * pnl_per_point
            else:
                # SPX options: premium-based
                # Entry cost = premium × 100 × contracts
                # Exit value = exit_premium × 100 × contracts  
                # For simplicity: user enters entry/exit as premium per share
                mult = 1  # options are always long (buy to open)
                pnl = (exit_price - entry) * 100 * contracts
            return round(pnl, 2)
        
        # Load persistent trades
        all_trades = load_trades()
        
        # ── Log New Trade ──
        with st.expander("➕ Log New Trade", expanded=len(all_trades) == 0):
            tcol1, tcol2 = st.columns(2)
            
            with tcol1:
                trade_date = st.date_input("Trade Date", value=datetime.now().date(), key="trade_date")
                trade_session = st.selectbox("Session", ["NY (Options)", "Asian (Futures)"], key="trade_sess")
                trade_direction_input = st.selectbox("Direction", 
                    ["PUT", "CALL"] if "Options" in trade_session else ["LONG", "SHORT"],
                    key="trade_dir")
                trade_confluence_input = st.slider("Confluence Score", 0.0, 5.0, 3.0, 0.5, key="trade_conf")
            
            with tcol2:
                if "Options" in trade_session:
                    trade_strike = st.number_input("Strike", value=6845, step=5, key="trade_strike")
                    trade_entry_premium = st.number_input("Entry Premium (per share)", value=6.50, step=0.25, format="%.2f", key="trade_entry_prem")
                    trade_exit_premium = st.number_input("Exit Premium (per share)", value=9.00, step=0.25, format="%.2f", key="trade_exit_prem")
                    trade_contracts_input = st.number_input("Contracts", value=3, min_value=1, key="trade_contracts")
                else:
                    trade_entry_price = st.number_input("Entry Price", value=6865.0, step=0.25, key="trade_entry_es")
                    trade_exit_price = st.number_input("Exit Price", value=6870.0, step=0.25, key="trade_exit_es")
                    trade_contracts_input = st.number_input("Contracts (MES)", value=2, min_value=1, key="trade_contracts_es")
                    trade_strike = 0
                    trade_entry_premium = trade_entry_price
                    trade_exit_premium = trade_exit_price
            
            trade_result = st.selectbox("Result", ["Win", "Loss", "Breakeven", "Stopped Out", "Time Stop"], key="trade_result")
            trade_notes_input = st.text_input("Notes", key="trade_notes", placeholder="What worked? What didn't?")
            
            # Preview P&L
            if "Options" in trade_session:
                preview_pnl = (trade_exit_premium - trade_entry_premium) * 100 * trade_contracts_input
                preview_cost = trade_entry_premium * 100 * trade_contracts_input
                st.markdown(f"""
                <div style="font-family: JetBrains Mono, monospace; font-size: 0.85rem; color: #8892b0; padding: 8px 0;">
                    Entry: {trade_contracts_input}× ${trade_entry_premium:.2f} = <span style="color:#ccd6f6;">${preview_cost:,.0f}</span> &nbsp;→&nbsp;
                    P&L: <span style="color: {'#00e676' if preview_pnl >= 0 else '#ff1744'}; font-weight:700;">${preview_pnl:+,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                mult = 1 if trade_direction_input == "LONG" else -1
                preview_pnl = mult * (trade_exit_price - trade_entry_price) * trade_contracts_input * 5
                st.markdown(f"""
                <div style="font-family: JetBrains Mono, monospace; font-size: 0.85rem; color: #8892b0; padding: 8px 0;">
                    {trade_direction_input} {trade_contracts_input} MES @ {trade_entry_price:.2f} → {trade_exit_price:.2f} &nbsp;→&nbsp;
                    P&L: <span style="color: {'#00e676' if preview_pnl >= 0 else '#ff1744'}; font-weight:700;">${preview_pnl:+,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            save_col1, save_col2 = st.columns([1, 3])
            with save_col1:
                if st.button("💾 Save Trade", use_container_width=True):
                    if "Options" in trade_session:
                        pnl = (trade_exit_premium - trade_entry_premium) * 100 * trade_contracts_input
                    else:
                        mult = 1 if trade_direction_input == "LONG" else -1
                        pnl = mult * (trade_exit_price - trade_entry_price) * trade_contracts_input * 5
                    
                    new_trade = {
                        'id': f"{trade_date}_{len(all_trades)+1}",
                        'date': str(trade_date),
                        'session': trade_session,
                        'direction': trade_direction_input,
                        'strike': trade_strike if "Options" in trade_session else 0,
                        'entry': trade_entry_premium if "Options" in trade_session else trade_entry_price,
                        'exit': trade_exit_premium if "Options" in trade_session else trade_exit_price,
                        'contracts': trade_contracts_input,
                        'pnl': round(pnl, 2),
                        'confluence': trade_confluence_input,
                        'result': trade_result,
                        'notes': trade_notes_input,
                    }
                    all_trades.append(new_trade)
                    save_trades(all_trades)
                    st.success(f"Trade saved! P&L: ${pnl:+,.0f}")
                    st.rerun()
        
        # ── Performance Dashboard ──
        if all_trades:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            render_section_banner("📊", "Performance Dashboard", "Equity curve • Win rate • Statistics", "#00d4ff")
            
            df_trades = pd.DataFrame(all_trades)
            df_trades['pnl'] = pd.to_numeric(df_trades['pnl'], errors='coerce').fillna(0)
            df_trades['date'] = pd.to_datetime(df_trades['date'])
            
            total_pnl = df_trades['pnl'].sum()
            total_trades = len(df_trades)
            wins = len(df_trades[df_trades['pnl'] > 0])
            losses = len(df_trades[df_trades['pnl'] < 0])
            breakevens = total_trades - wins - losses
            win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
            avg_win = df_trades[df_trades['pnl'] > 0]['pnl'].mean() if wins > 0 else 0
            avg_loss = df_trades[df_trades['pnl'] < 0]['pnl'].mean() if losses > 0 else 0
            profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
            best_trade = df_trades['pnl'].max()
            worst_trade = df_trades['pnl'].min()
            
            # Equity curve
            df_trades_sorted = df_trades.sort_values('date')
            df_trades_sorted['cumulative_pnl'] = df_trades_sorted['pnl'].cumsum()
            
            # Running max for drawdown
            df_trades_sorted['peak'] = df_trades_sorted['cumulative_pnl'].cummax()
            df_trades_sorted['drawdown'] = df_trades_sorted['cumulative_pnl'] - df_trades_sorted['peak']
            max_drawdown = df_trades_sorted['drawdown'].min()
            
            # ── Summary Cards ──
            pnl_color = "bull" if total_pnl >= 0 else "bear"
            wr_color = "bull" if win_rate >= 50 else ("neutral" if win_rate >= 40 else "bear")
            
            c1, c2, c3, c4 = st.columns(4)
            pnl_met_color = '#00e676' if total_pnl >= 0 else '#ff1744'
            wr_met_color = '#00e676' if win_rate >= 50 else ('#ffd740' if win_rate >= 40 else '#ff1744')
            pf_met_color = '#00e676' if profit_factor >= 1.5 else ('#ffd740' if profit_factor >= 1.0 else '#ff1744')
            
            render_metric_row([
                {'label': 'Total P&L', 'value': f'${total_pnl:+,.0f}', 'subtitle': f'{total_trades} trades', 'color': pnl_met_color},
                {'label': 'Win Rate', 'value': f'{win_rate:.0f}%', 'subtitle': f'{wins}W / {losses}L / {breakevens}BE', 'color': wr_met_color},
                {'label': 'Profit Factor', 'value': f'{profit_factor:.2f}', 'subtitle': f'Avg W: ${avg_win:+,.0f} / L: ${avg_loss:+,.0f}', 'color': pf_met_color},
                {'label': 'Max Drawdown', 'value': f'${max_drawdown:,.0f}', 'subtitle': f'Best: ${best_trade:+,.0f} / Worst: ${worst_trade:+,.0f}', 'color': '#ff1744'},
            ])
            
            # ── Equity Curve Chart ──
            if len(df_trades_sorted) >= 2:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                render_section_banner("📈", "Equity Curve", "Cumulative P&L over time", "#00d4ff")
                
                eq_fig = go.Figure()
                
                # Equity line with fill
                eq_fig.add_trace(go.Scatter(
                    x=df_trades_sorted['date'], 
                    y=df_trades_sorted['cumulative_pnl'],
                    mode='lines+markers',
                    name='Equity',
                    line=dict(color='#00d4ff', width=2.5),
                    marker=dict(size=6, color=df_trades_sorted['pnl'].apply(lambda x: '#00e676' if x >= 0 else '#ff1744')),
                    fill='tozeroy',
                    fillcolor='rgba(0,212,255,0.06)',
                    hovertemplate='<b>%{x|%b %d}</b><br>Equity: $%{y:+,.0f}<extra></extra>'
                ))
                
                # Zero line
                eq_fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.1)", line_width=1)
                
                # Drawdown shading
                if max_drawdown < 0:
                    eq_fig.add_trace(go.Scatter(
                        x=df_trades_sorted['date'],
                        y=df_trades_sorted['drawdown'],
                        mode='lines',
                        name='Drawdown',
                        line=dict(color='#ff1744', width=1, dash='dot'),
                        fill='tozeroy',
                        fillcolor='rgba(255,23,68,0.06)',
                        hovertemplate='Drawdown: $%{y:,.0f}<extra></extra>'
                    ))
                
                eq_fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(5,8,16,1)',
                    plot_bgcolor='rgba(8,13,22,1)',
                    height=350,
                    margin=dict(l=10, r=20, t=10, b=40),
                    xaxis=dict(
                        gridcolor='rgba(30,45,74,0.12)', showgrid=True,
                        tickfont=dict(family='Rajdhani', size=11, color='#3a4a6a'),
                    ),
                    yaxis=dict(
                        gridcolor='rgba(30,45,74,0.12)', showgrid=True,
                        tickformat='$,.0f', side='right',
                        tickfont=dict(family='JetBrains Mono', size=11, color='#5a6a8a'),
                    ),
                    legend=dict(bgcolor='rgba(6,9,16,0.95)', font=dict(size=10, family='JetBrains Mono', color='#8892b0')),
                    font=dict(family='JetBrains Mono', color='#8892b0'),
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='rgba(6,9,16,0.95)', bordercolor='rgba(0,212,255,0.2)',
                        font=dict(family='JetBrains Mono', size=11, color='#ccd6f6')),
                )
                st.plotly_chart(eq_fig, use_container_width=True)
            
            # ── Win Rate by Confluence ──
            if len(df_trades) >= 3:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown("### 🎯 Win Rate by Confluence Score")
                
                conf_groups = df_trades.groupby(df_trades['confluence'].apply(lambda x: f"{x:.0f}+")).agg(
                    trades=('pnl', 'count'),
                    wins=('pnl', lambda x: (x > 0).sum()),
                    total_pnl=('pnl', 'sum'),
                ).reset_index()
                conf_groups['win_rate'] = (conf_groups['wins'] / conf_groups['trades'] * 100).round(0)
                
                for _, row in conf_groups.iterrows():
                    wr = row['win_rate']
                    wr_bar_color = '#00e676' if wr >= 60 else ('#ffd740' if wr >= 45 else '#ff5252')
                    pnl_val = row['total_pnl']
                    pnl_color_str = '#00e676' if pnl_val >= 0 else '#ff1744'
                    bar_width = max(5, wr)
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap: 12px; padding: 8px 14px; margin: 3px 0;
                                background: rgba(255,255,255,0.02); border-radius: 8px;">
                        <span style="font-family: Outfit, sans-serif; color: #ccd6f6; font-size: 0.85rem; min-width: 50px;">
                            {row['confluence']}
                        </span>
                        <div style="flex:1; height: 20px; background: rgba(255,255,255,0.03); border-radius: 4px; overflow:hidden;">
                            <div style="height:100%; width:{bar_width}%; background: {wr_bar_color}; border-radius: 4px; 
                                        transition: width 0.5s ease;"></div>
                        </div>
                        <span style="font-family: JetBrains Mono, monospace; color: {wr_bar_color}; font-size: 0.85rem; min-width: 45px; text-align:right;">
                            {wr:.0f}%
                        </span>
                        <span style="font-family: JetBrains Mono, monospace; color: {pnl_color_str}; font-size: 0.8rem; min-width: 70px; text-align:right;">
                            ${pnl_val:+,.0f}
                        </span>
                        <span style="font-family: Rajdhani, sans-serif; color: #3a4a6a; font-size: 0.75rem; min-width: 50px;">
                            {int(row['trades'])} trades
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # ── Trade History Table ──
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📋 Trade History")
            
            # Format for display
            display_df = df_trades_sorted[['date', 'session', 'direction', 'strike', 'entry', 'exit', 
                                            'contracts', 'pnl', 'confluence', 'result', 'notes']].copy()
            display_df['date'] = display_df['date'].dt.strftime('%b %d')
            display_df.columns = ['Date', 'Session', 'Dir', 'Strike', 'Entry', 'Exit', 'Qty', 'P&L', 'Conf', 'Result', 'Notes']
            
            # Style the dataframe
            def style_pnl(val):
                if isinstance(val, (int, float)):
                    color = '#00e676' if val >= 0 else '#ff1744'
                    return f'color: {color}; font-weight: bold'
                return ''
            
            st.dataframe(
                display_df.style.applymap(style_pnl, subset=['P&L']),
                use_container_width=True, hide_index=True, height=400
            )
            
            # ── Delete Trade ──
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.expander("🗑️ Delete a Trade"):
                if all_trades:
                    trade_options = [f"{t['date']} | {t['direction']} | ${t['pnl']:+,.0f} | {t.get('notes','')[:30]}" for t in all_trades]
                    delete_idx = st.selectbox("Select trade to delete", range(len(trade_options)), format_func=lambda i: trade_options[i])
                    
                    dc1, dc2 = st.columns([1, 3])
                    with dc1:
                        if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                            all_trades.pop(delete_idx)
                            save_trades(all_trades)
                            st.success("Trade deleted.")
                            st.rerun()
            
            # ── Export ──
            with st.expander("📤 Export Trades"):
                export_col1, export_col2 = st.columns(2)
                with export_col1:
                    csv_data = display_df.to_csv(index=False)
                    st.download_button("📥 Download CSV", csv_data, "spx_prophet_trades.csv", "text/csv",
                                        use_container_width=True)
                with export_col2:
                    json_data = json.dumps(all_trades, indent=2)
                    st.download_button("📥 Download JSON", json_data, "spx_prophet_trades.json", "application/json",
                                        use_container_width=True)
        
        else:
            st.markdown("""
            <div class="signal-box-neutral" style="text-align:center; animation: none;">
                <div style="font-family: Outfit, sans-serif; color: #ffd740; font-size: 1.1rem; letter-spacing: 2px;">
                    NO TRADES LOGGED YET
                </div>
                <div style="font-family: Rajdhani, sans-serif; color: #8892b0; font-size: 1rem; margin-top: 10px;">
                    Start tracking your trades to build your performance history.
                </div>
            </div>
            """, unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()
