    # Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be :',name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe =  session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()



ingradients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingradients_list:
    ingradients_string = ''
    for fruit_chosen in ingradients_list:
        ingradients_string += fruit_chosen + ''
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ',fruit_chosen,'is ',search_on,'.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('""" + ingradients_string + """','""" + name_on_order + """') """
    st.write(my_insert_stmt)
    st.stop()


    
