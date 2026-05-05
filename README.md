# 🏙️ NYC 311 Service Requests Analysis
### *"What if Cairo had 311?"*

An end-to-end data analysis project on NYC 311 service requests, built as part of the Epsilon AI Data Science Diploma at Epsilon AI Academy.

## 💡 Project Idea
Every day, millions of New York City residents call **311** to report issues — noise complaints, illegal parking, broken infrastructure, and more. The city listens, tracks, and responds to every single one.

This raised a question: **What if Cairo had a 311 service?**

Cairo, like many cities in the developing world, lacks a centralized open data infrastructure for citizen complaints. There is no public dataset, no transparent response tracking, and no way to measure how well the city serves its residents.

This project uses NYC's rich 311 dataset as a **simulation lens** — by deeply understanding how a world-class city manages 2.9 million complaints, we can extract a framework of what an effective urban complaint system looks like, and imagine what insights Cairo *could* generate if such a system existed.

The goal is not just EDA — it is to answer:
- What complaint types dominate a large city?
- Which areas are underserved?
- How fast does the system respond, and to whom?
- What patterns emerge across time, borough, and agency?

These are questions Cairo cannot yet answer about itself. NYC can show us what the answers might look like.

## 📂 Project Structure
| File | Description |
|------|-------------|
| `Data Handling.ipynb` | Data loading, cleaning, and feature engineering |
| `EDA_nyc311.ipynb` | Exploratory data analysis and visualizations |
| `Insights.ipynb` | Deep-dive insights and findings |
| `Home.py` | Streamlit dashboard entry point |
| `Pages/` | Additional dashboard pages |

## 📊 Dataset
The full dataset (~2.9M rows) is hosted on Kaggle:  
👉 [NYC 311 Service Requests Dataset](https://www.kaggle.com/datasets/tarneemmedhat/311-service-requests-sample-csv)

Download the CSV and place it in the root project folder before running the notebooks.

## 🚀 How to Run
1. Clone the repository
2. Download the dataset from the Kaggle link above and place it in the root folder
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Run notebooks in this order:
   - `Data Handling.ipynb`
   - `EDA_nyc311.ipynb`
   - `Insights.ipynb`
5. Launch the dashboard:
```bash
   streamlit run Home.py
```

## 🛠️ Tools & Libraries
- Python, Pandas, Geopy
- Plotly
- Streamlit
- Jupyter Notebook
