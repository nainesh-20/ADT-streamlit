import streamlit as st
import pandas as pd
        
import base64


def main():

    # st.markdown(
    #      f"""
    #      <style>
    #      .stApp {{
    #          background: url("https://drive.google.com/file/d/14hbNHQ9gL3FEaByAf9qIIbZQX3IgcsMi/view?usp=sharing");
    #          background-size: cover
    #      }}
    #      </style>
    #      """,
    #      unsafe_allow_html=True
    #  )
    st.title("Upload your stock data to forecast")
    st.write("Upload a CSV or Excel file")

    file = st.file_uploader("Upload file", type=["csv", "xlsx"])

    if file is not None:
        df = read_file(file)
        if df is not None:
            st.write("File Uploaded Successfully!")
            # st.write(df.head())

            # Display information based on columns
            display_information(df)

# @st.cache(allow_output_mutation=True)

def set_bg_hack(main_bg):
        '''
        A function to unpack an image from root folder and set as bg.
    
        Returns
        -------
        The background.
        '''
        # set bg name
        main_bg_ext = "png"
            
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
     )
    
set_bg_hack("formbg.png")

def read_file(file):
    try:
        if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(file)
        elif file.type == "text/csv":
            df = pd.read_csv(file)
        else:
            st.error("File type not supported. Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"An error occurred while reading the file: {str(e)}")
        return 
    
def display_information(df):
    st.write("Items Going to Expire Soon (Within 20 days):")

    # Filter items that are going to expire within 20 days based on days_in_store
    expiring_soon = df[(df['days_in_store'] >= 15) & (df['days_in_store'] <= 20)]

    if expiring_soon.empty:
        st.write("No items are going to expire soon.")
    else:
        # Calculate the number of days left to expire
        expiring_soon.loc[:, 'days_left_to_expire'] = 20 - expiring_soon['days_in_store']
        
        # Select only the 'supplieslist' and 'days_left_to_expire' columns
        expiring_soon_display = expiring_soon[['provider_id', 'supplieslist', 'days_left_to_expire']]
        
        st.write(expiring_soon_display)

    st.write("Expired Items:")

    # Filter items that have already expired based on days_in_store
    expired_items = df[df['days_in_store'] > 20]

    if expired_items.empty:
        st.write("No items have expired.")
    else:
        st.write(expired_items)

if __name__ == "__main__":
    main()
