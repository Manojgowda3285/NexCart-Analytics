


/*==========================================================
  PRIMARY KEYS
==========================================================*/

ALTER TABLE dim_customer
ADD CONSTRAINT pk_dim_customer
PRIMARY KEY (CustomerID);

ALTER TABLE dim_date
ADD CONSTRAINT pk_dim_date
PRIMARY KEY (DateKey);

ALTER TABLE dim_product
ADD CONSTRAINT pk_dim_product
PRIMARY KEY (ProductID);

ALTER TABLE dim_seller
ADD CONSTRAINT pk_dim_seller
PRIMARY KEY (SellerID);

ALTER TABLE dim_warehouse
ADD CONSTRAINT pk_dim_warehouse
PRIMARY KEY (WarehouseID);

ALTER TABLE fact_order_items
ADD CONSTRAINT pk_fact_order_items
PRIMARY KEY (OrderItemID);

ALTER TABLE fact_inventory_snapshot
ADD CONSTRAINT pk_fact_inventory_snapshot
PRIMARY KEY (InventoryID);




