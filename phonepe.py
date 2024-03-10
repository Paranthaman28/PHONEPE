import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql
import mysql.connector
import pandas as pd
import requests
import json
import PIL 
from PIL import Image


#data frame creation
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()

mycursor.execute("SELECT * FROM project1.agg_insur2")
table_agg_insur=mycursor.fetchall()
agg_insur_pd=pd.DataFrame(table_agg_insur,columns=("States","Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#agg_trans_output_dataframe
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.agg_trans2")
table_agg_trans=mycursor.fetchall()
agg_trans_pd=pd.DataFrame(table_agg_trans,columns=("States","Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#table aggruser
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.agg_user2")
table_agg_user=mycursor.fetchall()
agg_user_pd=pd.DataFrame(table_agg_user,columns=("States","Years","Quater","Brands","Transaction_count","Percentage"))


#table for map_insur
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.map_insur2")
table_map_insur=mycursor.fetchall()
map_insur_pd=pd.DataFrame(table_map_insur,columns=("States","Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#table for map_trans
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.map_trans2")
table_map_trans=mycursor.fetchall()
map_trans_pd=pd.DataFrame(table_map_trans,columns=("States","Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#table for map_user
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.map_user2")
table_map_user=mycursor.fetchall()
map_user_pd=pd.DataFrame(table_map_user,columns=("States","Years","Quater","Districts","RegisteredUser","AppOpens"))

#table_top_insur
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.top_insur2")
table_top_insur=mycursor.fetchall()
top_insur_pd=pd.DataFrame(table_top_insur,columns=("States","Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#table_top_trans
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.top_trans1")
table_top_trans=mycursor.fetchall()
top_trans_pd=pd.DataFrame(table_top_trans,columns=("States","Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#table_top_user
connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
mycursor=connection.cursor()
mycursor.execute("SELECT * FROM project1.top_user1")
table_top_user=mycursor.fetchall()
top_user_pd=pd.DataFrame(table_top_user,columns=("States","Years","Quater","Pincodes","Registeredusers"))




def transaction_amount_count_Y(df,year):
    trans_amount_count_year=df[df["Years"]==year]
    trans_amount_count_year.reset_index(drop=True,inplace=True)
    trans_amount_count_year_group=trans_amount_count_year.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    trans_amount_count_year_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)

    with col1:


        fig_amount=px.bar(trans_amount_count_year_group,x='States',y='Transaction_amount',title=f'{year}Transaction Amount',height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:

    
        fig_count=px.bar(trans_amount_count_year_group,x='States',y=f'Transaction_count',title=f'{year}Transaction Count',color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()
    col1,col2=st.columns(2)

    with col1:

        fig_india_map=px.choropleth(trans_amount_count_year_group, geojson=data1,locations="States",featureidkey="properties.ST_NM",color="Transaction_amount",color_continuous_scale="Rainbow",range_color=(trans_amount_count_year_group["Transaction_amount"].min(),trans_amount_count_year_group["Transaction_amount"].max()),hover_name="States",title=f"{year}TRANSACTION AMOUNT",fitbounds="locations",height=600,width=600)
        fig_india_map.update_geos(visible=False)
        st.plotly_chart(fig_india_map)

    with col2:

        fig_india_map1=px.choropleth(trans_amount_count_year_group, geojson=data1,locations="States",featureidkey="properties.ST_NM",color="Transaction_count",color_continuous_scale="Rainbow",range_color=(trans_amount_count_year_group["Transaction_count"].min(),trans_amount_count_year_group["Transaction_count"].max()),hover_name="States",title=f"{year}TRANSACTION COUNT",fitbounds="locations",height=600,width=600)
        fig_india_map1.update_geos(visible=False)
        st.plotly_chart(fig_india_map1)

    return trans_amount_count_year


def transaction_amount_count_Y_Q(df,quater):
    trans_amount_count_year=df[df["Quater"]==quater]
    trans_amount_count_year.reset_index(drop=True,inplace=True)
    trans_amount_count_year_group=trans_amount_count_year.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    trans_amount_count_year_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(trans_amount_count_year_group,x='States',y='Transaction_amount',title=f"{trans_amount_count_year['Years'].unique()} YEAR {quater} QUATER Transaction Amount",height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:


        fig_count=px.bar(trans_amount_count_year_group,x='States',y=f'Transaction_count',title=f"{trans_amount_count_year['Years'].unique()} YEAR {quater} QUATER Transaction Count",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)


    col1,col2=st.columns(2)    
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
    
        fig_india_map=px.choropleth(trans_amount_count_year_group, geojson=data1,locations="States",featureidkey="properties.ST_NM",color="Transaction_amount",color_continuous_scale="Rainbow",range_color=(trans_amount_count_year_group["Transaction_amount"].min(),trans_amount_count_year_group["Transaction_amount"].max()),hover_name="States",title=f"{trans_amount_count_year['Years'].unique()} YEAR {quater} QUATER TRANSACTION AMOUNT",fitbounds="locations",height=600,width=600)
        fig_india_map.update_geos(visible=False)
        
        st.plotly_chart(fig_india_map)
    with col2:

        fig_india_map1=px.choropleth(trans_amount_count_year_group, geojson=data1,locations="States",featureidkey="properties.ST_NM",color="Transaction_count",color_continuous_scale="Rainbow",range_color=(trans_amount_count_year_group["Transaction_count"].min(),trans_amount_count_year_group["Transaction_count"].max()),hover_name="States",title=f"{trans_amount_count_year['Years'].unique()} YEAR {quater} QUATER TRANSACTION COUNT",fitbounds="locations",height=600,width=600)
        fig_india_map1.update_geos(visible=False)
        st.plotly_chart(fig_india_map1)  
    
    return trans_amount_count_year

def agg_transaction_type(df,state):

    trans_amount_count_year=df[df["States"]==state	]
    trans_amount_count_year.reset_index(drop=True,inplace=True)

    trans_amount_count_year_group=trans_amount_count_year.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    trans_amount_count_year_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)

    with col1:


        fig_pie_1=px.pie(data_frame=trans_amount_count_year_group,names="Transaction_type",values="Transaction_amount",width=600,title=f"{state.upper()}""TRANSACTION AMOUNT")
        st.plotly_chart(fig_pie_1)

    with col2:


        fig_pie_2=px.pie(data_frame=trans_amount_count_year_group,names="Transaction_type",values="Transaction_count",width=600,title=f"{state.upper()}" "TRANSACTION COUNT")
        st.plotly_chart(fig_pie_2)

def aggr_user(df,year):
    agg_user_year=df[df["Years"]==year]
    agg_user_year.reset_index(drop=True,inplace=True)
    agg_user_year_group=pd.DataFrame(agg_user_year.groupby("Brands")[["Transaction_count","Percentage"]].sum())
    agg_user_year_group.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

        fig_bar_user=px.bar(agg_user_year_group,x="Brands",y="Transaction_count",title=f"{year}BRAND AND TRANSACTION COUNT",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r,hover_name="Brands")
        st.plotly_chart(fig_bar_user)

    with col2:
        fig_bar_user=px.bar(agg_user_year_group,x="Brands",y="Percentage",title=f"{year}BRAND AND TRANSACTION PERCENTAGE",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r,hover_name="Brands")
        st.plotly_chart(fig_bar_user)

    return agg_user_year

def agg_user_quarter(df,quater):
    agg_user_year_quater=df[df["Quater"]==quater]
    agg_user_year_quater.reset_index(drop=True,inplace=True)
    agg_user_year_quater_group=pd.DataFrame(agg_user_year_quater.groupby("Brands")[["Transaction_count","Percentage"]].sum())
    agg_user_year_quater_group.reset_index(inplace=True)
    agg_user_year_quater_group
    
    col1,col2=st.columns(2)

    with col1:

        fig_bar_user1=px.bar(agg_user_year_quater_group,x="Brands",y="Transaction_count",title=f"{quater} Quater BRAND AND TRANSACTION COUNT",width=900,color_discrete_sequence=px.colors.sequential.Reds_r,hover_name="Brands")
        st.plotly_chart(fig_bar_user1)
    with col2:

        fig_bar_user2=px.bar(agg_user_year_quater_group,x="Brands",y="Percentage",title=f"{quater} Quater BRAND AND PERCENTAGE",width=900,color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
        st.plotly_chart(fig_bar_user2)


    return agg_user_year_quater


def agg_user_state(df,state):
    agg_Q_states=df[df['States']==state]
    agg_Q_states.reset_index(drop=True,inplace=True)
    col1,col2=st.columns(2)
    with col1:


        fig_agg_q_state1=px.line(agg_Q_states,x="Brands",y="Transaction_count",markers=True,title=f"{state}BRANDS TRANSACTION COUNT USE STATE",width=600,height=600,hover_name="Percentage")
        st.plotly_chart(fig_agg_q_state1)

    with col2:

        fig_agg_q_state2=px.line(agg_Q_states,x="Brands",y="Percentage",markers=True,title=f"{state}BRANDS TRANSACTION COUNT USE STATE",width=600,height=600,hover_name="Transaction_count")
        st.plotly_chart(fig_agg_q_state2)

    return agg_Q_states


def top_insur_plot1(df,state):

    top_insur_pin=df[df["States"]==state]
    top_insur_pin.reset_index(drop=True,inplace=True)
    top_insur_pin_g=top_insur_pin.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()

    top_insur_pin_g.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        fig_top_bar1=px.bar(top_insur_pin,x="Quater",y="Transaction_amount",hover_data="Pincodes",title="PINCODES AND TRANSACTION AMOUNT",width=600,height=600)
        st.plotly_chart(fig_top_bar1)

    with col2:
        

        fig_top_bar2=px.bar(top_insur_pin,x="Quater",y="Transaction_count",hover_data="Pincodes",title="PINCODES AND TRANSACTION COUNT",width=600,height=600,color_discrete_sequence=px.colors.sequential.Redor_r)
        st.plotly_chart(fig_top_bar2)
    return top_insur_pin

def top_user_plot(df,year):

    top_user_pin=df[df["Years"]==year]
    top_user_pin.reset_index(drop=True,inplace=True)
    top_user_pin_g=pd.DataFrame(top_user_pin.groupby(["States","Quater"])["Registeredusers"].sum())
    top_user_pin_g.reset_index(inplace=True)

    fig_top_bar=px.bar(top_user_pin_g,x="States",y="Registeredusers",hover_data="Quater",title="PINCODES AND Registeredusers",width=900)
    st.plotly_chart(fig_top_bar)
    return top_user_pin


def top_user_plot2(df,state):

    top_user_pin_y=df[df["States"]==state]
    top_user_pin_y.reset_index(drop=True,inplace=True)
    top_user_pin_y_g=pd.DataFrame(top_user_pin_y.groupby(["States","Quater"])[["Registeredusers","Pincodes"]].sum())
    top_user_pin_y_g.reset_index(inplace=True)

    fig_top_bar=px.bar(top_user_pin_y_g,x="Quater",y="Registeredusers",hover_data="Pincodes",title="PINCODES AND Registeredusers",width=600,height=600)
    st.plotly_chart(fig_top_bar)
    return top_user_pin_y_g


def map_insur_amount_count_Y(df,year):
    map_insu_amount_count_year=df[df["Years"]==year]
    map_insu_amount_count_year.reset_index(drop=True,inplace=True)
    map_insu_amount_count_year_group=map_insu_amount_count_year.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    map_insu_amount_count_year_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)

    with col1:


        fig_amount=px.bar(map_insu_amount_count_year,x='States',y='Transaction_amount',title=f'{year}Transaction Amount',height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:

    
        fig_count=px.bar(map_insu_amount_count_year,x='States',y=f'Transaction_count',title=f'{year}Transaction Count',color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)



def map_insur_Q(df,state):
    map_amount_count_year_sate=df[df["States"]==state]
    map_amount_count_year_sate.reset_index(drop=True,inplace=True)

    map_amount_count_year_sate_group=map_amount_count_year_sate.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    map_amount_count_year_sate_group.reset_index(inplace=True)
    col1,col2=st.columns(2)

    with col1:

        fig_pie_1=px.pie(data_frame=map_amount_count_year_sate,names="Transaction_type",values="Transaction_amount",width=600,title=f"{'quater'.upper()}""TRANSACTION AMOUNT")
        st.plotly_chart(fig_pie_1)
     
    with col2:

        fig_pie_2=px.pie(data_frame=map_amount_count_year_sate,names="Transaction_type",values="Transaction_count",width=600,title=f"{'quater'.upper()}" "TRANSACTION COUNT")
        st.plotly_chart(fig_pie_2)

    return map_amount_count_year_sate


def map_transaction_amount_count_Y_Q(df,quater):
    map_transaction_amount_count=df[df["Quater"]==quater]
    map_transaction_amount_count.reset_index(drop=True,inplace=True)
    map_transaction_amount_count_group=map_transaction_amount_count.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    map_transaction_amount_count_group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(map_transaction_amount_count,x='States',y='Transaction_amount',title=f"{map_transaction_amount_count ['Years'].unique()} YEAR {quater} QUATER Transaction Amount",height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:


        fig_count=px.bar(map_transaction_amount_count,x='States',y=f'Transaction_count',title=f"{map_transaction_amount_count ['Years'].unique()} YEAR {quater} QUATER Transaction Count",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)
    
    return map_transaction_amount_count



def map_user(df,year):
    map_user_year=df[df["Years"]==year]
    map_user_year.reset_index(drop=True,inplace=True)
    map_user_year_group=pd.DataFrame(map_user_year.groupby("States")[["RegisteredUser","AppOpens"]].sum())
    map_user_year_group.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:


        fig_bar_user=px.line(map_user_year_group,x="States",y=["RegisteredUser","AppOpens"],title=f"{year} MAP REGISTERED AND AppOpens USER",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_user)

    with col2:


        fig_bar_user=px.line(map_user_year_group,x="States",y=["RegisteredUser","AppOpens"],title=f"{year} MAP REGISTERED AND AppOpens USER",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_user)

    return map_user_year




def map_user_state(df,state):
    map_user_state=df[df["States"]==state]
    map_user_state.reset_index(drop=True,inplace=True)
    map_user_state_group=pd.DataFrame(map_user_state.groupby("Districts")[["RegisteredUser","AppOpens"]].sum())
    map_user_state_group.reset_index(inplace=True)


    col1,col2=st.columns(2)

    with col1:


        fig_bar_user=px.line(map_user_state_group,x="Districts",y="RegisteredUser",title=f"{state} MAP REGISTERED USER",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_user)

    with col2:

    
        fig_bar_user2=px.line(map_user_state_group,x="Districts",y="AppOpens",title=f"{state} MAP REGISTERED USER",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_user2)

    return map_user_state


def map_user_Q(df,quater):
    map_user_year=df[df["Quater"]==quater]
    map_user_year.reset_index(drop=True,inplace=True)
    map_user_year_group=pd.DataFrame(map_user_year.groupby("States")[["RegisteredUser","AppOpens"]].sum())
    map_user_year_group.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:


        fig_bar_user=px.line(map_user_year_group,x="States",y=["RegisteredUser","AppOpens"],title=f"{quater} MAP REGISTERED USER",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_user)
    
    with col2:
        fig_bar_user2=px.line(map_user_year_group,x="States",y=["RegisteredUser","AppOpens"],title=f"{quater} MAP REGISTERED USER",width=600,height=600,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_bar_user2)

    return map_user_year



def top_chart_trans_amount(table_name):



    connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
    mycursor=connection.cursor()

    #PLOT1
    query_1=f'''SELECT States,sum(Transaction_amount) as Transaction_amount
                FROM project1.{table_name}
                group by(States)
                order by Transaction_amount desc 
                limit 10;'''
    mycursor.execute(query_1)
    table_1=mycursor.fetchall()
    connection.commit()
    df_1=pd.DataFrame(table_1)
    df_1=pd.DataFrame(table_1,columns=('States','Transaction_amount'))
    col1,col2=st.columns(2)

    with col1:

        bar_df_1=px.bar(df_1,x="States",y="Transaction_amount",title="MAX TO MINI TRANSACTION AMOUNT",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(bar_df_1)

    #PLOT2
    query_2=f'''SELECT States,sum(Transaction_amount) as Transaction_amount
                FROM project1.{table_name}
                group by(States)
                order by Transaction_amount  
                limit 10;'''
    mycursor.execute(query_2)
    table_2=mycursor.fetchall()
    connection.commit()
    df_2=pd.DataFrame(table_2)
    df_2=pd.DataFrame(table_2,columns=('States','Transaction_amount'))

    with col2:

        bar_df_2=px.bar(df_2,x="States",y="Transaction_amount",title="MINI TO MAX TRANSACTION AMOUNT",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(bar_df_2)



    #PLOT3
    query_3=f'''SELECT States,avg(Transaction_amount) as Transaction_amount
                FROM project1.{table_name}
                group by(States)
                order by Transaction_amount'''
    mycursor.execute(query_3)
    table_3=mycursor.fetchall()
    connection.commit()
    df_3=pd.DataFrame(table_3)
    df_3=pd.DataFrame(table_3,columns=('States','Transaction_amount'))
    bar_df_3=px.bar(df_3,x="States",y="Transaction_amount",title="AVERAGE TRANSACTION AMOUNT",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.YlOrRd_r)
    st.plotly_chart(bar_df_3)


def top_chart_trans_count(table_name):



    connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
    mycursor=connection.cursor()

    #PLOT1
    query_1=f'''SELECT States,sum(Transaction_count) as Transaction_count
                FROM project1.{table_name}
                group by(States)
                order by Transaction_count desc 
                limit 10;'''
    mycursor.execute(query_1)
    table_1=mycursor.fetchall()
    connection.commit()
    df_1=pd.DataFrame(table_1)
    df_1=pd.DataFrame(table_1,columns=('States','Transaction_count'))
    col1,col2=st.columns(2)

    with col1:

        bar_df_1=px.bar(df_1,x="States",y="Transaction_count",title="MAX TO MINI TRANSACTION COUNT",width=700,height=700,hover_name="States",color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(bar_df_1)

    #PLOT2
    query_2=f'''SELECT States,sum(Transaction_count) as Transaction_count
                FROM project1.{table_name}
                group by(States)
                order by Transaction_count  
                limit 10;'''
    mycursor.execute(query_2)
    table_2=mycursor.fetchall()
    connection.commit()
    df_2=pd.DataFrame(table_2)
    df_2=pd.DataFrame(table_2,columns=('States','Transaction_count'))

    with col2:

        bar_df_2=px.bar(df_2,x="States",y="Transaction_count",title="MINI TO MAX TRANSACTION COUNT",width=700,height=700,hover_name="States",color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(bar_df_2)



    #PLOT3
    query_3=f'''SELECT States,avg(Transaction_count) as Transaction_count
                FROM project1.{table_name}
                group by(States)
                order by Transaction_count'''
    mycursor.execute(query_3)
    table_3=mycursor.fetchall()
    connection.commit()
    df_3=pd.DataFrame(table_3)
    df_3=pd.DataFrame(table_3,columns=('States','Transaction_count'))


    bar_df_3=px.bar(df_3,x="States",y="Transaction_count",title="AVERAGE TRANSACTION COUNT",width=700,height=700,hover_name="States",color_discrete_sequence=px.colors.sequential.YlGnBu_r)
    st.plotly_chart(bar_df_3)

    #PLOT1
def map_registered_user(table_name):



    connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
    mycursor=connection.cursor()

    #PLOT1
    query_1=f'''SELECT States,sum(registeredUser) as registeredUser
                FROM project1.{table_name}
                group by(States)
                order by registeredUser desc
                limit 10;'''
    mycursor.execute(query_1)
    table_1=mycursor.fetchall()
    connection.commit()
    df_1=pd.DataFrame(table_1)
    df_1=pd.DataFrame(table_1,columns=('States','registeredUser'))
    col1,col2=st.columns(2)
    with col1:

        bar_df_1=px.bar(df_1,x="States",y="registeredUser",title="MAX TO MINI REGSITERED",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(bar_df_1)

    #PLOT2
    query_2=f'''SELECT States,sum(registeredUser) as registeredUser
                FROM project1.{table_name}
                group by(States)
                order by registeredUser  
                limit 10;'''
    mycursor.execute(query_2)
    table_2=mycursor.fetchall()
    connection.commit()
    df_2=pd.DataFrame(table_2)
    df_2=pd.DataFrame(table_2,columns=('States','registeredUser'))

    with col2:
        bar_df_2=px.bar(df_2,x="States",y="registeredUser",title="MINI TO MAX REGSITERED",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(bar_df_2)



    #PLOT3
    query_3=f'''SELECT States,avg(registeredUser) as registeredUser
                FROM project1.{table_name}
                group by(States)
                order by registeredUser'''
    mycursor.execute(query_3)
    table_3=mycursor.fetchall()
    connection.commit()
    df_3=pd.DataFrame(table_3)
    df_3=pd.DataFrame(table_3,columns=('States','registeredUser'))
    bar_df_3=px.bar(df_3,x="States",y="registeredUser",title="AVERAGE REGSITERED",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.YlGnBu_r)
    st.plotly_chart(bar_df_3)


def map_App_user(table_name):



    connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
    mycursor=connection.cursor()

    #PLOT1
    query_1=f'''SELECT States,sum(appOpens) as appOpens
                FROM project1.{table_name}
                group by(States)
                order by appOpens desc
                limit 10;'''
    mycursor.execute(query_1)
    table_1=mycursor.fetchall()
    connection.commit()
    df_1=pd.DataFrame(table_1)
    df_1=pd.DataFrame(table_1,columns=('States','appOpens'))
    col1,col2=st.columns(2)
    with col1:

        bar_df_1=px.bar(df_1,x="States",y="appOpens",title="MAX TO MINI APPOPNES",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(bar_df_1)

    #PLOT2
    query_2=f'''SELECT States,sum(appOpens) as appOpens
                FROM project1.{table_name}
                group by(States)
                order by appOpens  
                limit 10;'''
    mycursor.execute(query_2)
    table_2=mycursor.fetchall()
    connection.commit()
    df_2=pd.DataFrame(table_2)
    df_2=pd.DataFrame(table_2,columns=('States','appOpens'))
    with col2:

        bar_df_2=px.bar(df_2,x="States",y="appOpens",title="MINI TO MAX APPOPNES",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(bar_df_2)



    #PLOT3
    query_3=f'''SELECT States,avg(appOpens) as appOpens
                FROM project1.{table_name}
                group by(States)
                order by appOpens'''
    mycursor.execute(query_3)
    table_3=mycursor.fetchall()
    connection.commit()
    df_3=pd.DataFrame(table_3)
    df_3=pd.DataFrame(table_3,columns=('States','appOpens'))
    bar_df_3=px.bar(df_3,x="States",y="appOpens",title="AVERAGE appOpens",width=600,height=600,hover_name="States",color_discrete_sequence=px.colors.sequential.YlGnBu_r)
    st.plotly_chart(bar_df_3)



def Agg_user(table_name):



    connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
    mycursor=connection.cursor()

    #PLOT1
    query_1=f'''SELECT Brands,sum(Transaction_count) as Transaction_count
                FROM project1.{table_name}
                group by(Brands)
                order by Transaction_count desc
                limit 10;'''
    mycursor.execute(query_1)
    table_1=mycursor.fetchall()
    connection.commit()
    df_1=pd.DataFrame(table_1)
    df_1=pd.DataFrame(table_1,columns=('Brands','Transaction_count'))

    col1,col2=st.columns(2)

    with col1:
        bar_df_1=px.bar(df_1,x="Brands",y="Transaction_count",title="MAX TO MINI BRAND TRANSCATION COUNT",width=600,height=600,hover_name="Brands",color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(bar_df_1)

    #PLOT2
    query_2=f'''SELECT Brands,sum(Transaction_count) as Transaction_count
                FROM project1.{table_name}
                group by(Brands)
                order by Transaction_count  
                limit 10;'''
    mycursor.execute(query_2)
    table_2=mycursor.fetchall()
    connection.commit()
    with col2:

        df_2=pd.DataFrame(table_2)
        df_2=pd.DataFrame(table_2,columns=('Brands','Transaction_count'))

        bar_df_2=px.bar(df_2,x="Brands",y="Transaction_count",title="MINI TO MAX BRAND TRANSCATION COUNT",width=600,height=600,hover_name="Brands",color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(bar_df_2)



    #PLOT3
    query_3=f'''SELECT Brands,avg(Transaction_count) as Transaction_count
                FROM project1.{table_name}
                group by(Brands)
                order by Transaction_count'''
    mycursor.execute(query_3)
    table_3=mycursor.fetchall()
    connection.commit()
    df_3=pd.DataFrame(table_3)
    df_3=pd.DataFrame(table_3,columns=('Brands','Transaction_count'))
    bar_df_3=px.bar(df_3,x="Brands",y="Transaction_count",title="AVERAGE BRAND TRANSCATION COUNT",width=600,height=600,hover_name="Brands",color_discrete_sequence=px.colors.sequential.YlGnBu_r)
    st.plotly_chart(bar_df_3)


def top_user(table_name):



    connection=mysql.connector.connect(host="localhost",user="root",password="12345",database="project1")
    mycursor=connection.cursor()

    #PLOT1
    query_1=f'''SELECT Pincodes,sum(Registeredusers) as Registeredusers
                FROM project1.{table_name}
                group by(Pincodes)
                order by Registeredusers desc
                limit 10;'''
    mycursor.execute(query_1)
    table_1=mycursor.fetchall()
    connection.commit()
    df_1=pd.DataFrame(table_1)
    df_1=pd.DataFrame(table_1,columns=('Pincodes','Registeredusers'))

    col1,col2=st.columns(2)

    with col1:
        bar_df_1=px.bar(df_1,x="Pincodes",y="Registeredusers",title="MAX TO MINI PINCODES AND REGISTERED USER",width=600,height=600,hover_name="Pincodes",color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(bar_df_1)

    #PLOT2
    query_2=f'''SELECT Pincodes,sum(Registeredusers) as Registeredusers
                FROM project1.{table_name}
                group by(Pincodes)
                order by Registeredusers  
                limit 10;'''
    mycursor.execute(query_2)
    table_2=mycursor.fetchall()
    connection.commit()
    with col2:

        df_2=pd.DataFrame(table_2)
        df_2=pd.DataFrame(table_2,columns=('Pincodes','Registeredusers'))

        bar_df_2=px.bar(df_2,x="Pincodes",y="Registeredusers",title="MINI TO MAX PINCODES AND REGISTERED USER",width=600,height=600,hover_name="Pincodes",color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(bar_df_2)



    #PLOT3
    query_3=f'''SELECT Pincodes,avg(Registeredusers) as Registeredusers
                FROM project1.{table_name}
                group by(Pincodes)
                order by Registeredusers'''
    mycursor.execute(query_3)
    table_3=mycursor.fetchall()
    connection.commit()
    df_3=pd.DataFrame(table_3)
    df_3=pd.DataFrame(table_3,columns=('Pincodes','Registeredusers'))
    bar_df_3=px.bar(df_3,x="Pincodes",y="Registeredusers",title="AVERAGE PINCODES AND REGISTERED USER",width=600,height=600,hover_name="Pincodes",color_discrete_sequence=px.colors.sequential.YlGnBu_r)
    st.plotly_chart(bar_df_3)



#streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPEE DATA VISUALIZATION")
with st.sidebar:
    select=option_menu("main menu",["Home","Data Explore","Maxi_data"])

if select=="Home":
    method=st.radio("PICK THE METHOD",["ABOUT","CONTACT"])

    if method=="ABOUT":
        st.video(r"C:\Users\Paranthaman\Downloads\pulse-video.mp4")
        col1,col2=st.columns(2)
        col1.image(Image.open(r"C:\Users\Paranthaman\Downloads\Phonepe_image2.png"))
        with col1:
                st.subheader("PhonePe is an India's best digital transaction of paymeby and finacial techanology company which HeadQuater is in Bengaluru,Karnataka,India.PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
                st.download_button("Download the APP Now","https://www.phonepe.com/app-download/")

        with col2:
            st.video(r"C:\Users\Paranthaman\Downloads\upi.mp4")

        col,col2=st.columns(2)
        with col1:
            st.image(Image.open(r"C:\Users\Paranthaman\Downloads\about_phonepe2.jpg"))        

        with col2:
          st.subheader("PhonePe becomes a leading payments company")

          st.image(Image.open(r"C:\Users\Paranthaman\Downloads\about_phonepe1.png"))
        
    elif method=="CONTACT":

        Name=st.write(f'{"Name:"}  {"Paranthaman"}')
        E_mail=st.write(f'{"Mail:"}   {"thalaivadhamu29@gmail.com"}')
        Description=st.write(f'{"Description:"} {"Become a Data Scientist"}')
        LinkedIn=st.write(f'{"LinkedIn"} {"www.linkedin.com/in/paranthamam-p-b468101b0"}')
        Phone=st.write(f'{"Phone:"} {"6384234070"}')
        visit=st.write(f'{"Visit"}  {"https://www.phonepe.com/"}')


elif select=="Data Explore":
    tab1,tab2,tab3=st.tabs(["Analysis of Aggregate","Analysis of Map","Analysis of Top"])
    with tab1:
        process=st.radio("Pick the process",["Insurance Analysis","Transaction Analysis","User Analysis"])
        if process=="Insurance Analysis":
        
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("pass the Year",agg_insur_pd["Years"].min(),agg_insur_pd["Years"].max(),agg_insur_pd["Years"].min())
            tacy_y=transaction_amount_count_Y(agg_insur_pd,years)

            col1,col2=st.columns(2)
            with col1:

                quater=st.slider("pass the Quater",tacy_y["Quater"].min(),tacy_y["Quater"].max(),tacy_y["Quater"].min())
            transaction_amount_count_Y_Q(tacy_y,quater)


        elif process=="Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("pass the Year",agg_trans_pd["Years"].min(),agg_trans_pd["Years"].max(),agg_trans_pd["Years"].min())
            agg_trans_amo_cou=tacy_y=transaction_amount_count_Y(agg_trans_pd,years)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("pass the states",agg_trans_amo_cou["States"].unique())

            agg_transaction_type(agg_trans_amo_cou,states)

            col1,col2=st.columns(2)
            with col1:

                quater=st.slider("pass the Quater",agg_trans_amo_cou["Quater"].min(),agg_trans_amo_cou["Quater"].max(),agg_trans_amo_cou["Quater"].min())
            argg_trans_amou_count_y_q=transaction_amount_count_Y_Q(agg_trans_amo_cou,quater)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("pass the states_tpye",argg_trans_amou_count_y_q["States"].unique())

            agg_transaction_type(argg_trans_amou_count_y_q,states)

        elif process=="User Analysis":
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("pass the Year",agg_user_pd["Years"].min(),agg_user_pd["Years"].max(),agg_user_pd["Years"].min())
            agg_user_y=aggr_user(agg_user_pd,years)

            col1,col2=st.columns(2)
            with col1:

                quater=st.slider("pass the Quater",agg_user_y["Quater"].min(),agg_user_y["Quater"].max(),agg_user_y["Quater"].min())
            agg_user_y_q=agg_user_quarter(agg_user_y,quater)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("pass the states",agg_user_y_q["States"].unique())

            agg_user_state(agg_user_y_q,states)

    with tab2:
        process1=st.radio("Pick the process1",["Insurance Analysis","Transaction Analysis","User Analysis"])
        if process1=="Insurance Analysis":
            years=st.slider("pass the Year_map",map_insur_pd["Years"].min(),map_insur_pd["Years"].max(),map_insur_pd["Years"].min())
            map_insur_year=map_insur_amount_count_Y(map_insur_pd,years)
            states=st.selectbox("pass the states_map_insur",map_insur_pd["States"].unique())

            map_insur_Q(map_insur_pd,states)

            quater=st.slider("pass the Quater_map_Q",map_insur_pd["Quater"].min(),map_insur_pd["Quater"].max(),map_insur_pd["Quater"].min())
            map_transaction_amount_count_Y_Q(map_insur_pd,quater)



        elif process1=="Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("pass the Year_top_trans",map_trans_pd["Years"].min(),map_trans_pd["Years"].max(),map_trans_pd["Years"].min())
            map_trans_year=transaction_amount_count_Y(map_trans_pd,years)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("pass the states_trans",map_trans_pd["States"].unique())

            map_insur_Q(map_trans_pd,states)

            quater=st.slider("pass the Quater_map_Q",map_trans_pd["Quater"].min(),map_trans_pd["Quater"].max(),map_trans_pd["Quater"].min())
            map_transaction_amount_count_Y_Q(map_trans_pd,quater)



        elif process1=="User Analysis":
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("pass the Year_top_USER",map_user_pd["Years"].min(),map_user_pd["Years"].max(),map_user_pd["Years"].min())
            map_user_year=map_user(map_user_pd,years)

            states=st.selectbox("pass the states_map",map_user_pd["States"].unique())
            map_user_state(map_user_pd,states)

            quater=st.slider("pass the Quater_user_Q",map_trans_pd["Quater"].min(),map_trans_pd["Quater"].max(),map_trans_pd["Quater"].min())
            map_user_Q(map_user_pd,quater)

    with tab3:
        process2=st.radio("Pick the process2",["Insurance Analysis","Transaction Analysis","User Analysis"])
        if process2=="Insurance Analysis":
            years=st.slider("pass the Year_top",top_insur_pd["Years"].min(),top_insur_pd["Years"].max(),top_insur_pd["Years"].min())
            top_insur_y=transaction_amount_count_Y(top_insur_pd,years)

            
            col1,col2=st.columns(2)
            with col1:

                quater=st.slider("pass the Quater_top_Q",top_insur_y["Quater"].min(),top_insur_y["Quater"].max(),top_insur_y["Quater"].min())
            transaction_amount_count_Y_Q(top_insur_y,quater)
            states=st.selectbox("pass the states_top",top_insur_y["States"].unique())
            
            top_insur_plot1(top_insur_y,states)
        elif process2=="Transaction Analysis":
            years=st.slider("pass the Year_top_trans",top_trans_pd["Years"].min(),top_trans_pd["Years"].max(),top_trans_pd["Years"].min())
            top_trans_y=transaction_amount_count_Y(top_trans_pd,years)
            col1,col2=st.columns(2)
            with col1:

                quater=st.slider("pass the Quater_top_trans_Q",top_trans_y["Quater"].min(),top_trans_y["Quater"].max(),top_trans_y["Quater"].min())
            transaction_amount_count_Y_Q(top_trans_y,quater)
            states=st.selectbox("pass the states_top",top_trans_y["States"].unique())
            
            top_insur_plot1(top_trans_y,states)
        elif process2=="User Analysis":
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("pass the Year_top_user",top_user_pd["Years"].min(),top_user_pd["Years"].max(),top_user_pd["Years"].min())
            top_user_y=top_user_plot(top_user_pd,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("pass the states_top_user_state",top_user_pd["States"].unique())

            top_user_plot2(top_user_pd,states)

elif select=="Maxi_data":
    what_you_want=st.selectbox("select the what you want",["1.Transaction Amount and Count of Aggregate Insurance",
                                                           "2.Transaction Amount and Count of Map Insurance",
                                                           "3.Transaction Amount and Count of Top Insurance",
                                                           "4.Transaction Amount and Count of Aggregate Transaction",
                                                           "5.Transaction Amount and Count of Map Transaction",
                                                           "6.Transaction Amount and Count of Top Transaction",
                                                           "7.Transaction Count of Aggregate User",
                                                           "8.Registereduser of Map User",
                                                           "9.AppOpens of Map User",
                                                           "10.Registereduser of Top User"])
    if what_you_want=="1.Transaction Amount and Count of Aggregate Insurance":
        top_chart_trans_amount('agg_insur2')
        top_chart_trans_count('agg_insur2')
    elif what_you_want== "2.Transaction Amount and Count of Map Insurance":
        top_chart_trans_amount('map_insur2')
        top_chart_trans_count('map_insur2')
    elif what_you_want=="3.Transaction Amount and Count of Top Insurance":
        top_chart_trans_amount('top_insur2')
        top_chart_trans_count('top_insur2')
    elif what_you_want=="4.Transaction Amount and Count of Aggregate Transaction":
        top_chart_trans_amount('agg_trans2')
        top_chart_trans_count('agg_trans2')
    elif what_you_want=="5.Transaction Amount and Count of Map Transaction":
        top_chart_trans_amount('map_trans2')
        top_chart_trans_count('map_trans2')
    elif what_you_want=="6.Transaction Amount and Count of Top Transaction":
        top_chart_trans_amount('top_trans2')
        top_chart_trans_count('top_trans2')
    elif what_you_want=="7.Transaction Count of Aggregate User":
         Agg_user('agg_user2')    
    elif what_you_want=="8.Registereduser of Map User":
        map_registered_user('map_user2')
    elif what_you_want== "9.AppOpens of Map User":
        map_App_user('map_user2')
    elif what_you_want=="10.Registereduser of Top User":
        top_user('top_user2')
