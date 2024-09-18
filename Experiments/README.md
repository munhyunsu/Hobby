# Export query result as csv file

```sql
.header on
.mode csv
.once output.csv
SELECT * FROM message ORDER BY created_at ASC;
```
