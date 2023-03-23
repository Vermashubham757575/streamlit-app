import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="centered")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)




# ---- MAINPAGE ----


st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")


tab1 , tab2  = st.tabs(["Page 1", "Page 2"])

with tab1:
    # SALES BY PRODUCT LINE [BAR CHART]
    sales_by_product_line = (
        df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    )
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
        template="plotly_white",
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    # SALES BY HOUR [BAR CHART]
    sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Total",
        title="<b>Sales by hour</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
    right_column.plotly_chart(fig_product_sales, use_container_width=True)

    st.write("bar chart")
    fig = px.bar(x= df["Gender"],y =  df["Total"], color=df["Gender"])
    st.plotly_chart(fig)

with tab2:
    # code
    st.subheader("boxplot Gender and total")
    plot1 = sns.catplot(x='Gender',y='Total',kind='box',data=df, height=4, aspect=2,width= 0.5)
    st.pyplot(plot1.figure)

    st.subheader("boxplot of city and total")
    plot2 = sns.catplot(x='City',y='Total',kind='box',data=df,height=4, aspect=2,width= 0.5)
    st.pyplot(plot2.figure)

    st.subheader("boxplot of comaprision between gender and city")
    plot3 = sns.catplot(x='City',y='Total',kind='box',hue='Gender',data=df, height=4, aspect=2,width= 0.5)
    st.pyplot(plot3.figure)

    st.subheader("pie chart of product line")
    fig4 = px.pie(df,names="Product line")
    st.plotly_chart(fig4)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




