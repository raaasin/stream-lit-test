import os

import pandas as pd

from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse

employees_df = pd.DataFrame(
    {
        "EmployeeID": [1, 2, 3, 4, 5],
        "Name": ["John", "Emma", "Liam", "Olivia", "William"],
        "Department": ["HR", "Sales", "IT", "Marketing", "Finance"],
    }
)

salaries_df = pd.DataFrame(
    {
        "EmployeeID": [1, 2, 3, 4, 5],
        "Salary": [5000, 6000, 4500, 7000, 5500],
    }
)

# By default, unless you choose a different LLM, it will use BambooLLM.
# You can get your free API key signing up at https://pandabi.ai (you can also configure it in your .env file)
os.environ["PANDASAI_API_KEY"] = "$2a$10$foYM9PHFSnQrKNdPmla6aeq.4Os1z8tO0opn7A3mtX4E.XrClySgq"

agent = Agent(
    [employees_df, salaries_df],
    config={"verbose": True, "response_parser": StreamlitResponse},
)

agent.chat("Plot salaries against employee name")