QUERY_1_CMD = """
    CREATE OR REPLACE FUNCTION query_1()
        RETURNS TABLE (
            id INTEGER,
            first_name VARCHAR,
            email VARCHAR
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                owner.id,
                owner.first_name,
                owner.email
            FROM
                owner;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_2_CMD = """
    CREATE OR REPLACE FUNCTION query_2()
        RETURNS TABLE (
            id INTEGER,
            brand VARCHAR,
            max_capacity SMALLINT
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                vehicle.id,
                vehicle.brand,
                vehicle.max_capacity
            FROM
                vehicle
            WHERE
                vehicle.max_capacity < 15;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_3_CMD = """
    CREATE OR REPLACE FUNCTION query_3()
        RETURNS TABLE (
            id INTEGER,
            name VARCHAR,
            address VARCHAR,
            max_capacity INTEGER
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                warehouse.id,
                warehouse.name,
                warehouse.address,
                warehouse.max_capacity
            FROM
                warehouse
            WHERE warehouse.max_capacity = (
                SELECT MAX(warehouse.max_capacity) FROM warehouse
            );
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_4_CMD = """
    CREATE OR REPLACE FUNCTION query_4(DATE)
        RETURNS TABLE (
            id INTEGER,
            name VARCHAR,
            address VARCHAR,
            date_start TIMESTAMP,
            date_end TIMESTAMP
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                warehouse.id,
                warehouse.name,
                warehouse.address,
                transit.date_start,
                transit.date_end
            FROM
                transit
            INNER JOIN
                warehouse ON warehouse.id = transit.warehouse_id
            WHERE
                transit.date_start::date = $1;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_5_CMD = """
    CREATE OR REPLACE FUNCTION query_5(VARCHAR, VARCHAR)
        RETURNS TABLE (
            id INTEGER,
            first_name VARCHAR,
            last_name VARCHAR,
            total_payload BIGINT
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                owner.id,
                owner.first_name,
                owner.last_name,
                SUM(warehouse.max_capacity)
            FROM
                warehouse
            INNER JOIN owner ON owner.id = warehouse.owner_id
            WHERE
                LOWER(owner.first_name) = LOWER($1) AND
                LOWER(owner.last_name) = LOWER($2)
            GROUP BY owner.id;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_6_CMD = """
    CREATE OR REPLACE FUNCTION query_6(VARCHAR, VARCHAR, DATE)
        RETURNS TABLE (
            id INTEGER,
            address VARCHAR,
            date DATE
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                warehouse.id,
                warehouse.address,
                transit.date_start::date
            FROM
                warehouse
            INNER JOIN
                transit ON warehouse.id = transit.warehouse_id
            INNER JOIN
                vehicle_transit ON vehicle_transit.transit_id = transit.id
            INNER JOIN
                vehicle ON vehicle.id = vehicle_transit.vehicle_id
            INNER JOIN
                owner ON owner.id = vehicle.owner_id
            WHERE
                LOWER(owner.first_name) = LOWER($1) AND
                LOWER(owner.last_name) = LOWER($2) AND
                transit.date_start::date = $3;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_7_CMD = """
    CREATE OR REPLACE FUNCTION query_7(DATE)
        RETURNS TABLE (
            id INTEGER,
            brand VARCHAR,
            max_capacity SMALLINT,
            date_start TIMESTAMP
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                DISTINCT vehicle.id,
                vehicle.brand,
                vehicle.max_capacity,
                product_shop_order.date_start
            FROM
                vehicle
            INNER JOIN
                product_shop_order ON product_shop_order.vehicle_id = vehicle.id
            WHERE
                EXTRACT(HOUR FROM product_shop_order.date_start) >= 16 AND
                product_shop_order.date_start::date = $1
            ORDER BY
                vehicle.max_capacity DESC;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_8_CMD = """
    CREATE OR REPLACE FUNCTION query_8 (DATE)
        RETURNS TABLE (
            id INTEGER,
            address VARCHAR
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                warehouse.id,
                warehouse.address
            FROM
                warehouse
            INNER JOIN
                product_shop_order ON product_shop_order.warehouse_id = warehouse.id
            WHERE
                product_shop_order.date_start::date = $1
            GROUP BY
                warehouse.id
            HAVING
                COUNT(*) = (
                    SELECT
                        COUNT(*) AS cnt
                    FROM
                        product_shop_order
                    WHERE
                        product_shop_order.date_start::date = $1
                    GROUP BY
                        product_shop_order.warehouse_id
                    ORDER BY
                        cnt ASC
                    LIMIT 1
                );
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_9_CMD = """
    CREATE OR REPLACE FUNCTION query_9(DATE)
        RETURNS TABLE (
            count BIGINT
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                COUNT(*) as count
            FROM
                transit
            WHERE
                transit.date_start::date = $1
                AND EXTRACT(epoch FROM transit.date_end - transit.date_start) > 10800;
    END; $$

    LANGUAGE 'plpgsql';
"""

QUERY_10_CMD = """
    CREATE OR REPLACE FUNCTION query_10(VARCHAR, VARCHAR)
        RETURNS TABLE (
            id INTEGER,
            name VARCHAR,
            article_number INTEGER,
            tonnage BIGINT
        )
    AS $$
    BEGIN
        RETURN QUERY
            SELECT
                product.id,
                product.name,
                product.article_number,
                SUM(product_warehouse.payload) as tonnage
            FROM
                warehouse
            INNER JOIN
                product_warehouse ON product_warehouse.warehouse_id = warehouse.id
            INNER JOIN
                product ON product.id = product_warehouse.product_id
            WHERE
                LOWER(warehouse.name) = LOWER($1)
                AND LOWER(warehouse.address) = LOWER($2)
            GROUP BY
                product.id
            ORDER BY
                tonnage DESC
            LIMIT 1;
    END; $$

    LANGUAGE 'plpgsql';
"""

CREATE_FUNCTIONS = [
    QUERY_1_CMD,
    QUERY_2_CMD,
    QUERY_3_CMD,
    QUERY_4_CMD,
    QUERY_5_CMD,
    QUERY_6_CMD,
    QUERY_7_CMD,
    QUERY_8_CMD,
    QUERY_9_CMD,
    QUERY_10_CMD
]
