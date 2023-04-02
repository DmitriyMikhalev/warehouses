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
        ('Кирова 79', 4),
        ('Ленина 17', 4),
        ('Сергинская 104', 5),
        ('Прямая 2', 5),
        ('Мира 50', 5);
"""

LOAD_VEHICLES_CMDS = """
    INSERT INTO
        vehicle (brand, max_capacity, owner_id, vin)
    VALUES
        ('ГАЗон Next 10, 2021', 4, 1, 95208256316690926),
        ('DongFeng AF 475410, 2022', 8, 2, 08176425349020835),
        ('Daewoo Novus, 2023', 16, 2, 17379753984359341),
        ('Daewoo Novus, 2022', 14, 2, 47992628126358840),
        ('Hyundai MegaTruck, 2019', 25, 1, 71061140506578487);
"""

LOAD_WAREHOUSES_CMDS = """
    INSERT INTO
        warehouse (name, address, max_capacity, owner_id)
    VALUES
        ('Склад_1', 'Пушкина 34', 350, 3),
        ('Склад_2', 'Луговая 108/1', 550, 4),
        ('Склад_3', 'Луговая 108/2', 580, 4),
        ('Склад_4', 'Луговая 108/3', 335, 4),
        ('Склад_5', 'Пушкина 36а', 270, 3);
"""

LOAD_TRANSIT_CMDS = """
    INSERT INTO
        transit (warehouse_id, date_start, date_end)
    VALUES
        (1, '2023-04-15 08:00:00', '2023-04-15 11:30:00'),
        (1, '2023-04-17 06:00:00', '2023-04-17 12:00:00'),
        (1, '2023-04-18 01:00:00', '2023-04-18 04:30:00'),
        (2, '2023-04-12 07:40:00', '2023-04-12 11:45:00'),
        (2, '2023-04-12 12:00:00', '2023-04-12 15:05:00'),
        (3, '2023-04-10 03:00:00', '2023-04-10 05:00:00'),
        (4, '2023-04-12 12:00:00', '2023-04-12 15:00:00'),
        (4, '2023-04-15 17:00:00', '2023-04-15 21:30:00'),
        (5, '2023-04-23 19:00:00', '2023-04-23 23:00:00'),
        (5, '2023-04-18 21:00:00', '2023-04-18 23:55:00');
"""

LOAD_PRODUCT_TRANSIT_CMDS = """
    INSERT INTO
        product_transit (transit_id, product_id, payload)
    VALUES
        (1, 1, 5), (1, 2, 4), (1, 3, 6),
        (2, 4, 10), (2, 5, 14), (2, 6, 10), (2, 1, 9),
        (3, 2, 4), (3, 3, 7),
        (4, 1, 15), (4, 3, 8), (4, 6, 4),
        (5, 1, 5), (5, 2, 5), (5, 3, 2), (5, 4, 4),
        (6, 3, 4), (6, 2, 5),
        (7, 6, 15), (7, 5, 5), (7, 4, 4),
        (8, 1, 30),
        (9, 5, 10), (9, 3, 13),
        (10, 1, 3), (10, 3, 4), (10, 5, 5), (10, 6, 8);
"""

LOAD_VEHICLE_TRANSIT_CMDS = """
    INSERT INTO
        vehicle_transit (transit_id, vehicle_id)
    VALUES
        (1, 1),
        (2, 1),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 2),
        (7, 3),
        (8, 4),
        (9, 5),
        (10, 2);
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
        (3, 1, 1, 1, 7, '2023-04-16 10:15:00', '2023-04-16 15:20:00'),
        (1, 1, 2, 2, 1, '2023-04-13 16:20:00', '2023-04-13 17:55:00'),
        (1, 2, 3, 3, 2, '2023-04-14 13:00:00', '2023-04-14 14:55:00'),
        (4, 3, 1, 4, 3, '2023-04-13 19:00:00', '2023-04-13 22:30:00'),
        (6, 3, 2, 4, 4, '2023-04-14 03:00:00', '2023-04-14 07:00:00'),
        (2, 4, 3, 5, 1, '2023-04-20 11:00:00', '2023-04-20 12:25:00'),
        (4, 4, 4, 1, 5, '2023-04-18 04:00:00', '2023-04-18 09:45:00'),
        (3, 5, 5, 1, 5, '2023-04-11 12:00:00', '2023-04-11 17:15:00'),
        (6, 5, 4, 3, 2, '2023-05-16 21:00:00', '2023-05-16 23:00:00');
"""

LOAD_PRODUCT_WAREHOUSE_CMDS = """
    INSERT INTO
        product_warehouse (warehouse_id, product_id, payload)
    VALUES
        (1, 1, 11),
        (1, 4, 3),
        (2, 1, 14),
        (2, 3, 6),
        (3, 6, 10),
        (3, 3, 7),
        (3, 4, 8),
        (3, 5, 2),
        (4, 1, 15),
        (4, 2, 5),
        (5, 6, 1);
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
