--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15 (Ubuntu 10.15-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.15 (Ubuntu 10.15-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cities; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.cities (
    city_id integer NOT NULL,
    city_name character varying NOT NULL,
    urban_area character varying,
    country character varying NOT NULL,
    teleport_id integer
);


ALTER TABLE public.cities OWNER TO vagrant;

--
-- Name: cities_city_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.cities_city_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cities_city_id_seq OWNER TO vagrant;

--
-- Name: cities_city_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.cities_city_id_seq OWNED BY public.cities.city_id;


--
-- Name: follows; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.follows (
    fid integer NOT NULL,
    follower integer,
    follow_target integer
);


ALTER TABLE public.follows OWNER TO vagrant;

--
-- Name: follows_fid_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.follows_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.follows_fid_seq OWNER TO vagrant;

--
-- Name: follows_fid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.follows_fid_seq OWNED BY public.follows.fid;


--
-- Name: user_cities; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.user_cities (
    connect_id integer NOT NULL,
    user_id integer,
    city_id integer,
    user_status character varying NOT NULL,
    tenure character varying
);


ALTER TABLE public.user_cities OWNER TO vagrant;

--
-- Name: user_cities_connect_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.user_cities_connect_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_cities_connect_id_seq OWNER TO vagrant;

--
-- Name: user_cities_connect_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.user_cities_connect_id_seq OWNED BY public.user_cities.connect_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public.users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: cities city_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.cities ALTER COLUMN city_id SET DEFAULT nextval('public.cities_city_id_seq'::regclass);


--
-- Name: follows fid; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.follows ALTER COLUMN fid SET DEFAULT nextval('public.follows_fid_seq'::regclass);


--
-- Name: user_cities connect_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_cities ALTER COLUMN connect_id SET DEFAULT nextval('public.user_cities_connect_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.cities (city_id, city_name, urban_area, country, teleport_id) FROM stdin;
1	san francisco	bay area	united states	\N
2	london	\N	united kingdom	\N
3	paris	\N	france	\N
4	taipei	\N	taiwan	\N
5	Paris	Paris	France	2988507
6	Berlin	Berlin	Germany	2950159
7	Berlin	Berlin	Germany	2950159
8	Berlin	Berlin	Germany	2950159
9	Seoul	Seoul	South Korea	1835848
10	bangkok	bangkok	thailand	1609350
11	seattle	seattle	united states	5809844
12	beijing	beijing	china	1816670
13	honolulu	honolulu	united states	5856195
14	seoul	seoul	south korea	1835848
15	boston	boston	united states	4930956
16	dubai	dubai	united arab emirates	292223
17	kuala lumpur	kuala lumpur	malaysia	1735161
18	singapore	singapore	singapore	1880252
19	klang	kuala lumpur	malaysia	1732905
20	shanghai	shanghai	china	1796236
21	kyoto	kyoto	japan	1857910
22	sydney	sydney	australia	2147714
23	dublin	dublin	ireland	2964574
24	florence	florence	italy	3176959
25	houston	houston	united states	4699066
26	lagos	lagos	nigeria	2332459
27	leeds	leeds	united kingdom	2644688
28	melbourne	melbourne	australia	2158177
29	portland	portland, or	united states	5746545
30	shanghai	shanghai	china	1796236
31	kyiv	kiev	ukraine	703448
32	chicago	chicago	united states	4887398
33	brussels	brussels	belgium	2800866
34	mexico city	mexico city	mexico	3530597
35	prague	prague	czechia	3067696
36	osaka	osaka	japan	1853909
37	rome	rome	italy	3169070
38	berlin	berlin	germany	2950159
39	new york city	new york	united states	5128581
40	new york city	new york	united states	5128581
41	new york city	new york	united states	5128581
42	new york city	new york	united states	5128581
43	new york city	new york	united states	5128581
44	new york city	new york	united states	5128581
45	new york city	new york	united states	5128581
46	nairobi	nairobi	kenya	184745
47	cape town	cape town	south africa	3369157
48	taipei	taipei	taiwan	1668341
49	london	london	united kingdom	2643743
50	lille	lille	france	2998324
51	tokyo	tokyo	japan	1850147
52	toronto	toronto	canada	6167865
53	palo alto	palo alto	united states	5380748
\.


--
-- Data for Name: follows; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.follows (fid, follower, follow_target) FROM stdin;
1	1	2
2	3	2
3	4	2
\.


--
-- Data for Name: user_cities; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.user_cities (connect_id, user_id, city_id, user_status, tenure) FROM stdin;
1	1	4	curr_local	mid
3	6	1	curr_local	new
4	6	2	past_local	long
5	6	4	future	\N
7	1	15	future	\N
8	1	16	future	\N
14	1	13	future	\N
17	1	18	future	\N
20	1	27	future	\N
22	1	12	future	\N
29	1	2	future	\N
31	1	22	future	\N
34	1	49	future	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.users (user_id, first_name, last_name, email) FROM stdin;
1	ada	test	ada@test.tst
2	bey	test	bey@test.tst
3	cat	test	cat@test.tst
4	dory	test	dory@test.tst
5	emma	test	emma@test.tst
6	finn	test	finn@test.tst
\.


--
-- Name: cities_city_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.cities_city_id_seq', 53, true);


--
-- Name: follows_fid_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.follows_fid_seq', 3, true);


--
-- Name: user_cities_connect_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.user_cities_connect_id_seq', 34, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.users_user_id_seq', 6, true);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (city_id);


--
-- Name: follows follows_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_pkey PRIMARY KEY (fid);


--
-- Name: user_cities user_cities_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_cities
    ADD CONSTRAINT user_cities_pkey PRIMARY KEY (connect_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: follows follows_follow_target_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follow_target_fkey FOREIGN KEY (follow_target) REFERENCES public.users(user_id);


--
-- Name: follows follows_follower_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.follows
    ADD CONSTRAINT follows_follower_fkey FOREIGN KEY (follower) REFERENCES public.users(user_id);


--
-- Name: user_cities user_cities_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_cities
    ADD CONSTRAINT user_cities_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(city_id);


--
-- Name: user_cities user_cities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.user_cities
    ADD CONSTRAINT user_cities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

