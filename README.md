# Blukola Data Transformation Project

## Project Overview

This project focuses on transforming raw e-commerce data into structured, reliable, and analytics-ready datasets using **dbt (Data Build Tool)** and **Snowflake**.

The goal is to organise data from different business areas, including customers, orders, order items, products, and payments, into well-structured models that can support business reporting and analysis.

This project is part of my ongoing journey into Data Engineering, where I am building practical experience with SQL, data transformation, data modelling, and data quality testing.

## Tools and Technologies

- **dbt:** Data transformation and modelling.
- **Snowflake:** Cloud data warehouse.
- **SQL:** Data manipulation and transformation.
- **Git and GitHub:** Version control and project management.

## Project Structure

The project follows a modular dbt structure:

```text
blukola/
│
├── models/
│   ├── staging/
│   │   ├── _sources.yml
│   │   ├── _staging.yml
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   ├── stg_order_items.sql
│   │   ├── stg_payments.sql
│   │   └── stg_products.sql
│   │
│   └── marts/
│       ├── customers.sql
│       ├── fct_orders.sql
│       ├── order_items.sql
│       ├── products.sql
│       └── ...
│
├── seeds/
├── macros/
├── dbt_project.yml
├── packages.yml
└── README.md
```

## Work Completed

### 1. Staging Models

Created staging models to prepare raw data for downstream transformations.

The staging layer covers:

- Customers
- Orders
- Order items
- Payments
- Products

### 2. Data Marts

Developed analytical models to organise the data around key business entities and processes.

Models completed and validated so far include:

- **fct_orders:** Provides order-level information, including order value, quantity, customer details, successful payments, and outstanding amounts.
- **customers:** Provides a customer-level overview, including lifetime orders, successful payment amounts, failed payment amounts, and customer classification.
- **order_items:** Provides item-level details, including product, quantity, unit price, and order information.
- **products:** Product dimension model currently being developed.

### 3. Data Quality Testing

Implemented dbt tests to improve data reliability and consistency.

Tests used include:

- `not_null` – checks for missing values.
- `unique` – checks for duplicate records.
- `relationships` – validates relationships between models.
- `accepted_values` – checks that columns contain expected values.
- `dbt_utils.expression_is_true` – validates business rules and SQL expressions.

### 4. Data Validation

Performed additional SQL checks to validate model outputs, including:

- Checking record counts and unique identifiers.
- Validating relationships between staging models.
- Checking calculations and aggregations.
- Reconciling successful payments against order values.
- Ensuring that transformations preserve the expected data grain.

## Key Concepts Practised

Through this project, I have gained practical experience with:

- dbt project structure and configuration.
- Sources and model references using `source()` and `ref()`.
- Staging and dimensional modelling.
- Fact and dimension tables.
- Common Table Expressions (CTEs).
- SQL joins, aggregations, and conditional logic.
- Data grain and avoiding duplicate records.
- Data quality testing and validation.
- Building transformations in Snowflake.

## Running the Project

To run this project locally, you need:

- Python installed.
- dbt with the Snowflake adapter installed.
- Access to a Snowflake account.
- A properly configured dbt `profiles.yml` file.

Configure your own Snowflake connection in `profiles.yml` before running the commands. Do not commit credentials, passwords, or other sensitive connection details to GitHub.

Run the following commands from the project directory:

```bash
# Check the dbt connection
dbt debug

# Parse the project
dbt parse

# Run staging models
dbt run --select staging

# Run a specific mart model
dbt run --select fct_orders

# Run tests for a specific model
dbt test --select fct_orders

# Build models and run associated tests
dbt build
```

`dbt build` builds selected resources and runs their associated tests according to the project's configuration and dependencies.

## Current Project Status

The staging layer has been completed and validated. Development and testing of the data marts are ongoing.

The project is being developed incrementally, with emphasis on understanding the transformation logic, validating business rules, and ensuring that the resulting datasets are reliable.

## Learning Objective

My objective is to strengthen my practical Data Engineering skills by building a complete transformation workflow with dbt and Snowflake, while developing a deeper understanding of data modelling, data quality, and analytics engineering.

**This project is a work in progress, and I will continue updating it as I implement and validate more models.**
