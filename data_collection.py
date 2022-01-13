import scrape_glassdoor as gs
import pandas as pd

df = gs.get_jobs('data scientist', 15, False, "./chromedriver.exe", 5)
df.to_csv('glassdoor_jobs.csv', index = False)