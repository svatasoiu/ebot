CREATE TABLE `Items` (
  `EbayID` varchar(127) NOT NULL,
  `Title` varchar(255) NOT NULL,
  `BidPrice` decimal(10,2) DEFAULT NULL,
  `BINPrice` decimal(10,2) DEFAULT NULL,
  `SellerName` varchar(255) DEFAULT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `TimeLeft` int(11) DEFAULT NULL,
  `NumBids` int(11) DEFAULT NULL,
  `SearchTerm` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`EbayID`)
)
