#Pulls birth data from wikipedia date pages and exports data to CSV

# Import package
import wikipedia
import calendar
import re
import pandas as pd
from countryinfo import CountryInfo

#-----------------------------------------------------------------------------------------------------------------------
#Date Module
#Generate wikipedia article list for days in a leap year

year = 2020
months = [1,2,3]
#Modify the above value for the months data is sourced from
cal = calendar.Calendar()
wikidate = []

for i in months:
    for day in cal.itermonthdays(year, i):
        if day == 0:
            pass
        else:
            date_month = str(calendar.month_name[i])
            date_day = str(day)
            date = " ".join([date_month, date_day])
            wikidate.append(date)

#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#Text-Partition Module

#Declare Lists
birth_year = []
birth_month_day = []
full_name = []
nationality = []
nationality_search_method = []
category_1, category_2, category_3, category_4, category_5, category_6, category_7, category_8, category_9, category_10 = [], [], [], [], [], [], [], [], [], []
births_remainder = []

for d in wikidate:
    import time
    start_time_secs = time.time()
    wiki = wikipedia.page(d, auto_suggest=False)
    # Extract the plain text content of the page
    wiki_text = wiki.content

    # Partitions into tuples to separate births/deaths
    wiki_text = wiki_text.partition('Births')
    wiki_text = (wiki_text[2])
    wiki_text = wiki_text.partition('Deaths')
    births = wiki_text[0]

    #Clean text births
    #Remove wiki formatting
    births = re.sub(r'==.*?==+', '', births)
    births = re.sub(r'==', '', births)
    births = re.sub("([\(\[]).*?([\)\]])", "", births)
    #Remove leading/trailing whitespace
    births = births.strip()
    #Convert to  list and remove blanks
    births = births.split("\n")
    while("" in births) :
        births.remove("")
    births = [i.strip() for i in births]
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#Get Birth Year and Month-Day Module

    for i in births:
        split_string = i.split("–", 1)
        split_string = split_string[0].strip()
        birth_year.append(split_string)
        birth_month_day.append(d)

#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#Get Full Name Module

    #Trim dash from text
    b_rem_process = [re.sub('^\d+\s|\s\d+\s|\s\d| +$', '', i) for i in births]
    births_remainder = [re.sub(r'– ', '', i) for i in b_rem_process]

    #Get Full Name
    for i in births_remainder:
        full_name_process = re.sub(r','+ ".*", '', i)
        full_name_process = full_name_process.strip()
        full_name.append(full_name_process)
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#Get nationality module

    # Resources for searching

    # Convert text read data to list and then to regex compatable string
    def read_list_regex_convert(read_list_name):
        converted_list = list(read_list_name.split(","))
        converted_list = [x.strip() for x in converted_list]
        return r'\b(?:%s)\b' % '|'.join(converted_list)

    #Nationality List
    with open('nationalities_list.txt', 'r', encoding='utf8') as nationalities_file:
        nationality_lines = nationalities_file.readlines()
        nationalities_list = lines[0]
    nat_list_regex = read_list_regex_convert(nationalities_list)

    #Country List
    with open('country_list.txt', 'r', encoding='utf8') as countries_file:
        country_lines = countries_file.readlines()
        country_list = lines[0]
    country_list_regex = read_list_regex_convert(country_list)

    #Get Nationality
    for i in births:
        # Search for matching nationality
        # Joins nationality list modifed to work for regex pattern search
        result = re.search(nat_list_regex, i, re.IGNORECASE)
        if result is None:
            search_result = re.search(country_list_regex, i, re.IGNORECASE)
            if search_result is None:
                nationality.append('None')
            else:
                try:
                    country = CountryInfo(search_result.group())
                    demonym_result = country.demonym()
                    nationality.append(demonym_result)
                except:
                    nationality.append('None')
        else:
            nationality.append(result.group())
    print('Day:', d, 'Number of names:', len(full_name))

#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#Category Assigner Module

    #Load Trait category data
    #Text file with each line containing keywords for each category
    with open('trait_categories.txt', 'r', encoding='utf8') as traits_file:
        lines = traits_file.readlines()
        athlete = lines[0]
        artist = lines[1]
        entertainer = lines[2]
        professional = lines[3]
        musician = lines[4]
        politician = lines[5]
        militant = lines[6]
        religious_figure = lines[7]
        aristocrat = lines[8]
        science_tech_academia = lines[9]
        misc = lines[10]

    # Define category regex strings
    athlete_regex = read_list_regex_convert(athlete)
    artist_regex = read_list_regex_convert(artist)
    entertainer_regex = read_list_regex_convert(entertainer)
    professional_regex = read_list_regex_convert(professional)
    musician_regex = read_list_regex_convert(musician)
    politician_regex = read_list_regex_convert(politician)
    militant_regex = read_list_regex_convert(militant)
    religious_figure_regex = read_list_regex_convert(religious_figure)
    aristocrat_regex = read_list_regex_convert(aristocrat)
    science_tech_academia_regex = read_list_regex_convert(science_tech_academia)
    misc_regex = read_list_regex_convert(misc)

    # Search data for each trait list and score
    def search_score(regex_list, string_name):
        result = re.findall(regex_list, string_name, re.IGNORECASE)
        count = len(result)
        return count

    for i in births:
        athlete_score = search_score(athlete_regex, i)
        artist_score = search_score(artist_regex, i)
        entertainer_score = search_score(entertainer_regex, i)
        professional_score = search_score(professional_regex, i)
        musician_score = search_score(musician_regex, i)
        politician_score = search_score(politician_regex, i)
        militant_score = search_score(militant_regex, i)
        religious_figure_score = search_score(religious_figure_regex, i)
        aristocrat_score = search_score(aristocrat_regex, i)
        science_tech_academia_score = search_score(science_tech_academia_regex, i)
        misc_score = search_score(misc_regex, i)

        #Scoring Dictionary, score values will be added here. Dictionary will later be sorted to determine catagory values
        score_dict = {
            'Athlete': '',
            'Artist': '',
            'Entertainer': '',
            'Professional': '',
            'Musician': '',
            'Politician': '',
            'Militant': '',
            'Religious Figure': '',
            'Aristocrat': '',
            'Science, Tech, Academia': '',
            'Misc': '',
        }

        # Appends scores to dictionary
        score_dict['Athlete'] = athlete_score
        score_dict['Artist'] = artist_score
        score_dict['Entertainer'] = entertainer_score
        score_dict['Professional'] = professional_score
        score_dict['Musician'] = musician_score
        score_dict['Politician'] = politician_score
        score_dict['Militant'] = militant_score
        score_dict['Religious Figure'] = religious_figure_score
        score_dict['Aristocrat'] = aristocrat_score
        score_dict['Science, Tech, Academia'] = science_tech_academia_score
        score_dict['Misc'] = misc_score

        # #Removes 0 values from dictionary
        new_score_dict = {k: v for k, v in score_dict.items() if int(v) != 0}

        # Sorts dictionary by value
        category_score_sorted = sorted(new_score_dict, key=new_score_dict.get)

        # Assign primary category to the highest value
        try:
            category_1.append(category_score_sorted[0])
        except:
            category_1.append('None')

        # Assign secondary category to second-highest value
        try:
            category_2.append(category_score_sorted[1])
        except:
            category_2.append('')

        # So on and so forth. Category 3
        try:
            category_3.append(category_score_sorted[2])
        except:
            category_3.append('')

        # Category 4
        try:
            category_4.append(category_score_sorted[3])
        except:
            category_4.append('')

        # Category 5
        try:
            category_5.append(category_score_sorted[4])
        except:
            category_5.append('')

        # Category 6
        try:
            category_6.append(category_score_sorted[5])
        except:
            category_6.append('')

        # Category 7
        try:
            category_7.append(category_score_sorted[6])
        except:
            category_7.append('')

        # Category 8
        try:
            category_8.append(category_score_sorted[7])
        except:
            category_8.append('')

        # Category 9
        try:
            category_9.append(category_score_sorted[8])
        except:
            category_9.append('')
        # Category 10
        try:
            category_10.append(category_score_sorted[9])
        except:
            category_10.append('')
#-----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------
#Get Name's URL and Word Count Module

#Declare lists
url = []
word_count = []

#Variable for counting passes
current_search_num = 0
total_search_num = len(full_name)

for n in full_name:
    current_search_num = current_search_num + 1
    try:
        url_word_count_wiki_page = wikipedia.page(n, auto_suggest=False)
        url_word_count_wiki = url_word_count_wiki_page.url
    except:
        url_word_count_wiki = ''
    url.append(url_word_count_wiki)
    if url_word_count_wiki != '':
        word_count_wiki_content = url_word_count_wiki_page.content
        word_count_wiki = len(word_count_wiki_content.split(' '))
        word_count.append(word_count_wiki)
    else:
        word_count.append('')
    print("Searched", current_search_num,"out of", total_search_num)
    
# -----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
#CSV Export Module
dict = {'full_name': full_name,
        'birth_year': birth_year,
        'birth_month_day': birth_month_day,
        'nationality': nationality,
        'primary_category': category_1,
        'category_2': category_2,
        'category_3': category_3,
        'category_4': category_4,
        'category_5': category_5,
        'category_6': category_6,
        'category_7': category_7,
        'category_8': category_8,
        'category_9': category_9,
        'category_10': category_10,
        'url': url,
        'word_count': word_count
        }
df = pd.DataFrame(dict)

#Input file name:
print('Input File Name (Be sure to include .csv)')
file_name = input()

# saving the dataframe
df.to_csv(file_name)