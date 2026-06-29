import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
from db_config import get_connection

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import clean font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 15px;
        padding: 6px 0;
    }

    /* Main background */
    .main {
        background-color: #f8fafc;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* Section headers */
    .section-title {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 16px;
        margin-top: 8px;
    }

    /* Table styling */
    .dataframe {
        border: none !important;
        font-size: 14px !important;
    }

    /* Success/error toast override */
    div[data-testid="stAlert"] {
        border-radius: 8px;
    }

    /* AI insight box */
    .ai-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
        border-left: 3px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 14px;
        color: #1e293b;
    }

    .ai-label {
        font-size: 11px;
        font-weight: 600;
        color: #3b82f6;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    /* Button tweaks */
    .stButton > button {
        border-radius: 7px;
        font-weight: 500;
        font-size: 14px;
    }

    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─── DB HELPERS ────────────────────────────────────────────────────────────────
def fetch_all_students():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return pd.DataFrame(rows, columns=["ID", "Name", "Age", "Course", "Marks"])
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


def insert_student(name, age, course, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO students(name, age, course, marks)
        VALUES (%s, %s, %s, %s)
        """,
        (name, age, course, marks)
    )
    conn.commit()
    cur.close()
    conn.close()


def update_student_marks(sid, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET marks = %s WHERE id = %s ", (marks, sid))
    conn.commit()
    cur.close()
    conn.close()


def delete_student(sid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (sid,))
    conn.commit()
    cur.close()
    conn.close()


# ─── AI / ML HELPER ────────────────────────────────────────────────────────────
def predict_grade(marks):
    """Simple rule-based grade prediction (no training data needed)."""
    if marks >= 90:
        return "A+", "Excellent performance"
    elif marks >= 80:
        return "A", "Above average"
    elif marks >= 70:
        return "B", "Good standing"
    elif marks >= 60:
        return "C", "Needs improvement"
    else:
        return "F", "At risk — consider intervention"


def ml_marks_predictor(df):
    """
    Uses Linear Regression to predict what marks a student might score
    based on their age (demo of ML integration).
    Returns the model and a prediction for a given age.
    """
    if len(df) < 3:
        return None, None
    X = df[["Age"]].values
    y = df["Marks"].values
    model = LinearRegression()
    model.fit(X, y)
    return model


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 SMS")
    st.markdown("**Student Management System**")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["Dashboard", "Add Student", "Update Marks", "Delete Student", "AI Insights"],
        label_visibility="collapsed"
    )
    


# ─── PAGE: DASHBOARD ───────────────────────────────────────────────────────────
if page == "Dashboard":
    st.markdown("## Dashboard")
    st.markdown('<p class="section-title">Overview</p>', unsafe_allow_html=True)

    df = fetch_all_students()

    if df.empty:
        st.info("No student records found. Add students to get started.")
    else:
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", len(df))
        col2.metric("Average Marks", f"{df['Marks'].mean():.1f}")
        col3.metric("Highest Marks", int(df['Marks'].max()))
        col4.metric("Courses", df['Course'].nunique())

        st.markdown("---")

        # Table + Chart side by side
        left, right = st.columns([1.4, 1])

        with left:
            st.markdown('<p class="section-title">All Students</p>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)

        with right:
            st.markdown('<p class="section-title">Marks by Course</p>', unsafe_allow_html=True)
            course_avg = df.groupby("Course")["Marks"].mean().reset_index()
            fig = px.bar(
                course_avg, x="Course", y="Marks",
                color="Marks",
                color_continuous_scale=["#bfdbfe", "#1d4ed8"],
                template="plotly_white",
                height=280
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                coloraxis_showscale=False,
                font=dict(family="Inter", size=12),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

        # Distribution chart
        st.markdown('<p class="section-title">Marks Distribution</p>', unsafe_allow_html=True)
        fig2 = px.histogram(
            df, x="Marks", nbins=10,
            template="plotly_white",
            color_discrete_sequence=["#3b82f6"],
            height=200
        )
        fig2.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            bargap=0.1,
            font=dict(family="Inter", size=12),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─── PAGE: ADD STUDENT ─────────────────────────────────────────────────────────
elif page == "Add Student":
    st.markdown("## Add Student")
    st.markdown('<p class="section-title">New Record</p>', unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name   = c1.text_input("Full Name")
        age    = c2.number_input("Age", min_value=15, max_value=40, value=20)
        course = c1.text_input("Course")
        marks  = c2.number_input("Marks (out of 100)", min_value=0, max_value=100, value=75)
        submitted = st.form_submit_button("Add Student", use_container_width=True)

    if submitted:
        if name.strip() and course.strip():
            try:
                insert_student(name.strip(), int(age), course.strip(), int(marks))
                grade, label = predict_grade(marks)
                st.success(f"✓ {name} added successfully.")
                st.markdown(f"""
                <div class="ai-box">
                    <div class="ai-label">🤖 AI Grade Prediction</div>
                    Based on the entered marks ({marks}/100), this student is predicted to receive 
                    grade <strong>{grade}</strong> — {label}.
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill in all fields.")


# ─── PAGE: UPDATE MARKS ────────────────────────────────────────────────────────
elif page == "Update Marks":
    st.markdown("## Update Marks")

    df = fetch_all_students()

    if df.empty:
        st.info("No students found.")
    else:
        st.dataframe(df[["ID", "Name", "Course", "Marks"]], use_container_width=True, hide_index=True)
        st.markdown("---")

        with st.form("update_form"):
            c1, c2 = st.columns(2)
            sid   = c1.number_input("Student ID", min_value=1, step=1)
            marks = c2.number_input("New Marks", min_value=0, max_value=100, value=75)
            submitted = st.form_submit_button("Update", use_container_width=True)

        if submitted:
            if int(sid) in df["ID"].values:
                try:
                    update_student_marks(int(sid), int(marks))
                    grade, label = predict_grade(marks)
                    st.success(f"✓ Marks updated for student ID {sid}.")
                    st.markdown(f"""
                    <div class="ai-box">
                        <div class="ai-label">🤖 Updated Grade Prediction</div>
                        New marks ({marks}/100) → Grade <strong>{grade}</strong> — {label}.
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning(f"No student found with ID {sid}.")


# ─── PAGE: DELETE STUDENT ──────────────────────────────────────────────────────
elif page == "Delete Student":
    st.markdown("## Delete Student")

    df = fetch_all_students()

    if df.empty:
        st.info("No students found.")
    else:
        st.dataframe(df[["ID", "Name", "Course", "Marks"]], use_container_width=True, hide_index=True)
        st.markdown("---")

        with st.form("delete_form"):
            sid = st.number_input("Enter Student ID to delete", min_value=1, step=1)
            confirm = st.checkbox("I confirm I want to delete this record permanently.")
            submitted = st.form_submit_button("Delete", use_container_width=True)

        if submitted:
            if not confirm:
                st.warning("Please confirm deletion by checking the box.")
            elif int(sid) in df["ID"].values:
                try:
                    delete_student(int(sid))
                    st.success(f"✓ Student ID {sid} deleted.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning(f"No student found with ID {sid}.")


# ─── PAGE: AI INSIGHTS ─────────────────────────────────────────────────────────
elif page == "AI Insights":
    st.markdown("## AI Insights")
    st.markdown('<p class="section-title">Machine Learning Analysis</p>', unsafe_allow_html=True)

    df = fetch_all_students()

    if df.empty or len(df) < 3:
        st.info("Add at least 3 students to unlock AI insights.")
    else:
        # ── 1. Grade distribution ──────────────────────────────────────
        df["Grade"] = df["Marks"].apply(lambda m: predict_grade(m)[0])

        left, right = st.columns(2)

        with left:
            st.markdown('<p class="section-title">Grade Distribution</p>', unsafe_allow_html=True)
            grade_counts = df["Grade"].value_counts().reset_index()
            grade_counts.columns = ["Grade", "Count"]
            fig = px.pie(
                grade_counts, names="Grade", values="Count",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                template="plotly_white", height=280
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                font=dict(family="Inter", size=12),
                paper_bgcolor="#ffffff"
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.markdown('<p class="section-title">Marks vs Age (Regression)</p>', unsafe_allow_html=True)
            model = ml_marks_predictor(df)

            if model:
                age_range = np.linspace(df["Age"].min(), df["Age"].max(), 50).reshape(-1, 1)
                pred_marks = model.predict(age_range)

                fig2 = px.scatter(
                    df, x="Age", y="Marks", color="Course",
                    template="plotly_white", height=280
                )
                fig2.add_scatter(
                    x=age_range.flatten(), y=pred_marks,
                    mode="lines", name="Trend",
                    line=dict(color="#3b82f6", width=2, dash="dot")
                )
                fig2.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0),
                    font=dict(family="Inter", size=12),
                    paper_bgcolor="#ffffff",
                    plot_bgcolor="#ffffff"
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ── 2. Marks predictor widget ──────────────────────────────────
        st.markdown("---")
        st.markdown('<p class="section-title">Predict Marks by Age</p>', unsafe_allow_html=True)
        st.caption("Uses Linear Regression trained on your current student data.")

        input_age = st.slider("Select an age to predict expected marks", 15, 35, 20)

        if model:
            predicted = model.predict([[input_age]])[0]
            predicted = max(0, min(100, predicted))
            grade, label = predict_grade(predicted)
            st.markdown(f"""
            <div class="ai-box">
                <div class="ai-label">🤖 ML Prediction</div>
                A student aged <strong>{input_age}</strong> is predicted to score approximately 
                <strong>{predicted:.1f} / 100</strong> → Grade <strong>{grade}</strong> ({label}).
                <br><br>
                <span style="color:#64748b; font-size:12px;">
                Model trained on {len(df)} students · R² = {model.score(df[['Age']], df['Marks']):.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)

        # ── 3. At-risk students table ──────────────────────────────────
        st.markdown("---")
        st.markdown('<p class="section-title">At-Risk Students (Marks < 60)</p>', unsafe_allow_html=True)
        at_risk = df[df["Marks"] < 60][["ID", "Name", "Course", "Marks", "Grade"]]
        if at_risk.empty:
            st.success("✓ No at-risk students. All students are passing.")
        else:
            st.dataframe(at_risk, use_container_width=True, hide_index=True)
            st.markdown(f"""
            <div class="ai-box">
                <div class="ai-label">⚠️ Recommendation</div>
                {len(at_risk)} student(s) have marks below 60 and may need academic support 
                or additional coaching.
            </div>
            """, unsafe_allow_html=True)