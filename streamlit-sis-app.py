# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Copy & Paste Into Table")
st.write(
    """Select cells from Excel, paste in the 'Dataset' section, and automatically create a table"""
)

# Get the current credentials
session = get_active_session()

with st.form("my_form"):
    header = st.columns(3)
    dbschema = session.sql("SELECT CURRENT_DATABASE() AS DB, CURRENT_SCHEMA() AS SCMA").to_pandas()
    with header[0]:
        db = st.text_input('Database', dbschema["DB"][0])
    
    with header[1]:
        schema = st.text_input('Schema', dbschema["SCMA"][0])
    
    with header[2]:
        table = st.text_input('New Table', f"NEW_TABLE")

    dataset = st.text_area("Dataset")
    
   	# Every form must have a submit button.
    submitted = st.form_submit_button("Create Table")
    if submitted:
        lines = dataset.split("\n")

        i = 0
        for line in lines:
            cols = line.split("\t")
            if(i==0):
                fields = []
                for col in cols:
                    fields.append(f'"{col}" string')
                query = f'CREATE OR REPLACE TABLE "{db}"."{schema}"."{table}" ({", ".join(fields)})'
            else:
                fields = []
                for col in cols:
                    fields.append(f"'{col}'")
                query = f"""INSERT INTO "{db}"."{schema}"."{table}" VALUES ({', '.join(fields)})"""
            session.sql(query).collect()
            i = i+1

        st.caption(f'SELECT * FROM "{db}"."{schema}"."{table}"')
        st.write(session.table(f'"{db}"."{schema}"."{table}"').to_pandas())        