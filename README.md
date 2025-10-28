🌍 Global Human Impact Dashboard
🖤 Overview
The Global Human Impact Dashboard is an interactive data analytics web app built with Streamlit, designed to visualise how various global calamities affect humanity.
It integrates multiple datasets — from pandemics and pollution to road and conflict fatalities — into one cohesive dark-themed dashboard.

📊 Datasets Used
The app processes and visualises five major datasets:
🦠 COVID-19 Pandemic Data — Global infection and fatality rates.
🐖 H1N1 (Swine Flu) Data — Historical outbreak trends and mortality.
🌫️ Air Pollution (PM2.5) — Average air quality levels across nations.
🚗 Road Accident Fatalities — WHO road safety and death statistics.
⚔️ Conflict & War Fatalities — Human losses in major global conflicts.

💡 Features
Dynamic country & year filtering
Metric cards highlighting total impact
Interactive trend lines, bar charts, and choropleth maps
Elegant dark-mode interface
Built entirely using free, open-source tools

⚙️ Technologies Used
Streamlit for the web app interface
Pandas for data processing
Plotly Express for interactive visualisations

🚀 Deployment
The dashboard is hosted freely on Streamlit Community Cloud:
👉 https://global-human-impact-dashboard.streamlit.app

To run locally:
pip install -r requirements.txt
streamlit run app.py

📂 Folder Structure
global_human_impact_dashboard/
│
├── app.py
├── clean_covid19_data.csv
├── clean_h1n1_data.csv
├── clean_pm25_air_pollution.csv
├── clean_road_accident_fatalities.csv
├── clean_conflict_fatalities.csv
└── requirements.txt

👤 Author

Vishwajeet
📧 vishwajeetdhali42@gmail.com 
🖤 Dark Mode Edition — Powered by Data and Streamlit
