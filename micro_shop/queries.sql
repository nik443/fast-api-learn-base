SELECT orders.promocode, orders.created_ad, orders.id
FROM orders
ORDER BY orders.id


SELECT
    order_product_association.order_id AS order_product_association_order_id,
    order_product_association.product_id AS order_product_association_product_id,
    order_product_association.count AS order_product_association_count,
    order_product_association.id AS order_product_association_id,
    products_1.name AS products_1_name,
    products_1.description AS products_1_description,
    products_1.price AS products_1_price,
    products_1.id AS products_1_id
FROM order_product_association
    LEFT OUTER JOIN products AS products_1 ON products_1.id = order_product_association.product_id
WHERE order_product_association.order_id IN (?, ?)