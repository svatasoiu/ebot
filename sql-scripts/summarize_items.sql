select SearchTerm, count(*), avg(BidPrice) as AvgBid, avg(BINPrice) as AvgBIN from Items GROUP BY SearchTerm;
