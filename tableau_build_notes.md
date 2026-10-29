# My Tableau build notes — TheLook 2023

These are my own notes for how I built the dashboard, so I can rebuild it exactly.

## My published dashboard

- Tableau Public link: https://public.tableau.com/app/profile/jayadeep.varma.dandu/viz/TheLookeCommerce2023SalesDashboard/Dashboard1
- Workbook name on publish: "TheLook eCommerce 2023 — Sales Dashboard"
- Dashboard title inside: "TheLook eCommerce — 2023 Sales Dashboard"
- Dashboard subtitle inside: "Fictitious sample data (TheLook / Looker), 2023 orders only. Revenue = Completed orders only. Gross margin = sale price minus product cost."
- First published: October 29, 2026
- Data source I used in Tableau: my single flat file, 85,528 rows, item grain, 2023 orders only, personal information already dropped. I used an Extract, not Live, for publishing.

## My calculated fields

I created these fields in Tableau. If Tableau shows underscores as spaces, I use the name shown in my Data pane.

- Revenue Complete: `SUM(IF [status] = 'Complete' THEN [sale_price] ELSE 0 END)`
- Completed Orders: `COUNTD(IF [status] = 'Complete' THEN [order_id] END)`
- AOV Complete: `[Revenue Complete] / [Completed Orders]`
- Return Rate: `SUM(IF [status] = 'Returned' THEN 1 ELSE 0 END) / COUNT([id])` — where [id] is the order_items id
- Cancel Rate: `SUM(IF [status] = 'Cancelled' THEN 1 ELSE 0 END) / COUNT([id])`
- Margin Complete: `SUM(IF [status] = 'Complete' THEN [sale_price] - [cost] ELSE 0 END)`
- Margin %: `[Margin Complete] / [Revenue Complete]`

## My sheets

1. Trend: order month on Columns, Revenue Complete on Rows — 12 marks, 2023-01 to 2023-12 only, total $1,286,122.
2. What sells: category on Rows, sorted descending by Revenue Complete, Margin % on Colour. My margin % legend runs 0.3714 to 0.6229.
3. Who buys — Country: country sorted descending by Revenue Complete. China, United States, and Brasil are first.
4. Who buys — Traffic: traffic source by Revenue Complete. Search is first, then Organic, Facebook, Email, and Display.
5. Operations — Status: count of items by status, in Shipped, Complete, Processing, Cancelled, Returned order. Total items 85,528.
6. Return by Category: return rate by category, axis 0.00 to 0.13.

I built country and traffic source as separate sheets, and status counts and return by category as separate sheets, so my dashboard has 6 sheets, not 4.

## My dashboard layout

- Title and subtitle as above
- KPI tiles on top: Completed Orders 14,817, Revenue Complete $1,286,122, AOV $86.80, Return Rate 10.18% — with a note that these are values with filters cleared, because my KPI display is a static text box and does not change when I filter (my charts do)
- Trend full width
- Category and buyers side by side
- Operations full width

## My filters and action

Filters, applied to all sheets:
- Order Month: 12 values, 2023-01 to 2023-12
- Category: 26 values
- Department: Men, Women
- Country: 16 values

I did not add a Status filter to my revenue sheets. Status belongs only on my Operations sheets.

Dashboard action: "Filter by Category" — source is What sells only, targets are all 6 sheets, Run on Select, Clearing shows all values, Filter is All fields.

"Show sheets as tabs" was enabled when I published, so my individual sheets also show as tabs alongside Dashboard 1.
