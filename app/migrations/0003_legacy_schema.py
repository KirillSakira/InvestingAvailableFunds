from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_balancehistory_options_alter_message_options"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE auth_user
            ADD COLUMN IF NOT EXISTS id_user smallint,
            ADD COLUMN IF NOT EXISTS patronymic varchar(150);

            CREATE TABLE IF NOT EXISTS posts (
                id_post smallserial PRIMARY KEY,
                post_name varchar(100) NOT NULL,
                salary numeric(8,2) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS employees (
                id_employee smallserial PRIMARY KEY,
                id_post smallint NOT NULL REFERENCES posts(id_post)
            );

            CREATE TABLE IF NOT EXISTS enterprises (
                id_enterprise smallserial PRIMARY KEY,
                title varchar(100) NOT NULL,
                type_property varchar(50) NOT NULL,
                address varchar(150) NOT NULL,
                tel varchar(11) NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS users (
                id_user smallserial PRIMARY KEY,
                id_employee smallint UNIQUE REFERENCES employees(id_employee),
                id_enterprise smallint UNIQUE REFERENCES enterprises(id_enterprise),
                CONSTRAINT user_check_is_null CHECK (
                    (id_employee IS NULL OR id_enterprise IS NULL)
                    AND
                    (id_employee IS NOT NULL OR id_enterprise IS NOT NULL)
                )
            );

            CREATE TABLE IF NOT EXISTS catalogs (
                id_catalog smallserial PRIMARY KEY,
                catalog_name varchar(100) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS additional_info (
                id_add_info smallserial PRIMARY KEY,
                yield_close varchar(20) NOT NULL,
                closing_date timestamp with time zone NOT NULL,
                coupon_payment_date timestamp with time zone NOT NULL,
                coupon varchar(50) NOT NULL,
                coupon_value numeric(20,5) NOT NULL,
                nominal numeric(20,5) NOT NULL,
                number_payments_per_year bigint NOT NULL,
                depreciation varchar(10) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS securities (
                id_securitie smallserial PRIMARY KEY,
                sec_name varchar(100) NOT NULL UNIQUE,
                ticker varchar(100) NOT NULL UNIQUE,
                quotation numeric(15,5) NOT NULL,
                id_catalog smallint NOT NULL REFERENCES catalogs(id_catalog),
                description text,
                id_add_info smallint REFERENCES additional_info(id_add_info),
                icon varchar(40)
            );

            CREATE TABLE IF NOT EXISTS portfolios (
                id_portfolio smallserial PRIMARY KEY,
                balance numeric(20,5) NOT NULL,
                id_employee smallint REFERENCES employees(id_employee),
                deposition numeric(20,5) NOT NULL,
                account_number numeric(21,0) NOT NULL UNIQUE,
                id_enterprise smallint NOT NULL REFERENCES enterprises(id_enterprise)
            );

            CREATE TABLE IF NOT EXISTS portfolio_to_securitie (
                id_portfolio smallint NOT NULL REFERENCES portfolios(id_portfolio),
                id_securitie smallint NOT NULL REFERENCES securities(id_securitie),
                total_quantity numeric(20,5) NOT NULL,
                avg_quotation numeric(20,5) NOT NULL,
                PRIMARY KEY (id_portfolio, id_securitie)
            );

            CREATE TABLE IF NOT EXISTS queue (
                id_portfolio smallint NOT NULL REFERENCES portfolios(id_portfolio),
                id_securitie smallint NOT NULL REFERENCES securities(id_securitie),
                queue_date timestamp with time zone NOT NULL,
                quantity bigint NOT NULL,
                quotation numeric(20,5) NOT NULL,
                PRIMARY KEY (id_portfolio, id_securitie, queue_date)
            );

            CREATE TABLE IF NOT EXISTS requests (
                id_request serial PRIMARY KEY,
                id_portfolio smallint NOT NULL REFERENCES portfolios(id_portfolio),
                id_securitie smallint NOT NULL REFERENCES securities(id_securitie),
                req_type boolean NOT NULL,
                req_status boolean NOT NULL DEFAULT true,
                quantity bigint NOT NULL,
                req_date timestamp with time zone NOT NULL DEFAULT now(),
                commission numeric(20,5) NOT NULL DEFAULT 0,
                total_price numeric(20,5) NOT NULL DEFAULT 0,
                id_employee smallint NOT NULL DEFAULT 1 REFERENCES employees(id_employee)
            );

            CREATE TABLE IF NOT EXISTS operations_history (
                id_operation serial PRIMARY KEY,
                oper_type boolean NOT NULL,
                oper_status boolean NOT NULL DEFAULT true,
                oper_date timestamp with time zone NOT NULL DEFAULT now(),
                amount numeric(20,5) NOT NULL,
                id_portfolio smallint NOT NULL REFERENCES portfolios(id_portfolio)
            );

            CREATE TABLE IF NOT EXISTS balances_history (
                id_portfolio smallint NOT NULL REFERENCES portfolios(id_portfolio),
                balance_date timestamp with time zone NOT NULL,
                balance numeric(20,5) NOT NULL,
                PRIMARY KEY (id_portfolio, balance_date)
            );

            CREATE TABLE IF NOT EXISTS messages (
                id_message serial PRIMARY KEY,
                id_sender smallint NOT NULL REFERENCES users(id_user),
                id_receiver smallint NOT NULL REFERENCES users(id_user),
                message_date timestamp with time zone NOT NULL DEFAULT now(),
                message_content text NOT NULL
            );
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS messages CASCADE;
            DROP TABLE IF EXISTS balances_history CASCADE;
            DROP TABLE IF EXISTS operations_history CASCADE;
            DROP TABLE IF EXISTS requests CASCADE;
            DROP TABLE IF EXISTS queue CASCADE;
            DROP TABLE IF EXISTS portfolio_to_securitie CASCADE;
            DROP TABLE IF EXISTS portfolios CASCADE;
            DROP TABLE IF EXISTS securities CASCADE;
            DROP TABLE IF EXISTS additional_info CASCADE;
            DROP TABLE IF EXISTS catalogs CASCADE;
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS enterprises CASCADE;
            DROP TABLE IF EXISTS employees CASCADE;
            DROP TABLE IF EXISTS posts CASCADE;

            ALTER TABLE auth_user
            DROP COLUMN IF EXISTS id_user,
            DROP COLUMN IF EXISTS patronymic;
            """,
        )
    ]