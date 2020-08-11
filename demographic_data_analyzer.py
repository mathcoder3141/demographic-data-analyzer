import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    adult = pd.read_csv('adult_data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = adult['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(adult[adult['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(100 * len(adult[adult['education'] == 'Bachelors']) / len(adult), 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    adult['education class'] = adult['education-num'].apply(lambda x: 'Advanced' if x in (13, 14, 16) else 'No Advanced')
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = adult[adult['education class'] == 'Advanced']
    lower_education = adult[adult['education class'] == 'No Advanced']

    # percentage with salary >50K
    higher_education_rich = round(100 * higher_education['salary'].value_counts(normalize=True).get('>50K'), 1)
    lower_education_rich = round(100 * lower_education['salary'].value_counts(normalize=True).get('>50K'), 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = adult['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = len(adult[adult['hours-per-week'] == adult['hours-per-week'].min()])

    rich_percentage = len(adult[(adult['hours-per-week'] == adult['hours-per-week'].min()) & (adult['salary'] == '>50K')]) * 100 / num_min_workers

    # What country has the highest percentage of people that earn >50K?
    all = adult[['salary', 'native-country']]
    entire = all.groupby(['native-country']).count()
    plus50k = all[all['salary'] == '>50K'].groupby('native-country').count()
    plus50k = (plus50k * 100) / entire
    plus50k.sort_values(by='salary', ascending=False, inplace=True)
    final = pd.Series(plus50k['salary'])
    highest_earning_country = final.index[0]
    highest_earning_country_percentage = round(final.values[0], 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = adult[(adult['native-country'] == 'India') & (adult['salary'] >= '50K')]['occupation'].value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
