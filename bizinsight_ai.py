# bizinsight_ai_saas.py
# Full BizInsight AI with SaaS-style UI layout

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION (must be first)
# ------------------------------------------------------------
st.set_page_config(page_title="BizInsight AI", layout="wide", initial_sidebar_state="expanded")

# ------------------------------------------------------------
# 2. SESSION STATE
# ------------------------------------------------------------
if "scenario_results" not in st.session_state:
    st.session_state.scenario_results = []

# ------------------------------------------------------------
# 3. BUSINESS LOGIC FUNCTIONS
# ------------------------------------------------------------
def compute_financials(units, price, cost):
    revenue = units * price
    total_cost = units * cost
    profit = revenue - total_cost
    margin = profit / revenue if revenue > 0 else 0
    return revenue, total_cost, profit, margin

def compute_eoq(D, S, H):
    if H <= 0:
        return float('inf')
    return np.sqrt((2 * D * S) / H)

# ------------------------------------------------------------
# 4. SIDEBAR – ALL INPUTS (Control Panel)
# ------------------------------------------------------------
st.sidebar.title("⚙️ Control Panel")

# Basic financial inputs
units_sold = st.sidebar.number_input("Units Sold", min_value=0, value=1000, step=100)
unit_price = st.sidebar.number_input("Unit Price ($)", min_value=0.0, value=50.0, step=1.0)
unit_cost = st.sidebar.number_input("Unit Cost ($)", min_value=0.0, value=30.0, step=1.0)

st.sidebar.markdown("---")

# EOQ specific inputs
annual_demand = st.sidebar.number_input("Annual Demand (D)", min_value=1, value=5000, step=500)
ordering_cost = st.sidebar.number_input("Ordering Cost per Order (S) ($)", min_value=0.0, value=100.0, step=10.0)
holding_cost_rate = st.sidebar.number_input("Holding Cost Rate (% of unit cost)", min_value=0.0, value=0.20, step=0.01)
holding_cost = unit_cost * holding_cost_rate

st.sidebar.markdown("---")

# Target margin for optimizer
target_margin = st.sidebar.slider("Target Profit Margin (%)", 0, 100, 30) / 100.0

st.sidebar.markdown("---")
theme = st.sidebar.toggle("🌙 Dark Mode (UI)")

# ------------------------------------------------------------
# 5. TOP HEADER & KPI STRIP
# ------------------------------------------------------------
st.title("📊 BizInsight AI")
st.caption("Business Analytics • Profit Optimization • Inventory Intelligence")
st.markdown("---")

revenue, total_cost, profit, margin = compute_financials(units_sold, unit_price, unit_cost)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue", f"${revenue:,.0f}")
col2.metric("Total Cost", f"${total_cost:,.0f}")
col3.metric("Profit", f"${profit:,.0f}", delta=f"${profit:,.0f}")
col4.metric("Profit Margin", f"{margin:.1%}")

# ------------------------------------------------------------
# 6. MAIN DASHBOARD – TABS (Clean modular structure)
# ------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "💰 Profit Engine",
    "📦 Inventory (EOQ)",
    "🔄 Scenario Lab"
])

# ===================== TAB 1: OVERVIEW =====================
with tab1:
    st.subheader("Executive Summary")
    st.write(
        "This dashboard provides real‑time business health indicators, profit insights, "
        "and inventory optimization. Adjust inputs in the sidebar to see instant impact."
    )
    
    # Simple bar chart of current profit structure
    st.subheader("Current Profit Structure")
    chart_df = pd.DataFrame({
        "Metric": ["Revenue", "Total Cost", "Profit"],
        "Amount": [revenue, total_cost, profit]
    })
    st.bar_chart(chart_df.set_index("Metric"))
    
    st.info(f"🔍 Key insight: Your profit margin is **{margin:.1%}**. "
            f"A 1% improvement in margin would add **${revenue * 0.01:,.0f}** to profit.")

# ===================== TAB 2: PROFIT ENGINE =====================
with tab2:
    st.subheader("Profit Intelligence Engine")
    
    # Detailed KPI cards (already shown at top, but repeat for context)
    pc1, pc2, pc3, pc4 = st.columns(4)
    pc1.metric("Revenue", f"${revenue:,.0f}")
    pc2.metric("Total Cost", f"${total_cost:,.0f}")
    pc3.metric("Profit", f"${profit:,.0f}")
    pc4.metric("Margin", f"{margin:.1%}")
    
    st.markdown("---")
    st.subheader("🎯 Pricing & Margin Optimizer")
    
    opt_col1, opt_col2 = st.columns(2)
    with opt_col1:
        required_price = unit_cost / (1 - target_margin) if target_margin < 1 else float('inf')
        st.metric(f"Price needed for {target_margin:.0%} margin",
                  f"${required_price:,.2f}" if required_price != float('inf') else "Not possible")
    with opt_col2:
        max_cost = unit_price * (1 - target_margin)
        st.metric(f"Max unit cost for {target_margin:.0%} margin",
                  f"${max_cost:,.2f}" if max_cost >= 0 else "Negative")
    
    st.caption("Use the sidebar slider to adjust target margin and see required price/cost changes.")

# ===================== TAB 3: INVENTORY (EOQ) =====================
with tab3:
    st.subheader("Inventory Optimization (EOQ Model)")
    
    eoq = compute_eoq(annual_demand, ordering_cost, holding_cost)
    if eoq != float('inf'):
        st.metric("Economic Order Quantity (EOQ)", f"{eoq:.0f} units")
        n_orders = annual_demand / eoq if eoq > 0 else 0
        st.caption(f"📦 Orders per year: {n_orders:.1f} | ⏱️ Order cycle: {365/n_orders:.1f} days")
    else:
        st.warning("Holding cost is zero – EOQ undefined (infinite).")
    
    # EOQ Cost Curves
    st.subheader("📉 EOQ Cost Trade‑off Analysis")
    if eoq != float('inf') and eoq > 0:
        Q_range = np.linspace(max(1, eoq*0.1), eoq*3, 100)
        ordering_costs = (annual_demand / Q_range) * ordering_cost
        holding_costs = (Q_range / 2) * holding_cost
        total_costs = ordering_costs + holding_costs
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(Q_range, ordering_costs, label="Ordering Cost", linestyle="--")
        ax.plot(Q_range, holding_costs, label="Holding Cost", linestyle="--")
        ax.plot(Q_range, total_costs, label="Total Cost", linewidth=2)
        ax.axvline(eoq, color='red', linestyle=':', label=f"EOQ = {eoq:.0f}")
        ax.set_xlabel("Order Quantity (Q)")
        ax.set_ylabel("Annual Cost ($)")
        ax.set_title("EOQ Cost Curves")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Adjust holding cost or other parameters to see the EOQ curve.")

# ===================== TAB 4: SCENARIO LAB =====================
with tab4:
    st.subheader("Scenario Simulator – Compare Strategies")
    with st.form("scenario_form"):
        colA, colB, colC = st.columns(3)
        with colA:
            sim_units = st.number_input("Units", value=units_sold)
        with colB:
            sim_price = st.number_input("Price ($)", value=unit_price)
        with colC:
            sim_cost = st.number_input("Cost ($)", value=unit_cost)
        sim_name = st.text_input("Scenario name", placeholder="e.g., High price, Low cost")
        submitted = st.form_submit_button("➕ Add Scenario")
    
    if submitted and sim_name:
        rev, cost, prof, mar = compute_financials(sim_units, sim_price, sim_cost)
        st.session_state.scenario_results.append({
            "Scenario": sim_name,
            "Units": sim_units,
            "Price": sim_price,
            "Cost": sim_cost,
            "Revenue": rev,
            "Total Cost": cost,
            "Profit": prof,
            "Margin": mar
        })
        st.success(f"Scenario '{sim_name}' added!")
    
    if st.session_state.scenario_results:
        df_scenarios = pd.DataFrame(st.session_state.scenario_results)
        st.dataframe(df_scenarios.style.format({
            "Revenue": "${:,.0f}", "Total Cost": "${:,.0f}", "Profit": "${:,.0f}", "Margin": "{:.1%}"
        }), use_container_width=True)
    else:
        st.info("No scenarios added yet. Use the form above to compare business strategies.")

# ------------------------------------------------------------
# 7. INSIGHTS FOOTER (Decision Support Panel)
# ------------------------------------------------------------
st.markdown("---")
st.subheader("🧠 AI Insights")
insight_col1, insight_col2 = st.columns(2)
with insight_col1:
    st.write("• Current margin is **{:.1%}** – ".format(margin) + 
             ("above 20% target ✓" if margin > 0.2 else "below 20% target ⚠️"))
    st.write("• EOQ suggests ordering **{} units** per batch to minimise costs".format(
        round(eoq) if eoq != float('inf') else "optimal"))
with insight_col2:
    st.write("• Scenario comparisons help evaluate pricing strategies")
    st.write("• Adjust target margin to see required price changes instantly")

# ------------------------------------------------------------
# 8. PDF REPORT GENERATION (placed below insights)
# ------------------------------------------------------------
st.subheader("📄 Generate Business Report")

def create_pdf_report():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    story = []
    story.append(Paragraph("BizInsight AI – Business Summary", title_style))
    story.append(Spacer(1, 0.25*inch))

    # Profit Intelligence
    story.append(Paragraph("Profit Intelligence", heading_style))
    profit_data = [
        ["Metric", "Value"],
        ["Revenue", f"${revenue:,.0f}"],
        ["Total Cost", f"${total_cost:,.0f}"],
        ["Profit", f"${profit:,.0f}"],
        ["Profit Margin", f"{margin:.1%}"]
    ]
    profit_table = Table(profit_data, colWidths=[2.5*inch, 2.5*inch])
    profit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(profit_table)
    story.append(Spacer(1, 0.2*inch))

    # EOQ Summary
    story.append(Paragraph("Inventory Optimization (EOQ)", heading_style))
    eoq_data = [
        ["Parameter", "Value"],
        ["Annual Demand (D)", f"{annual_demand}"],
        ["Ordering Cost (S)", f"${ordering_cost:,.2f}"],
        ["Holding Cost (H)", f"${holding_cost:,.2f}"],
        ["EOQ", f"{eoq:.0f} units" if eoq != float('inf') else "N/A"],
        ["Orders per Year", f"{annual_demand/eoq:.1f}" if eoq != float('inf') else "N/A"]
    ]
    eoq_table = Table(eoq_data, colWidths=[2.5*inch, 2.5*inch])
    eoq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(eoq_table)
    story.append(Spacer(1, 0.2*inch))

    # Scenarios
    if st.session_state.scenario_results:
        story.append(Paragraph("Compared Scenarios", heading_style))
        scenario_table_data = [["Scenario", "Profit", "Margin"]]
        for s in st.session_state.scenario_results:
            scenario_table_data.append([s["Scenario"], f"${s['Profit']:,.0f}", f"{s['Margin']:.1%}"])
        sc_table = Table(scenario_table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
        sc_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(sc_table)
    else:
        story.append(Paragraph("No scenarios saved for this report.", normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("📥 Download PDF Report"):
    pdf_buffer = create_pdf_report()
    st.download_button(
        label="Click to download PDF",
        data=pdf_buffer,
        file_name="bizinsight_report.pdf",
        mime="application/pdf"
    )

# ------------------------------------------------------------
# 9. DARK MODE STYLE (OPTIONAL)
# ------------------------------------------------------------
if theme:
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stTabs [data-baseweb="tab-list"] button {
            background-color: #1e1e2e;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# 10. FOOTER
# ------------------------------------------------------------
st.divider()
st.caption("BizInsight AI — Built with Streamlit, NumPy, Matplotlib, ReportLab | SaaS-style Dashboard")