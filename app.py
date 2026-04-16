import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Emerging Tech Career Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Emerging Tech Career Explorer")
st.markdown("""
This interactive tool analyzes skill demand and salary patterns across AI, Blockchain, Green Tech, and Quantum Computing industries.
**Target User:** University students planning careers in emerging technology.
""")

# -----------------------------
# Load and Cache Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("future_jobs_dataset.csv")
    
    # 数据清洗
    df["salary_usd"] = pd.to_numeric(df["salary_usd"], errors="coerce")
    df = df.dropna(subset=["salary_usd"])
    
    # 技能拆分
    def clean_skills(text):
        if pd.isna(text): 
            return []
        return [s.strip().lower() for s in re.split(r'[;,]', str(text)) if s.strip()]
    
    df["skill_list"] = df["skills_required"].apply(clean_skills)
    return df

df = load_data()

# 生成全量 skills_df（用于Chart 2 全行业热力图）
skills_df = df.explode("skill_list", ignore_index=True)
skills_df.rename(columns={"skill_list": "skill"}, inplace=True)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
industry_list = ["All"] + sorted(df["industry"].unique().tolist())
selected_industry = st.sidebar.selectbox("Select Industry", industry_list)

# 筛选数据
if selected_industry != "All":
    filtered_df = df[df["industry"] == selected_industry]
    filtered_skills_df = skills_df[skills_df["industry"] == selected_industry]
else:
    filtered_df = df.copy()
    filtered_skills_df = skills_df.copy()

# -----------------------------
# Main Dashboard Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Job Postings", len(filtered_df))
with col2:
    avg_sal = filtered_df["salary_usd"].mean()
    st.metric("Average Salary", f"${avg_sal:,.0f}")
with col3:
    if not filtered_skills_df.empty:
        top_skill = filtered_skills_df["skill"].mode()[0].title()
        st.metric("Top Skill", top_skill)
    else:
        st.metric("Top Skill", "N/A")

st.divider()

# ==================================================
# 📊 CHART 1: Top 10 Most In-Demand Skills
# ==================================================
st.subheader(f"Chart 1: Top 10 Most In-Demand Skills: {selected_industry}")
st.markdown("This chart identifies the most frequently requested skills in the selected industry.")

if not filtered_skills_df.empty:
    skill_counts = filtered_skills_df["skill"].value_counts().head(10).reset_index()
    skill_counts.columns = ["skill", "count"]

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=skill_counts, x="count", y="skill", hue="skill", palette="viridis", legend=False)
    ax1.set_title(f"Top 10 Most In-Demand Skills: {selected_industry}", fontsize=14)
    ax1.set_xlabel("Number of Job Postings", fontsize=12)
    ax1.set_ylabel("Skill", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig1)
else:
    st.write("No skill data available for this selection.")

st.divider()

# ==================================================
# 📊 CHART 2: Skill Demand by Industry (Heatmap)
# ==================================================
st.subheader("Chart 2: Skill Demand by Industry (Top 10 Skills Overall)")
st.markdown("This heatmap compares how top 10 skills are demanded across all industries.")

top10_skill_names = skills_df["skill"].value_counts().head(10).index.tolist()
heatmap_data = (
    skills_df[skills_df["skill"].isin(top10_skill_names)]
    .groupby(["industry", "skill"])
    .size()
    .unstack(fill_value=0)
)
heatmap_data = heatmap_data[top10_skill_names]

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", ax=ax2)
ax2.set_title("Skill Demand by Industry (Top 10 Skills)", fontsize=14)
ax2.set_xlabel("Skill", fontsize=12)
ax2.set_ylabel("Industry", fontsize=12)
plt.tight_layout()
st.pyplot(fig2)

st.divider()


# ==================================================
# 📊 CHART 3: Relative Salary by Common Job Title
# ==================================================
st.subheader(f"Chart 4: Relative Salary by Common Job Title ({selected_industry})")
st.markdown("This chart compares the average salary of common job titles relative to the lowest-paying job title.")

if not filtered_df.empty:
    job_salary = (
        filtered_df.groupby("job_title")["salary_usd"]
        .agg(["mean"])
        .reset_index()
        .rename(columns={"mean": "average_salary"})
        .sort_values("average_salary", ascending=False)
    )

    min_salary = job_salary["average_salary"].min()
    job_salary["relative_salary_pct"] = (job_salary["average_salary"] / min_salary - 1) * 100

    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=job_salary, x="job_title", y="relative_salary_pct", 
                hue="job_title", palette="Purples_r", legend=False)
    ax4.set_title(f"Relative Salary by Job Title: {selected_industry}", fontsize=14)
    ax4.set_xlabel("Job Title", fontsize=12)
    ax4.set_ylabel("Relative Salary Increase (%)", fontsize=12)
    
    plt.xticks(rotation=45, ha="right")
    ax4.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig4)
else:
    st.write("No job title data available for this selection.")

st.divider()

# ==================================================
# 📊 CHART 4: Relative Salary for Selected High-Demand Skills
# ==================================================
st.subheader(f"Chart 5: Relative Salary for Selected Skills ({selected_industry})")
st.markdown("This chart shows the salary premium for top 8 high-demand skills relative to the lowest-paying skill.")

if not filtered_skills_df.empty:
    top8_skills = filtered_skills_df["skill"].value_counts().head(8).index.tolist()
    skill_salary = (
        filtered_skills_df[filtered_skills_df["skill"].isin(top8_skills)]
        .groupby("skill")["salary_usd"]
        .agg(["mean", "count"])
        .reset_index()
        .sort_values("mean", ascending=False)
    )
    skill_salary.columns = ["skill", "average_salary", "job_count"]
    skill_salary = skill_salary[skill_salary["job_count"] >= 5]

    if not skill_salary.empty:
        min_salary_skill = skill_salary["average_salary"].min()
        skill_salary["relative_salary_pct"] = (skill_salary["average_salary"] / min_salary_skill - 1) * 100

        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=skill_salary, x="skill", y="relative_salary_pct", 
                    hue="skill", palette="Reds_r", legend=False, dodge=False)
        ax5.set_title(f"Relative Salary by Skill: {selected_industry}", fontsize=14)
        ax5.set_xlabel("Skill", fontsize=12)
        ax5.set_ylabel("Relative Salary Increase (%)", fontsize=12)
       
        plt.xticks(rotation=30, ha="right")
        ax5.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig5)
    else:
        st.write("No skill salary data available for this selection.")
else:
    st.write("No skill data available for this selection.")

st.divider()

# ==================================================
# 📋 Raw Data Explorer
# ==================================================
with st.expander(f"View Full Job Posting Data: {selected_industry}"):
    st.dataframe(filtered_df.drop(columns=["skill_list"]), use_container_width=True)

# ==================================================
# 📝 Footer
# ==================================================
st.info("""
**Key Insights:**
- Quantum Computing and AI lead in salary premiums, while Green Tech and Blockchain offer competitive compensation.
- Foundational skills like Qiskit, Quantum Algorithms, and Linear Algebra command the highest salary premiums.
- Career choices should balance skill demand, salary potential, and personal interest.
""")

st.info("""
**Note:** This analysis suggests that career choices in emerging tech should be guided by skill demand and personal interest, as average salaries across AI, Blockchain, Green Tech, and Quantum sectors are relatively comparable.
""")