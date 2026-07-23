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

## Architecture

*(Architecture diagram coming soon)*

The application consists of four main components:

### 1. Data Collection

- Retrieves Pokémon card information and pricing data through external API.
- Focuses on English Pokémon cards across all available sets.
- Collects daily market snapshots.

### 2. ETL Pipeline

- Cleans and transforms raw API responses.
- Standardizes card information and pricing fields.
- Handles missing values and maintains consistent data quality.
- Prepares data for database storage.

### 3. Database Storage

Data is stored using **Supabase PostgreSQL**.

The database maintains:

**Card Information**
- Card name
- Set
- Card number
- Rarity
- Release information
- Other card metadata

**Price History**
- Card identifier
- Date of price snapshot
- Market price
- Historical price changes (last 7d, 14d, etc)

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
- Pandas
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

-The original version of this project used web scraping from PriceCharting.com to collect data, which had a few issues.
-For storage I used GCS (Google Cloud Storage) - also wanted to move on from this.

The project has since been redesigned around API-based data collection and Supabase to improve reliability, scalability, and automation.

---

# Demo

Streamlit App: Coming soon...

---

# Medium Articles

Previous project development:

- Part 1: Building a Pokémon Card Price Tracker App with Web Scraping ()
- Part 2: Historical Tracking, Cloud Storage, and Interactive Analysis ()

- FINAL APP: Coming Soon...