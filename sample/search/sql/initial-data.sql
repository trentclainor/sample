--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.4
-- Dumped by pg_dump version 9.6.6


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET search_path = public, pg_catalog;

--
-- Name: cv_inserts_tg(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION cv_inserts_tg() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
    IF tg_op = 'INSERT' THEN
        INSERT INTO
        cand_skills(skill_id, cv_id, prominence)
        SELECT skill_id, new.cv_id, prominence
        FROM (
            SELECT skill_id, char_length(regexp_replace(new.cv_content, rex, '')) AS prominence
            FROM (
                SELECT skill_id, '\y' || f_regexp_escape(skill) || '\y.*$' as rex, skill
                FROM skills
                WHERE strpos(new.cv_content, skill) > 0
                ) AS ta
            ) AS tb
        WHERE prominence < char_length(new.cv_content);

        INSERT INTO
        cand_titles(title_id, cv_id, prominence)
        SELECT title_id, new.cv_id, prominence
        FROM (
            SELECT title_id, char_length(regexp_replace(new.cv_content, rex, '')) AS prominence
            FROM (
                SELECT title_id, '\y' || f_regexp_escape(title) || '\y.*$' as rex, title
                FROM titles_clean
                WHERE strpos(new.cv_content, title) > 0
                ) AS ta
            ) AS tb
        WHERE prominence < char_length(new.cv_content);

        INSERT INTO
        cand_companies(company_id, cv_id, prominence)
        SELECT company_id, new.cv_id, prominence
        FROM (
            SELECT company_id, char_length(regexp_replace(new.cv_content, rex, '')) AS prominence
            FROM (
                SELECT company_id, '\y' || f_regexp_escape(company) || '\y.*$' as rex, company
                FROM companies_clean
                WHERE strpos(new.cv_content, company) > 0
                ) AS ta
            ) AS tb
        WHERE prominence < char_length(new.cv_content);
        RETURN new;
    END IF;
END;
$_$;


--
-- Name: cvs_sha256_tg(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION cvs_sha256_tg() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF Tg_op = 'INSERT' OR tg_op = 'UPDATE' THEN
        new.cv_sha256 = encode(digest(new.cv_content, 'sha256'), 'hex');
        return new;
    END IF;
END;
$$;


--
-- Name: f_regexp_escape(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_regexp_escape(text) RETURNS text
    LANGUAGE sql IMMUTABLE
    AS $_$
SELECT regexp_replace($1, '([!$()*+.:<=>?[\\\]^{|}-])', '\\\1', 'g')
$_$;


--
-- Name: job_inserts_tg(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION job_inserts_tg() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
    IF tg_op = 'INSERT' THEN

        -- Inserting job skills
        INSERT INTO posting_skills(skill_id, job_id, prominence)
        SELECT skill_id, new.job_id, prominence
        FROM (
            SELECT skill_id, char_length(regexp_replace(new.job_posting, rex, '')) AS prominence
            FROM (
                SELECT skill_id, '\y' || f_regexp_escape(skill) || '\y.*$' as rex, skill
                FROM skills
                WHERE strpos(new.job_posting, skill) > 0
                ) AS ta
            ) AS tb
        WHERE prominence < char_length(new.job_posting);

        -- Inserting job titles
        INSERT INTO posting_titles(title_id, job_id, prominence)
        SELECT title_id, new.job_id, prominence
        FROM (
            SELECT title_id, char_length(regexp_replace(new.job_posting, rex, '')) AS prominence
            FROM (
                SELECT title_id, '\y' || f_regexp_escape(title) || '\y.*$' as rex, title
                FROM titles_clean
                WHERE strpos(new.job_posting, title) > 0
                ) AS ta
            ) AS tb
        WHERE prominence < char_length(new.job_posting);

        -- Inserting job companies
        INSERT INTO posting_companies(company_id, job_id, prominence)
        SELECT company_id, new.job_id, prominence
        FROM (
            SELECT company_id, char_length(regexp_replace(new.job_posting, rex, '')) AS prominence
            FROM (
                SELECT company_id, '\y' || f_regexp_escape(company) || '\y.*$' as rex, company
                FROM companies_clean
                WHERE strpos(new.job_posting, company) > 0
                ) AS ta
            ) AS tb
        WHERE prominence < char_length(new.job_posting);

        RETURN new;
    END IF;
END;
$_$;


--
-- Name: jobs_sha256_tg(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION jobs_sha256_tg() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF Tg_op = 'INSERT' OR tg_op = 'UPDATE' THEN
        new.job_sha256 = encode(digest(new.job_posting, 'sha256'), 'hex');
        return new;
    END IF;
END;
$$;


SET default_with_oids = false;

--
-- Name: cand_companies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE cand_companies (
    cand_company_id integer NOT NULL,
    company_id integer,
    cv_id integer,
    prominence integer NOT NULL,
    CONSTRAINT cand_companies_prominence_check CHECK ((prominence >= 0))
);


--
-- Name: cand_companies_cand_company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cand_companies_cand_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cand_companies_cand_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cand_companies_cand_company_id_seq OWNED BY cand_companies.cand_company_id;


--
-- Name: cand_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE cand_skills (
    cand_skill_id integer NOT NULL,
    skill_id integer,
    cv_id integer,
    prominence integer NOT NULL,
    CONSTRAINT cand_skills_prominence_check CHECK ((prominence >= 0))
);


--
-- Name: cv_skill_correlations; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW cv_skill_correlations AS
 SELECT tb.skill_id_1,
    tb.skill_id_2,
    avg(((tb.cv1 = tb.cv2))::integer) AS correlation,
    avg(tb.dist) AS dist_avg
   FROM ( SELECT ta.skill_id_1,
            ta.skill_id_2,
            ta.p1,
            ta.p2,
            ta.cv1,
            ta.cv2,
                CASE
                    WHEN (ta.cv1 = ta.cv2) THEN abs((ta.p1 - ta.p2))
                    ELSE NULL::integer
                END AS dist
           FROM ( SELECT c1.skill_id AS skill_id_1,
                    c2.skill_id AS skill_id_2,
                    c1.cv_id AS cv1,
                    c2.cv_id AS cv2,
                    c1.prominence AS p1,
                    c2.prominence AS p2
                   FROM cand_skills c1,
                    cand_skills c2) ta) tb
  GROUP BY tb.skill_id_1, tb.skill_id_2
 HAVING (tb.skill_id_1 <> tb.skill_id_2)
  WITH NO DATA;


--
-- Name: cand_skill_importance; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW cand_skill_importance AS
 SELECT tc.cv_id,
    tc.skill_id,
    tc.correlation_avg,
    tc.dist_avg,
    (tc.correlation_avg *
        CASE
            WHEN (tc.dist_avg > (10)::numeric) THEN 0.9
            ELSE 1.1
        END) AS importance
   FROM ( SELECT tb.cv_id,
            tb.skill_id_1 AS skill_id,
            avg(tb.correlation) AS correlation_avg,
            avg(tb.dist_avg) AS dist_avg
           FROM ( SELECT ta.skill_id_1,
                    ta.skill_id_2,
                    ta.cv_id,
                    cv_skill_correlations.correlation,
                    cv_skill_correlations.dist_avg
                   FROM (( SELECT s1.skill_id AS skill_id_1,
                            s2.skill_id AS skill_id_2,
                            s1.cv_id
                           FROM cand_skills s1,
                            cand_skills s2
                          WHERE ((s1.cv_id = s2.cv_id) AND (s1.skill_id <> s2.skill_id))) ta
                     JOIN cv_skill_correlations USING (skill_id_1, skill_id_2))) tb
          GROUP BY tb.skill_id_1, tb.cv_id
          ORDER BY tb.cv_id, tb.skill_id_1) tc
  WITH NO DATA;


--
-- Name: posting_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE posting_skills (
    req_skill_id integer NOT NULL,
    skill_id integer,
    job_id integer,
    prominence integer NOT NULL,
    CONSTRAINT posting_skills_prominence_check CHECK ((prominence >= 0))
);


--
-- Name: posting_skill_importance; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW posting_skill_importance AS
 SELECT tc.job_id,
    tc.skill_id,
    tc.correlation_avg,
    tc.dist_avg,
    (tc.correlation_avg *
        CASE
            WHEN (tc.dist_avg > (10)::numeric) THEN 0.9
            ELSE 1.1
        END) AS importance
   FROM ( SELECT tb.job_id,
            tb.skill_id_1 AS skill_id,
            avg(tb.correlation) AS correlation_avg,
            avg(tb.dist_avg) AS dist_avg
           FROM ( SELECT ta.skill_id_1,
                    ta.skill_id_2,
                    ta.job_id,
                    cv_skill_correlations.correlation,
                    cv_skill_correlations.dist_avg
                   FROM (( SELECT s1.skill_id AS skill_id_1,
                            s2.skill_id AS skill_id_2,
                            s1.job_id
                           FROM posting_skills s1,
                            posting_skills s2
                          WHERE ((s1.job_id = s2.job_id) AND (s1.skill_id <> s2.skill_id))) ta
                     JOIN cv_skill_correlations USING (skill_id_1, skill_id_2))) tb
          GROUP BY tb.skill_id_1, tb.job_id
          ORDER BY tb.job_id, tb.skill_id_1) tc
  WITH NO DATA;


--
-- Name: cand_job_matches; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW cand_job_matches AS
 SELECT ta.cv_id,
    ta.job_id,
    sum(ta.importance) AS match_score
   FROM ( SELECT (c.importance + j.importance) AS importance,
            c.cv_id,
            j.job_id
           FROM cand_skill_importance c,
            posting_skill_importance j
          WHERE (c.skill_id = j.skill_id)) ta
  GROUP BY ta.cv_id, ta.job_id
  WITH NO DATA;


--
-- Name: cand_skills_cand_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cand_skills_cand_skill_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cand_skills_cand_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cand_skills_cand_skill_id_seq OWNED BY cand_skills.cand_skill_id;


--
-- Name: cand_titles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE cand_titles (
    cand_title_id integer NOT NULL,
    title_id integer,
    cv_id integer,
    prominence integer NOT NULL,
    CONSTRAINT cand_titles_prominence_check CHECK ((prominence >= 0))
);


--
-- Name: cand_titles_cand_title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cand_titles_cand_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cand_titles_cand_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cand_titles_cand_title_id_seq OWNED BY cand_titles.cand_title_id;


--
-- Name: companies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE companies (
    company_id integer NOT NULL,
    company character varying(1024) NOT NULL,
    company_tally integer NOT NULL
);


--
-- Name: companies_clean; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW companies_clean AS
 WITH tabstem AS (
         SELECT companies.company_id,
            companies.company,
            btrim(regexp_replace(regexp_replace(lower((companies.company)::text), '\y(the|limited|ltd|plc)\y'::text, ''::text), ' +'::text, ' '::text)) AS stem
           FROM companies
        )
 SELECT tabstem.company_id,
    tabstem.company,
    tx.pref_spelling
   FROM (( SELECT DISTINCT ON (tb.stem) tb.company AS pref_spelling,
            tb.stem,
            tb.tally
           FROM ( SELECT tabstem_1.company,
                    tabstem_1.stem,
                    count(*) AS tally
                   FROM tabstem tabstem_1
                  GROUP BY tabstem_1.company, tabstem_1.stem
                  ORDER BY (count(*)) DESC) tb) tx
     JOIN tabstem USING (stem))
  WITH NO DATA;


--
-- Name: companies_company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE companies_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: companies_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE companies_company_id_seq OWNED BY companies.company_id;


--
-- Name: cvs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE cvs (
    cv_id integer NOT NULL,
    cv_content text NOT NULL,
    cv_sha256 character(64) DEFAULT NULL::bpchar,
    update_time timestamp without time zone DEFAULT now(),
    cv_source character varying(1024) DEFAULT NULL::character varying
);


--
-- Name: cvs_cv_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cvs_cv_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cvs_cv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cvs_cv_id_seq OWNED BY cvs.cv_id;


--
-- Name: jobs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE jobs (
    job_id integer NOT NULL,
    job_posting text NOT NULL,
    job_sha256 character(64) DEFAULT NULL::bpchar,
    update_time timestamp without time zone DEFAULT now(),
    job_source character varying(1024) DEFAULT NULL::character varying
);


--
-- Name: jobs_job_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE jobs_job_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: jobs_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE jobs_job_id_seq OWNED BY jobs.job_id;


--
-- Name: posting_companies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE posting_companies (
    post_company_id integer NOT NULL,
    company_id integer,
    job_id integer,
    prominence integer NOT NULL,
    CONSTRAINT posting_companies_prominence_check CHECK ((prominence >= 0))
);


--
-- Name: posting_companies_post_company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE posting_companies_post_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: posting_companies_post_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE posting_companies_post_company_id_seq OWNED BY posting_companies.post_company_id;


--
-- Name: posting_skill_correlations; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW posting_skill_correlations AS
 SELECT tb.skill_id_1,
    tb.skill_id_2,
    avg(((tb.job1 = tb.job2))::integer) AS correlation,
    avg(tb.dist) AS dist_avg
   FROM ( SELECT ta.skill_id_1,
            ta.skill_id_2,
            ta.p1,
            ta.p2,
            ta.job1,
            ta.job2,
                CASE
                    WHEN (ta.job1 = ta.job2) THEN abs((ta.p1 - ta.p2))
                    ELSE NULL::integer
                END AS dist
           FROM ( SELECT c1.skill_id AS skill_id_1,
                    c2.skill_id AS skill_id_2,
                    c1.job_id AS job1,
                    c2.job_id AS job2,
                    c1.prominence AS p1,
                    c2.prominence AS p2
                   FROM posting_skills c1,
                    posting_skills c2) ta) tb
  GROUP BY tb.skill_id_1, tb.skill_id_2
 HAVING (tb.skill_id_1 <> tb.skill_id_2)
  WITH NO DATA;


--
-- Name: posting_skills_req_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE posting_skills_req_skill_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: posting_skills_req_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE posting_skills_req_skill_id_seq OWNED BY posting_skills.req_skill_id;


--
-- Name: posting_titles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE posting_titles (
    post_title_id integer NOT NULL,
    title_id integer,
    job_id integer,
    prominence integer NOT NULL,
    CONSTRAINT posting_titles_prominence_check CHECK ((prominence >= 0))
);


--
-- Name: posting_titles_post_title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE posting_titles_post_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: posting_titles_post_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE posting_titles_post_title_id_seq OWNED BY posting_titles.post_title_id;


--
-- Name: skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE skills (
    skill_id integer NOT NULL,
    skill text NOT NULL
);


--
-- Name: skills_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE skills_skill_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: skills_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE skills_skill_id_seq OWNED BY skills.skill_id;


--
-- Name: titles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE titles (
    title_id integer NOT NULL,
    title character varying(1024) NOT NULL,
    title_tally integer NOT NULL
);


--
-- Name: titles_clean; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW titles_clean AS
 SELECT titles.title_id,
    regexp_replace(regexp_replace((titles.title)::text, '\([^\)]+\)?'::text, ''::text, 'g'::text), '//.*$'::text, ''::text, 'g'::text) AS title,
    titles.title_tally
   FROM titles
  WHERE ((titles.title_tally > 1) AND (character_length((titles.title)::text) > 2))
  WITH NO DATA;


--
-- Name: titles_title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE titles_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: titles_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE titles_title_id_seq OWNED BY titles.title_id;


--
-- Name: cand_companies cand_company_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_companies ALTER COLUMN cand_company_id SET DEFAULT nextval('cand_companies_cand_company_id_seq'::regclass);


--
-- Name: cand_skills cand_skill_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_skills ALTER COLUMN cand_skill_id SET DEFAULT nextval('cand_skills_cand_skill_id_seq'::regclass);


--
-- Name: cand_titles cand_title_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_titles ALTER COLUMN cand_title_id SET DEFAULT nextval('cand_titles_cand_title_id_seq'::regclass);


--
-- Name: companies company_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY companies ALTER COLUMN company_id SET DEFAULT nextval('companies_company_id_seq'::regclass);


--
-- Name: cvs cv_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY cvs ALTER COLUMN cv_id SET DEFAULT nextval('cvs_cv_id_seq'::regclass);


--
-- Name: jobs job_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY jobs ALTER COLUMN job_id SET DEFAULT nextval('jobs_job_id_seq'::regclass);


--
-- Name: posting_companies post_company_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_companies ALTER COLUMN post_company_id SET DEFAULT nextval('posting_companies_post_company_id_seq'::regclass);


--
-- Name: posting_skills req_skill_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_skills ALTER COLUMN req_skill_id SET DEFAULT nextval('posting_skills_req_skill_id_seq'::regclass);


--
-- Name: posting_titles post_title_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_titles ALTER COLUMN post_title_id SET DEFAULT nextval('posting_titles_post_title_id_seq'::regclass);


--
-- Name: skills skill_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY skills ALTER COLUMN skill_id SET DEFAULT nextval('skills_skill_id_seq'::regclass);


--
-- Name: titles title_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY titles ALTER COLUMN title_id SET DEFAULT nextval('titles_title_id_seq'::regclass);


--
-- Name: cand_companies cand_companies_company_id_cv_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_companies
    ADD CONSTRAINT cand_companies_company_id_cv_id_key UNIQUE (company_id, cv_id);


--
-- Name: cand_companies cand_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_companies
    ADD CONSTRAINT cand_companies_pkey PRIMARY KEY (cand_company_id);


--
-- Name: cand_skills cand_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_skills
    ADD CONSTRAINT cand_skills_pkey PRIMARY KEY (cand_skill_id);


--
-- Name: cand_skills cand_skills_skill_id_cv_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_skills
    ADD CONSTRAINT cand_skills_skill_id_cv_id_key UNIQUE (skill_id, cv_id);


--
-- Name: cand_titles cand_titles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_titles
    ADD CONSTRAINT cand_titles_pkey PRIMARY KEY (cand_title_id);


--
-- Name: cand_titles cand_titles_title_id_cv_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_titles
    ADD CONSTRAINT cand_titles_title_id_cv_id_key UNIQUE (title_id, cv_id);


--
-- Name: companies companies_company_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY companies
    ADD CONSTRAINT companies_company_key UNIQUE (company);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (company_id);


--
-- Name: cvs cvs_cv_sha256_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cvs
    ADD CONSTRAINT cvs_cv_sha256_key UNIQUE (cv_sha256);


--
-- Name: cvs cvs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cvs
    ADD CONSTRAINT cvs_pkey PRIMARY KEY (cv_id);


--
-- Name: jobs jobs_job_sha256_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY jobs
    ADD CONSTRAINT jobs_job_sha256_key UNIQUE (job_sha256);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (job_id);


--
-- Name: posting_companies posting_companies_company_id_job_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_companies
    ADD CONSTRAINT posting_companies_company_id_job_id_key UNIQUE (company_id, job_id);


--
-- Name: posting_companies posting_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_companies
    ADD CONSTRAINT posting_companies_pkey PRIMARY KEY (post_company_id);


--
-- Name: posting_skills posting_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_skills
    ADD CONSTRAINT posting_skills_pkey PRIMARY KEY (req_skill_id);


--
-- Name: posting_skills posting_skills_skill_id_job_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_skills
    ADD CONSTRAINT posting_skills_skill_id_job_id_key UNIQUE (skill_id, job_id);


--
-- Name: posting_titles posting_titles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_titles
    ADD CONSTRAINT posting_titles_pkey PRIMARY KEY (post_title_id);


--
-- Name: posting_titles posting_titles_title_id_job_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_titles
    ADD CONSTRAINT posting_titles_title_id_job_id_key UNIQUE (title_id, job_id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (skill_id);


--
-- Name: skills skills_skill_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY skills
    ADD CONSTRAINT skills_skill_key UNIQUE (skill);


--
-- Name: titles titles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY titles
    ADD CONSTRAINT titles_pkey PRIMARY KEY (title_id);


--
-- Name: titles titles_title_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY titles
    ADD CONSTRAINT titles_title_key UNIQUE (title);


--
-- Name: cand_companies_company_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_companies_company_id_idx ON cand_companies USING btree (company_id);


--
-- Name: cand_companies_cv_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_companies_cv_id_idx ON cand_companies USING btree (cv_id);


--
-- Name: cand_companies_prominence_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_companies_prominence_idx ON cand_companies USING btree (prominence);


--
-- Name: cand_skills_cv_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_skills_cv_id_idx ON cand_skills USING btree (cv_id);


--
-- Name: cand_skills_prominence_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_skills_prominence_idx ON cand_skills USING btree (prominence);


--
-- Name: cand_skills_skill_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_skills_skill_id_idx ON cand_skills USING btree (skill_id);


--
-- Name: cand_titles_cv_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_titles_cv_id_idx ON cand_titles USING btree (cv_id);


--
-- Name: cand_titles_prominence_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_titles_prominence_idx ON cand_titles USING btree (prominence);


--
-- Name: cand_titles_title_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cand_titles_title_id_idx ON cand_titles USING btree (title_id);


--
-- Name: cvs_update_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX cvs_update_time_idx ON cvs USING btree (update_time);


--
-- Name: jobs_update_time_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX jobs_update_time_idx ON jobs USING btree (update_time);


--
-- Name: posting_companies_company_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_companies_company_id_idx ON posting_companies USING btree (company_id);


--
-- Name: posting_companies_job_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_companies_job_id_idx ON posting_companies USING btree (job_id);


--
-- Name: posting_companies_prominence_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_companies_prominence_idx ON posting_companies USING btree (prominence);


--
-- Name: posting_skills_job_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_skills_job_id_idx ON posting_skills USING btree (job_id);


--
-- Name: posting_skills_prominence_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_skills_prominence_idx ON posting_skills USING btree (prominence);


--
-- Name: posting_skills_skill_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_skills_skill_id_idx ON posting_skills USING btree (skill_id);


--
-- Name: posting_titles_job_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_titles_job_id_idx ON posting_titles USING btree (job_id);


--
-- Name: posting_titles_prominence_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_titles_prominence_idx ON posting_titles USING btree (prominence);


--
-- Name: posting_titles_title_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX posting_titles_title_id_idx ON posting_titles USING btree (title_id);


--
-- Name: cvs cv_inserts; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER cv_inserts AFTER INSERT ON cvs FOR EACH ROW EXECUTE PROCEDURE cv_inserts_tg();


--
-- Name: cvs cvs_hash_update; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER cvs_hash_update BEFORE INSERT OR UPDATE ON cvs FOR EACH ROW EXECUTE PROCEDURE cvs_sha256_tg();


--
-- Name: jobs job_inserts; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER job_inserts AFTER INSERT ON jobs FOR EACH ROW EXECUTE PROCEDURE job_inserts_tg();


--
-- Name: jobs jobs_hash_update; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER jobs_hash_update BEFORE INSERT OR UPDATE ON jobs FOR EACH ROW EXECUTE PROCEDURE jobs_sha256_tg();


--
-- Name: cand_companies cand_companies_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_companies
    ADD CONSTRAINT cand_companies_company_id_fkey FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE;


--
-- Name: cand_companies cand_companies_cv_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_companies
    ADD CONSTRAINT cand_companies_cv_id_fkey FOREIGN KEY (cv_id) REFERENCES cvs(cv_id) ON DELETE CASCADE;


--
-- Name: cand_skills cand_skills_cv_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_skills
    ADD CONSTRAINT cand_skills_cv_id_fkey FOREIGN KEY (cv_id) REFERENCES cvs(cv_id) ON DELETE CASCADE;


--
-- Name: cand_skills cand_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_skills
    ADD CONSTRAINT cand_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE;


--
-- Name: cand_titles cand_titles_cv_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_titles
    ADD CONSTRAINT cand_titles_cv_id_fkey FOREIGN KEY (cv_id) REFERENCES cvs(cv_id) ON DELETE CASCADE;


--
-- Name: cand_titles cand_titles_title_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cand_titles
    ADD CONSTRAINT cand_titles_title_id_fkey FOREIGN KEY (title_id) REFERENCES titles(title_id) ON DELETE CASCADE;


--
-- Name: posting_companies posting_companies_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_companies
    ADD CONSTRAINT posting_companies_company_id_fkey FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE;


--
-- Name: posting_companies posting_companies_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_companies
    ADD CONSTRAINT posting_companies_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE;


--
-- Name: posting_skills posting_skills_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_skills
    ADD CONSTRAINT posting_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE;


--
-- Name: posting_skills posting_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_skills
    ADD CONSTRAINT posting_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE;


--
-- Name: posting_titles posting_titles_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_titles
    ADD CONSTRAINT posting_titles_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE;


--
-- Name: posting_titles posting_titles_title_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posting_titles
    ADD CONSTRAINT posting_titles_title_id_fkey FOREIGN KEY (title_id) REFERENCES titles(title_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

-- REFRESH MATERIALIZED VIEW titles_clean;
