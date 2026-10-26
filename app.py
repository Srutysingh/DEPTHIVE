import streamlit as st
import pandas as pd

from auth import init_db, create_user, verify_user
from data_processor import (
    load_dataset,
    generate_data_quality_report,
    clean_dataset
)
from intelligence_engine import analyze_department_performance

st.set_page_config(
    page_title="DEPTHIVE | Organizational Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#050b18; --panel:#0b1730; --line:#17365b; --cyan:#42d9ff; --violet:#8a5cff; --muted:#9bb0cc; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #10264b 0%, #050b18 48%, #07091a 100%); color:#f4f7ff; font-family:'DM Sans',sans-serif; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.04em; }
.block-container { padding-top:2rem; max-width:1220px; }
div[data-testid="stForm"] { background:rgba(10,23,47,.88); border:1px solid #1a3b62; padding:1.5rem; border-radius:18px; }
.stTextInput input, .stSelectbox div[data-baseweb="select"] { background:#08152b !important; color:#f4f7ff !important; border-color:#25466c !important; border-radius:10px !important; }
.stButton>button, .stFormSubmitButton>button { border:1px solid #4d76ff; border-radius:10px; color:white; background:linear-gradient(100deg,#176be8,#7650ed); font-weight:700; min-height:2.7rem; transition:all .2s ease; }
.stButton>button:hover, .stFormSubmitButton>button:hover { border-color:#42d9ff; box-shadow:0 0 22px #1c8bdf55; transform:translateY(-1px); }
a { color:#42d9ff !important; }
.brand { font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:700; letter-spacing:.16em; }
.brand-mark { display:inline-flex; width:34px; height:34px; align-items:center; justify-content:center; margin-right:10px; border-radius:11px; color:#051020; background:linear-gradient(135deg,#42d9ff,#8a5cff); font-size:1.25rem; }
.eyebrow { color:#42d9ff; font-size:.76rem; font-weight:700; letter-spacing:.2em; text-transform:uppercase; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2.8rem,6vw,5.3rem); line-height:1.02; font-weight:700; letter-spacing:-.065em; margin:.6rem 0 1rem; }
.gradient-text { background:linear-gradient(90deg,#fff,#70dcff 55%,#a28aff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.subtle { color:#a7bad4; font-size:1.05rem; line-height:1.8; max-width:610px; }
.glass-card { background:linear-gradient(145deg,rgba(17,39,72,.88),rgba(7,17,36,.92)); border:1px solid #1a416b; border-radius:18px; padding:20px; min-height:130px; box-shadow:0 14px 50px #00000020; }
.card-label { color:#a4b7d0; font-size:.83rem; }
.card-value { font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; margin-top:8px; }
.pill { display:inline-block; border:1px solid #20527b; background:#0b2542; color:#63dcff; border-radius:99px; padding:6px 11px; font-size:.76rem; }
hr { border-color:#1a3150 !important; }
div[data-testid="stMetric"] { background:#0b1730; padding:18px; border:1px solid #1a3b62; border-radius:14px; }
div[data-testid="stMetricLabel"] { color:#9bb0cc; }
div[data-testid="stMetricValue"] { color:#f4f7ff; }
#MainMenu, footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

def brand():
    st.markdown('<div class="brand"><span class="brand-mark">◈</span>DEPTHIVE</div>', unsafe_allow_html=True)

def set_page(page):
    st.session_state.page = page

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "user" not in st.session_state:
    st.session_state.user = None

# Authenticated navigation
if st.session_state.user:
    with st.sidebar:
        brand()
        st.caption("ORGANIZATIONAL INTELLIGENCE")
        st.markdown("---")
        pages = ["Overview", "Data Hub", "Department Intelligence", "KPI Explorer",
                 "Predictive Analytics", "WHY Engine", "Risk Center",
                 "Recommendations & Actions", "What-If Lab", "AI Copilot",
                 "Reports", "Settings & Audit Logs"]
        choice = st.radio("WORKSPACE", pages, label_visibility="visible")
        st.markdown("---")
        st.caption(f"Signed in as **{st.session_state.user['name']}**")
        if st.button("Log out", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "Home"
            st.rerun()
    st.markdown(f'<div class="eyebrow">DEPTHIVE WORKSPACE</div><h1>{choice}</h1>', unsafe_allow_html=True)
    st.write("A connected view of organizational performance, risks, and decisions.")
    if choice == "Overview":
        cols = st.columns(4)
        for col, label, value, delta in zip(cols,
            ["Organization Health", "Departments", "Risks to Review", "Open Actions"],
            ["— / 100", "0 connected", "0", "0"], ["Awaiting data", "Configure setup", "No data loaded", "No actions yet"]):
            with col:
                st.markdown(f'<div class="glass-card"><div class="card-label">{label}</div><div class="card-value">{value}</div><div class="card-label">{delta}</div></div>', unsafe_allow_html=True)
        st.info("Your workspace is ready. Connect a dataset in **Data Hub** to populate real analytics. No sample values are presented as live data.")
        a,b = st.columns(2)
        with a:
            st.markdown('<div class="glass-card"><h3>Performance intelligence</h3><p class="subtle">Department trends, KPI targets, and evidence-linked findings will appear here after data is connected.</p></div>', unsafe_allow_html=True)
        with b:
            st.markdown('<div class="glass-card"><h3>Decision center</h3><p class="subtle">Review recommendations, assign actions, and track outcomes in one workflow.</p></div>', unsafe_allow_html=True)
    elif choice == "Data Hub":
        st.subheader("Bring your data into Depthive")
        st.write(
            "Upload a CSV or Excel dataset to inspect data quality "
            "and remove exact duplicate rows."
        )

        upload = st.file_uploader(
            "Upload organization dataset",
            type=["csv", "xlsx"],
            key="data_hub_upload"
        )

        if upload is not None:
            try:
                # Load uploaded dataset
                df = load_dataset(upload)

                st.success(
                    f"Loaded {len(df):,} rows and "
                    f"{len(df.columns)} columns."
                )

                # Dataset preview
                st.subheader("Dataset Preview")
                st.dataframe(df.head(100), use_container_width=True)

                # Data quality analysis
                report = generate_data_quality_report(df)

                st.subheader("Data Quality Report")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Total Rows", report["total_rows"])
                col2.metric("Total Columns", report["total_columns"])
                col3.metric("Duplicate Rows", report["duplicate_rows"])
                col4.metric("Missing Cells", report["missing_cells"])

                # Column-level details
                with st.expander("View Column Details"):
                    column_details = pd.DataFrame({
                        "Column": report["column_names"],
                        "Data Type": [
                            report["data_types"][column]
                            for column in report["column_names"]
                        ],
                        "Missing Values": [
                            report["missing_values_by_column"][column]
                            for column in report["column_names"]
                        ]
                    })

                    st.dataframe(
                        column_details,
                        use_container_width=True
                    )

                # Remove duplicate rows
                st.subheader("Data Cleaning")

                cleaned_df, summary = clean_dataset(df)

                st.write(
                    f"**Original rows:** {summary['original_rows']}"
                )
                st.write(
                    f"**Cleaned rows:** {summary['cleaned_rows']}"
                )
                st.write(
                    f"**Duplicate rows removed:** "
                    f"{summary['duplicates_removed']}"
                )
                st.info(
                    "Missing values are retained for now; "
                    "they are reported rather than automatically deleted."
                )

                st.dataframe(
                    cleaned_df.head(100),
                    use_container_width=True
                )

                # Download cleaned dataset
                csv_data = cleaned_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Download Cleaned CSV",
                    data=csv_data,
                    file_name="depthive_cleaned_dataset.csv",
                    mime="text/csv"
                )

                # Keep original and cleaned datasets available during the session
                st.session_state["uploaded_preview"] = df
                st.session_state["cleaned_dataset"] = cleaned_df

            except Exception as e:
                st.error(f"Could not process this file: {e}")
    elif choice == "Department Intelligence":
        st.subheader("Department Performance Intelligence")

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        else:
            result = analyze_department_performance(df)

            if not result["success"]:
                st.warning(result["message"])

            else:
                performance = result["department_performance"]

                col1, col2 = st.columns(2)

                col1.metric(
                    "Total Departments",
                    result["total_departments"]
                )

                col2.metric(
                    "Top Performing Department",
                    result["top_department"]
                )

                st.subheader("Department Performance Ranking")
                st.dataframe(
                    performance,
                    use_container_width=True
                )

                st.subheader("Performance Score Comparison")
                st.bar_chart(performance["Performance Score"])

    elif choice == "KPI Explorer":
        st.subheader("KPI Explorer")
        st.write("Explore key performance indicators across departments.")

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        else:
            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if not numeric_columns:
                st.warning("No numeric KPI columns found in the dataset.")

            else:
                selected_kpi = st.selectbox(
                    "Select a KPI",
                    numeric_columns
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Average",
                    round(df[selected_kpi].mean(), 2)
                )

                col2.metric(
                    "Maximum",
                    round(df[selected_kpi].max(), 2)
                )

                col3.metric(
                    "Minimum",
                    round(df[selected_kpi].min(), 2)
                )

                st.subheader(f"{selected_kpi} — Data Distribution")
                st.bar_chart(df[selected_kpi])

                if "Department" in df.columns:
                    st.subheader(f"{selected_kpi} by Department")

                    department_kpi = (
                        df.groupby("Department")[selected_kpi]
                        .mean()
                        .sort_values(ascending=False)
                    )

                    st.bar_chart(department_kpi)

                    st.dataframe(
                        department_kpi.reset_index(),
                        use_container_width=True
                    )

    elif choice == "Predictive Analytics":
        st.subheader("Predictive Analytics")
        st.write("Analyze historical KPI values and estimate the next value.")

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")
        else:
            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if not numeric_columns:
                st.warning("No numeric KPI columns found.")
            else:
                selected_kpi = st.selectbox(
                    "Select KPI for prediction",
                    numeric_columns,
                    key="prediction_kpi"
                )

                values = (
                    pd.to_numeric(df[selected_kpi], errors="coerce")
                    .dropna()
                    .reset_index(drop=True)
                )

                if len(values) < 3:
                    st.warning("At least 3 numeric observations are required.")
                else:
                    prediction = round(values.tail(5).mean(), 2)

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Latest Observed Value",
                        round(values.iloc[-1], 2)
                    )

                    col2.metric(
                        "Estimated Next Value",
                        prediction
                    )

                    st.subheader("Historical KPI Trend")
                    st.line_chart(values)

                    st.subheader("Latest vs Estimated Value")
                    st.bar_chart(
                        pd.DataFrame({
                            "Value": [
                                round(values.iloc[-1], 2),
                                prediction
                            ]
                        }, index=["Latest Observed", "Estimated Next"])
                    )

                    st.caption(
                        "Prototype estimate based on the last five observations; "
                        "this is not a validated forecasting model."
                    )
    elif choice == "WHY Engine":
        st.subheader("WHY Engine")
        st.write("Understand why a department's performance may be changing.")

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")
        else:
            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if "Department" not in df.columns:
                st.warning(
                    "Dataset must contain a 'Department' column."
                )
            elif not numeric_columns:
                st.warning("No numeric KPI columns found.")
            else:
                departments = df["Department"].dropna().unique().tolist()

                selected_department = st.selectbox(
                    "Select Department",
                    departments,
                    key="why_department"
                )

                department_df = df[
                    df["Department"] == selected_department
                ]

                st.markdown("### Department KPI Analysis")

                findings = []

                for col in numeric_columns:
                    department_avg = pd.to_numeric(
                        department_df[col], errors="coerce"
                    ).mean()

                    overall_avg = pd.to_numeric(
                        df[col], errors="coerce"
                    ).mean()

                    if pd.isna(department_avg) or pd.isna(overall_avg):
                        continue

                    difference = department_avg - overall_avg

                    if difference < 0:
                        status = "Below overall average"
                    elif difference > 0:
                        status = "Above overall average"
                    else:
                        status = "At overall average"

                    findings.append({
                        "KPI": col,
                        "Department Average": round(department_avg, 2),
                        "Overall Average": round(overall_avg, 2),
                        "Difference": round(difference, 2),
                        "Finding": status
                    })

                if findings:
                    findings_df = pd.DataFrame(findings)

                    st.dataframe(
                        findings_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown("### Possible Reasons")

                    below_average = findings_df[
                        findings_df["Difference"] < 0
                    ]

                    if not below_average.empty:
                        for _, row in below_average.iterrows():
                            st.warning(
                                f"**{row['KPI']}** is below the overall "
                                f"average by {abs(row['Difference'])}. "
                                "This KPI may need investigation."
                            )
                    else:
                        st.success(
                            "No numeric KPI is below the overall average."
                        )

                    st.caption(
                        "These are comparisons, not proven causes. "
                        "Business context is needed to confirm the reasons."
                    )
                else:
     
                    st.warning("No usable numeric KPI values were found.")
    elif choice == "Risk Center":
        st.subheader("🚨 Risk Center")
        st.write("Identify departments that may need attention.")

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        elif "Department" not in df.columns:
            st.warning(
                "Dataset must contain a 'Department' column."
            )

        else:
            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if not numeric_columns:
                st.warning("No numeric KPI columns found.")

            else:
                risk_records = []

                for department in df["Department"].dropna().unique():
                    dept_df = df[df["Department"] == department]
                    risk_count = 0
                    checked_count = 0

                    for col in numeric_columns:
                        dept_avg = pd.to_numeric(
                            dept_df[col], errors="coerce"
                        ).mean()

                        overall_avg = pd.to_numeric(
                            df[col], errors="coerce"
                        ).mean()

                        if pd.isna(dept_avg) or pd.isna(overall_avg):
                            continue

                        checked_count += 1

                        if overall_avg != 0 and dept_avg < overall_avg * 0.8:
                            risk_count += 1

                    if checked_count == 0:
                        risk_level = "Insufficient Data"
                    elif risk_count >= 2:
                        risk_level = "High Risk"
                    elif risk_count == 1:
                        risk_level = "Medium Risk"
                    else:
                        risk_level = "Low Risk"

                    risk_records.append({
                        "Department": department,
                        "KPIs Below 80% of Overall Average": risk_count,
                        "KPIs Checked": checked_count,
                        "Risk Level": risk_level
                    })

                risk_df = pd.DataFrame(risk_records)

                high = (risk_df["Risk Level"] == "High Risk").sum()
                medium = (risk_df["Risk Level"] == "Medium Risk").sum()
                low = (risk_df["Risk Level"] == "Low Risk").sum()

                col1, col2, col3 = st.columns(3)

                col1.metric("🔴 High Risk", int(high))
                col2.metric("🟡 Medium Risk", int(medium))
                col3.metric("🟢 Low Risk", int(low))

                st.markdown("### Department Risk Assessment")

                st.dataframe(
                    risk_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("### Risk Overview")

                chart_df = risk_df.set_index("Department")[
                    "KPIs Below 80% of Overall Average"
                ]

                st.bar_chart(chart_df)

                st.caption(
                    "Prototype risk screening: a KPI is flagged when its "
                    "department average is below 80% of the overall average. "
                    "This assumes lower values are undesirable. Configure "
                    "KPI-specific thresholds and business rules before "
                    "using this for real decisions."
                )
    elif choice == "Recommendations & Actions":
        st.subheader("Recommendations & Actions")
        st.write(
            "Turn department performance findings into actionable next steps."
        )

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        elif "Department" not in df.columns:
            st.warning(
                "Dataset must contain a 'Department' column."
            )

        else:
            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if not numeric_columns:
                st.warning("No numeric KPI columns found.")

            else:
                departments = df["Department"].dropna().unique().tolist()

                selected_department = st.selectbox(
                    "Select Department",
                    departments,
                    key="recommendation_department"
                )

                dept_df = df[
                    df["Department"] == selected_department
                ]

                st.markdown("### Department Findings")

                recommendations = []

                for col in numeric_columns:
                    dept_avg = pd.to_numeric(
                        dept_df[col], errors="coerce"
                    ).mean()

                    overall_avg = pd.to_numeric(
                        df[col], errors="coerce"
                    ).mean()

                    if pd.isna(dept_avg) or pd.isna(overall_avg):
                        continue

                    if overall_avg != 0 and dept_avg < overall_avg * 0.8:
                        recommendations.append({
                            "KPI": col,
                            "Department Average": round(dept_avg, 2),
                            "Overall Average": round(overall_avg, 2),
                            "Priority": "High",
                            "Recommended Action": (
                                f"Investigate why {col} is below the "
                                "overall average. Review the underlying "
                                "records and identify improvement steps."
                            )
                        })

                    elif dept_avg < overall_avg:
                        recommendations.append({
                            "KPI": col,
                            "Department Average": round(dept_avg, 2),
                            "Overall Average": round(overall_avg, 2),
                            "Priority": "Medium",
                            "Recommended Action": (
                                f"Monitor {col}, compare recent results, "
                                "and review whether corrective action is needed."
                            )
                        })

                if recommendations:
                    recommendations_df = pd.DataFrame(recommendations)

                    st.dataframe(
                        recommendations_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown("### Action Plan")

                    for i, item in enumerate(recommendations, start=1):
                        with st.expander(
                            f"{i}. {item['KPI']} — {item['Priority']} Priority"
                        ):
                            st.write(item["Recommended Action"])

                            owner = st.text_input(
                                "Action Owner",
                                key=f"action_owner_{i}"
                            )

                            due_date = st.date_input(
                                "Target Date",
                                key=f"action_date_{i}"
                            )

                            st.text_area(
                                "Progress Notes",
                                key=f"action_notes_{i}"
                            )

                    st.caption(
                        "Recommendations are generated from KPI comparisons. "
                        "Validate whether higher or lower values are desirable "
                        "before acting on them."
                    )

                else:
                    st.success(
                        "No below-average numeric KPIs were identified "
                        "for this department."
                    )
    elif choice == "What-If Lab":
        st.subheader("What-If Lab")
        st.write(
            "Simulate KPI changes and explore their potential impact."
        )

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        elif "Department" not in df.columns:
            st.warning("Dataset must contain a 'Department' column.")

        else:
            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if not numeric_columns:
                st.warning("No numeric KPI columns found.")

            else:
                departments = df["Department"].dropna().unique().tolist()

                selected_department = st.selectbox(
                    "Select Department",
                    departments,
                    key="whatif_department"
                )

                selected_kpi = st.selectbox(
                    "Select KPI",
                    numeric_columns,
                    key="whatif_kpi"
                )

                dept_df = df[
                    df["Department"] == selected_department
                ]

                current_value = pd.to_numeric(
                    dept_df[selected_kpi], errors="coerce"
                ).mean()

                overall_value = pd.to_numeric(
                    df[selected_kpi], errors="coerce"
                ).mean()

                if pd.isna(current_value):
                    st.warning("No valid numeric values for this KPI.")
                else:
                    st.metric(
                        "Current Department Average",
                        round(current_value, 2)
                    )

                    st.metric(
                        "Overall Dataset Average",
                        round(overall_value, 2)
                        if pd.notna(overall_value) else "N/A"
                    )

                    st.markdown("### Simulate a KPI Change")

                    change_pct = st.slider(
                        "Adjust KPI value (%)",
                        min_value=-50,
                        max_value=100,
                        value=10,
                        step=5,
                        key="whatif_change"
                    )

                    simulated_value = current_value * (
                        1 + change_pct / 100
                    )

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Current Value",
                        round(current_value, 2)
                    )

                    col2.metric(
                        "Simulated Value",
                        round(simulated_value, 2),
                        delta=f"{change_pct}%"
                    )

                    if pd.notna(overall_value):
                        if simulated_value > overall_value:
                            st.success(
                                "In this simulation, the KPI is above "
                                "the overall dataset average."
                            )
                        elif simulated_value < overall_value:
                            st.warning(
                                "In this simulation, the KPI remains below "
                                "the overall dataset average."
                            )
                        else:
                            st.info(
                                "In this simulation, the KPI matches "
                                "the overall dataset average."
                            )

                    comparison_df = pd.DataFrame({
                        "Value": [
                            current_value,
                            simulated_value
                        ]
                    }, index=["Current", "Simulated"])

                    st.bar_chart(comparison_df)

                    st.caption(
                        "This is a mathematical what-if simulation, not a "
                        "causal prediction. It assumes the selected KPI "
                        "changes while other factors remain constant."
                    )
    elif choice == "AI Copilot":
        st.subheader("🤖 DEPTHIVE AI Copilot")
        st.write(
            "Ask questions about your uploaded department dataset."
        )

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        else:
            st.markdown("### Dataset Overview")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Records", len(df))
            col2.metric("Total Columns", len(df.columns))
            col3.metric(
                "Departments",
                df["Department"].nunique()
                if "Department" in df.columns else "N/A"
            )

            st.markdown("### Ask a Question")

            question = st.text_input(
                "Your question",
                placeholder="e.g. Which department has the highest average KPI?"
            )

            if st.button("Analyze", key="copilot_analyze"):
                if not question.strip():
                    st.warning("Please enter a question.")

                else:
                    q = question.lower()
                    numeric_columns = df.select_dtypes(
                        include=["number"]
                    ).columns.tolist()

                    if "department" in q and (
                        "list" in q or "how many" in q
                    ):
                        if "Department" in df.columns:
                            departments = (
                                df["Department"]
                                .dropna()
                                .unique()
                                .tolist()
                            )

                            st.write(
                                f"**Number of departments:** {len(departments)}"
                            )
                            st.write("**Departments:**", ", ".join(
                                map(str, departments)
                            ))
                        else:
                            st.warning(
                                "The dataset has no Department column."
                            )

                    elif any(word in q for word in [
                        "average", "mean", "highest", "maximum",
                        "lowest", "minimum"
                    ]):
                        if not numeric_columns:
                            st.warning(
                                "No numeric columns found in the dataset."
                            )

                        else:
                            selected_kpi = st.selectbox(
                                "Choose KPI to analyze",
                                numeric_columns,
                                key="copilot_kpi"
                            )

                            values = pd.to_numeric(
                                df[selected_kpi], errors="coerce"
                            )

                            if "highest" in q or "maximum" in q:
                                st.success(
                                    f"Highest {selected_kpi}: "
                                    f"{values.max():.2f}"
                                )

                            elif "lowest" in q or "minimum" in q:
                                st.info(
                                    f"Lowest {selected_kpi}: "
                                    f"{values.min():.2f}"
                                )

                            else:
                                st.success(
                                    f"Average {selected_kpi}: "
                                    f"{values.mean():.2f}"
                                )

                    elif "department" in q and any(
                        word in q for word in [
                            "performance", "compare", "ranking"
                        ]
                    ):
                        if "Department" not in df.columns:
                            st.warning(
                                "The dataset has no Department column."
                            )

                        elif not numeric_columns:
                            st.warning("No numeric KPI columns found.")

                        else:
                            selected_kpi = st.selectbox(
                                "Choose KPI for department comparison",
                                numeric_columns,
                                key="copilot_compare_kpi"
                            )

                            summary = df.groupby("Department")[
                                selected_kpi
                            ].mean().sort_values(ascending=False)

                            st.write("Department averages:")
                            st.dataframe(
                                summary.reset_index(),
                                use_container_width=True,
                                hide_index=True
                            )

                            st.bar_chart(summary)

                    elif "missing" in q or "null" in q:
                        missing = df.isna().sum()
                        st.write("Missing values by column:")
                        st.dataframe(
                            missing[missing > 0].rename(
                                "Missing Values"
                            ).reset_index().rename(
                                columns={"index": "Column"}
                            ),
                            use_container_width=True,
                            hide_index=True
                        )

                    else:
                        st.info(
                            "I can currently answer questions about "
                            "department counts, KPI averages, maximum/minimum "
                            "values, department comparisons, and missing data. "
                            "Try rephrasing your question using one of these topics."
                        )

            st.caption(
                "Prototype dataset assistant using predefined analytical rules. "
                "It is not connected to an external LLM."
            )
    elif choice == "Reports":
        st.subheader("📄 DEPTHIVE Reports")
        st.write("Generate downloadable reports from your uploaded dataset.")

        df = st.session_state.get("uploaded_preview")

        if df is None:
            st.info("Please upload a dataset in Data Hub first.")

        else:
            st.markdown("### Dataset Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Records", len(df))
            col2.metric("Total Columns", len(df.columns))
            col3.metric(
                "Missing Values",
                int(df.isna().sum().sum())
            )

            st.markdown("### Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            st.markdown("### Download Reports")

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Dataset Report (CSV)",
                data=csv_data,
                file_name="depthive_dataset_report.csv",
                mime="text/csv"
            )

            summary_lines = [
                "DEPTHIVE - DATASET SUMMARY REPORT",
                "=" * 40,
                f"Total Records: {len(df)}",
                f"Total Columns: {len(df.columns)}",
                f"Total Missing Values: {int(df.isna().sum().sum())}",
                "",
                "COLUMN DETAILS"
            ]

            for col in df.columns:
                summary_lines.append(
                    f"{col}: {df[col].nunique(dropna=True)} unique values, "
                    f"{int(df[col].isna().sum())} missing values"
                )

            numeric_columns = df.select_dtypes(
                include=["number"]
            ).columns.tolist()

            if numeric_columns:
                summary_lines.extend([
                    "",
                    "NUMERIC KPI STATISTICS"
                ])

                summary_lines.append(
                    df[numeric_columns].describe().round(2).to_string()
                )

            if "Department" in df.columns:
                summary_lines.extend([
                    "",
                    "DEPARTMENT RECORD COUNTS",
                    df["Department"].value_counts().to_string()
                ])

            report_text = "\n".join(summary_lines)

            st.download_button(
                label="📄 Download Executive Summary (TXT)",
                data=report_text,
                file_name="depthive_executive_summary.txt",
                mime="text/plain"
            )

            if numeric_columns:
                st.markdown("### KPI Statistics")
                st.dataframe(
                    df[numeric_columns].describe().round(2),
                    use_container_width=True
                )

            st.caption(
                "Reports summarize the uploaded dataset. "
                "They do not represent an independently validated audit."
            )
    elif choice == "Settings & Audit Logs":
        st.subheader("⚙️ Settings & Audit Logs")
        st.write("Review the current session and track app activities.")

        df = st.session_state.get("uploaded_preview")

        if "activity_logs" not in st.session_state:
            st.session_state["activity_logs"] = []

        if not st.session_state.get("audit_initialized"):
            st.session_state["activity_logs"].append({
                "Timestamp": pd.Timestamp.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Activity": "Settings & Audit Logs opened",
                "Details": "Session activity tracking initialized"
            })
            st.session_state["audit_initialized"] = True

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Session User",
            str(st.session_state.get("user", "Logged in"))
        )

        col2.metric(
            "Dataset Status",
            "Uploaded" if df is not None else "Not uploaded"
        )

        col3.metric(
            "Tracked Activities",
            len(st.session_state["activity_logs"])
        )

        st.markdown("### Dataset Settings")

        if df is not None:
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
            st.write("**Column names:**", ", ".join(map(str, df.columns)))

            if st.button("Log Dataset Review"):
                st.session_state["activity_logs"].append({
                    "Timestamp": pd.Timestamp.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "Activity": "Dataset review",
                    "Details": f"Reviewed dataset with {len(df)} rows"
                })
                st.success("Dataset review activity logged.")

        else:
            st.info("Upload a dataset in Data Hub to view dataset settings.")

        st.markdown("### Activity Log")

        logs_df = pd.DataFrame(
            st.session_state["activity_logs"]
        )

        if not logs_df.empty:
            st.dataframe(
                logs_df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "📥 Download Audit Log (CSV)",
                data=logs_df.to_csv(index=False).encode("utf-8"),
                file_name="depthive_audit_log.csv",
                mime="text/csv"
            )

        else:
            st.info("No activities have been recorded yet.")

        st.caption(
            "Prototype session log only. It is not a permanent, "
            "tamper-proof security audit trail."
        )
    else:
        st.markdown(
            '<div class="glass-card">'
            '<span class="pill">MODULE SCAFFOLD</span>'
            '<h3>Ready for implementation</h3>'
            '<p class="subtle">This page is in the product navigation. '
            'We will connect its real calculations, database records, '
            'and interactions in the next build step.</p></div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Only implemented features should be presented as live capabilities."
        )
else:
    brand()
    st.markdown("<br>", unsafe_allow_html=True)
    page = st.session_state.page
    if page == "Home":
        left, right = st.columns([1.12, .88], gap="large")
        with left:
            st.markdown('<div class="eyebrow">ORGANIZATIONAL INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
            st.markdown('<div class="hero-title">See Beyond Data.<br><span class="gradient-text">Decide with Intelligence.</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="subtle">Bring organizational data together, uncover performance signals, investigate risks, and turn analysis into measurable action.</p>', unsafe_allow_html=True)
            st.markdown('<span class="pill">DATA • ANALYTICS • DECISIONS</span>', unsafe_allow_html=True)
            st.write("")
            c1,c2 = st.columns([1,1])
            with c1:
                if st.button("Get Started  →", use_container_width=True):
                    set_page("Sign Up"); st.rerun()
            with c2:
                if st.button("Sign In", use_container_width=True):
                    set_page("Login"); st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Built for evidence-led decisions—not just another dashboard.")
        with right:
            st.markdown("""
            <div class="glass-card" style="min-height:430px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:radial-gradient(circle at 50% 35%,#173c72 0%,#0a1932 45%,#081126 100%);">
              <div style="font-size:7rem;line-height:1.1;background:linear-gradient(135deg,#42d9ff,#6c75ff,#a16aff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">◉</div>
              <div class="eyebrow">INTELLIGENCE CORE</div>
              <h2 style="margin-top:12px;">One workspace.<br>Clearer decisions.</h2>
              <p class="subtle" style="font-size:.9rem;">Connect data · Understand performance · Take action</p>
              <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;"><span class="pill">Analytics</span><span class="pill">Risk signals</span><span class="pill">Action tracking</span></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        f1,f2,f3 = st.columns(3)
        for col, title, desc in [
            (f1,"01 / Connect","Import and validate organizational data."),
            (f2,"02 / Understand","Explore KPIs, trends, and possible risk signals."),
            (f3,"03 / Improve","Review recommendations and measure outcomes.")]:
            with col:
                st.markdown(f'<div class="glass-card"><div class="eyebrow">{title}</div><p class="subtle" style="font-size:.92rem">{desc}</p></div>', unsafe_allow_html=True)

    elif page == "Login":
        left, right = st.columns([.9,1.1], gap="large")
        with left:
            st.markdown('<div class="eyebrow">WELCOME BACK</div><h1>Sign in to your<br>intelligence workspace.</h1><p class="subtle">Your data. Your teams. A clearer view of what comes next.</p>', unsafe_allow_html=True)
        with right:
            st.markdown("### Sign in")
            with st.form("login_form"):
                email = st.text_input("Work email", placeholder="you@organization.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In →", use_container_width=True)
            if submitted:
                user = verify_user(email.strip().lower(), password)
                if user:
                    st.session_state.user = user
                    st.session_state.page = "Overview"
                    st.rerun()
                else:
                    st.error("Sign-in failed. Check your email and password, or create an account.")
            c1,c2 = st.columns(2)
            with c1:
                if st.button("Create account", use_container_width=True):
                    set_page("Sign Up"); st.rerun()
            with c2:
                if st.button("Forgot password?", use_container_width=True):
                    set_page("Forgot Password"); st.rerun()
    elif page == "Sign Up":
        left, right = st.columns([.85,1.15], gap="large")
        with left:
            st.markdown('<div class="eyebrow">CREATE YOUR WORKSPACE</div><h1>Build a smarter<br><span class="gradient-text">organization.</span></h1><p class="subtle">Create your account to begin setting up Depthive. Access to organization data should be granted by an authorized administrator.</p>', unsafe_allow_html=True)
        with right:
            st.markdown("### Create account")
            with st.form("signup_form"):
                name = st.text_input("Full name", placeholder="Your full name")
                email = st.text_input("Work email", placeholder="you@organization.com")
                org = st.text_input("Organization name", placeholder="Organization or college")
                role = st.selectbox("Requested role", ["Analyst / Viewer", "Department Lead", "HOD / Manager", "Admin"])
                password = st.text_input("Password", type="password", help="Use at least 10 characters.")
                confirm = st.text_input("Confirm password", type="password")
                accepted = st.checkbox("I agree to the workspace terms and privacy notice.")
                submitted = st.form_submit_button("Create account →", use_container_width=True)
            if submitted:
                if not all([name.strip(), email.strip(), org.strip(), password, confirm]):
                    st.error("Please complete every field.")
                elif "@" not in email or "." not in email.split("@")[-1]:
                    st.error("Enter a valid email address.")
                elif len(password) < 10:
                    st.error("Use a password with at least 10 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif not accepted:
                    st.error("Please accept the terms to continue.")
                else:
                    ok, message = create_user(name.strip(), email.strip().lower(), org.strip(), role, password)
                    if ok:
                        st.success(message)
                        st.info("For this local prototype, email verification and admin approval workflows are not yet configured.")
                    else:
                        st.error(message)
            if st.button("← Back to sign in"):
                set_page("Login"); st.rerun()
    elif page == "Forgot Password":
        st.markdown('<div class="eyebrow">ACCOUNT RECOVERY</div><h1>Reset your password.</h1><p class="subtle">Password recovery needs a verified email delivery service. This starter keeps account security explicit rather than pretending to send an email.</p>', unsafe_allow_html=True)
        with st.form("forgot_form"):
            email = st.text_input("Account email", placeholder="you@organization.com")
            submitted = st.form_submit_button("Request reset instructions")
        if submitted:
            st.info("Password-reset email is not configured in this prototype. We will add a secure, expiring reset-token flow with email delivery before deployment.")
        if st.button("← Back to login"):
            set_page("Login"); st.rerun()

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("DEPTHIVE • Prototype foundation • Use synthetic or authorized data for testing.")
