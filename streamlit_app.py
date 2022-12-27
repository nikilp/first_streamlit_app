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


def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruitvice_normalized


streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruitvice_data = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_data)

except URLError as e:
  streamlit.error()

streamlit.stop()
cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
cur = cnx.cursor()
cur.execute("SELECT * from fruit_load_list")

data_rows = cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(data_rows)

add_fruit = streamlit.text_input("What fruit do you want to add to the list?", 'jackfruit')
streamlit.write(f"Thanks for adding {add_fruit}")

if add_fruit not in data_rows:
  cur.execute(f"insert into fruit_load_list values ('{add_fruit}')")


