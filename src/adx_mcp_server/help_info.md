# Azure Data Explorer MCP Help Information

## Table Names and Columns
1. **BillingUsage_Daily**: Date,Region,SubscriptionId,ResourceId,SKU,Quantity
2. **ResourceMetrics**: Date,Region,ResourceId,SumMessageCount,MaxConnectionCount,AvgConnectionCount,SumSystemErrors,SumTotalOperations

## Predefined Queries
1. **List Tables**: `.show tables | project TableName, Folder, DatabaseName`
2. **Table Schema**: `.show table <table_name>`
3. **Sample Data**: `<table_name> | sample 10`
4. **Function Schema**: `.show function <function_name>`
5. **Query Example: Query recent top AI customers**:
    ```
    BillingUsage_Daily
    // filter the time window, 
    | where Date >= startofmonth(now(), -1) and Date < startofmonth(now()) and 
    // filter AI naming pattern in ResourceId
    (ResourceId has 'ai' or ResourceId has 'gpt' or ResourceId has 'ml' or ResourceId has 'cognitive' or ResourceId contains 'openai' or ResourceId contains 'chatgpt')
    // calculate revenuw
    | extend Revenue = case(SKU == 'Free', 0.0, SKU == 'Standard', 1.61, SKU == 'Premium', 2.0, 1.0) * Quantity
    // join metrics table to get metrics usage like message count and connection count
    | join kind = inner (ResourceMetrics) on Date, ResourceId
    | summarize Revenue = sum(Revenue), Units = sumif(Quantity, SKU in ('Standard', 'Premium')), MessageCount = sum(SumMessageCount), MaxConnectionCount = max(MaxConnectionCount) by ResourceId, Region, SubscriptionId
    // join CustomerModel function to get customer information
    | join kind = inner (CustomerModel) on SubscriptionId
    | where SubscriptionId != 'c24a3833-f66c-4c0b-8263-91c5cc408ff9'
    | where MessageCount > 10000 and MaxConnectionCount > 20
    | top 10 by Revenue
    | project ResourceId, Region, SubscriptionId, SubscriptionCreatedDate, Revenue, Units, MessageCount, MaxConnectionCount, CustomerName, BillingType, SegmentName, S500
    ```
6. **Query Example: Query recent CSS (Customer Support Service cases)**: `CSSTicketsByStartTime(<start_time>)`
7. **Query Example: Query Customer information**: `CustomerModel | where SubscriptionId == <SubscriptionId> | project CustomerName, SubscriptionId, BillingType`
