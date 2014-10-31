#!/bin/bash
for i in {0..15}
	do
		echo "CREATE TABLE IF NOT EXISTS ItemsWeek$i LIKE ebay.Items;" | mysql -u root -D ebay
done
