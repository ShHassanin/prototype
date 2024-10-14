import streamlit as st
import pandas as pd
import os 
import plotly.express as px

st.set_page_config(page_icon = '1fac0.png',page_title= 'Sentiment Analysis',layout='wide')
st.title(':chart_with_upwards_trend: Sentiment Analysis Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)
st.sidebar.header('Select Analysis')
Analysis = st.sidebar.radio('Select Plot type',['Distribution','Pie','Barplot','Scatter','Strip','Aggregation'])

files=[file for file in os.listdir('1-XML_to_CSV')]
files 
eda = pd.DataFrame()
for file in files:
    df= pd.read_csv(f'1-XML_to_CSV/{file}')
    eda = pd.concat([eda,df],axis=0)
columns = ['product_name', 'product_type', 'helpful','rating', 'title', 'date', 'reviewer', 'reviewer_location','review_text']
continuous = ['rating']
cat_discrete = ['product_name', 'product_type','title','helpful','reviewer', 'reviewer_location']
t=st.slider('Select height for the figure: ',400,2000,600)

if Analysis=='Distribution':
    st.subheader('Distribution for features')
    Dist_col = st.selectbox('selsect feature to explore Distribution:',eda.columns)
    Dist_y = st.selectbox('selsect feature to explore summition for it :', continuous)
    Dist_color = st.selectbox('selsect feature to explore values in it:',eda.columns )
    st.plotly_chart(px.histogram(eda,x=Dist_col,y=Dist_y ,color=Dist_color,barmode='group',opacity=.5,marginal='violin',
                                 text_auto=True,height=t,title=f'{Dist_col} Distribution'),  use_container_width=True)

elif Analysis=='Pie':
    st.subheader('Percentage of each label in the data or of the feature\'s label from a summation of other  feature   (Bivariate & Univariate Analysis)')
    name= st.selectbox('Select categorical feature: ',cat_discrete)
    values= st.selectbox(f'Select feature to sum for each {name} label: ', continuous)
    st.plotly_chart(px.pie(eda ,names=name,values=values,hover_data=values),  use_container_width=True)

elif Analysis=='Strip':
    strip_x = st.selectbox('Select feature to see density in each value :',eda.columns)
    strip_rest = eda.columns.drop(strip_x)
    strip_y = st.selectbox('Select feature to see density for :',continuous)
    strip_color = st.selectbox('Select feature for color :',eda.columns)
    st.plotly_chart(px.strip(eda,x=strip_x,y=strip_y,height=t,title=f' Distribution and density for {strip_y} in the data for each value in {strip_x}')  , use_container_width=True)



elif Analysis=='Scatter':
    st.subheader('Correlations between features(Bivariate Analysis)')

    scatter_x = st.selectbox('Select x axis: ',continuous)
    scatter_y= st.selectbox('Select y axis: ',continuous)
    scatter_color = st.selectbox('Select color: ',eda.columns)
    st.plotly_chart(px.scatter(eda,x=scatter_x,y=scatter_y,color= scatter_color ,height=t),  use_container_width=True)

elif Analysis=='Barplot':
    st.subheader('Barplots for features(Bivariate Analysis)')

    bar_x= st.selectbox('Select categorical feature: ',eda.columns)
    bar_y= st.selectbox('Select numerical feature: ',continuous)
    color_bar = st.selectbox('Select third feature for color: ',eda.columns)
    st.plotly_chart(px.bar(eda,x=bar_x,y=bar_y,height=t,color=color_bar),  use_container_width=True)



elif Analysis=='Aggregation':
    st.subheader('Aggregation for features (Bivariate Analysis)')

    agg_column = st.selectbox('Select column to aggregate: ',eda.columns)
    rest = eda.columns.drop(agg_column)
    num_agg = st.selectbox('Select column to aggregate for: ', continuous )
    agg_fun = st.selectbox('Select  aggregate function: ',['mean','sum','count'])
    agg_df = eda.groupby(agg_column).agg({
                        num_agg: agg_fun 
    }).reset_index()

    st.plotly_chart(px.bar(agg_df,x=agg_column,y=num_agg,height=t,title=f'{agg_fun} of {num_agg}  for each {agg_column} value'), use_container_width=True)
