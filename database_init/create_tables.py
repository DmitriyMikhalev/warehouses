OWNER_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS owner(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(15) NOT NULL,
        last_name VARCHAR(15) NOT NULL,
        email VARCHAR(30) NOT NULL UNIQUE
    );
"""

WAREHOUSE_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS warehouse(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE,
        address VARCHAR(50) NOT NULL,
        max_capacity INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES owner (id) ON DELETE CASCADE,
        CHECK(max_capacity > 0)
    );
"""

VEHICLE_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS vehicle(
        id SERIAL PRIMARY KEY,
        brand VARCHAR(30) NOT NULL,
        max_capacity SMALLINT NOT NULL,
        owner_id INTEGER NOT NULL,
        vin VARCHAR(17) NOT NULL UNIQUE,
        FOREIGN KEY (owner_id) REFERENCES owner (id) ON DELETE CASCADE,
        CHECK(max_capacity > 0)
    );
"""

SHOP_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS shop(
        id SERIAL PRIMARY KEY,
        address VARCHAR(50) NOT NULL,
        name VARCHAR(50) NOT NULL UNIQUE,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES owner (id) ON DELETE CASCADE
    );
"""

PRODUCT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS product(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        article_number INTEGER NOT NULL UNIQUE
    );
"""

TRANSIT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS transit(
        id SERIAL PRIMARY KEY,
        warehouse_id INTEGER NOT NULL,
        date_start TIMESTAMPTZ NOT NULL,
        date_end TIMESTAMPTZ NOT NULL,
        accepted BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (warehouse_id) REFERENCES warehouse (id) ON DELETE CASCADE,
        CHECK(date_end > date_start)
    );
"""

VEHICLE_TRANSIT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS vehicle_transit(
        id SERIAL PRIMARY KEY,
        transit_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        FOREIGN KEY (transit_id) REFERENCES transit (id) ON DELETE CASCADE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicle (id) ON DELETE CASCADE,
        UNIQUE(transit_id, vehicle_id)
    );
"""

PRODUCT_TRANSIT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS product_transit(
        id SERIAL PRIMARY KEY,
        transit_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        payload SMALLINT NOT NULL,
        FOREIGN KEY (transit_id) REFERENCES transit (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
        UNIQUE(transit_id, product_id),
        CHECK(payload > 0)
    );
"""

ORDER_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS order_table(
        id SERIAL PRIMARY KEY,
        shop_id INTEGER NOT NULL,
        warehouse_id INTEGER NOT NULL,
        date_start TIMESTAMPTZ NOT NULL,
        date_end TIMESTAMPTZ NOT NULL,
        accepted BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (shop_id) REFERENCES shop (id) ON DELETE CASCADE,
        FOREIGN KEY (warehouse_id) REFERENCES warehouse (id) ON DELETE CASCADE,
        CHECK(date_end > date_start)
    );
"""

PRODUCT_ORDER_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS product_order(
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        payload SMALLINT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES order_table (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
        UNIQUE(order_id, product_id),
        CHECK(payload > 0)
    );
"""

PRODUCT_WAREHOUSE_CMD = """
    CREATE TABLE IF NOT EXISTS product_warehouse(
        id SERIAL PRIMARY KEY,
        warehouse_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        payload INTEGER NOT NULL,
        FOREIGN KEY (warehouse_id) REFERENCES warehouse (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
        CHECK(payload > 0),
        UNIQUE(warehouse_id, product_id)
    )
"""

VEHICLE_ORDER_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS vehicle_order(
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES order_table (id) ON DELETE CASCADE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicle (id) ON DELETE CASCADE,
        UNIQUE(order_id, vehicle_id)
    );
"""

PRODUCT_NAME_INDEX_CMD = """
    CREATE UNIQUE INDEX IF NOT EXISTS product_article_index ON product (
        name,
        article_number
    );
"""

CREATE_TABLES_CMDS = [
    OWNER_TABLE_CMD,
    WAREHOUSE_TABLE_CMD,
    VEHICLE_TABLE_CMD,
    SHOP_TABLE_CMD,
    PRODUCT_TABLE_CMD,
    ORDER_TABLE_CMD,
    PRODUCT_ORDER_TABLE_CMD,
    TRANSIT_TABLE_CMD,
    VEHICLE_TRANSIT_TABLE_CMD,
    PRODUCT_TRANSIT_TABLE_CMD,
    PRODUCT_WAREHOUSE_CMD,
    VEHICLE_ORDER_TABLE_CMD
]

CREATE_INDEXES_CMDS = [
    PRODUCT_NAME_INDEX_CMD
]
