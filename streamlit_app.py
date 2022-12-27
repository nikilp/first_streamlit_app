import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_data)

except URLError as e:
  streamlit.error()


streamlit.header("View Our Fruit List - Add Your Favorites!")

def get_fruit_load_list():
  with cnx.cursor() as cur:
    cur.execute("SELECT * from fruit_load_list")
    return cur.fetchall()

if streamlit.button('Get Fruit List'):
  cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
  data_rows = get_fruit_load_list()
  cnx.close()
  streamlit.dataframe(data_rows)


# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with cnx.cursor() as cur:
    cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
  return f"Thanks for adding {new_fruit}"

add_fruit = streamlit.text_input("What fruit do you want to add to the list?", 'jackfruit')
if streamlit.button("Add Fruit to the List"):
  cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
  inserted_in_snowflake = insert_row_snowflake(add_fruit)
  cnx.close()
  streamlit.text(inserted_in_snowflake)


