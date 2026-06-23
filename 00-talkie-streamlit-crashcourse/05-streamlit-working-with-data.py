import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

st.title("Streamlit with data, plotting")

auto_data = pd.read_csv("data/auto.csv", header=0, index_col=None)
st.write(auto_data.head(10))

st.area_chart(auto_data[["mpg",  "cylinders"]])
st.line_chart(auto_data[["mpg",  "cylinders"]])

st.bar_chart(auto_data.head(20)[["mpg",  "cylinders"]])


corr = auto_data[["mpg",  "cylinders", "displacement", "horsepower"]].corr()
st.write(corr)

fig, axe = plt.subplots()
sns.heatmap(corr, annot=True)
axe.set_title("Correlation matrix")
st.pyplot(fig)

fig = px.scatter(auto_data, x="mpg", y="horsepower")
st.plotly_chart(fig)

temperatures = pd.read_csv("data/weather_data.csv")
st.write(temperatures)
st.map(temperatures, latitude="lat", longitude="long", size="temp")

alt_chart = alt.Chart(auto_data).mark_circle().encode(
    x='mpg', y='horsepower',
    color='origin'
).interactive()

st.write(alt_chart)