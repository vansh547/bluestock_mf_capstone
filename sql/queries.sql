SELECT fund_house, aum_crore 
FROM fact_aum 
ORDER BY aum_crore DESC 
LIMIT 5;

SELECT amfi_code, strftime('%Y-%m', date) AS month, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month;

SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

SELECT amfi_code, scheme_name, expense_ratio_pct 
FROM fact_performance 
WHERE expense_ratio_pct < 1.0;

SELECT risk_category, COUNT(*) as scheme_count
FROM dim_fund
GROUP BY risk_category;

SELECT transaction_type, COUNT(*) as volume, SUM(amount_inr) as total_value
FROM fact_transactions
GROUP BY transaction_type;

SELECT strftime('%Y-%m', transaction_date) AS sip_month, SUM(amount_inr) as total_sip_inflow
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY sip_month
ORDER BY sip_month ASC;

SELECT amfi_code, scheme_name, return_3yr_pct 
FROM fact_performance 
WHERE return_3yr_pct IS NOT NULL
ORDER BY return_3yr_pct DESC 
LIMIT 5;

SELECT kyc_status, COUNT(*) as count, AVG(amount_inr) as avg_transaction_amount
FROM fact_transactions
GROUP BY kyc_status;


SELECT category, COUNT(*) as total_schemes
FROM dim_fund
GROUP BY category
ORDER BY total_schemes DESC;