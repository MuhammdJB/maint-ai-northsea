import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

# ================= CONFIGURATION =================
st.set_page_config(
    page_title="maintAI | North Sea",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= PRO CSS =================
st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    div[data-testid="stDataFrame"] { border: 1px solid #333; border-radius: 8px; background-color: #161B22; }
    
    /* KPI Cards */
    .kpi-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00Cca3;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        text-align: center;
    }
    .kpi-value { font-size: 28px; font-weight: bold; color: #FFFFFF; }
    .kpi-label { font-size: 12px; color: #A0A0A0; text-transform: uppercase; margin-top: 5px;}
    
    /* Tech Card */
    .tech-card { background-color: #2b2d3e; border: 1px solid #444; padding: 15px; border-radius: 8px; font-size: 13px; }
    .wo-ticket { background-color: #1F2937; border: 1px dashed #00Cca3; padding: 30px; border-radius: 15px; margin-top: 20px; }
    .ticket-header { color: #00Cca3; font-size: 20px; font-weight: bold; border-bottom: 1px solid #444; padding-bottom: 10px; margin-bottom: 15px; }
    .ticket-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 15px; }
    .ticket-label { color: #BBB; } 
    .ticket-val { color: #FFF; font-weight: 600; } 
    .alert-critical { background-color: #3d0c0c; color: #ff6b6b; padding: 15px; border-radius: 8px; border: 1px solid #ff6b6b; font-weight: 500; margin-top: 15px; }
    
    /* Buttons */
    div.stButton > button { background-color: #262730; color: white; border: 1px solid #444; font-weight: 600; }
    div.stButton > button:hover { border-color: #00Cca3; color: #00Cca3; }
</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "step" not in st.session_state: st.session_state.step = 1
def go_next(): st.session_state.step += 1
def go_back(): 
    if st.session_state.step > 1: st.session_state.step -= 1
def reset_workflow(): st.session_state.step = 1

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## maintAI")
    st.caption("North Sea Operations")
    st.markdown("---")
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Workflows", "Fault Reports", "Work Orders", "Schedule"],
        icons=["grid-1x2", "diagram-3", "graph-up", "clipboard-check", "calendar-range"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00Cca3", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "margin":"5px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#00857A"},
        }
    )

# ================= PAGE 1: HOME (MAP FIXED) =================
if selected_page == "Home":
    st.title("🚀 Command Center")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown('<div class="kpi-card"><div class="kpi-value">88%</div><div class="kpi-label">Health Score</div></div>', unsafe_allow_html=True)
    k2.markdown('<div class="kpi-card"><div class="kpi-value">14</div><div class="kpi-label">Open Critical WOs</div></div>', unsafe_allow_html=True)
    k3.markdown('<div class="kpi-card"><div class="kpi-value">£185k</div><div class="kpi-label">Maint. Spend</div></div>', unsafe_allow_html=True)
    k4.markdown('<div class="kpi-card"><div class="kpi-value">92%</div><div class="kpi-label">PM Compliance</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Asset Location: North Sea")
        
        # --- NEW VISIBLE MAP LOGIC ---
        fig = go.Figure()

        # 1. Asset Point (Green Pulse)
        fig.add_trace(go.Scattermapbox(
            lat=[57.8], lon=[1.6],
            mode='markers+text',
            marker=go.scattermapbox.Marker(size=25, color='#00Cca3', opacity=0.9),
            text=["Offshore Asset A"],
            textposition="top center",
            name="Asset"
        ))
        
        # 2. Field Boundary (Visual)
        fig.add_trace(go.Scattermapbox(
            lat=[57.8], lon=[1.6],
            mode='markers',
            marker=go.scattermapbox.Marker(size=80, color='#00Cca3', opacity=0.3),
            hoverinfo='none',
        ))

        fig.update_layout(
            # STYLE CHANGED TO 'open-street-map' for maximum visibility
            mapbox_style="open-street-map",
            mapbox=dict(
                center=dict(lat=57.0, lon=0.5), # Centered to show UK coast
                zoom=5 # Wide enough to see land
            ),
            margin={"r":0,"t":0,"l":0,"b":0},
            height=450,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Criticality Breakdown")
        labels = ['High (A)', 'Medium (B)', 'Low (C)']
        values = [15, 45, 40]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=14), legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color='white')))
        fig.update_traces(marker=dict(colors=['#FF4B4B', '#FFAA00', '#00Cca3']))
        st.plotly_chart(fig, use_container_width=True)

# ================= OTHER PAGES (Same as before) =================
elif selected_page == "Fault Reports":
    st.title("📉 Fault & Anomaly Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Top Failure Modes")
        data = pd.DataFrame({"Mode": ["Seal Leak", "Vibration High", "Corrosion", "Bearing Wear", "Elec Trip"], "Count": [24, 18, 12, 9, 5]})
        fig = px.bar(data, x="Count", y="Mode", orientation='h', color="Count", color_continuous_scale="Teal")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("### 12-Month Trend")
        dates = pd.date_range(start='1/1/2025', periods=12, freq='M'); trend = [5, 4, 6, 8, 12, 15, 10, 8, 6, 5, 4, 3]
        fig2 = px.line(x=dates, y=trend, markers=True)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)); fig2.update_traces(line_color='#FF4B4B')
        st.plotly_chart(fig2, use_container_width=True)

elif selected_page == "Work Orders":
    st.title("🛠️ Work Order Management")
    col1, col2 = st.columns([3, 1]); col1.markdown("Manage corrective and preventive maintenance tasks."); col2.button("＋ Create WO", type="primary")
    wo_data = pd.DataFrame({
        "WO ID": ["WO-1001", "WO-1002", "WO-1003", "WO-1004", "WO-1005"],
        "Description": ["Pump P-101 Seal Replacement", "Vibration Analysis on Compressor", "Annual Safety Valve Test", "Lighting Circuit Repair", "Heat Exchanger Cleaning"],
        "Functional Loc": ["NS-PROD-PUMP-01", "NS-COMP-02", "NS-SAFE-PSV-05", "NS-UTIL-LIGHT-09", "NS-PROC-HEX-03"],
        "Priority": ["High", "Medium", "High", "Low", "Medium"], "Status": ["In Progress", "Open", "Scheduled", "Completed", "Open"]
    })
    st.dataframe(wo_data, use_container_width=True, hide_index=True, column_config={"Status": st.column_config.SelectboxColumn("Status", options=["Open", "In Progress", "Completed"], required=True)})
    st.markdown("### Budget Utilization"); budget_data = pd.DataFrame({"Category": ["Mechanical", "Electrical", "Instrumentation"], "Spent": [45000, 12000, 30000], "Budget": [50000, 20000, 35000]})
    fig = go.Figure(data=[go.Bar(name='Spent', x=budget_data['Category'], y=budget_data['Spent'], marker_color='#FF4B4B'), go.Bar(name='Budget', x=budget_data['Category'], y=budget_data['Budget'], marker_color='#00Cca3')])
    fig.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=300, legend=dict(font=dict(color='white'))); st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Schedule":
    st.title("🗓️ Optimization Schedule")
    df_gantt = pd.DataFrame([dict(Task="NS-6009 Review", Start='2026-01-01', Finish='2026-01-05', Resource="Engineer A"), dict(Task="Pump 101 Overhaul", Start='2026-01-10', Finish='2026-01-20', Resource="Tech B"), dict(Task="Safety Audit", Start='2026-01-15', Finish='2026-02-01', Resource="Team C"), dict(Task="Shutdown Window", Start='2026-02-05', Finish='2026-02-15', Resource="Plant")])
    fig = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Resource", title="Project Timeline")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), legend=dict(font=dict(color='white'))); st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Workflows":
    steps = ["Selection", "Overview", "Analysis", "Effectiveness", "Solutions", "Execute"]
    progress = st.session_state.step / 6
    st.progress(progress); st.caption(f"PHASE: {steps[st.session_state.step-1].upper()}")
    def nav_buttons(next_label="Next ➜"):
        st.markdown("<br>", unsafe_allow_html=True); c1, c2, c3 = st.columns([1, 4, 1]); c1.button("⬅ Back", on_click=go_back, key=f"back_{st.session_state.step}"); c3.button(next_label, type="primary", on_click=go_next, key=f"next_{st.session_state.step}")

    if st.session_state.step == 1:
        st.header("Step 1: Equipment Selection"); c1, c2 = st.columns([3, 1]); c1.text_input("Search Tag", "NS-6009"); c2.write("##"); c2.button("Begin ➜", type="primary", on_click=go_next)
    elif st.session_state.step == 2:
        st.header("Step 2: Operational Context"); st.info("ℹ️ Asset is located in hazardous zone (Zone 1). Permit required."); st.markdown("""<div style="background-color:#161B22; padding:20px; border-radius:10px; border:1px solid #333;"><h2 style="margin:0; color:#00Cca3">NS-6009</h2><p><b>Site:</b> North Sea Field | <b>System:</b> Separation</p><p><b>Description:</b> MVR Reboiler Unit - Criticality A</p></div>""", unsafe_allow_html=True); nav_buttons()
    elif st.session_state.step == 3:
        st.header("Step 3: Failure Analysis"); k1, k2, k3, k4 = st.columns(4); k1.markdown('<div class="kpi-card"><div class="kpi-value">12</div><div class="kpi-label">MTBF (Mo)</div></div>', unsafe_allow_html=True); k2.markdown('<div class="kpi-card"><div class="kpi-value">4</div><div class="kpi-label">MTTR (Hrs)</div></div>', unsafe_allow_html=True); k3.markdown('<div class="kpi-card"><div class="kpi-value">99%</div><div class="kpi-label">Uptime</div></div>', unsafe_allow_html=True); k4.markdown('<div class="kpi-card"><div class="kpi-value">1</div><div class="kpi-label">Fail/Yr</div></div>', unsafe_allow_html=True); nav_buttons()
    elif st.session_state.step == 4:
        st.header("Step 4: Effectiveness Review"); comp_data = pd.DataFrame({"Failure Mode": ["Vibration", "Seal Leak", "Corrosion"], "Current Task": ["None", "Visual Check", "3-Year Paint"], "Effectiveness": ["Low", "Low", "Medium"], "Gap Analysis": ["CRITICAL", "High", "None"]}); st.dataframe(comp_data, use_container_width=True, hide_index=True); st.markdown("""<div class="alert-critical">🚨 CRITICAL GAP: No Vibration Monitoring task found for MVR unit.</div>""", unsafe_allow_html=True); nav_buttons()
    elif st.session_state.step == 5:
        st.header("Step 5: Define & Approve Solutions"); st.markdown("### 🛠️ Strategic Recommendations"); c1, c2 = st.columns([1, 1])
        with c1: st.info("**Option 1: Material Upgrade**"); st.image("https://www.martins-rubber.co.uk/wp-content/uploads/2018/06/viton-o-rings.jpg", width=200, caption="Viton (FKM) High-Temp Seal"); st.markdown("""<div class="tech-card"><b>Tech Spec:</b> Fluoroelastomer (FKM)<br><b>Temp Rating:</b> -20°C to +200°C<br><b>Chemical Resistance:</b> Excellent for Hydrocarbons<br><b>Benefit:</b> Current Nitrile seals degrade at 100°C. Since MVR Reboiler operates at 110°C, Viton prevents the recurring leaks.</div>""", unsafe_allow_html=True)
        with c2: st.info("**Option 2: Predictive Monitoring**"); st.write("Deploy wireless vibration sensor."); st.write("**Cost:** £500/year | **ROI:** 24x")
        st.markdown("---"); st.markdown("### 📝 Approval Decision")
        with st.form("approval_form"):
            selected_actions = st.multiselect("Select Actions to Approve:", ["Upgrade Seal to Viton (Code: MAT-99)", "Install Vib Sensor (Code: IOT-04)", "Decommission Visual Check"])
            comments = st.text_area("Engineering Justification", "Viton upgrade selected to address thermal degradation root cause.")
            submitted = st.form_submit_button("Approve & Generate Work Order ➜", type="primary")
            if submitted:
                if not selected_actions: st.error("Please select at least one action.")
                else:
                    with st.spinner("Connecting to SAP PM... Creating Notification..."):
                        time.sleep(2); st.session_state.selected_actions = selected_actions; go_next()
    elif st.session_state.step == 6:
        st.header("Step 6: Execution Confirmation"); st.balloons(); actions_list = ", ".join(st.session_state.get("selected_actions", ["Standard Optimization"])); date_now = datetime.now().strftime("%d/%m/%Y")
        st.markdown(f"""<div class="wo-ticket"><div class="ticket-header">✅ SAP Transaction Successful</div><div class="ticket-row"><span class="ticket-label">Work Order ID:</span><span class="ticket-val">WO-2026-88991</span></div><div class="ticket-row"><span class="ticket-label">Functional Location:</span><span class="ticket-val">NS-PROC-MVR-009</span></div><div class="ticket-row"><span class="ticket-label">Approved Scope:</span><span class="ticket-val">{actions_list}</span></div><div class="ticket-row"><span class="ticket-label">Material Spec:</span><span class="ticket-val" style="color:#FFAA00">Upgrade to FKM (Viton)</span></div><div class="ticket-row"><span class="ticket-label">Status:</span><span class="ticket-val" style="color:#00Cca3">Released</span></div><hr style="border-color:#444"><div style="font-size:12px; color:#666;">Generated by maintAI Resolve Agent | User: Muhammad Jibril | Date: {date_now}</div></div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True); 
        if st.button("Start New Asset Review"): reset_workflow()