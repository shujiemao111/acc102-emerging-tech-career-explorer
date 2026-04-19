# Emerging Tech Career Explorer

## 1. Problem & User
This project explores which skills are most in demand in emerging technology industries and how these skills relate to salary patterns. It is designed for university students who want to understand the job market and make better career planning decisions in fields such as Artificial Intelligence, Blockchain, Green Tech, and Quantum Computing.

## 2. Data 
- **Source:** Kaggle
- **Dataset:** `future_jobs_dataset.csv`
- **Access date:** [2026.4.14]
- **Key fields:** `job_title`, `industry`, `salary_usd`, `skills_required`

## 3. Methods 
- Loaded the dataset using `pandas`
- Cleaned and checked the salary data
- Processed the `skills_required` column
- Counted skill frequency across job postings
- Compared salary patterns by industry, job title, and selected skills
- Created charts with `matplotlib` and `seaborn`
- Built an interactive Streamlit app for data exploration

## 4. Key Findings 
- Some skills appear much more frequently than others in emerging technology job postings.
- Skill demand differs across industries such as AI, Blockchain, Green Tech, and Quantum Computing.
- Salary patterns vary across industries and job titles, but the differences are not always large.
- Some selected skills are linked to relatively higher salary levels in certain contexts.
- The results can help students identify useful skills for future career preparation.

## 5. How to run
1.Download this repository and extract it to a folder.
2.Make sure app.py, requirements.txt, and future_jobs_dataset.csv are in the same folder.
3.Open Anaconda Prompt and navigate to your project folder.
4.Install required libraries:
  pip install -r requirements.txt
5.Run the Streamlit application:
  streamlit run app.py

## 6. Product link / Demo

-   **Product link:** [Paste your Streamlit app link here]
-   **Demo video:** [Paste your demo video link here]

## 7. Limitations & next steps

### Limitations

-   The analysis depends on the quality and completeness of the dataset.
-   The dataset may not fully represent the entire real-world job market.
-   The project mainly uses descriptive analysis rather than advanced predictive modelling.

### Next steps

-   Add more filters such as location and experience level.
-   Improve skill grouping and text cleaning.
-   Expand the dataset to include more job postings.
-   Add more interactive features to the Streamlit app.
   
