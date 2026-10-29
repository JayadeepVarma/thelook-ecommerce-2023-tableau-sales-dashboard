# TheLook eCommerce — 2023 Sales Dashboard (Tableau Public)

By Jayadeep Varma Dandu

**Live dashboard:** https://public.tableau.com/app/profile/jayadeep.varma.dandu/viz/TheLookeCommerce2023SalesDashboard/Dashboard1

## What I built

I built a Tableau Public sales dashboard for TheLook eCommerce, a fictitious clothing store, using only orders from 2023. I wanted a clean, commercial sales story for my portfolio — something different from my healthcare and transport projects — so I focused on revenue, margin, what sells, who buys, and operations, all from one 2023 slice.

I built the dashboard in Tableau Public Web Authoring, from a single flat file I prepared in Python. I did not use live BigQuery, because live totals drift. I froze a 2023 snapshot first, and then built from that snapshot.

## Important: this data is fictitious

TheLook is a fictitious sample dataset created by the Looker team for product testing and evaluation. It is not a real company's results, and I do not present it as one.

- Source: Kaggle, "Looker Ecommerce BigQuery Dataset" by mustafakeser4
- Scope I used: orders created in 2023 only, from 4 tables only — orders, order_items, products, users
- Revenue in this dashboard: Completed orders only
- Gross margin in this dashboard: sale price minus product cost. That is a gross-margin proxy only. It is not net profit — I do not have shipping, marketing, or other costs in these tables, so I do not claim net profit anywhere.

## What I found (2023, Completed orders only)

| KPI | Value |
|---|---|
| Completed orders | 14,817 |
| Completed items | 21,525 |
| Revenue (Complete) | $1,286,122 |
| Average order value (Complete) | $86.80 |
| Return rate (by item) | 10.18% |
| Cancel rate (by item) | 14.90% |
| Gross margin (Complete) | $667,877 / 51.93% |

My monthly trend, by order month, runs from $73,593 in January 2023 to $179,675 in December 2023, for a total of $1,286,122.

What sells, by Completed revenue:
- Outerwear & Coats: $155,728
- Jeans: $146,295
- Sweaters: $101,777

By department, by Completed revenue:
- Men: $681,675
- Women: $604,447

Who buys, by Completed revenue:
- China: $452,666
- United States: $280,999
- Brasil: $190,870

By traffic source, by Completed revenue:
- Search: $915,136
- Organic: $185,097

## How I prepared the data

1. I downloaded the Kaggle dataset and kept the original files untouched.
2. I ran my own filtering script, `filter_thelook_2023.py`, which:
   - Keeps only orders created in 2023
   - Keeps only the items, products, and users linked to those 2023 orders
   - Drops personal information from users — first name, last name, email, street address, postal code, latitude, and longitude — before I used the file in Tableau
3. My 2023 slice, by file size:
   - Originals: 125,226 orders / 181,759 items / 29,120 products / 100,000 users
   - Filtered 2023: 59,041 orders / 85,528 items / 27,521 products / 44,513 users

I did not push the row-level data files to this repo. I push only my script and my build notes, plus this README. The row-level flat file I used in Tableau is 85,528 rows and 25 MB, and I keep it out of GitHub on purpose, to keep this repo light and to avoid publishing user-level rows. Anyone can reproduce my slice from the Kaggle source by running my script.

## How I built the dashboard

I built 6 sheets in Tableau, plus the dashboard:

1. **Trend** — order month vs. Revenue (Complete), January to December 2023 only
2. **What sells** — category vs. Revenue (Complete), with margin % on colour
3. **Who buys — Country** — country vs. Revenue (Complete)
4. **Who buys — Traffic** — traffic source vs. Revenue (Complete)
5. **Operations — Status** — count of items by status (Shipped 25,383, Complete 21,525, Processing 17,169, Cancelled 12,744, Returned 8,707)
6. **Operations — Return by Category** — return rate by category

My dashboard filters, applied to all sheets, are Order Month (12 values), Category (26 values), Department (Men, Women), and Country (16 values). I deliberately did not add a Status filter to the revenue sheets, because revenue here means Completed only, and a Status filter would change that definition.

I also added a dashboard action: clicking a category in "What sells" filters the other sheets. Clicking again restores the full dashboard.

My calculated fields, dashboard layout, and filter setup are written out in full in `tableau_build_notes.md`, so I can rebuild the dashboard exactly as I built it.

## Choices I made, and why

- **I used order month, not item month, for the trend.** Item timestamps leak into December 2022 ($234) and January 2024 ($9,254). Order month keeps the trend cleanly in 2023.
- **I did not merge country spellings.** The source has both Germany and Deutschland, and both Spain and España, as separate values, and Brasil as a spelling. I kept them as they are in the source, so my totals stay faithful to the source. That is also why my country filter shows 16 values, while Completed revenue shows 14 countries — Austria and España each have only one non-Complete item, so they appear in the filter but not in Completed revenue.
- **I did not claim a top product.** The same product name appears under two different product IDs in the source, so I do not quote a top product by name alone.
- **I kept my KPI tiles as cleared-filter values.** The KPI text box on my dashboard states the values with filters cleared. It does not change when I filter; the charts and their totals do. I note that on the dashboard itself, so no one mistakes a cleared-filter KPI for a filtered total.
- **I excluded 3,063 original orders with unparseable dates.** My 2023 scope is therefore "2023 orders with a parseable date", not every original row. I state that here rather than hiding it.

## Tools I used

- Tableau Public (Web Authoring) — dashboard, calculated fields, filters, and dashboard action
- Python (pandas) — filtering only, before Tableau
- Kaggle TheLook dataset — source data only, fictitious sample

## How to reproduce my work

1. Download the Kaggle dataset above and unzip it, keeping the originals untouched.
2. Run `python filter_thelook_2023.py --source ./thelook_original --output ./thelook_2023`
3. Join the filtered files (or flatten them to one item-grain file, as I did for Web Authoring) and upload to Tableau Public.
4. Follow `tableau_build_notes.md` for my calculated fields, sheets, filters, and dashboard action.
5. Publish to Tableau Public.
