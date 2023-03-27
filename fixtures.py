LOAD_OWNERS_CMDS = """
    INSERT INTO
        owner (first_name, last_name, email)
    VALUES
        ('Первый', 'Владелец', 'first_owner@mail.ru'),
        ('Второй', 'Овнер', 'second_owner@mail.ru'),
        ('Третий', 'Бизнесмен', 'third_owner@mail.ru'),
        ('Четвертый', 'Предприниматель', 'fourth_owner@mail.ru'),
        ('Пятый', 'Собственник', 'fifth_owner@mail.ru');
"""

LOAD_PRODUCTS_CMDS = """
    INSERT INTO
        product (name, article_number)
    VALUES
        ('Сахар', 10000),
        ('Мука', 10001),
        ('Картофель', 10002),
        ('Соль', 10003),
        ('Морковь', 10004),
        ('Свёкла', 10005);
"""

LOAD_SHOPS_CMDS = """
    INSERT INTO
        shop (address, owner_id)
    VALUES
        ('Краснофлотская 13, дом 3, строение 2', 5),
        ('Ленина 17', 4);
"""

LOAD_VEHICLES_CMDS = """
    INSERT INTO
        vehicle (brand, max_capacity, owner_id)
    VALUES
        ('ГАЗон Next 10, 2021', 4, 1),
        ('DongFeng AF 475410, 2022', 8, 1),
        ('Daewoo Novus, 2023', 16, 2),
        ('Hyundai MegaTruck, 2019', 25, 3);
"""

LOAD_WAREHOUSES_CMDS = """
    INSERT INTO
        warehouse (name, address, max_capacity, owner_id)
    VALUES
        ('Склад_1', 'Пушкина 34', 50, 5),
        ('Склад_2', 'Луговая 108', 250, 4),
        ('Склад_3', 'Пушкина 36а', 70, 5);
"""

LOAD_TRANSIT_CMDS = """
    INSERT INTO
        transit (warehouse_id, date_start, date_end)
    VALUES
        (1, '2023-04-01 08:00:00', '2023-04-01 11:30:00'),
        (1, '2023-05-03 06:00:00', '2023-05-03 15:00:00'),
        (2, '2023-04-22 01:00:00', '2023-04-22 06:30:00');
"""

LOAD_PRODUCT_TRANSIT_CMDS = """
    INSERT INTO
        product_transit (transit_id, product_id, payload)
    VALUES
        (1, 4, 14),
        (1, 3, 15),
        (1, 6, 7),
        (2, 5, 2),
        (2, 4, 3),
        (3, 1, 30),
        (3, 5, 24);
"""

LOAD_VEHICLE_TRANSIT_CMDS = """
    INSERT INTO
        vehicle_transit (transit_id, vehicle_id)
    VALUES
        (1, 4),
        (2, 3),
        (3, 4);
"""

LOAD_PRODUCT_SHOP_ORDER_CMDS = """
    INSERT INTO
        product_shop_order (
            product_id,
            shop_id,
            warehouse_id,
            vehicle_id,
            payload,
            date_start,
            date_end
        )
    VALUES
        (3, 1, 1, 3, 7, '2023-04-02 09:15:00', '2023-04-02 10:20:00'),
        (4, 1, 1, 2, 3, '2023-04-02 13:00:00', '2023-04-02 16:15:00'),
        (5, 2, 1, 4, 2, '2023-05-04 19:00:00', '2023-05-04 20:00:00'),
        (1, 1, 1, 1, 1, '2023-05-04 16:00:00', '2023-05-04 16:55:00');
"""

LOAD_PRODUCT_WAREHOUSE_CMDS = """
    INSERT INTO
        product_warehouse (warehouse_id, product_id, payload)
    VALUES
        (1, 5, 10),
        (1, 3, 1);
"""

LOAD_DATA_CMDS = [
    LOAD_OWNERS_CMDS,
    LOAD_PRODUCTS_CMDS,
    LOAD_SHOPS_CMDS,
    LOAD_VEHICLES_CMDS,
    LOAD_WAREHOUSES_CMDS,
    LOAD_TRANSIT_CMDS,
    LOAD_PRODUCT_TRANSIT_CMDS,
    LOAD_VEHICLE_TRANSIT_CMDS,
    LOAD_PRODUCT_SHOP_ORDER_CMDS,
    LOAD_PRODUCT_WAREHOUSE_CMDS
]
