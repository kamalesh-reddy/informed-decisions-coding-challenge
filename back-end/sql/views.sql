-- View: public.ranged_fact_population

-- DROP VIEW public.ranged_fact_population;

CREATE OR REPLACE VIEW public.ranged_fact_population
 AS
 SELECT dimsex.sex_abs,
    dimsex.sex,
    concat(floor((factpopulation.age / 5)::double precision) * 5::double precision, '-', floor((factpopulation.age / 5)::double precision) * 5::double precision + 4::double precision, ' year old') AS age_range,
    dimstate.state_id,
    dimstate.state,
    dimregion.asgs_2016,
    dimregion.region,
    factpopulation.census_year,
    sum(factpopulation.value) AS total_value
   FROM dimregion
     JOIN factpopulation ON dimregion.asgs_2016 = factpopulation.asgs_2016
     JOIN dimsex ON dimsex.sex_abs = factpopulation.sex_abs
     JOIN dimstate ON dimstate.state_id = dimregion.state_id
  GROUP BY dimregion.asgs_2016, dimstate.state_id, factpopulation.census_year, (floor((factpopulation.age / 5)::double precision)), dimsex.sex_abs
  ORDER BY dimregion.asgs_2016, factpopulation.census_year, (floor((factpopulation.age / 5)::double precision));

ALTER TABLE public.ranged_fact_population
    OWNER TO postgres;

