# TC - 255

Package written while studying SQL, OOP, and web scraping [@TuringCollege](https://www.turingcollege.com/)

## Usage and examples

Install dependencies:

```python
pip install -r requirements.txt
```

Folder tc255 contains two files `database.py` and `scraper.py` you should create `main.py` and in it import the main functions:

```python
from tc255.scraper import scrape_ebay
from tc255.database import setup_db, insert_to_db, export_csv
```

There should be files `secrets.json` in the root of the repository containing pstgresql connection information.

### setup_db(categories)

Creates a 2 tables for storing data. Also fills in `keyword` table with category values. For now it only accepts 3 arguments.

### insert_to_db(dataframe)

Inserts dataframe from `scrape_ebay` function into the database.

### export_csv(path)

Joins the two tables and exports them into csv file.

### scrape_ebay(keyword, n=3000)

 Finds n amount of ebay listings for the given keyword and returns a dataframe.

DataFrame columns: category, title, price, item_url, img_url. All columns are of type string.

## License 

[MIT](https://opensource.org/licenses/MIT)

