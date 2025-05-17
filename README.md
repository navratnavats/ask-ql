#  AskQL: Natural Language to SQL Interface

**AskQL** is a powerful Python-based tool that allows users to interact with SQL databases using natural language questions. It supports both Command-Line Interface (CLI) and a sleek Streamlit-based UI, making it ideal for developers and non-technical users alike.

---

## Features

### Current Features

| Feature                | CLI                   | UI (Streamlit App)      |
| ---------------------- | --------------------- | ----------------------- |
| MySQL & SQLite support | Yes                 | Yes                   |
| Natural Language → SQL | Via LangChain Agent | Via LangChain Agent   |
| DB selection prompt    | Yes                 | Via sidebar selector  |
| Display query output   | In terminal         | In table format in UI |
| Session memory         |   No                  | History panel         |

###  Upcoming Features

*  **Data Visualization:** Render charts from SQL results (bar, pie, line).
*  **Download CSV:** Export query results as downloadable CSV files.
*  **Multi-DB Support:** Extend support to PostgreSQL, MSSQL, and MongoDB.

---

##  How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/navratnavats/ask-ql.git
cd ask-ql
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

##  How to Use

###  CLI Interface

```bash
cd cli
python main.py
```

* Lists available databases
* Lets user select DB
* Accepts a natural language question and converts it to SQL
* Executes and prints result

###  UI Interface (Streamlit App)

```bash
cd cli  # UI file is also in cli directory
streamlit run askql_ui.py
```

* Choose between MySQL and SQLite
* Ask questions via textbox
* See query + results
* Visual interface for easier use

---

##  Required Python Packages

```plaintext
python-dotenv
streamlit
langchain
sqlalchemy
pymysql
```

Also recommended:

```plaintext
openai  # for LLM queries (ensure API key set)
```

---

##  Environment Variables

Create a `.env` file in the root folder with the following:

```env
# Required for MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_db_name

# OpenAI key for LangChain agent
OPENAI_API_KEY=your_openai_api_key
```


---

##  Contribution

Open to contributions for:

* Adding more database support (PostgreSQL, MSSQL)
* Chart rendering improvements
* Security and query optimization

Feel free to fork and raise a PR! 

---

##  License


---

Let me know if you'd like this in markdown file format as well!
