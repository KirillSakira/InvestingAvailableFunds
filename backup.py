import os
import re
from io import StringIO

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finportfolio.settings")
django.setup()

from django.db import connection, transaction


BACKUP_FILE = "backup.sql"

TABLES_ORDER = [
    "django_content_type",
    "auth_permission",
    "auth_group",
    "auth_group_permissions",

    "posts",
    "employees",
    "enterprises",
    "users",
    "auth_user",
    "auth_user_groups",
    "auth_user_user_permissions",

    "catalogs",
    "additional_info",
    "securities",

    "portfolios",
    "portfolio_to_securitie",
    "queue",
    "requests",
    "operations_history",
    "balances_history",
    "messages",

    "django_admin_log",
    "django_migrations",
    "django_session",
]


def extract_copy_blocks(sql_text):
    pattern = re.compile(
        r"^COPY public\.([a-zA-Z_][a-zA-Z0-9_]*) \((.*?)\) FROM stdin;\n(.*?)\n\\\.",
        re.MULTILINE | re.DOTALL,
    )

    blocks = {}

    for match in pattern.finditer(sql_text):
        table_name = match.group(1)
        columns = match.group(2)
        data = match.group(3)

        blocks[table_name] = {
            "columns": columns,
            "data": data,
        }

    return blocks


def table_exists(cursor, table_name):
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = %s
        )
        """,
        [table_name],
    )
    return cursor.fetchone()[0]


def reset_sequences(cursor):
    cursor.execute(
        """
        SELECT
            c.relname AS sequence_name,
            t.relname AS table_name,
            a.attname AS column_name
        FROM pg_class c
        JOIN pg_depend d ON d.objid = c.oid
        JOIN pg_class t ON d.refobjid = t.oid
        JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = d.refobjsubid
        WHERE c.relkind = 'S'
          AND t.relnamespace = 'public'::regnamespace
        """
    )

    for sequence_name, table_name, column_name in cursor.fetchall():
        cursor.execute(
            f"""
            SELECT setval(
                %s,
                COALESCE((SELECT MAX("{column_name}") FROM public."{table_name}"), 1),
                COALESCE((SELECT MAX("{column_name}") FROM public."{table_name}"), 0) > 0
            )
            """,
            [f"public.{sequence_name}"],
        )


def import_backup():
    with open(BACKUP_FILE, "r", encoding="utf-8") as file:
        sql_text = file.read()

    blocks = extract_copy_blocks(sql_text)

    missing = [table for table in TABLES_ORDER if table not in blocks]

    if missing:
        print("В backup.sql нет COPY-блоков для таблиц:")
        for table in missing:
            print(f"  - {table}")

    with transaction.atomic():
        with connection.cursor() as cursor:
            existing_tables = [
                table for table in TABLES_ORDER
                if table in blocks and table_exists(cursor, table)
            ]

            if not existing_tables:
                raise RuntimeError("Не найдено ни одной подходящей таблицы для импорта")

            print("Очищаю таблицы...")

            truncate_sql = ", ".join(
                f'public."{table}"' for table in reversed(existing_tables)
            )

            cursor.execute(
                f"TRUNCATE TABLE {truncate_sql} RESTART IDENTITY CASCADE;"
            )

            print("Импортирую данные...")

            for table in TABLES_ORDER:
                if table not in blocks:
                    continue

                if table not in existing_tables:
                    print(f"Пропускаю {table}: таблицы нет в новой БД")
                    continue

                columns = blocks[table]["columns"]
                data = blocks[table]["data"]

                copy_sql = f'COPY public."{table}" ({columns}) FROM STDIN;'

                print(f"  -> {table}")

                cursor.copy_expert(
                    copy_sql,
                    StringIO(data + "\n"),
                )

            print("Обновляю sequence...")
            reset_sequences(cursor)

    print("Готово: данные из backup.sql перенесены.")


if __name__ == "__main__":
    import_backup()