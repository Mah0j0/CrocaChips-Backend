from django.db import connection

def eliminar_trigger_stock():
    with connection.cursor() as cursor:
        cursor.execute("DROP TRIGGER IF EXISTS after_update_stock")

def crear_trigger_stock():
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TRIGGER after_update_stock
        AFTER UPDATE ON productos
        FOR EACH ROW
        BEGIN
            DECLARE cantidad_nueva INT;

            IF NEW.stock > OLD.stock THEN
                SET cantidad_nueva = NEW.stock - OLD.stock;

                IF EXISTS (
                    SELECT 1 FROM lotes_produccion
                    WHERE id_producto = NEW.id_producto AND fecha_elaboracion = CURDATE()
                ) THEN
                    UPDATE lotes_produccion
                    SET cantidad = cantidad + cantidad_nueva
                    WHERE id_producto = NEW.id_producto AND fecha_elaboracion = CURDATE();
                ELSE
                    INSERT INTO lotes_produccion (id_producto, cantidad, fecha_elaboracion)
                    VALUES (NEW.id_producto, cantidad_nueva, CURDATE());
                END IF;
            END IF;
        END;
        """)
