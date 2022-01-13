import pandas as pd
from datetime import date

df = pd.read_csv('glassdoor_salary.csv')

# salary parsing
# company name
# state
# age of company
# parsing jd


# salary parsing
df['hourly'] = df['Salary Estimate'].apply(lambda x: 'per hour' in x.lower() and 1 or 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 'employer provided salary' in x.lower() and 1 or 0)
# print(df[df['employer_provided'] == 1])

df = df[df['Salary Estimate']!='-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0].strip(' '))
salary_wo_symbols = salary.apply(lambda x: x.lower().replace('k', '').replace('$', '').replace('per hour','').replace('employer provided salary',''))
df['min_salary'] = salary_wo_symbols.apply(lambda x: int(x.split('-')[0].strip(' ').replace(':','')))
df['max_salary'] = salary_wo_symbols.apply(lambda x: int(x.split('-')[1].strip(' ').replace(':','')))
df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2

# company name
df['company_name_text'] = df.apply(lambda x: x['Rating'] < 0 and x['Company Name'] or x['Company Name'][:-3].strip('\r\n'), axis=1)

# state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1].strip(' '))
df['same_state'] = df.apply(lambda x: x['Location'] == x['Headquarters'] and 1 or 0, axis = 1)

# age of company
df['age'] = df['Founded'].apply(lambda x: x<0 and x or date.today().year - x)

# parsing jd
df['python_jd'] = df['Job Description'].apply(lambda x: 'python' in x.lower() and 1 or 0)
df['rstudio_jd'] = df['Job Description'].apply(lambda x: 'r studio' in x.lower() and 1 or 0)
df['aws_jd'] = df['Job Description'].apply(lambda x: 'aws' in x.lower() and 1 or 0)
df['spark_jd'] = df['Job Description'].apply(lambda x: 'spark' in x.lower() and 1 or 0)
df['excel_jd'] = df['Job Description'].apply(lambda x: 'excel' in x.lower() and 1 or 0)

df_out = df.drop(['Unnamed: 0'], axis = 1)
df_out.to_csv('glassdoor_salary_cleaned.csv', index = False)