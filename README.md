## Live Demo
https://nightbyte-business-intelligence-dashboard-8tayl8rw7n5mgyvephoa.streamlit.app/
# NightByte Business Intelligence & Demand Forecasting Dashboard

A food delivery analytics dashboard built using Python, Pandas, Streamlit, Matplotlib, and Scikit-Learn.

## Project Overview

This project analyzes 1000+ food delivery orders for a canteen-style ordering platform. It provides business insights into revenue, customer behavior, popular food items, peak ordering hours, payment trends, and demand forecasting.

## Features

- Total revenue, total orders, average order value
- Top selling food items
- Item-wise revenue analysis
- Peak ordering hour analysis
- Location-wise revenue analysis
- Payment mode distribution
- Daily revenue trend
- Customer segmentation
- Machine learning based revenue prediction
- Interactive filters
- Download filtered dataset

## Tech Stack

- Python
- Pandas
- Matplotlib
- Scikit-Learn
- Streamlit

## Machine Learning

Used Linear Regression to predict next-day revenue based on daily revenue trends.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py