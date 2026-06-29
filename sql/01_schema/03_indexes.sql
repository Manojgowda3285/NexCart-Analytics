/*==========================================================
  INDEXES - FACT ORDER ITEMS
==========================================================*/

CREATE INDEX idx_order_customer
ON fact_order_items(CustomerID);

CREATE INDEX idx_order_product
ON fact_order_items(ProductID);

CREATE INDEX idx_order_seller
ON fact_order_items(SellerID);

CREATE INDEX idx_order_warehouse
ON fact_order_items(WarehouseID);

CREATE INDEX idx_order_date
ON fact_order_items(OrderDateKey);

CREATE INDEX idx_delivery_date
ON fact_order_items(DeliveryDateKey);

/*==========================================================
  INDEXES - FACT INVENTORY SNAPSHOT
==========================================================*/

CREATE INDEX idx_inventory_product
ON fact_inventory_snapshot(ProductID);

CREATE INDEX idx_inventory_warehouse
ON fact_inventory_snapshot(WarehouseID);

CREATE INDEX idx_inventory_date
ON fact_inventory_snapshot(SnapshotDateKey);