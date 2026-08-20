# Pokémon Price Tracker

**Author:** Logan Laszewski

**Project Type:** Data Engineering, API Integration, Database Design, Data Analytics

**Status:** In Development

---

## Overview

The Pokémon Price Tracker is a data pipeline and analytics application designed to monitor Pokémon card market trends over time.

The project collects Pokémon card pricing data, stores historical records in a cloud database, and provides interactive dashboards and price data to analyze price movements, trends, and market opportunities across English Pokémon card sets.

The goal of this project is to build a warehouse of Pokémon market data that transforms raw pricing information into actionable insights within the Streamlit application, while also supporting further analysis outside of the application.

---


## Project Workflow

The project follows a this workflow:

Data Collection (API)
↓
Database Storage (Supabase PostgreSQL)
↓
Data Exploration & Analysis (SQL + Tableau)
↓
Identify Trends & Insights
↓
Interactive Dashboard / Web Application (Streamlit)

---

## Architecture

*(Architecture diagram coming soon)*

The application consists of four main components:

### 1. Data Collection

- **API:** pokemonpricetracker.com (English cards, TCGPlayer market prices)
- Replaces previous web scraping approach

### 2. ETL Pipeline

- `pipeline/api_fill_sets_FINAL.py` — one-time set data load
- `pipeline/api_fill_cards_FINAL.py` — initial card + price history load  
- `pipeline/api_daily_run_FINAL.py` — daily price updates

### 3. Database Storage

Data is stored using **Supabase PostgreSQL**.

Four tables:
- `sets` — set metadata
- `cards` — card metadata
- `price_history` — daily price snapshots
- (planned) `sealed_products` + `sealed_price_history`

### 4. Analytics Dashboard

A Streamlit application provides an interactive interface for exploring Pokémon card market data.


# Analytics & Insights

The dashboard will explore questions such as:

- Which cards are increasing in value?
- Which sets are performing best over time?
- How do card prices change after release events?
- Which cards show unusual price movement?
- How do different rarities perform historically?

---

# Technical Stack

## Languages

- Python

## Data Engineering

- API Integration
- Data Cleaning Pipelines
- Automated Data Collection

## Database

- Supabase PostgreSQL

## Visualization

- Streamlit
- Plotly
- Matplotlib

---

# Previous Version

**v1** — Web scraping from PriceCharting.com + Google Cloud Storage. Replaced due to scraping reliability issues and lack of historical price data.

**v2** — GitHub JSON repo (pokemon-tcg-data) for card/set metadata + pokemonpricetracker.com API for prices. Replaced because maintaining two data sources with mismatched IDs added unnecessary complexity.

**Current** — Single API source (pokemonpricetracker.com) for both metadata and pricing, stored in Supabase PostgreSQL.

---

# Demo

Streamlit App: Coming soon...

---

# Medium Articles

Previous project development:

- Part 1: Building a Pokémon Card Price Tracker App with Web Scraping ()
- Part 2: Historical Tracking, Cloud Storage, and Interactive Analysis ()

- FINAL APP: Coming Soon...