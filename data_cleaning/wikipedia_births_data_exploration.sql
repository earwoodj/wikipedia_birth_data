--Basic Data Exploration
SELECT id, full_name, birth_year, birth_month_day, nationality, primary_category, category_2, category_3, category_4, category_5, url, word_count
FROM `wikipedia-birth-data`.working_data.birth_data
ORDER BY id
LIMIT 100

--Number of id's, names, years, birthdates, nationalities, and URL's
SELECT COUNT(DISTINCT(id)) AS number_of_records,
COUNT(DISTINCT(full_name)) AS number_of_distinct_names,
COUNT(DISTINCT(url)) AS number_of_distinct_urls,
COUNT(DISTINCT(birth_year)) AS number_of_distinct_years,
COUNT(DISTINCT(birth_month_day)) AS number_of_distinct_birthday,
COUNT(DISTINCT(nationality)) AS number_of_distinct_nationalies
FROM `wikipedia-birth-data`.working_data.birth_data

--Number in each primary category
SELECT primary_category, COUNT(*) AS number_in_category
FROM `wikipedia-birth-data`.working_data.birth_data
GROUP BY primary_category 
ORDER BY number_in_category DESC

--Number in each nationality 
SELECT nationality , COUNT(*) AS number_in_nationality
FROM `wikipedia-birth-data`.working_data.birth_data
GROUP BY nationality  
ORDER BY number_in_nationality DESC

--Number of people with 5, 4, 3, 2, 1, and no categories


--Number with and without links
SELECT COUNT(word_count) AS number_with_links
FROM `wikipedia-birth-data`.working_data.birth_data
WHERE url IS NOT NULL 

--Max values of word count and associated link
SELECT full_name, word_count, url
FROM `wikipedia-birth-data`.working_data.birth_data
ORDER BY word_count DESC 
LIMIT 100

--Max and min values for year,
SELECT MIN(birth_year) AS min_birth_year, MAX(birth_year) as max_birth_year
FROM `wikipedia-birth-data`.working_data.birth_data

--Check to see if there are any null values where they are not expected
SELECT *
FROM `wikipedia-birth-data`.working_data.birth_data
WHERE
	id IS NULL
	OR full_name IS NULL
	OR birth_year IS NULL
	OR nationality IS NULL
	OR birth_month_day IS NULL 
	OR primary_category IS NULL
	
--Check to see what longest names are 
SELECT full_name
FROM `wikipedia-birth-data`.working_data.birth_data
ORDER BY LENGTH(full_name)


--Problems Identified:
--Duplicate names 
--Missing URLs
--Missing primary categories
--Shortest full names are not coherent
--All of these will need to be removed to certify visualization integrity

--How many will remain after removing problematic records?
SELECT COUNT(*) AS remaining_records
FROM `wikipedia-birth-data`.working_data.birth_data
WHERE full_name NOT IN
(
	SELECT full_name
	FROM `wikipedia-birth-data`.working_data.birth_data
	GROUP BY full_name 
	HAVING COUNT(*) > 1
	
)
AND full_name NOT IN 
(
	SELECT full_name
	FROM `wikipedia-birth-data`.working_data.birth_data
	ORDER BY LENGTH(full_name)
	LIMIT 5
)
AND url IS NOT NULL 
AND primary_category IS NOT NULL


--Revised data exploration
--Will to download this data and re-upload to big query 
SELECT *
FROM `wikipedia-birth-data`.working_data.birth_data
WHERE full_name NOT IN
(
	SELECT full_name
	FROM `wikipedia-birth-data`.working_data.birth_data
	GROUP BY full_name 
	HAVING COUNT(*) > 1
	
)
AND full_name NOT IN 
(
	SELECT full_name
	FROM `wikipedia-birth-data`.working_data.birth_data
	ORDER BY LENGTH(full_name)
	LIMIT 5
)
AND url IS NOT NULL 
AND primary_category IS NOT NULL
ORDER BY id

--The following identified are problems, but do not break the visualization that I am trying to complete:
--These problems cannot be fixed without modifying the python program that was used to collect this data 
--Hyphenated nationalities are often not represented accurately
--In rare cases, an incorrect wikipedia article is used as the link/word count source 
--Aristocrats are underrepresented. Wikipedia often has their name as Princess name_name_name X of Y-Z with no other context.
--If a title is not included with these aristocrats, then they are flagged as having "None" as their primary category

--A problem that can be fixed is that birth_month_day is a string when it should be combined with the year to create a unique date
--Note that Feb-29 has the month first rather than the day. This will need to be fixed later
 SELECT DISTINCT birth_month_day 
FROM `wikipedia-birth-data`.working_data.preliminary_data 
ORDER BY birth_month_day DESC

--First, lets separate the day and the month
--Parses string using - as the delineator
SELECT birth_month_day, LEFT(birth_month_day, ((STRPOS(birth_month_day ,'-')-1))) AS birth_day, RIGHT(birth_month_day, CHAR_LENGTH(birth_month_day)-(STRPOS(birth_month_day ,'-'))) AS birth_month
FROM `wikipedia-birth-data`.working_data.preliminary_data 

ALTER TABLE `wikipedia-birth-data`.working_data.preliminary_data 
ADD COLUMN birth_day int;

ALTER TABLE `wikipedia-birth-data`.working_data.preliminary_data 
ADD COLUMN birth_month int;

--Sadly, I am using the free version of big query. That being said, I cannot use DML queries. This is what I would have used. I edited the data using Excel instead. 
UPDATE `wikipedia-birth-data`.working_data.preliminary_data
SET birth_day = LEFT(birth_month_day, ((STRPOS(birth_month_day ,'-')-1))), birth_month = RIGHT(birth_month_day, CHAR_LENGTH(birth_month_day)-(STRPOS(birth_month_day ,'-')))
WHERE id = 1
