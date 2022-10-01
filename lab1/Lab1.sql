--
-- PostgreSQL database dump
--

-- Dumped from database version 11.17
-- Dumped by pg_dump version 11.17

-- Started on 2022-10-01 19:33:13

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


SET default_with_oids = false;

--
-- TOC entry 201 (class 1259 OID 16441)
-- Name: film_genres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.film_genres (
    film_id integer NOT NULL,
    genre_id integer NOT NULL
);


--
-- TOC entry 200 (class 1259 OID 16436)
-- Name: films; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.films (
    "id " integer NOT NULL,
    title character varying(50) NOT NULL,
    producer character varying(50),
    release_year integer,
    duration integer NOT NULL
);


--
-- TOC entry 199 (class 1259 OID 16431)
-- Name: genres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.genres (
    id integer NOT NULL,
    name character varying(30) NOT NULL
);


--
-- TOC entry 198 (class 1259 OID 16421)
-- Name: halls; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.halls (
    number integer NOT NULL,
    technology_id integer NOT NULL
);


--
-- TOC entry 203 (class 1259 OID 16471)
-- Name: prices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prices (
    id integer NOT NULL,
    technology_id integer NOT NULL,
    price integer NOT NULL,
    CONSTRAINT positive_price CHECK ((price > 0))
);


--
-- TOC entry 202 (class 1259 OID 16456)
-- Name: session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.session (
    id integer NOT NULL,
    hall_id integer NOT NULL,
    film_id integer NOT NULL,
    date_time timestamp without time zone NOT NULL
);


--
-- TOC entry 204 (class 1259 OID 16482)
-- Name: sold_tickets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sold_tickets (
    id integer NOT NULL,
    session_id integer NOT NULL,
    place integer NOT NULL,
    "row" integer NOT NULL,
    CONSTRAINT tickets_place_check CHECK ((place > 0)),
    CONSTRAINT tickets_row_check CHECK (("row" > 0))
);


--
-- TOC entry 197 (class 1259 OID 16416)
-- Name: technologies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.technologies (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    description character varying(256)
);


--
-- TOC entry 2724 (class 2606 OID 16445)
-- Name: film_genres film_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.film_genres
    ADD CONSTRAINT film_genres_pkey PRIMARY KEY (film_id, genre_id);


--
-- TOC entry 2722 (class 2606 OID 16440)
-- Name: films films_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.films
    ADD CONSTRAINT films_pkey PRIMARY KEY ("id ");


--
-- TOC entry 2720 (class 2606 OID 16435)
-- Name: genres genres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (id);


--
-- TOC entry 2718 (class 2606 OID 16425)
-- Name: halls halls_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.halls
    ADD CONSTRAINT halls_pkey PRIMARY KEY (number);


--
-- TOC entry 2728 (class 2606 OID 16476)
-- Name: prices prices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_pkey PRIMARY KEY (id);


--
-- TOC entry 2726 (class 2606 OID 16460)
-- Name: session session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_pkey PRIMARY KEY (id);


--
-- TOC entry 2716 (class 2606 OID 16420)
-- Name: technologies technologies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technologies
    ADD CONSTRAINT technologies_pkey PRIMARY KEY (id);


--
-- TOC entry 2730 (class 2606 OID 16488)
-- Name: sold_tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sold_tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (id);


--
-- TOC entry 2732 (class 2606 OID 16446)
-- Name: film_genres film_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.film_genres
    ADD CONSTRAINT film_id FOREIGN KEY (film_id) REFERENCES public.films("id ");


--
-- TOC entry 2735 (class 2606 OID 16466)
-- Name: session film_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT film_id FOREIGN KEY (film_id) REFERENCES public.films("id ");


--
-- TOC entry 2733 (class 2606 OID 16451)
-- Name: film_genres genre_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.film_genres
    ADD CONSTRAINT genre_id FOREIGN KEY (genre_id) REFERENCES public.genres(id);


--
-- TOC entry 2734 (class 2606 OID 16461)
-- Name: session hall_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT hall_id FOREIGN KEY (hall_id) REFERENCES public.halls(number);


--
-- TOC entry 2737 (class 2606 OID 16489)
-- Name: sold_tickets session_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sold_tickets
    ADD CONSTRAINT session_id FOREIGN KEY (session_id) REFERENCES public.session(id);


--
-- TOC entry 2731 (class 2606 OID 16426)
-- Name: halls technology_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.halls
    ADD CONSTRAINT technology_id FOREIGN KEY (technology_id) REFERENCES public.technologies(id);


--
-- TOC entry 2736 (class 2606 OID 16477)
-- Name: prices technology_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT technology_id FOREIGN KEY (technology_id) REFERENCES public.technologies(id);


-- Completed on 2022-10-01 19:33:14

--
-- PostgreSQL database dump complete
--

