--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: change_avg_quotation(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.change_avg_quotation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$declare
sum numeric;
n numeric;
begin
 	if (tg_op = 'INSERT') then
		select sum(quantity * quotation), sum(quantity)
		into sum, n from queue
		where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie;
		
		update portfolio_to_securitie
		set avg_quotation = sum / n
		where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie;
		
		return new;
 	else
		select sum(quantity * quotation), sum(quantity)
		into sum, n from queue
		where id_portfolio = old.id_portfolio and id_securitie = old.id_securitie;

		if (n is not null) then
			update portfolio_to_securitie
			set avg_quotation = sum / n
			where id_portfolio = old.id_portfolio and id_securitie = old.id_securitie;
		end if;
		
		if (tg_op = 'DELETE') then
			return old;
		else
			return new;
		end if;
 	end if;
end;$$;


ALTER FUNCTION public.change_avg_quotation() OWNER TO postgres;

--
-- Name: change_deposition_balance_funds(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.change_deposition_balance_funds() RETURNS trigger
    LANGUAGE plpgsql
    AS $$begin
	if (new.oper_type) then
		update portfolios
		set deposition = deposition + new.amount,
			balance = balance + new.amount
		where id_portfolio = new.id_portfolio;

		update portfolio_to_securitie
		set total_quantity = total_quantity + new.amount
		where id_portfolio = new.id_portfolio and id_securitie = 36;
	else
		if (new.amount <= (select total_quantity from portfolio_to_securitie
						   where id_portfolio = new.id_portfolio and id_securitie = 36)) then
			update portfolios
			set deposition = deposition - new.amount,
				balance = balance - new.amount
			where id_portfolio = new.id_portfolio;

			update portfolio_to_securitie
			set total_quantity = total_quantity - new.amount
			where id_portfolio = new.id_portfolio and id_securitie = 36;
		else
			new.oper_status := false;
		end if;
	end if;
 	return new;
end;$$;


ALTER FUNCTION public.change_deposition_balance_funds() OWNER TO postgres;

--
-- Name: change_portfolio_to_securitie_queue(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.change_portfolio_to_securitie_queue() RETURNS trigger
    LANGUAGE plpgsql
    AS $$declare
quot numeric(20, 5) := (select quotation from securities
						where id_securitie = new.id_securitie);
total_quant bigint := (select total_quantity from portfolio_to_securitie
					   where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie);
n bigint;
rowq record;
summa numeric(20, 5) := 0;
begin
	new.id_employee := (select id_employee from portfolios
						where id_portfolio = new.id_portfolio);
	new.total_price := new.quantity * quot;
	if (new.req_type) then
		if (new.total_price <= (select total_quantity from portfolio_to_securitie
								where id_portfolio = new.id_portfolio and id_securitie = 36)) then
			if (total_quant is null) then
				insert into portfolio_to_securitie
				values (new.id_portfolio, new.id_securitie, new.quantity, quot);
			else
				update portfolio_to_securitie
				set total_quantity = total_quantity + new.quantity
				where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie;
			end if;
			
			update portfolio_to_securitie
			set total_quantity = total_quantity - new.total_price
			where id_portfolio = new.id_portfolio and id_securitie = 36;
			
			insert into queue
			values (new.id_portfolio, new.id_securitie, new.req_date, new.quantity, quot);
		else
			new.req_status := false;
		end if;
	else
		if (new.quantity <= total_quant) then
			n := new.quantity;
			for rowq in (select * from queue
						 where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie
						 order by queue_date)
			loop
				if (n = 0) then exit;
				end if;
				
				if (n >= rowq.quantity) then
					n := n - rowq.quantity;
					summa := summa + rowq.quantity * rowq.quotation;
					delete from queue
					where id_portfolio = rowq.id_portfolio and id_securitie = rowq.id_securitie and
						queue_date = rowq.queue_date;
				else
					summa := summa + n * rowq.quotation;
					update queue
					set quantity = quantity - n
					where id_portfolio = rowq.id_portfolio and id_securitie = rowq.id_securitie and
						queue_date = rowq.queue_date;
					n := 0;
				end if;
			end loop;
			
			new.commission := (new.total_price - summa) * 0.2504;
			
			if (new.quantity = total_quant) then
				delete from portfolio_to_securitie
				where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie;
			else
				update portfolio_to_securitie
				set total_quantity = total_quantity - new.quantity
				where id_portfolio = new.id_portfolio and id_securitie = new.id_securitie;
			end if;
			
			update portfolio_to_securitie
			set total_quantity = total_quantity + new.total_price - new.commission
			where id_portfolio = new.id_portfolio and id_securitie = 36;
		else
			new.req_status := false;
		end if;
	end if;
	return new;
end;$$;


ALTER FUNCTION public.change_portfolio_to_securitie_queue() OWNER TO postgres;

--
-- Name: insert_quotations(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_quotations() RETURNS trigger
    LANGUAGE plpgsql
    AS $$begin
	insert into quotations_history
	values (new.id_securitie, default, new.quotation);
	
	return new;
end;
$$;


ALTER FUNCTION public.insert_quotations() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: additional_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.additional_info (
    id_add_info smallint NOT NULL,
    yield_close character varying(20) NOT NULL,
    closing_date timestamp with time zone NOT NULL,
    coupon_payment_date timestamp with time zone NOT NULL,
    coupon character varying(50) NOT NULL,
    coupon_value numeric(20,5) NOT NULL,
    nominal numeric(20,5) NOT NULL,
    number_payments_per_year bigint NOT NULL,
    depreciation character varying(10) NOT NULL
);


ALTER TABLE public.additional_info OWNER TO postgres;

--
-- Name: additional_info_id_add_info_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.additional_info_id_add_info_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.additional_info_id_add_info_seq OWNER TO postgres;

--
-- Name: additional_info_id_add_info_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.additional_info_id_add_info_seq OWNED BY public.additional_info.id_add_info;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id_user smallint,
    patronymic character varying(150)
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: balances_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.balances_history (
    id_portfolio smallint NOT NULL,
    balance_date timestamp with time zone NOT NULL,
    balance numeric(20,5) NOT NULL
);


ALTER TABLE public.balances_history OWNER TO postgres;

--
-- Name: catalogs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.catalogs (
    id_catalog smallint NOT NULL,
    catalog_name character varying(100) NOT NULL
);


ALTER TABLE public.catalogs OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id_employee smallint NOT NULL,
    id_post smallint NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_id_employee_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_employee_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_employee_seq OWNER TO postgres;

--
-- Name: employees_id_employee_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_employee_seq OWNED BY public.employees.id_employee;


--
-- Name: enterprises; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enterprises (
    id_enterprise smallint NOT NULL,
    title character varying(100) NOT NULL,
    type_property character varying(50) NOT NULL,
    address character varying(150) NOT NULL,
    tel character varying(11) NOT NULL
);


ALTER TABLE public.enterprises OWNER TO postgres;

--
-- Name: enterprises_id_ent_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enterprises_id_ent_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enterprises_id_ent_seq OWNER TO postgres;

--
-- Name: enterprises_id_ent_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enterprises_id_ent_seq OWNED BY public.enterprises.id_enterprise;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    id_message integer NOT NULL,
    id_sender smallint NOT NULL,
    id_receiver smallint NOT NULL,
    message_date timestamp with time zone DEFAULT now() NOT NULL,
    message_content text NOT NULL
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: messages_id_message_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_id_message_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.messages_id_message_seq OWNER TO postgres;

--
-- Name: messages_id_message_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_id_message_seq OWNED BY public.messages.id_message;


--
-- Name: operations_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operations_history (
    id_operation integer NOT NULL,
    oper_type boolean NOT NULL,
    oper_status boolean DEFAULT true NOT NULL,
    oper_date timestamp with time zone DEFAULT now() NOT NULL,
    amount numeric(20,5) NOT NULL,
    id_portfolio smallint NOT NULL
);


ALTER TABLE public.operations_history OWNER TO postgres;

--
-- Name: operations_history_id_operation_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operations_history_id_operation_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.operations_history_id_operation_seq OWNER TO postgres;

--
-- Name: operations_history_id_operation_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operations_history_id_operation_seq OWNED BY public.operations_history.id_operation;


--
-- Name: portfolio_to_securitie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.portfolio_to_securitie (
    id_portfolio smallint NOT NULL,
    id_securitie smallint NOT NULL,
    total_quantity numeric(20,5) NOT NULL,
    avg_quotation numeric(20,5) NOT NULL
);


ALTER TABLE public.portfolio_to_securitie OWNER TO postgres;

--
-- Name: portfolios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.portfolios (
    id_portfolio smallint NOT NULL,
    balance numeric(20,5) NOT NULL,
    id_employee smallint,
    deposition numeric(20,5) NOT NULL,
    account_number numeric(21,0) NOT NULL,
    id_enterprise smallint NOT NULL
);


ALTER TABLE public.portfolios OWNER TO postgres;

--
-- Name: portfolios_id_portfolio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.portfolios_id_portfolio_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.portfolios_id_portfolio_seq OWNER TO postgres;

--
-- Name: portfolios_id_portfolio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.portfolios_id_portfolio_seq OWNED BY public.portfolios.id_portfolio;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    id_post smallint NOT NULL,
    post_name character varying(100) NOT NULL,
    salary numeric(8,2) NOT NULL
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_id_post_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_post_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_post_seq OWNER TO postgres;

--
-- Name: posts_id_post_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_post_seq OWNED BY public.posts.id_post;


--
-- Name: queue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.queue (
    id_portfolio smallint NOT NULL,
    id_securitie smallint NOT NULL,
    queue_date timestamp with time zone NOT NULL,
    quantity bigint NOT NULL,
    quotation numeric(20,5) NOT NULL
);


ALTER TABLE public.queue OWNER TO postgres;

--
-- Name: requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requests (
    id_request integer NOT NULL,
    id_portfolio smallint NOT NULL,
    id_securitie smallint NOT NULL,
    req_type boolean NOT NULL,
    req_status boolean DEFAULT true NOT NULL,
    quantity bigint NOT NULL,
    req_date timestamp with time zone DEFAULT now() NOT NULL,
    commission numeric(20,5) DEFAULT 0 NOT NULL,
    total_price numeric(20,5) DEFAULT 0 NOT NULL,
    id_employee smallint DEFAULT 1 NOT NULL
);


ALTER TABLE public.requests OWNER TO postgres;

--
-- Name: requests_id_request_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requests_id_request_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.requests_id_request_seq OWNER TO postgres;

--
-- Name: requests_id_request_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requests_id_request_seq OWNED BY public.requests.id_request;


--
-- Name: securities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.securities (
    id_securitie smallint NOT NULL,
    sec_name character varying(100) NOT NULL,
    ticker character varying(100) NOT NULL,
    quotation numeric(15,5) NOT NULL,
    id_catalog smallint NOT NULL,
    description text,
    id_add_info smallint,
    icon character varying(40)
);


ALTER TABLE public.securities OWNER TO postgres;

--
-- Name: TABLE securities; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.securities IS 'Ценные бумаги';


--
-- Name: securities_id_securitie_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.securities_id_securitie_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.securities_id_securitie_seq OWNER TO postgres;

--
-- Name: securities_id_securitie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.securities_id_securitie_seq OWNED BY public.securities.id_securitie;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id_user smallint NOT NULL,
    id_employee smallint,
    id_enterprise smallint,
    CONSTRAINT user_check_is_null CHECK ((((id_employee IS NULL) OR (id_enterprise IS NULL)) AND ((id_employee IS NOT NULL) OR (id_enterprise IS NOT NULL))))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_user_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_user_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_user_seq OWNER TO postgres;

--
-- Name: users_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_user_seq OWNED BY public.users.id_user;


--
-- Name: сatalogs_id_catalog_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."сatalogs_id_catalog_seq"
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."сatalogs_id_catalog_seq" OWNER TO postgres;

--
-- Name: сatalogs_id_catalog_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."сatalogs_id_catalog_seq" OWNED BY public.catalogs.id_catalog;


--
-- Name: additional_info id_add_info; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.additional_info ALTER COLUMN id_add_info SET DEFAULT nextval('public.additional_info_id_add_info_seq'::regclass);


--
-- Name: catalogs id_catalog; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalogs ALTER COLUMN id_catalog SET DEFAULT nextval('public."сatalogs_id_catalog_seq"'::regclass);


--
-- Name: employees id_employee; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id_employee SET DEFAULT nextval('public.employees_id_employee_seq'::regclass);


--
-- Name: enterprises id_enterprise; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enterprises ALTER COLUMN id_enterprise SET DEFAULT nextval('public.enterprises_id_ent_seq'::regclass);


--
-- Name: messages id_message; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN id_message SET DEFAULT nextval('public.messages_id_message_seq'::regclass);


--
-- Name: operations_history id_operation; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations_history ALTER COLUMN id_operation SET DEFAULT nextval('public.operations_history_id_operation_seq'::regclass);


--
-- Name: portfolios id_portfolio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolios ALTER COLUMN id_portfolio SET DEFAULT nextval('public.portfolios_id_portfolio_seq'::regclass);


--
-- Name: posts id_post; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN id_post SET DEFAULT nextval('public.posts_id_post_seq'::regclass);


--
-- Name: requests id_request; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests ALTER COLUMN id_request SET DEFAULT nextval('public.requests_id_request_seq'::regclass);


--
-- Name: securities id_securitie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.securities ALTER COLUMN id_securitie SET DEFAULT nextval('public.securities_id_securitie_seq'::regclass);


--
-- Name: users id_user; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id_user SET DEFAULT nextval('public.users_id_user_seq'::regclass);


--
-- Data for Name: additional_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.additional_info (id_add_info, yield_close, closing_date, coupon_payment_date, coupon, coupon_value, nominal, number_payments_per_year, depreciation) FROM stdin;
1	15.05%	2041-05-15 10:00:00+03	2024-06-05 10:00:00+03	Фиксированный	32.48000	1000.00000	2	Нет
2	14.23%	2038-05-19 10:00:00+03	2024-06-05 10:00:00+03	Фиксированный	44.84000	1000.00000	2	Нет
3	14.07%	2034-05-10 10:00:00+03	2024-06-22 10:00:00+03	Фиксированный	36.15000	1000.00000	2	Нет
4	18.06%	2029-04-06 10:00:00+03	2024-07-12 10:00:00+03	Фиксированный	24.68000	1000.00000	4	Нет
5	17.02%	2027-08-18 10:00:00+03	2024-06-04 10:00:00+03	Фиксированный	11.26000	1000.00000	12	Нет
6	20.27%	2025-07-22 10:00:00+03	2024-07-23 10:00:00+03	Фиксированный	30.79000	1000.00000	4	Нет
7	18.95%	2027-10-12 10:00:00+03	2024-07-16 10:00:00+03	Фиксированный	37.40000	1000.00000	2	Нет
8	23.67%	2026-01-26 10:00:00+03	2025-01-26 10:00:00+03	Фиксированный	3849.36000	98777.60000	1	Нет
9	6.79%	2028-02-26 10:00:00+03	2024-08-26 10:00:00+03	Фиксированный	2183.70000	90987.30000	2	Нет
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, id_user, patronymic) FROM stdin;
8	pbkdf2_sha256$720000$6flrWKZAOzPr9YzFW9mqde$j9MB2Jvnq/On7hPUQtDBzIpoHyUKIcOit6mllh1ifSE=	2024-06-27 13:24:34.532258+03	f	mmmm2@mmm.mm	Qqqq	Qqq	mmmm2@mmm.mm	f	t	2024-06-27 13:24:32.61663+03	32	Qq
10	pbkdf2_sha256$720000$VaFhjToTtfC7cTGnJlmTYE$/qPolvYbK9o5fYPA68GQ5O05fmxCphJGfZEP57amGKU=	2024-07-01 13:15:02.519995+03	f	qusssttt@gmail.com	Александр	Носков	qusssttt@gmail.com	f	t	2024-07-01 13:15:00.52734+03	34	Николаевич
3	pbkdf2_sha256$720000$B5rKpTrFi3aSiS8QDebR74$hYzWJ6Qi8N0DXoAZ099IuD5olBVmXBdYBjAmemjWiYM=	2024-06-24 21:39:47.737801+03	f	lesnoyvv@icloud.com	Л	Вячеслав	lesnoyvv@icloud.com	f	t	2024-06-24 21:39:45.777997+03	27	\N
4	pbkdf2_sha256$720000$YrafGZQDCTZL3RkPERcX7i$79oftjTFz4GFaMKCy+vB8dwxCOM+Xrspr77fia2WKpk=	2024-06-24 21:43:10.459234+03	f	cccc2@ccc.cc	Aawdwada	Wdadwa	cccc2@ccc.cc	f	t	2024-06-24 21:43:08.531698+03	28	\N
11	pbkdf2_sha256$720000$Ugk8cSoFAEVdarCNdk7NLi$H+DfqGz79uodFFgCVJPro7MkIjSX8tJluupR2JunH7s=	2024-07-10 23:47:16.933962+03	f	ilya070105@gmail.com	Илья	Андрияш	ilya070105@gmail.com	f	t	2024-07-10 23:47:14.955152+03	35	Влвлйц
13	pbkdf2_sha256$720000$C6hVFXGDc9OoorZSdhGniy$RwZ4qRn6mwYKNlSrcxiZEbIEMBAI5w3jeE4KSUCGQPU=	\N	f	bbbb@bbb.b	Админ	Админ	bbbb@bbb.b	f	t	2024-11-09 13:47:37.025932+03	37	Админович
6	pbkdf2_sha256$720000$tyGoTBWD13I9k0qASDj7Ty$UTZ3SvClOeJbOy6YTs8iyIIWQ/lsB7D29kBAldNA61s=	2024-06-27 06:45:22.882979+03	f	Vova@gmail.com	V	Mazur	Vova@gmail.com	f	t	2024-06-27 06:45:06.849895+03	30	V
2	pbkdf2_sha256$720000$oIWW51e4twGXRONnjF8bfN$1FDUmZUXv1AreXGv0UV/WZsTCBuwmNURmwXFozv7qQ8=	2024-11-09 15:49:35.738442+03	f	cccc@ccc.cc	Клиент	Клиентов	cccc@ccc.cc	f	t	2024-06-24 02:32:56.985648+03	26	Клиентский
5	pbkdf2_sha256$720000$LdcSKKLJzOxYjVf3ftM0FK$NQZOtPFMn95lDYMbuP0wRW0aih09MM5kzJwRLC3Tkj4=	2025-02-18 08:11:11.998818+03	f	aaaa@aaa.aa	Администратор	Администраторов	aaaa@aaa.aa	f	t	2024-06-26 23:26:31.335916+03	29	Администраторович
12	pbkdf2_sha256$720000$0tVe87jkpkneGRmRzwlswr$s+zzqO8mfPm4kh3LndQb762y9g/i6zUs8kYx+tAK9ns=	2024-07-18 20:11:52.103545+03	f	viktoriasalygina89@gmail.com	Виктория	Шалыгина	viktoriasalygina89@gmail.com	f	t	2024-07-18 20:11:50.014918+03	36	Святославовна
7	pbkdf2_sha256$720000$jEceQJa6setkyK5OoJVdC2$pvYKitUAVhBoXyNOpt7jdk/ZyLQWKRHQ+I8grk6anzg=	2024-06-27 13:20:41.160927+03	f	olga_ned@mail.ru	Ольга	Руденко	olga_ned@mail.ru	f	t	2024-06-27 13:20:16.346789+03	31	Валентиновна
14	pbkdf2_sha256$720000$wbF0kNYsNjOGCMZCCidCzE$uCxFpxA7OiIt+wnwesTAlfCBYBWnrf8MpjSJ6v+oTYA=	2025-02-18 09:33:49.652768+03	f	123@mail.ri	Awdawdaw	Awdawdawd	123@mail.ri	f	t	2025-02-18 09:33:48.586878+03	38	\N
1	pbkdf2_sha256$1000000$nVRDMW68JrpEVzcS4PyaTw$ocGlXHvyLuox8vO4iWcHjLyk+IeqXaVNFQjWt3j5Hf4=	2025-08-01 08:42:14.799186+03	f	mmmm@mmm.mm	Мен	Менеджеров	mmmm@mmm.mm	f	t	2024-06-24 02:31:59.715316+03	25	Менеджерский
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: balances_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.balances_history (id_portfolio, balance_date, balance) FROM stdin;
6	2024-06-27 11:08:06.014021+03	0.00000
7	2024-06-27 11:08:06.014021+03	0.00000
5	2024-06-27 11:08:06.014021+03	121892079541.00000
5	2024-06-27 13:37:48.646954+03	121892097048.00000
6	2024-06-27 13:37:48.646954+03	0.00000
7	2024-06-27 13:37:48.646954+03	0.00000
8	2024-06-27 13:37:48.646954+03	10000.00000
\.


--
-- Data for Name: catalogs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.catalogs (id_catalog, catalog_name) FROM stdin;
1	Акции
2	Облигации
3	Фонды
4	Валюта и металлы
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2024-06-22 17:50:28.161866+03
2	auth	0001_initial	2024-06-22 17:50:28.317379+03
3	admin	0001_initial	2024-06-22 17:50:28.36195+03
4	admin	0002_logentry_remove_auto_add	2024-06-22 17:50:28.375359+03
5	admin	0003_logentry_add_action_flag_choices	2024-06-22 17:50:28.422582+03
6	contenttypes	0002_remove_content_type_name	2024-06-22 17:50:28.450471+03
7	auth	0002_alter_permission_name_max_length	2024-06-22 17:50:28.466177+03
8	auth	0003_alter_user_email_max_length	2024-06-22 17:50:28.4814+03
9	auth	0004_alter_user_username_opts	2024-06-22 17:50:28.495105+03
10	auth	0005_alter_user_last_login_null	2024-06-22 17:50:28.510627+03
11	auth	0006_require_contenttypes_0002	2024-06-22 17:50:28.513886+03
12	auth	0007_alter_validators_add_error_messages	2024-06-22 17:50:28.528937+03
13	auth	0008_alter_user_username_max_length	2024-06-22 17:50:28.554016+03
14	auth	0009_alter_user_last_name_max_length	2024-06-22 17:50:28.56847+03
15	auth	0010_alter_group_name_max_length	2024-06-22 17:50:28.584571+03
16	auth	0011_update_proxy_permissions	2024-06-22 17:50:28.597767+03
17	auth	0012_alter_user_first_name_max_length	2024-06-22 17:50:28.612822+03
18	sessions	0001_initial	2024-06-22 17:50:28.642385+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
ikwk1cqgecnry3nltiwmruz29yr33fcl	.eJxVjEEOwiAQRe_C2hCcAmVcuu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERIE6_W6D4SHUHfKd6azK2ui5zkLsiD9rl1Dg9r4f7d1Col299HtgarQk4GTI4qmSNipHYMZJSBhBHygGyQ50Tg3IBTbY42AgMqMX7A98NN7Y:1sLWhe:cUXPkLP4fZcmDmdmlKtc-yoE6qF1YNGvusJUrq3DloY	2024-07-08 02:32:58.92021+03
0vkz5z81cftxwcn7t2r3xqtiir69ooga	.eJxVjEEOwiAQRe_C2hAQGCYu3XsGAswgVQNJaVeNd9cmXej2v_f-JkJclxrWwXOYSFyEF6ffLcX85LYDesR27zL3tsxTkrsiDzrkrRO_rof7d1DjqN-6OHJEVqO2Thej4rlEzrpgZgLHHhQDkvdWGZMsenCIqMkbpgQGknh_AOygN7w:1sMmF7:Wi4nRIFdb33KWU7yjOjnVLPuQVOs_elRCxGmiM31ZnQ	2024-07-11 13:20:41.164678+03
zicywwue50izf5sf7dgpi48yrl1rn4r0	.eJxVjMsOwiAUBf-FtSG8ubh0328gPC5SNZCUdmX8d9ukC92emTlv4sO2Vr8NXPycyZUocvndYkhPbAfIj9Dunabe1mWO9FDoSQedesbX7XT_DmoYda8LRJtQ6BJd0TFwFrXRUhorhdHMZcsKz253lJBJoTOcKVAIgA4QCpDPF-BuN2o:1sLoek:5Zz4WMgxo0rCGOVgN9OxD7mKMzYWG6KnfMoKmtQ5ua8	2024-07-08 21:43:10.466874+03
3zjdvzbguqiv27825ovwvbrqqd628yys	.eJxVjDsOwjAQBe_iGln-rT-U9JzBWq8dHEC2FCcV4u4QKQW0b2bei0Xc1hq3UZY4Z3Zmnp1-t4T0KG0H-Y7t1jn1ti5z4rvCDzr4tefyvBzu30HFUb81BgAURktD1qBTAmzyOmTvYQInKSStErls0TsVwBRDSYsJZXFCEjr2_gDBzTdH:1sMmIs:Aiy0BhAEF4GAf8nFfl0PRmPSGWbZvsFPuqiEJzJThOc	2024-07-11 13:24:34.542184+03
9kyk7n4kjxf6csijbt771vsdqo6marts	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sMmVj:7170tYUeo2rXwhqqbXeoX88ZJvG7V7p5uBnTys0GbKQ	2024-07-11 13:37:51.703586+03
dh18hs5ditudphp94ie3pby1ac7px6l5	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sMmWf:ELuoqI-NuQbn12yR293VNH7IL4MfxofARJrNKGjnQSU	2024-07-11 13:38:49.386227+03
j6hpmnio525fkj420u3bfzq5zb54spkl	.eJxVjMsOwiAQRf-FtSEBOjC6dO83kBkeUjWQlHbV-O9K0oVuzzn37sLTtha_9bT4OYqLAHH6ZUzhmeoQ8UH13mRodV1mliORh-3y1mJ6XY_276BQL2ONCZVGQs6Gzg4REuesJ5Md6MxTsKw0GNQ2mmjBAijtJnSBjDNfLN4f4Q83Ag:1sMugd:oNrDohNalOuu-7dj-OAQfF-1GxbnZ3yZ9wxwJQDiY4Y	2024-07-11 22:21:39.139251+03
9oa8gcuxsdyn7n7rnbc67dx0hcxwdj61	.eJxVjEEOwiAQRe_C2hCcAmVcuu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERIE6_W6D4SHUHfKd6azK2ui5zkLsiD9rl1Dg9r4f7d1Col299HtgarQk4GTI4qmSNipHYMZJSBhBHygGyQ50Tg3IBTbY42AgMqMX7A98NN7Y:1sMjrp:BYAx47aCVBc_mt3Wna02LCXRdoN-QqN8j8sipLYI2c8	2024-07-11 10:48:29.550384+03
3ov3agfjeo1herdslc0lur2pbtvoyqpg	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sNBKW:pc4V8Lf8Jm0KLoGo8MCsifMvE0lsIicRQlDT75F8w1c	2024-07-12 16:07:56.130213+03
s4r0hmsxqprmc55q47mrp9bvf3p8q4qr	.eJxVjEEOwiAQRe_C2hCcAmVcuu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERIE6_W6D4SHUHfKd6azK2ui5zkLsiD9rl1Dg9r4f7d1Col299HtgarQk4GTI4qmSNipHYMZJSBhBHygGyQ50Tg3IBTbY42AgMqMX7A98NN7Y:1sMjtX:L5fju7kDmQPvNUWqvZT6ebFFenTSnMJB8D0wMP7x2bI	2024-07-11 10:50:15.193087+03
rd5bggj6t3pcsg9rajyiufwafcoedfzf	.eJxVjMsOwiAQRf-FtSEBOjC6dO83kBkeUjWQlHbV-O9K0oVuzzn37sLTtha_9bT4OYqLAHH6ZUzhmeoQ8UH13mRodV1mliORh-3y1mJ6XY_276BQL2ONCZVGQs6Gzg4REuesJ5Md6MxTsKw0GNQ2mmjBAijtJnSBjDNfLN4f4Q83Ag:1sNfoS:qKkwyD86W4YazS_gKTjgwpSB2uOYViQaXK9ygMVKogk	2024-07-14 00:40:52.64414+03
8xkmpsxptiqe0aswvtd898ry8mfixpcy	.eJxVjEEOwiAQRe_C2pCBUqAu3XsGwsyAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsFIjT74iRHqnuhO-x3pqkVtdlRrkr8qBdXhun5-Vw_w5K7OVb59HmnICQBvIGELweJnRegdWAI5lojAdngBz7KcWUmZ1lCzk71IrE-wMMXDhf:1sOE3q:u6VRYcPu0sK-Vm_WNZyd6n_cBZeN3V9OBVZ-Pefumhk	2024-07-15 13:15:02.528067+03
ktdlic0bhsq64deohozpkijx1ljlo3bv	.eJxVjMsOwiAQRf-FtSEBOjC6dO83kBkeUjWQlHbV-O9K0oVuzzn37sLTtha_9bT4OYqLAHH6ZUzhmeoQ8UH13mRodV1mliORh-3y1mJ6XY_276BQL2ONCZVGQs6Gzg4REuesJ5Md6MxTsKw0GNQ2mmjBAijtJnSBjDNfLN4f4Q83Ag:1sMlca:HCk8UnqDv8DIMUW-3_RdOfu2D25KY4vRLJuxszz-ZEE	2024-07-11 12:40:52.155322+03
8of8tyh2gbk0z4ksu4yy3ex8o04lkpdf	.eJxVjDsOwjAQBe_iGlnexJ-Ykj5nsHa9Dg4gW4qTCnF3CEoB7ZuZ9xQBtzWHraUlzCzOAkCcfkfCeE9lJ3zDcq0y1rIuM8ldkQdtcqycHpfD_TvI2PKnVlb7jvt-cmDIRD0YFTHR4DSTt5MnIiRnk1IadO8UglcMHbkvMFq83vxtOBg:1sReDc:-TqSRLM1r0JWbJ_2tUgiD1YRIoaXKFaZqU5Z5owd_d8	2024-07-24 23:47:16.94557+03
ubtmry3q1xps5st3nd0pww52rqqb79cb	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sUUGM:lDHIK6Mp_B8vSbwDOgrKU3j-zx1b_yqX4ke_wiP_4YI	2024-08-01 19:45:50.699879+03
bzk8rp9wcgo8anqd7hshte7a1yjimn9b	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sUUH0:Pch99uPIoKDD2zFDT_WBcWWPFZiMsqx3YK-D15hO4pA	2024-08-01 19:46:30.483445+03
dgw6cfiicnymroebdwqku9i8938vllpi	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sUUH1:EjH7YMFMbBKnp91dkpHDvhg3b1xDfFcdVHezgIkAHJ8	2024-08-01 19:46:31.601079+03
v9md9k72lq87f4q1a49hzi3gbfgqq2xn	.eJxVjEEOwiAQRe_C2hBgChSX7j0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kTgLbcTpd0yYH9x2Qndst1nmua3LlOSuyIN2eZ2Jn5fD_Tuo2Ou3HgwUyBmAwBscktVKWw_BYrAFkMkbJkfZusC6qDzCyAmt9-yDVs6I9wf3eTeo:1sUUfY:xPM8hYDGOs8nCsbyWvieXJzv2KHozHHZpkYzqvYFlqY	2024-08-01 20:11:52.115358+03
1n71ym1r6ipasahgca4hunzafzlu6kfb	.eJxVjMsOwiAQRf-FtSEBOjC6dO83kBkeUjWQlHbV-O9K0oVuzzn37sLTtha_9bT4OYqLAHH6ZUzhmeoQ8UH13mRodV1mliORh-3y1mJ6XY_276BQL2ONCZVGQs6Gzg4REuesJ5Md6MxTsKw0GNQ2mmjBAijtJnSBjDNfLN4f4Q83Ag:1sUUuN:SdTjq3yE6g1B-QGXwDG2ApVbYrpEOUgyI_oG5sxJZRY	2024-08-01 20:27:11.568706+03
4gvzyb4sg4ua2qr73rnduf6tuea7ggwh	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sXRDf:oVClXEip7U3t4NxIurrx7WcBNOfC23OHOtDkIfdeip4	2024-08-09 23:07:15.220573+03
xmroy4ok9v0dt7u02cv2i8s74pvsiqoq	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sqoRa:EOJ1FQ6S8QDP0aUEgowiwRv2tYwpdahq7k0ADU_AELk	2024-10-02 09:45:42.800208+03
ede7txr3qg5uhwqd1ff3zprulhpfyxxk	.eJxVjDsOwjAQRO-yNbLkbxZKes5grb1OHEC2FCcV4u44UgrSjea9mQ942tbst5YWPzPcQMLlvwsUX6nsgJ9UpipiLesyB7Er4qBNPCqn9_1wTweZWu5rlFahG5WxVulEeqDryBgNSmRChYwGtZOGXRg09ZS0Jdslx4YjIXx_vB03WQ:1sx7FB:NkYB4RycmZXqKuOpL08i1F3NPHK3zkPKmYRdfhOg7YU	2024-10-19 19:02:57.77619+03
qlvgam16nlr0l8vps27c2mjs835antr8	.eJxVjEEOwiAQRe_C2hCcAmVcuu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERIE6_W6D4SHUHfKd6azK2ui5zkLsiD9rl1Dg9r4f7d1Col299HtgarQk4GTI4qmSNipHYMZJSBhBHygGyQ50Tg3IBTbY42AgMqMX7A98NN7Y:1t9kuF:NwxB4we1nQmdeWfk5EVssP9IlAw01o_FzOCk0ypdfxI	2024-11-23 15:49:35.742098+03
zjrnhzs7r6rei516zvjcdqrn1xg8o5n4	.eJxVjDsOwjAQBe_iGln-xR9K-pzB8nrXOIAcKU4qxN1JpBTQzsx7bxbTtta4dVrihOzKpGGXXwgpP6kdBh-p3Wee57YuE_Aj4aftfJyRXrez_Tuoqdd9LTw6iQhEuWhlURZCBdIGTx6yNhjUTr12EAYwVgypGCgyqKKhOOHY5wsrxzii:1tkHAz:8uv_uf6Xq19RQ8qIjx7MozgaWD7U9tS08bNYf6P1Msw	2025-03-04 09:33:49.657198+03
9xp449eer2vgrgvp72ezqbl0y1tbp21c	.eJxVjEEOwiAQRe_C2hCGAnFcuvcMZBimUjWQlHZlvLsh6UK3_7333yrSvpW4d1njktVFgTr9bon4KXWA_KB6b5pb3dYl6aHog3Z9a1le18P9OyjUy6gNAjpM3sJk2HAA5x14A-lsKPuJrJ2dxeACEAiSlSQWUTwTpZlRfb6sLDdX:1uByf7:tLlevBXnZoNjFfukAfkyW0IaCmQQPe4If0BuDramjlM	2025-05-19 19:27:25.721285+03
on41vni4em24r57ng14pgisb458tbnmu	.eJxVjEEOwiAQRe_C2hCGAnFcuvcMZBimUjWQlHZlvLsh6UK3_7333yrSvpW4d1njktVFgTr9bon4KXWA_KB6b5pb3dYl6aHog3Z9a1le18P9OyjUy6gNAjpM3sJk2HAA5x14A-lsKPuJrJ2dxeACEAiSlSQWUTwTpZlRfb6sLDdX:1uHM6E:2H2b5oIQUjG4ZWLLe7QMTxG_lImOGWAexuSzYheDJNo	2025-06-03 15:29:38.481928+03
7u02ma37k8tj886qtvijq8ge099zwqfb	.eJxVjEEOwiAQRe_C2hCGAnFcuvcMZBimUjWQlHZlvLsh6UK3_7333yrSvpW4d1njktVFgTr9bon4KXWA_KB6b5pb3dYl6aHog3Z9a1le18P9OyjUy6gNAjpM3sJk2HAA5x14A-lsKPuJrJ2dxeACEAiSlSQWUTwTpZlRfb6sLDdX:1uhiX0:kPrsuB7kFJPlvbKn7c23IwMBgOec5qg4d5IHOP2Lga0	2025-08-15 08:42:14.802127+03
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id_employee, id_post) FROM stdin;
21	2
22	2
23	1
24	2
25	1
\.


--
-- Data for Name: enterprises; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enterprises (id_enterprise, title, type_property, address, tel) FROM stdin;
5	cl	ie	nt	33333333333
6	123	123	123	12345678912
7	VOVACOMP	IP	Karelskaya	89787012803
8	КуБГУ	ООО	г.Краснодар, ул.Ставропольская, 149	89034506544
10	SunRise Tactics	cybersport	ул. Красный путь 14	89081151186
11	1234	123	Rhfycjlfhj 123 	89180783773
12	rrrr	ип	крл	79533986751
13	awdawdawd	adwadawdawd	awdaw	89189688678
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (id_message, id_sender, id_receiver, message_date, message_content) FROM stdin;
\.


--
-- Data for Name: operations_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.operations_history (id_operation, oper_type, oper_status, oper_date, amount, id_portfolio) FROM stdin;
39	t	t	2024-06-27 08:28:36.429981+03	100000.00000	5
40	t	t	2024-06-27 08:29:07.908621+03	100000.00000	5
41	t	t	2024-06-27 08:29:19.079146+03	123123213.00000	5
42	t	t	2024-06-27 08:33:25.742698+03	123123123123.00000	5
43	f	t	2024-06-27 08:36:04.026018+03	1231231323.00000	5
44	f	t	2024-06-27 08:36:12.599851+03	123123123.00000	5
45	t	t	2024-06-27 10:02:20.021872+03	1.00000	5
46	t	t	2024-06-27 10:35:00.214337+03	1.00000	5
47	t	t	2024-06-27 10:51:15.926864+03	1.00000	5
48	t	t	2024-06-27 10:51:20.905912+03	1.00000	5
49	f	t	2024-06-27 10:51:31.234651+03	12345.00000	5
50	f	t	2024-06-27 10:51:51.357502+03	1.00000	5
51	f	t	2024-06-27 10:57:26.714891+03	1.00000	5
52	f	t	2024-06-27 10:57:36.613123+03	1.00000	5
53	f	t	2024-06-27 11:01:37.460846+03	1.00000	5
54	f	t	2024-06-27 11:01:44.960205+03	1.00000	5
55	f	t	2024-06-27 11:01:50.932156+03	1.00000	5
56	f	t	2024-06-27 11:02:12.550463+03	1.00000	5
57	f	t	2024-06-27 11:02:18.881268+03	1.00000	5
58	t	t	2024-06-27 13:33:54.750809+03	10000.00000	8
59	t	t	2024-06-27 15:56:02.644075+03	56.00000	5
60	f	t	2024-06-27 15:56:18.744298+03	56.00000	5
62	t	t	2024-06-30 00:33:18.667032+03	10000.00000	5
63	f	t	2024-06-30 00:34:04.386246+03	30000.00000	5
64	t	t	2024-07-01 13:16:12.023416+03	1500000.00000	10
65	t	t	2025-02-18 09:34:23.691446+03	123.00000	13
66	f	t	2025-02-18 09:35:03.74413+03	12.00000	13
\.


--
-- Data for Name: portfolio_to_securitie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.portfolio_to_securitie (id_portfolio, id_securitie, total_quantity, avg_quotation) FROM stdin;
6	36	0.00000	1.00000
7	36	0.00000	1.00000
5	20	3694596889.00000	0.97400
8	21	10.00000	8.16000
5	23	1232123.00000	1.42360
5	15	234567.00000	89.90000
8	31	7.00000	89.10250
5	26	123123.00000	190.34000
8	36	8613.68250	1.00000
8	10	15.00000	45.40000
5	33	3774755856.00000	11.42700
5	32	3576900077.00000	18.71000
5	3	5.00000	2988.50000
5	11	10.00000	53.29900
10	2	15.00000	324.17000
10	10	1500.00000	45.40000
10	20	100000.00000	0.97400
10	36	973227.45000	1.00000
10	31	4000.00000	89.10250
11	36	0.00000	1.00000
12	36	0.00000	1.00000
5	5	1.00000	3013.40000
13	36	111.00000	1.00000
5	2	9.00000	324.17000
5	10	179999999.00000	45.40000
5	36	3602470.73640	1.00000
5	1	1900.00000	7210.00000
\.


--
-- Data for Name: portfolios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.portfolios (id_portfolio, balance, id_employee, deposition, account_number, id_enterprise) FROM stdin;
5	121892076832.40560	21	121892059541.00000	76455921881807559324	5
6	0.00000	22	0.00000	39996540043303547693	6
7	0.00000	\N	0.00000	43359019036690122802	7
8	10000.00000	24	10000.00000	51606125698265791686	8
10	1500000.00000	21	1500000.00000	32226462900470345964	10
11	0.00000	21	0.00000	64932822062202554400	11
12	0.00000	21	0.00000	68479968148897686144	12
13	111.00000	\N	111.00000	37862949060169222338	13
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (id_post, post_name, salary) FROM stdin;
1	Администратор	200000.00
2	Менеджер	100000.00
\.


--
-- Data for Name: queue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.queue (id_portfolio, id_securitie, queue_date, quantity, quotation) FROM stdin;
5	23	2024-06-27 12:00:18.111569+03	1232123	1.42360
5	15	2024-06-27 12:17:52.941209+03	234567	89.90000
5	26	2024-06-27 12:18:59.141544+03	123123	190.34000
5	33	2024-06-27 12:19:12.503879+03	1231231231	11.42700
5	33	2024-06-27 12:19:27.741749+03	1312312313	11.42700
5	33	2024-06-27 12:19:31.371141+03	1231212312	11.42700
5	32	2024-06-27 12:19:49.061191+03	2345678765	18.71000
5	32	2024-06-27 12:19:52.943686+03	1231221312	18.71000
5	20	2024-06-27 12:20:18.788768+03	1231233132	0.97400
5	20	2024-06-27 12:20:21.94094+03	1232131231	0.97400
5	20	2024-06-27 12:20:24.77892+03	1231232131	0.97400
5	1	2024-06-27 12:23:07.370259+03	1000	7210.00000
5	1	2024-06-27 12:23:16.530216+03	50	7210.00000
5	1	2024-06-27 12:23:23.590037+03	3	7210.00000
5	20	2024-06-27 12:23:39.306967+03	385	0.97400
5	20	2024-06-27 12:23:43.159766+03	10	0.97400
8	21	2024-06-27 13:34:30.957084+03	10	8.16000
8	31	2024-06-27 13:34:43.148018+03	7	89.10250
8	10	2024-06-27 13:34:59.33941+03	15	45.40000
5	2	2024-06-27 15:13:26.339942+03	5	324.17000
5	3	2024-06-27 15:53:41.246554+03	5	2988.50000
5	11	2024-06-30 00:36:26.717627+03	10	53.29900
10	2	2024-07-01 13:17:37.589703+03	15	324.17000
10	10	2024-07-01 13:17:54.692026+03	1500	45.40000
10	20	2024-07-01 13:18:19.453165+03	100000	0.97400
10	31	2024-07-01 13:18:35.121218+03	4000	89.10250
5	5	2024-07-26 23:08:52.436298+03	1	3013.40000
5	2	2025-05-06 11:30:56.325576+03	4	324.17000
5	10	2025-07-17 08:58:53.499924+03	12	45.40000
5	10	2024-06-27 12:22:29.508703+03	179999987	45.40000
5	1	2024-06-27 12:22:51.840706+03	347	7210.00000
5	1	2025-08-01 08:44:55.901584+03	500	7210.00000
\.


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requests (id_request, id_portfolio, id_securitie, req_type, req_status, quantity, req_date, commission, total_price, id_employee) FROM stdin;
67	5	1	t	f	1	2024-06-27 06:54:10.268008+03	0.00000	7066.50000	21
68	5	1	f	f	1	2024-06-27 06:54:11.566377+03	0.00000	7066.50000	21
69	5	1	t	t	123	2024-06-27 08:39:22.694375+03	0.00000	869179.50000	21
70	5	1	f	t	1	2024-06-27 08:39:26.140306+03	0.00000	7066.50000	21
71	5	21	t	t	2	2024-06-27 11:37:54.562734+03	0.00000	16.32000	21
72	5	21	f	t	2	2024-06-27 11:37:58.230282+03	0.00000	16.32000	21
73	5	21	t	t	2	2024-06-27 11:38:00.189341+03	0.00000	16.32000	21
74	5	21	f	f	3	2024-06-27 11:38:02.467565+03	0.00000	24.48000	21
75	5	21	f	t	2	2024-06-27 11:38:07.867746+03	0.00000	16.32000	21
76	5	21	t	t	1000	2024-06-27 11:38:13.508959+03	0.00000	8160.00000	21
77	5	21	f	t	1000	2024-06-27 11:38:19.481609+03	0.00000	8160.00000	21
78	5	23	t	t	1232123	2024-06-27 12:00:18.111569+03	0.00000	1754050.30280	21
79	5	15	t	t	234567	2024-06-27 12:17:52.941209+03	0.00000	21087573.30000	21
80	5	26	t	t	123123	2024-06-27 12:18:59.141544+03	0.00000	23435231.82000	21
81	5	33	t	t	1231231231	2024-06-27 12:19:12.503879+03	0.00000	14069279276.63700	21
82	5	33	t	t	1312312313	2024-06-27 12:19:27.741749+03	0.00000	14995792800.65100	21
83	5	33	t	t	1231212312	2024-06-27 12:19:31.371141+03	0.00000	14069063089.22400	21
84	5	32	t	t	2345678765	2024-06-27 12:19:49.061191+03	0.00000	43887649693.15000	21
85	5	32	t	t	1231221312	2024-06-27 12:19:52.943686+03	0.00000	23036150747.52000	21
86	5	20	t	t	1231233132	2024-06-27 12:20:18.788768+03	0.00000	1199221070.56800	21
87	5	20	t	t	1232131231	2024-06-27 12:20:21.94094+03	0.00000	1200095818.99400	21
88	5	20	t	t	1231232131	2024-06-27 12:20:24.77892+03	0.00000	1199220095.59400	21
89	5	10	t	f	9999999999	2024-06-27 12:20:50.332882+03	0.00000	453999999954.60000	21
90	5	10	t	t	179999999	2024-06-27 12:22:29.508703+03	0.00000	8171999954.60000	21
91	5	1	t	t	1231	2024-06-27 12:22:51.840706+03	0.00000	8875510.00000	21
92	5	1	t	t	1000	2024-06-27 12:23:07.370259+03	0.00000	7210000.00000	21
93	5	1	t	t	50	2024-06-27 12:23:16.530216+03	0.00000	360500.00000	21
94	5	1	t	t	3	2024-06-27 12:23:23.590037+03	0.00000	21630.00000	21
95	5	20	t	t	385	2024-06-27 12:23:39.306967+03	0.00000	374.99000	21
96	5	20	t	t	10	2024-06-27 12:23:43.159766+03	0.00000	9.74000	21
97	8	2	t	f	81	2024-06-27 13:26:09.566197+03	0.00000	26257.77000	24
98	8	21	t	t	10	2024-06-27 13:34:30.957084+03	0.00000	81.60000	24
99	8	31	t	t	7	2024-06-27 13:34:43.148018+03	0.00000	623.71750	24
100	8	10	t	t	15	2024-06-27 13:34:59.33941+03	0.00000	681.00000	24
101	5	1	f	t	6	2024-06-27 15:13:12.359296+03	215.59440	43260.00000	21
102	5	2	t	t	5	2024-06-27 15:13:26.339942+03	0.00000	1620.85000	21
103	5	3	t	t	5	2024-06-27 15:53:41.246554+03	0.00000	14942.50000	21
104	5	11	t	t	10	2024-06-30 00:36:26.717627+03	0.00000	532.99000	21
105	10	2	t	t	15	2024-07-01 13:17:37.589703+03	0.00000	4862.55000	21
106	10	10	t	t	1500	2024-07-01 13:17:54.692026+03	0.00000	68100.00000	21
107	10	20	t	t	100000	2024-07-01 13:18:19.453165+03	0.00000	97400.00000	21
108	10	31	t	t	4000	2024-07-01 13:18:35.121218+03	0.00000	356410.00000	21
109	5	5	t	t	1	2024-07-26 23:08:52.436298+03	0.00000	3013.40000	21
110	5	1	t	f	1	2025-02-18 08:10:04.886045+03	0.00000	7210.00000	21
111	5	2	t	f	12	2025-05-06 11:25:53.055787+03	0.00000	3890.04000	21
112	5	2	t	t	4	2025-05-06 11:30:56.325576+03	0.00000	1296.68000	21
113	5	10	t	t	12	2025-07-17 08:58:53.499924+03	0.00000	544.80000	21
114	5	10	f	t	12	2025-07-17 08:59:00.903126+03	0.00000	544.80000	21
115	5	10	t	f	2143	2025-07-17 08:59:04.33768+03	0.00000	97292.20000	21
116	5	1	f	t	1000	2025-08-01 08:44:51.843592+03	4168.15840	7210000.00000	21
117	5	1	t	t	500	2025-08-01 08:44:55.901584+03	0.00000	3605000.00000	21
\.


--
-- Data for Name: securities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.securities (id_securitie, sec_name, ticker, quotation, id_catalog, description, id_add_info, icon) FROM stdin;
36	Рубль	RUB	1.00000	4	\N	\N	\N
15	Делимобиль 1Р-03	RU000A106A86	89.90000	2	Делимобиль — российский сервис краткосрочной аренды автомобилей, запущенный в 2015 году. Делимобиль работает в ряде городов России.	5	delimobile_1P-03.png
8	Совкомфлот	FLOT	118.96000	1	Совкомфлот — крупнейшая судоходная компания России, один из мировых лидеров в области морской транспортировки сжиженного газа, сырой нефти и нефтепродуктов, а также обслуживания и обеспечения морской добычи углеводородов. Рыночная доля компании по морским перевозкам энергоносителей в 2023 году приблизилась к 20%, тогда как в 2021-м была на уровне 5%.\nКомпания принимает участие в развитии десяти крупномасштабных энергетических проектов в тяжелых климатических условиях: восемь из них располагаются в России, по одному — в Индонезии и Канаде.	\N	sovkomflot.png
17	ВИС Финанс выпуск 1	RU000A102952	98.43000	2	Группа «ВИС» – российский инфраструктурный холдинг, один из лидеров рынка государственно-частного партнёрства (ГЧП). Холдинг инвестирует собственные средства в создание объектов транспортной, социальной и коммунальной инфраструктуры и реализует проекты ГЧП и концессий «под ключ», управляя каждым этапом их жизненного цикла.	7	vis_finance_vipusk_1.png
11	ОФЗ 26238	SU26238RMFS4	53.29900	2	Облигации федерального займа (ОФЗ) – самые надежные ценные бумаги на российском фондовом рынке, потому что их выпускает государство в лице Минфина. Государство же и будет их погашать (возвращать номинал).	1	ofz_26238.png
6	Novabev Group	BELU	5714.00000	1	Novabev Group — один из ведущих игроков алкогольного сектора российской экономики, лидер по производству крепкого алкоголя: водки, коньяка, виски и ликеро-водочных изделий. В активах компании семь производственных комплексов, а продуктовая линейка представлена более 100 партнерскими и более 50 собственными брендами, три из которых — Беленькая, Архангельская и Царь — вошли в рейтинг 30 самых продаваемых водок в мире по версии The Millionaires’ Club в 2023 году.\nС 2011 года компания также сделала упор на дистрибуцию, стали открываться магазины сети Винлаб. В 2023 году масштаб собственной розничной сети превысил планку в 1 650 торговых точек, а общая аудитория программы лояльности превысила 7,0 млн человек.	\N	novabev_group.png
7	Ozon Holdings PLC	OZON	4253.00000	1	Ozon — мультикатегорийный маркетплейс, с развитой логистической сетью. Компания входит в топ-5 крупнейших российских ритейлеров и развивает бизнес в России, странах СНГ, Китае и Турции. По итогам первой половины 2023 года оборот маркетплейса превысил 675 млрд рублей. На Ozon торгует более 300 000 продавцов, которые предлагают на площадке более 200 млн товарных наименований. Платформу ежемесячно посещает более 65 млн пользователей Рунета, а число ее активных покупателей достигло 40 млн человек.\nOzon активно развивает систему сервисов, в числе которых собственный банк, а также сервисы быстрой доставки продуктов и бронирования путешествий.	\N	ozon_holdings_plc.png
1	Лукойл	LKOH	7210.00000	1	ЛУКОЙЛ — одна из крупнейших нефтегазовых компаний в мире, на ее долю приходится 2% мировой добычи нефти и 1% доказанных запасов углеводородов. Компания представлена более чем в 30 странах, а в России ее деятельность охватывает около 70% регионов.\nЗначительную часть нефтепродуктов ЛУКОЙЛ реализует на розничном рынке через диверсифицированную сбытовую сеть, которая состоит из 5 309 АЗС и 132 нефтебаз в 18 странах мира. В 2022 году компания осуществила несколько крупных сделок по приобретению российских активов Shell – 411 АЗС, также завершила покупку доли 56,4% в энергетической компании «Энел Россия» в октябре 2022 года.	\N	lukoil.png
9	АЛРОСА	ALRS	70.85000	1	АЛРОСА — крупнейшая в мире алмазодобывающая компания, занимается обработкой, продажей алмазов, производством бриллиантов. На компанию приходится более 25% мировой добычи алмазов. Ключевые добывающие активы расположены в Якутии и Архангельской области.\nКомпания имеет активную поддержку от государства: новый флагманский проект строительства подземного рудника на месторождении «Мир» в Якутии получит господдержку.	\N	alrosa.png
12	ОФЗ 26243	SU26243RMFS4	70.13000	2	Облигации федерального займа (ОФЗ) – самые надежные ценные бумаги на российском фондовом рынке, потому что их выпускает государство в лице Минфина. Государство же и будет их погашать (возвращать номинал).	2	ofz_26243.png
25	ВИМ Индекс Московской биржи 	EQMX	142.75000	3	\N	\N	vim_index_mosbirzhi.png
16	М. Видео выпуск 3 	RU000A104ZK2	91.70000	2	М.Видео — крупнейшая в России сеть по продаже бытовой техники и электроники, объединяет розничные бренды М.Видео и Эльдорадо. Компания является одним из пионеров онлайн-ритейла в России: первый интернет-магазин М.Видео был открыт в 2001 году, а с 2014 года компания начала внедрение омниканальной бизнес-модели.\nВ 2021 году компания объединяла 1 137 магазинов в 314 городах России. Оборот М.Видео в 2021 году превысил 570 миллиардов рублей, при этом доля онлайн-продаж составила 68%, что делает компанию одним из крупнейших игроков онлайн-торговли в России.	6	m.video_vipusk_3.png
27	Альфа-Капитал Золото 	AKGD	147.84000	3	\N	\N	alfa-kapital_zoloto.png
26	Альфа-Капитал Управление 	AKME	190.34000	3	\N	\N	alfa-kapital_upravlenie.png
28	АТОН Российские акции	AMRE	110.80000	3	\N	\N	aton_rossiyskie_akcii.png
4	Магнит	MGNT	6363.00000	1	Магнит — одна из ведущих розничных сетей по торговле продуктами питания в России. Работает по мультиформатной модели, которая включает в себя магазины «у дома», супермаркеты, аптеки и дискаунтеры. Компания также занимается производством продуктов питания под собственными торговыми марками и выращиванием овощей на предприятиях.\nНа конец июня 2023 года сеть насчитывает более 28 300 торговых точек и покрывает более 75% регионов России. Ежедневно магазины компании принимают около 17 млн посетителей, а в программе лояльности Магнита участвует более 72 млн человек.	\N	magnit.png
2	Сбер	SBER	324.17000	1	СберБанк — крупнейший банк в России, Центральной и Восточной Европе, один из ведущих международных финансовых институтов. Сбер также является системно значимым банком и одной из крупнейших экосистем страны.\nУ компании более 107 млн активных частных клиентов и 3 млн активных корпоративных клиентов в России. Отделения Сбербанка представлены практически во всех населенных пунктах, а общее их число свыше 13 тысяч. Сбер — это флагман российского фондового рынка, как по капитализации, так и по дивидендам, которые компания выплачивает.	\N	sber.png
3	ГК Самолёт	SMLT	2988.50000	1	ГК Самолет — одна из крупнейших федеральных корпораций в сфере PropTech и девелопмента. Портфель компании включает 43 проекта, а земельный банк составляет более 28 млн кв. м. Группа входит в число системообразующих организаций российской экономики и занимает первое место в Москве по объемам текущего строительства и второе место в России. Компания активно развивает свою онлайн-платформу, фонды коммерческой и арендной недвижимости и другие.	\N	gk_samolet.png
13	ОФЗ 26225	SU26225RMFS1	61.45500	2	Облигации федерального займа (ОФЗ) – самые надежные ценные бумаги на российском фондовом рынке, потому что их выпускает государство в лице Минфина. Государство же и будет их погашать (возвращать номинал).	3	ofz_26225.png
18	Газпром Капитал  БЗО26-1-Е	RU000A105QW3	77.99980	2	«Газпром» — глобальная энергетическая компания, кладовая мировых запасов природного газа. На нее приходится 12% мировой и 68% российской добычи газа. Входит в четвёрку крупнейших российских производителей нефти и является самой прибыльной российской компанией в 2022 году по версии Forbes.\nГазпром реализует более половины газа на внутреннем рынке, а также занимается его поставками в более чем 30 стран ближнего и дальнего зарубежья. В настоящее время компания активно реализует масштабные проекты по освоению газовых ресурсов арктического шельфа, Восточной Сибири и Дальнего Востока, а также ряд проектов по разведке и добыче углеводородов за рубежом.	8	gazprom_capital_b3026-1-e.png
14	ОКЕЙ ВЫПУСК 2	RU000A1009Z8	93.39000	2	О’кей входит в число крупнейших розничных сетей России. Группа представлена гипермаркетами под брендом О’кей и дискаунтерами под брендом ДА! Компания развивает стратегию омниканальности, это первый российский ритейлер, который запустил онлайн-сервис по заказу продуктов на базе гипермаркетов в Москве и Санкт-Петербурге. В активы компании входит около 250 магазинов в России общей торговой площадью 638 638 м².	4	okey_vipusk_2.png
19	ГТЛК ЗО28-Д	RU000A107CX7	89.99930	2	Государственная транспортная лизинговая компания - публичное акционерное общество, 100 % акций находятся в Государственной собственности. Работает на рынке лизинговых услуг с 2001 года. ГТЛК предлагает в лизинг все виды техники и оборудования для транспортной отрасли: лизинг автотранспорта и спецтехники (в том числе грузовых автомобилей и пассажирского транспорта), лизинг авиационной техники и аэропортового оборудования, лизинг железнодорожного подвижного состава, а также водного транспорт и портового оборудования.	9	gtlk_3028-d.png
20	Тинькофф Вечный портфель 	TUSD	0.97400	3	Биржевой фонд в рублях, задача которого — показывать результат и в период роста экономики, и в турбулентные времена.\nСбалансированный портфель фонда состоит из акций, долгосрочных облигаций, инструментов денежного рынка, а также золота.	\N	tinkoff_vechniy_portfel.png
23	ВИМ Ликвидность 	LQDT	1.42360	3	\N	\N	vim_likvidnost.png
24	ВИМ Фонд Золото 	GOLD	1.63800	3	\N	\N	vim_fond_zoloto.png
22	Тинькофф IMOEX 	TMOS	6.49000	3	Биржевой фонд в рублях позволяет вложиться в бумаги сразу нескольких десятков эмитентов по цене пая.\nОн повторяет индекс Мосбиржи и инвестирует в акции крупнейших российских компаний.	\N	tinkoff_imoex.png
21	Тинькофф Золото 	TGLD	8.16000	3	Биржевой фонд поможет защитить накопления от инфляции без инфраструктурных рисков: золото хранится на территории России, валюта торгов — рубли.\nОн инвестирует в физическое золото на рынке драгоценных металлов Московской биржи.	\N	tinkoff_zoloto.png
30	Серебро	SLVRUB_TOM	112.34000	4	\N	\N	serebro.png
32	Тенге	KZTRUB_TOM	18.71000	4	\N	\N	tenge.png
35	Турецкая лира 	TRYRUB_TOM	2.62000	4	\N	\N	tureckaya_lira.png
31	Доллар США	USD000UTSTOM	89.10250	4	\N	\N	dollar_usa.png
29	Золото	GLDRUB_TOM	6390.70000	4	\N	\N	zoloto.png
33	Китайский юань 	CNYRUB_TOM	11.42700	4	\N	\N	kitaiskiy_yuan.png
34	Платина	PLTRUB_TOM	10.36900	4	\N	\N	platina.png
10	Fix Price Group	FIXP	45.40000	1	Fix Price — крупнейшая российская сеть магазинов в сегменте низких фиксированных цен. Под брендом работает более 5 600 магазинов в России и на шести зарубежных рынках: в Беларуси и Казахстане представлены собственные магазины, а в Узбекистане, Латвии, Грузии и Киргизии сеть развивается за счет франчайзинга.\nЗа 2022 год компания нарастила сеть торговых площадок на 15%, открыв 759 новых магазинов. Fix Price предлагает широкий ассортимент товаров повседневного спроса: около двух тысяч товарных позиций в 20 различных категориях.	\N	fix_price.png
5	Трубная Металлургическая Компания	TRMK	3013.40000	1	ТМК — крупнейший производитель и экспортер трубной продукции в России, входит в топ-3 мировых производителей бесшовных труб. Деятельность компании охватывает разные сферы, от энергетики до машиностроения, но преимущественно ТМК работает с нефтегазовым сектором, который приносит ей около 80% выручки.\nПомимо услуг, связанных с трубами и трубными решениями, компания предоставляет своим клиентам ремонтный сервис, инженерное сопровождение и другие сопутствующие услуги. У компании более 50 заводов и сервисных предприятий в разных регионах России.	\N	trub_metal_company.png
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id_user, id_employee, id_enterprise) FROM stdin;
25	21	\N
26	\N	5
27	22	\N
28	\N	6
29	23	\N
30	\N	7
31	\N	8
32	24	\N
34	\N	10
35	\N	11
36	\N	12
37	25	\N
38	\N	13
\.


--
-- Name: additional_info_id_add_info_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.additional_info_id_add_info_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 24, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 14, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 6, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 18, true);


--
-- Name: employees_id_employee_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_employee_seq', 26, true);


--
-- Name: enterprises_id_ent_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enterprises_id_ent_seq', 13, true);


--
-- Name: messages_id_message_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.messages_id_message_seq', 8, true);


--
-- Name: operations_history_id_operation_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.operations_history_id_operation_seq', 66, true);


--
-- Name: portfolios_id_portfolio_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.portfolios_id_portfolio_seq', 13, true);


--
-- Name: posts_id_post_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posts_id_post_seq', 3, true);


--
-- Name: requests_id_request_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requests_id_request_seq', 117, true);


--
-- Name: securities_id_securitie_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.securities_id_securitie_seq', 36, true);


--
-- Name: users_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_user_seq', 38, true);


--
-- Name: сatalogs_id_catalog_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."сatalogs_id_catalog_seq"', 4, true);


--
-- Name: additional_info additional_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.additional_info
    ADD CONSTRAINT additional_info_pkey PRIMARY KEY (id_add_info);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: balances_history balances_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.balances_history
    ADD CONSTRAINT balances_history_pkey PRIMARY KEY (id_portfolio, balance_date);


--
-- Name: catalogs catalogs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.catalogs
    ADD CONSTRAINT catalogs_pkey PRIMARY KEY (id_catalog);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id_employee);


--
-- Name: enterprises enterprises_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enterprises
    ADD CONSTRAINT enterprises_pkey PRIMARY KEY (id_enterprise);


--
-- Name: enterprises enterprises_tel_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enterprises
    ADD CONSTRAINT enterprises_tel_key UNIQUE (tel);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id_message);


--
-- Name: operations_history operations_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations_history
    ADD CONSTRAINT operations_history_pkey PRIMARY KEY (id_operation);


--
-- Name: portfolio_to_securitie portfolio_to_securitie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolio_to_securitie
    ADD CONSTRAINT portfolio_to_securitie_pkey PRIMARY KEY (id_portfolio, id_securitie);


--
-- Name: portfolios portfolios_account_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_account_number_key UNIQUE (account_number);


--
-- Name: portfolios portfolios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_pkey PRIMARY KEY (id_portfolio);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id_post);


--
-- Name: queue queue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_pkey PRIMARY KEY (id_portfolio, id_securitie, queue_date);


--
-- Name: requests requests_id_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_id_request_pkey PRIMARY KEY (id_request);


--
-- Name: securities securities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.securities
    ADD CONSTRAINT securities_pkey PRIMARY KEY (id_securitie);


--
-- Name: securities securities_sec_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.securities
    ADD CONSTRAINT securities_sec_name_key UNIQUE (sec_name);


--
-- Name: securities securities_ticker_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.securities
    ADD CONSTRAINT securities_ticker_key UNIQUE (ticker);


--
-- Name: users users_employee_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_employee_key UNIQUE (id_employee);


--
-- Name: users users_ent_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_ent_key UNIQUE (id_enterprise);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id_user);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: queue change_avg_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER change_avg_trigger AFTER INSERT OR DELETE OR UPDATE ON public.queue FOR EACH ROW EXECUTE FUNCTION public.change_avg_quotation();


--
-- Name: operations_history change_deposition_balance_funds_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER change_deposition_balance_funds_trigger BEFORE INSERT ON public.operations_history FOR EACH ROW EXECUTE FUNCTION public.change_deposition_balance_funds();


--
-- Name: requests change_portfolio_to_securitie_queue_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER change_portfolio_to_securitie_queue_trigger BEFORE INSERT ON public.requests FOR EACH ROW EXECUTE FUNCTION public.change_portfolio_to_securitie_queue();


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: balances_history balances_history_id_portfolio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.balances_history
    ADD CONSTRAINT balances_history_id_portfolio_fkey FOREIGN KEY (id_portfolio) REFERENCES public.portfolios(id_portfolio);


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees employees_id_post_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_id_post_fkey FOREIGN KEY (id_post) REFERENCES public.posts(id_post);


--
-- Name: messages messages_id_receiver_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_id_receiver_fkey FOREIGN KEY (id_receiver) REFERENCES public.users(id_user);


--
-- Name: messages messages_id_sender_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_id_sender_fkey FOREIGN KEY (id_sender) REFERENCES public.users(id_user);


--
-- Name: operations_history operations_history_id_portfolio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations_history
    ADD CONSTRAINT operations_history_id_portfolio_fkey FOREIGN KEY (id_portfolio) REFERENCES public.portfolios(id_portfolio);


--
-- Name: portfolio_to_securitie portfolio_to_securitie_id_portfolio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolio_to_securitie
    ADD CONSTRAINT portfolio_to_securitie_id_portfolio_fkey FOREIGN KEY (id_portfolio) REFERENCES public.portfolios(id_portfolio);


--
-- Name: portfolio_to_securitie portfolio_to_securitie_id_securitie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolio_to_securitie
    ADD CONSTRAINT portfolio_to_securitie_id_securitie_fkey FOREIGN KEY (id_securitie) REFERENCES public.securities(id_securitie);


--
-- Name: portfolios portfolios_id_employee_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_id_employee_fk FOREIGN KEY (id_employee) REFERENCES public.employees(id_employee);


--
-- Name: portfolios portfolios_id_ent_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_id_ent_fkey FOREIGN KEY (id_enterprise) REFERENCES public.enterprises(id_enterprise);


--
-- Name: queue queue_id_portfolio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_id_portfolio_fkey FOREIGN KEY (id_portfolio) REFERENCES public.portfolios(id_portfolio);


--
-- Name: queue queue_id_securitie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_id_securitie_fkey FOREIGN KEY (id_securitie) REFERENCES public.securities(id_securitie);


--
-- Name: requests requests_id_employee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_id_employee_fkey FOREIGN KEY (id_employee) REFERENCES public.employees(id_employee);


--
-- Name: requests requests_id_portfolio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_id_portfolio_fkey FOREIGN KEY (id_portfolio) REFERENCES public.portfolios(id_portfolio);


--
-- Name: requests requests_id_securitie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_id_securitie_fkey FOREIGN KEY (id_securitie) REFERENCES public.securities(id_securitie);


--
-- Name: securities securities_catalog_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.securities
    ADD CONSTRAINT securities_catalog_fk FOREIGN KEY (id_catalog) REFERENCES public.catalogs(id_catalog);


--
-- Name: securities securities_id_add_info_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.securities
    ADD CONSTRAINT securities_id_add_info_fkey FOREIGN KEY (id_add_info) REFERENCES public.additional_info(id_add_info);


--
-- Name: users users_id_employee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id_employee_fkey FOREIGN KEY (id_employee) REFERENCES public.employees(id_employee);


--
-- Name: users users_id_ent_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id_ent_fkey FOREIGN KEY (id_enterprise) REFERENCES public.enterprises(id_enterprise);


--
-- PostgreSQL database dump complete
--

