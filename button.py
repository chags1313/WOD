# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:32:38 2022

@author: chags
"""
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import pandas as pd
from deta import Deta
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import itertools
from numpy import random

#set page config settings
st.set_page_config(layout="wide",
    page_title="DailyWOD",
    page_icon="weight_lifter")

#hide streamlit menu bar
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#calling database
deta = Deta("b02l5gt3_MFtTQuHFmWUEofyrn54FjjnWxAevcaY1")
wo_db = deta.Base("wodb")
db = deta.Base("fitusers")



#getting todays date
date = date.today()
#getting workouts
url = 'wods.csv'
wods = pd.read_csv(url)

#header colors
HEADER_COLOR_CYCLE = itertools.cycle(
    [
        "#00c0f2",  # light-blue-70",
        "#ffbd45",  # "orange-70",
        "#00d4b1",  # "blue-green-70",
        "#1c83e1",  # "blue-70",
        "#803df5",  # "violet-70",
        "#ff4b4b",  # "red-70",
        "#21c354",  # "green-70",
        "#faca2b",  # "yellow-80",
    ]
)
#underline header function
def colored_header(label, description=None, color=None):
    """Shows a header with a colored underline and an optional description."""
    st.write("")
    if color is None:
        color = next(HEADER_COLOR_CYCLE)
    st.subheader(label)
    st.write(
        f'<hr style="background-color: {color}; margin-top: 0; margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)

        
##### UI ######

#option menu
with st.sidebar:
    menu = option_menu(None, ["Account", "Dashboard", "Workouts", 'Max'], 
    icons=['person-lines-fill',  "house", 'table', 'graph-up', 'table'], 
    menu_icon="cast", default_index=1, orientation="vertical")
    
    
if menu == 'Account':
    st.header("Welcome to DailyWOD 🏋️‍")
    if 'auth_status' not in st.session_state:
      user_name = st.text_input("User Name")
      st.session_state.user_name = user_name
      st.session_state.password = st.text_input("Password",type = 'password')

      login_btn = st.button("Log In")
      if login_btn:
          result = db.fetch().items
          df = pd.DataFrame(result)
          user_check_df = df[df['user_name'] == st.session_state.user_name]
          user_check_df = user_check_df.reset_index()
          if  st.session_state.password == user_check_df['password'].max():
              st.session_state.auth_status = True
              db.put({"user_name": st.session_state.user_name, "password": st.session_state.password})
              st.success("Lookin good " + st.session_state.user_name, icon = '🤘')
          else:
              st.error("Incorrect password or user name. Please try again.")

      account_btn = st.button("Create Account")
      if account_btn:
          result1 = db.fetch().items
          df1 = pd.DataFrame(result1)
          user_check_df1 = df1[df1['user_name'] == st.session_state.user_name]
          if len(user_check_df1) < 1:
          
              db.put({"user_name": st.session_state.user_name, "password": st.session_state.password})
              st.info("Welcome " + st.session_state.user_name + " please proceed to login in with your new acount.")
          else:
              st.error("User Name Taken. If you already have an account, please enter your user name and select log in. If you are a new user, please enter a new user name.")
      forgot_password = st.button("Change Password")
      if forgot_password:
          st.info("Please reach out to Cole @ hagencolej@gmail.com")
    else:
      colored_header(st.session_state.user_name)
      affiliation = st.text_input("Gym Affiliation")
      dems1, dems2 = st.columns(2)
      with dems1:
        age = st.text_input("Age")
        sex = st.text_input("Sex")
      with dems2:
        weigh = st.text_input("Body Weight")
        height = st.text_input("Height")
      result1 = wo_db.fetch().items
      df1 = pd.DataFrame(result1)
      user_check_df1 = df1[df1['name'] == st.session_state.user_name]
      workouts1 = user_check_df1[user_check_df1['Movements'].str.len() > 1]
      weights1 = user_check_df1[user_check_df1['weight'] > 1]
      sid1, sid2 = st.columns(2)
      with sid1:
        colored_header("Workouts")
        st.dataframe(workouts1[['date', 'Workout', 'Performance']])
      with sid2:
        colored_header("Max PRs")
        st.dataframe(weights1[['date', 'lift', 'weight']])
      
    
if menu == 'Dashboard':
    if 'num' not in st.session_state:
        st.session_state.num = random.randint(len(wods))
    list_html = ""
    for cs in wods.columns.unique():
        wods[cs] = wods[cs].astype(str)
    for d in wods.columns.unique():
        if d == 'Workout':
            continue
        if wods[d].iloc[st.session_state.num]  == 'None':
            continue
        list_html += f"<div style='width: fit-content; " \
                     f"background: linear-gradient(246.65deg, #BDCDFF -17.53%, #D2F4D8 83.84%, #E0FFE7 104.88%); " \
                     f"color: #555D9D; letter-spacing: 0.2em; border-radius: 2rem; " \
                     f"padding: 0 1.5rem; margin-bottom: 0.5rem';>" \
                     f"{d}: {wods[d].iloc[st.session_state.num]} </div>" 
    
        
    full_html = f"""
                 <script>
                        document.head.innerHTML += 
                        '<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">'
                    </script>
                 <div style="font-family: 'Open Sans';">
                    <div style="color: white; margin-bottom: 1rem;"> 
                    {wods['Workout'].iloc[st.session_state.num]}
                    </div>
                    <div style="display: flex; flex-direction: column;">{list_html}</div>
                </div>
                """
    if 'user_name' not in st.session_state:
        HWOD = "Please sign in"
    else:
        HWOD = st.session_state.user_name

    cal_html = """
<html lang="en"><head>

  <meta charset="UTF-8">
  
  
<link rel="apple-touch-icon" type="image/png" href="https://cpwebassets.codepen.io/assets/favicon/apple-touch-icon-5ae1a0698dcc2402e9712f7d01ed509a57814f994c660df9f7a952f3060705ee.png">
<meta name="apple-mobile-web-app-title" content="CodePen">

<link rel="shortcut icon" type="image/x-icon" href="https://cpwebassets.codepen.io/assets/favicon/favicon-aec34940fbc1a6e787974dcd360f2c6b63348d4b1f4e06c77743096d55480f33.ico">

<link rel="mask-icon" type="image/x-icon" href="https://cpwebassets.codepen.io/assets/favicon/logo-pin-8f3771b1072e3c38bd662872f6b673a722f4b3ca2421637d5596661b4e2132cc.svg" color="#111">


  <title>CodePen - Circular Calendar Display</title>
  <link href="https://fonts.googleapis.com/css?family=Roboto+Mono" rel="stylesheet">
  
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">
  
<style>
#x1 {
  background: #FF3B30;
}

#x2 {
  background: #FF9500;
}

#x3 {
  background: #FFCC00;
}

#x4 {
  background: #4CD964;
}

#x5 {
  background: #5AC8FA;
}

#x6 {
  background: #007AFF;
}

#x7 {
  background: #5856D6;
}

.bar:nth-child(1) {
  position: absolute;
  top: 0px;
  left: 0px;
}

.bar:nth-child(2) {
  position: absolute;
  top: 0px;
  left: 20px;
}

.bar:nth-child(3) {
  position: absolute;
  top: 0px;
  left: 40px;
}

.bar:nth-child(4) {
  position: absolute;
  top: 0px;
  left: 60px;
}

.bar:nth-child(5) {
  position: absolute;
  top: 0px;
  left: 80px;
}

.bar:nth-child(6) {
  position: absolute;
  top: 0px;
  left: 100px;
}

.bar:nth-child(7) {
  position: absolute;
  top: 0px;
  left: 120px;
}

.day-dial, .month-dial, .day-name-dial {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
}

.head {
  position: relative;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
}

.day-text span, .day-preview span, .month-text span, .month-preview span, .day-name-text span, .day-name-preview span, .hand-container, .center-preview span {
  text-align: center;
  moz-transform-origin: center center;
  -o-transform-origin: center center;
  -ms-transform-origin: center center;
  -webkit-transform-origin: center center;
  transform-origin: center center;
}

* {
  box-sizing: border-box;
}

html,
body {
  background: #00000;
  border: 0;
  font-family: "Roboto Mono", monospace;
  height: 100%;
  margin: 0px;
  width: 100%;
}

h1 {
  color: #555;
  font-size: 25px;
}

h2 {
  color: #555;
  font-size: 15px;
}

.center-dial {
  position: absolute;
  top: calc(50% - 75px);
  left: calc(50% - 75px);
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
  width: 150px;
  height: 150px;
  background-color: #202020;
  border-radius: 50%;
  color: #000;
  box-shadow: 0px 2px 2px #000;
  cursor: pointer;
  overflow: hidden;
}

.center-preview span {
  position: absolute;
  top: 0%;
  left: calc(50% - 12.5px);
  height: 150px;
  width: 25px;
}

.center-preview {
  opacity: 0;
  filter: alpha(opacity=0);
}
.center-preview .char1 {
  -moz-transform: rotate(-40deg);
  -o-transform: rotate(-40deg);
  -ms-transform: rotate(-40deg);
  -webkit-transform: rotate(-40deg);
  transform: rotate(-40deg);
}
.center-preview .char2 {
  -moz-transform: rotate(-20deg);
  -o-transform: rotate(-20deg);
  -ms-transform: rotate(-20deg);
  -webkit-transform: rotate(-20deg);
  transform: rotate(-20deg);
}
.center-preview .char3 {
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}
.center-preview .char4 {
  -moz-transform: rotate(20deg);
  -o-transform: rotate(20deg);
  -ms-transform: rotate(20deg);
  -webkit-transform: rotate(20deg);
  transform: rotate(20deg);
}
.center-preview .char5 {
  -moz-transform: rotate(40deg);
  -o-transform: rotate(40deg);
  -ms-transform: rotate(40deg);
  -webkit-transform: rotate(40deg);
  transform: rotate(40deg);
}
.center-preview .char6 {
  -moz-transform: rotate(60deg);
  -o-transform: rotate(60deg);
  -ms-transform: rotate(60deg);
  -webkit-transform: rotate(60deg);
  transform: rotate(60deg);
}

.head {
  width: 50px;
  height: 50px;
  background: #FFF;
  border-radius: 50%;
}

.torso {
  position: relative;
  top: calc(50% - 20px);
  left: calc(50% - 50px);
  width: 100px;
  height: 100px;
  background: #FFF;
  border-radius: 50%;
}

.hand-container {
  position: absolute;
  top: 0%;
  left: calc(50% - 12.5px);
  opacity: 0;
  filter: alpha(opacity=0);
  width: 25px;
  height: 150px;
  moz-transform-origin: center center;
  -o-transform-origin: center center;
  -ms-transform-origin: center center;
  -webkit-transform-origin: center center;
  transform-origin: center center;
}

.hour-hand {
  width: 10px;
  height: 50px;
  position: relative;
  top: calc(50% - 45px);
  left: calc(50% - 5px);
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
  background: #FFF;
  border-radius: 5px;
}

.minute-hand {
  width: 10px;
  height: 70px;
  position: relative;
  top: calc(50% - 65px);
  left: calc(50% - 5px);
  background: #CCC;
  border-radius: 5px;
}

.second-hand {
  width: 2px;
  height: 70px;
  position: relative;
  top: calc(50% - 69px);
  left: calc(50% - 1px);
  background: #AAA;
  border-radius: 1px;
}

.day-name-dial {
  width: 250px;
  height: 250px;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
}

.day-name-preview span {
  position: absolute;
  top: calc(-25% - 5px);
  left: calc(50% - 12.5px);
  height: 250px;
  width: 25px;
}

.day-name-preview {
  opacity: 0;
  filter: alpha(opacity=0);
}
.day-name-preview .char1 {
  -moz-transform: rotate(-35deg);
  -o-transform: rotate(-35deg);
  -ms-transform: rotate(-35deg);
  -webkit-transform: rotate(-35deg);
  transform: rotate(-35deg);
}
.day-name-preview .char2 {
  -moz-transform: rotate(-25deg);
  -o-transform: rotate(-25deg);
  -ms-transform: rotate(-25deg);
  -webkit-transform: rotate(-25deg);
  transform: rotate(-25deg);
}
.day-name-preview .char3 {
  -moz-transform: rotate(-15deg);
  -o-transform: rotate(-15deg);
  -ms-transform: rotate(-15deg);
  -webkit-transform: rotate(-15deg);
  transform: rotate(-15deg);
}
.day-name-preview .char4 {
  -moz-transform: rotate(-5deg);
  -o-transform: rotate(-5deg);
  -ms-transform: rotate(-5deg);
  -webkit-transform: rotate(-5deg);
  transform: rotate(-5deg);
}
.day-name-preview .char5 {
  -moz-transform: rotate(5deg);
  -o-transform: rotate(5deg);
  -ms-transform: rotate(5deg);
  -webkit-transform: rotate(5deg);
  transform: rotate(5deg);
}
.day-name-preview .char6 {
  -moz-transform: rotate(15deg);
  -o-transform: rotate(15deg);
  -ms-transform: rotate(15deg);
  -webkit-transform: rotate(15deg);
  transform: rotate(15deg);
}
.day-name-preview .char7 {
  -moz-transform: rotate(25deg);
  -o-transform: rotate(25deg);
  -ms-transform: rotate(25deg);
  -webkit-transform: rotate(25deg);
  transform: rotate(25deg);
}
.day-name-preview .char8 {
  -moz-transform: rotate(35deg);
  -o-transform: rotate(35deg);
  -ms-transform: rotate(35deg);
  -webkit-transform: rotate(35deg);
  transform: rotate(35deg);
}
.day-name-preview .char9 {
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}

.day-name-text span {
  position: absolute;
  top: calc(-25% + 5px);
  left: calc(50% - 6px);
  height: 232px;
  width: 12px;
}

.day-name-text {
  opacity: 0;
  filter: alpha(opacity=0);
}
.day-name-text .char1 {
  -moz-transform: rotate(-125.3571428571deg);
  -o-transform: rotate(-125.3571428571deg);
  -ms-transform: rotate(-125.3571428571deg);
  -webkit-transform: rotate(-125.3571428571deg);
  transform: rotate(-125.3571428571deg);
}
.day-name-text .char2 {
  -moz-transform: rotate(-115.7142857143deg);
  -o-transform: rotate(-115.7142857143deg);
  -ms-transform: rotate(-115.7142857143deg);
  -webkit-transform: rotate(-115.7142857143deg);
  transform: rotate(-115.7142857143deg);
}
.day-name-text .char3 {
  -moz-transform: rotate(-106.0714285714deg);
  -o-transform: rotate(-106.0714285714deg);
  -ms-transform: rotate(-106.0714285714deg);
  -webkit-transform: rotate(-106.0714285714deg);
  transform: rotate(-106.0714285714deg);
}
.day-name-text .char4 {
  -moz-transform: rotate(-96.4285714286deg);
  -o-transform: rotate(-96.4285714286deg);
  -ms-transform: rotate(-96.4285714286deg);
  -webkit-transform: rotate(-96.4285714286deg);
  transform: rotate(-96.4285714286deg);
}
.day-name-text .char5 {
  -moz-transform: rotate(-86.7857142857deg);
  -o-transform: rotate(-86.7857142857deg);
  -ms-transform: rotate(-86.7857142857deg);
  -webkit-transform: rotate(-86.7857142857deg);
  transform: rotate(-86.7857142857deg);
}
.day-name-text .char6 {
  -moz-transform: rotate(-77.1428571429deg);
  -o-transform: rotate(-77.1428571429deg);
  -ms-transform: rotate(-77.1428571429deg);
  -webkit-transform: rotate(-77.1428571429deg);
  transform: rotate(-77.1428571429deg);
}
.day-name-text .char7 {
  -moz-transform: rotate(-67.5deg);
  -o-transform: rotate(-67.5deg);
  -ms-transform: rotate(-67.5deg);
  -webkit-transform: rotate(-67.5deg);
  transform: rotate(-67.5deg);
}
.day-name-text .char8 {
  -moz-transform: rotate(-57.8571428571deg);
  -o-transform: rotate(-57.8571428571deg);
  -ms-transform: rotate(-57.8571428571deg);
  -webkit-transform: rotate(-57.8571428571deg);
  transform: rotate(-57.8571428571deg);
}
.day-name-text .char9 {
  -moz-transform: rotate(-48.2142857143deg);
  -o-transform: rotate(-48.2142857143deg);
  -ms-transform: rotate(-48.2142857143deg);
  -webkit-transform: rotate(-48.2142857143deg);
  transform: rotate(-48.2142857143deg);
}
.day-name-text .char10 {
  -moz-transform: rotate(-38.5714285714deg);
  -o-transform: rotate(-38.5714285714deg);
  -ms-transform: rotate(-38.5714285714deg);
  -webkit-transform: rotate(-38.5714285714deg);
  transform: rotate(-38.5714285714deg);
}
.day-name-text .char11 {
  -moz-transform: rotate(-28.9285714286deg);
  -o-transform: rotate(-28.9285714286deg);
  -ms-transform: rotate(-28.9285714286deg);
  -webkit-transform: rotate(-28.9285714286deg);
  transform: rotate(-28.9285714286deg);
}
.day-name-text .char12 {
  -moz-transform: rotate(-19.2857142857deg);
  -o-transform: rotate(-19.2857142857deg);
  -ms-transform: rotate(-19.2857142857deg);
  -webkit-transform: rotate(-19.2857142857deg);
  transform: rotate(-19.2857142857deg);
}
.day-name-text .char13 {
  -moz-transform: rotate(-9.6428571429deg);
  -o-transform: rotate(-9.6428571429deg);
  -ms-transform: rotate(-9.6428571429deg);
  -webkit-transform: rotate(-9.6428571429deg);
  transform: rotate(-9.6428571429deg);
}
.day-name-text .char14 {
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}
.day-name-text .char15 {
  -moz-transform: rotate(9.6428571429deg);
  -o-transform: rotate(9.6428571429deg);
  -ms-transform: rotate(9.6428571429deg);
  -webkit-transform: rotate(9.6428571429deg);
  transform: rotate(9.6428571429deg);
}
.day-name-text .char16 {
  -moz-transform: rotate(19.2857142857deg);
  -o-transform: rotate(19.2857142857deg);
  -ms-transform: rotate(19.2857142857deg);
  -webkit-transform: rotate(19.2857142857deg);
  transform: rotate(19.2857142857deg);
}
.day-name-text .char17 {
  -moz-transform: rotate(28.9285714286deg);
  -o-transform: rotate(28.9285714286deg);
  -ms-transform: rotate(28.9285714286deg);
  -webkit-transform: rotate(28.9285714286deg);
  transform: rotate(28.9285714286deg);
}
.day-name-text .char18 {
  -moz-transform: rotate(38.5714285714deg);
  -o-transform: rotate(38.5714285714deg);
  -ms-transform: rotate(38.5714285714deg);
  -webkit-transform: rotate(38.5714285714deg);
  transform: rotate(38.5714285714deg);
}
.day-name-text .char19 {
  -moz-transform: rotate(48.2142857143deg);
  -o-transform: rotate(48.2142857143deg);
  -ms-transform: rotate(48.2142857143deg);
  -webkit-transform: rotate(48.2142857143deg);
  transform: rotate(48.2142857143deg);
}
.day-name-text .char20 {
  -moz-transform: rotate(57.8571428571deg);
  -o-transform: rotate(57.8571428571deg);
  -ms-transform: rotate(57.8571428571deg);
  -webkit-transform: rotate(57.8571428571deg);
  transform: rotate(57.8571428571deg);
}
.day-name-text .char21 {
  -moz-transform: rotate(67.5deg);
  -o-transform: rotate(67.5deg);
  -ms-transform: rotate(67.5deg);
  -webkit-transform: rotate(67.5deg);
  transform: rotate(67.5deg);
}
.day-name-text .char22 {
  -moz-transform: rotate(77.1428571429deg);
  -o-transform: rotate(77.1428571429deg);
  -ms-transform: rotate(77.1428571429deg);
  -webkit-transform: rotate(77.1428571429deg);
  transform: rotate(77.1428571429deg);
}
.day-name-text .char23 {
  -moz-transform: rotate(86.7857142857deg);
  -o-transform: rotate(86.7857142857deg);
  -ms-transform: rotate(86.7857142857deg);
  -webkit-transform: rotate(86.7857142857deg);
  transform: rotate(86.7857142857deg);
}
.day-name-text .char24 {
  -moz-transform: rotate(96.4285714286deg);
  -o-transform: rotate(96.4285714286deg);
  -ms-transform: rotate(96.4285714286deg);
  -webkit-transform: rotate(96.4285714286deg);
  transform: rotate(96.4285714286deg);
}
.day-name-text .char25 {
  -moz-transform: rotate(106.0714285714deg);
  -o-transform: rotate(106.0714285714deg);
  -ms-transform: rotate(106.0714285714deg);
  -webkit-transform: rotate(106.0714285714deg);
  transform: rotate(106.0714285714deg);
}
.day-name-text .char26 {
  -moz-transform: rotate(115.7142857143deg);
  -o-transform: rotate(115.7142857143deg);
  -ms-transform: rotate(115.7142857143deg);
  -webkit-transform: rotate(115.7142857143deg);
  transform: rotate(115.7142857143deg);
}
.day-name-text .char27 {
  -moz-transform: rotate(125.3571428571deg);
  -o-transform: rotate(125.3571428571deg);
  -ms-transform: rotate(125.3571428571deg);
  -webkit-transform: rotate(125.3571428571deg);
  transform: rotate(125.3571428571deg);
}
.day-name-text .char28 {
  -moz-transform: rotate(135deg);
  -o-transform: rotate(135deg);
  -ms-transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
  transform: rotate(135deg);
}

.month-dial {
  width: 350px;
  height: 350px;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
}

.month-preview span {
  position: absolute;
  top: calc(-25% + 20px);
  left: calc(50% - 12.5px);
  height: 350px;
  width: 25px;
}

.month-preview {
  opacity: 0;
  filter: alpha(opacity=0);
}
.month-preview .char1 {
  -moz-transform: rotate(-30deg);
  -o-transform: rotate(-30deg);
  -ms-transform: rotate(-30deg);
  -webkit-transform: rotate(-30deg);
  transform: rotate(-30deg);
}
.month-preview .char2 {
  -moz-transform: rotate(-15deg);
  -o-transform: rotate(-15deg);
  -ms-transform: rotate(-15deg);
  -webkit-transform: rotate(-15deg);
  transform: rotate(-15deg);
}
.month-preview .char3 {
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}
.month-preview .char4 {
  -moz-transform: rotate(15deg);
  -o-transform: rotate(15deg);
  -ms-transform: rotate(15deg);
  -webkit-transform: rotate(15deg);
  transform: rotate(15deg);
}
.month-preview .char5 {
  -moz-transform: rotate(30deg);
  -o-transform: rotate(30deg);
  -ms-transform: rotate(30deg);
  -webkit-transform: rotate(30deg);
  transform: rotate(30deg);
}
.month-preview .char6 {
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}

.month-text span {
  position: absolute;
  top: calc(-25% + 30px);
  left: calc(50% - 6px);
  height: 332px;
  width: 12px;
}

.month-text {
  opacity: 0;
  filter: alpha(opacity=0);
}
.month-text .char1 {
  -moz-transform: rotate(-129.375deg);
  -o-transform: rotate(-129.375deg);
  -ms-transform: rotate(-129.375deg);
  -webkit-transform: rotate(-129.375deg);
  transform: rotate(-129.375deg);
}
.month-text .char2 {
  -moz-transform: rotate(-123.75deg);
  -o-transform: rotate(-123.75deg);
  -ms-transform: rotate(-123.75deg);
  -webkit-transform: rotate(-123.75deg);
  transform: rotate(-123.75deg);
}
.month-text .char3 {
  -moz-transform: rotate(-118.125deg);
  -o-transform: rotate(-118.125deg);
  -ms-transform: rotate(-118.125deg);
  -webkit-transform: rotate(-118.125deg);
  transform: rotate(-118.125deg);
}
.month-text .char4 {
  -moz-transform: rotate(-112.5deg);
  -o-transform: rotate(-112.5deg);
  -ms-transform: rotate(-112.5deg);
  -webkit-transform: rotate(-112.5deg);
  transform: rotate(-112.5deg);
}
.month-text .char5 {
  -moz-transform: rotate(-106.875deg);
  -o-transform: rotate(-106.875deg);
  -ms-transform: rotate(-106.875deg);
  -webkit-transform: rotate(-106.875deg);
  transform: rotate(-106.875deg);
}
.month-text .char6 {
  -moz-transform: rotate(-101.25deg);
  -o-transform: rotate(-101.25deg);
  -ms-transform: rotate(-101.25deg);
  -webkit-transform: rotate(-101.25deg);
  transform: rotate(-101.25deg);
}
.month-text .char7 {
  -moz-transform: rotate(-95.625deg);
  -o-transform: rotate(-95.625deg);
  -ms-transform: rotate(-95.625deg);
  -webkit-transform: rotate(-95.625deg);
  transform: rotate(-95.625deg);
}
.month-text .char8 {
  -moz-transform: rotate(-90deg);
  -o-transform: rotate(-90deg);
  -ms-transform: rotate(-90deg);
  -webkit-transform: rotate(-90deg);
  transform: rotate(-90deg);
}
.month-text .char9 {
  -moz-transform: rotate(-84.375deg);
  -o-transform: rotate(-84.375deg);
  -ms-transform: rotate(-84.375deg);
  -webkit-transform: rotate(-84.375deg);
  transform: rotate(-84.375deg);
}
.month-text .char10 {
  -moz-transform: rotate(-78.75deg);
  -o-transform: rotate(-78.75deg);
  -ms-transform: rotate(-78.75deg);
  -webkit-transform: rotate(-78.75deg);
  transform: rotate(-78.75deg);
}
.month-text .char11 {
  -moz-transform: rotate(-73.125deg);
  -o-transform: rotate(-73.125deg);
  -ms-transform: rotate(-73.125deg);
  -webkit-transform: rotate(-73.125deg);
  transform: rotate(-73.125deg);
}
.month-text .char12 {
  -moz-transform: rotate(-67.5deg);
  -o-transform: rotate(-67.5deg);
  -ms-transform: rotate(-67.5deg);
  -webkit-transform: rotate(-67.5deg);
  transform: rotate(-67.5deg);
}
.month-text .char13 {
  -moz-transform: rotate(-61.875deg);
  -o-transform: rotate(-61.875deg);
  -ms-transform: rotate(-61.875deg);
  -webkit-transform: rotate(-61.875deg);
  transform: rotate(-61.875deg);
}
.month-text .char14 {
  -moz-transform: rotate(-56.25deg);
  -o-transform: rotate(-56.25deg);
  -ms-transform: rotate(-56.25deg);
  -webkit-transform: rotate(-56.25deg);
  transform: rotate(-56.25deg);
}
.month-text .char15 {
  -moz-transform: rotate(-50.625deg);
  -o-transform: rotate(-50.625deg);
  -ms-transform: rotate(-50.625deg);
  -webkit-transform: rotate(-50.625deg);
  transform: rotate(-50.625deg);
}
.month-text .char16 {
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
  transform: rotate(-45deg);
}
.month-text .char17 {
  -moz-transform: rotate(-39.375deg);
  -o-transform: rotate(-39.375deg);
  -ms-transform: rotate(-39.375deg);
  -webkit-transform: rotate(-39.375deg);
  transform: rotate(-39.375deg);
}
.month-text .char18 {
  -moz-transform: rotate(-33.75deg);
  -o-transform: rotate(-33.75deg);
  -ms-transform: rotate(-33.75deg);
  -webkit-transform: rotate(-33.75deg);
  transform: rotate(-33.75deg);
}
.month-text .char19 {
  -moz-transform: rotate(-28.125deg);
  -o-transform: rotate(-28.125deg);
  -ms-transform: rotate(-28.125deg);
  -webkit-transform: rotate(-28.125deg);
  transform: rotate(-28.125deg);
}
.month-text .char20 {
  -moz-transform: rotate(-22.5deg);
  -o-transform: rotate(-22.5deg);
  -ms-transform: rotate(-22.5deg);
  -webkit-transform: rotate(-22.5deg);
  transform: rotate(-22.5deg);
}
.month-text .char21 {
  -moz-transform: rotate(-16.875deg);
  -o-transform: rotate(-16.875deg);
  -ms-transform: rotate(-16.875deg);
  -webkit-transform: rotate(-16.875deg);
  transform: rotate(-16.875deg);
}
.month-text .char22 {
  -moz-transform: rotate(-11.25deg);
  -o-transform: rotate(-11.25deg);
  -ms-transform: rotate(-11.25deg);
  -webkit-transform: rotate(-11.25deg);
  transform: rotate(-11.25deg);
}
.month-text .char23 {
  -moz-transform: rotate(-5.625deg);
  -o-transform: rotate(-5.625deg);
  -ms-transform: rotate(-5.625deg);
  -webkit-transform: rotate(-5.625deg);
  transform: rotate(-5.625deg);
}
.month-text .char24 {
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}
.month-text .char25 {
  -moz-transform: rotate(5.625deg);
  -o-transform: rotate(5.625deg);
  -ms-transform: rotate(5.625deg);
  -webkit-transform: rotate(5.625deg);
  transform: rotate(5.625deg);
}
.month-text .char26 {
  -moz-transform: rotate(11.25deg);
  -o-transform: rotate(11.25deg);
  -ms-transform: rotate(11.25deg);
  -webkit-transform: rotate(11.25deg);
  transform: rotate(11.25deg);
}
.month-text .char27 {
  -moz-transform: rotate(16.875deg);
  -o-transform: rotate(16.875deg);
  -ms-transform: rotate(16.875deg);
  -webkit-transform: rotate(16.875deg);
  transform: rotate(16.875deg);
}
.month-text .char28 {
  -moz-transform: rotate(22.5deg);
  -o-transform: rotate(22.5deg);
  -ms-transform: rotate(22.5deg);
  -webkit-transform: rotate(22.5deg);
  transform: rotate(22.5deg);
}
.month-text .char29 {
  -moz-transform: rotate(28.125deg);
  -o-transform: rotate(28.125deg);
  -ms-transform: rotate(28.125deg);
  -webkit-transform: rotate(28.125deg);
  transform: rotate(28.125deg);
}
.month-text .char30 {
  -moz-transform: rotate(33.75deg);
  -o-transform: rotate(33.75deg);
  -ms-transform: rotate(33.75deg);
  -webkit-transform: rotate(33.75deg);
  transform: rotate(33.75deg);
}
.month-text .char31 {
  -moz-transform: rotate(39.375deg);
  -o-transform: rotate(39.375deg);
  -ms-transform: rotate(39.375deg);
  -webkit-transform: rotate(39.375deg);
  transform: rotate(39.375deg);
}
.month-text .char32 {
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}
.month-text .char33 {
  -moz-transform: rotate(50.625deg);
  -o-transform: rotate(50.625deg);
  -ms-transform: rotate(50.625deg);
  -webkit-transform: rotate(50.625deg);
  transform: rotate(50.625deg);
}
.month-text .char34 {
  -moz-transform: rotate(56.25deg);
  -o-transform: rotate(56.25deg);
  -ms-transform: rotate(56.25deg);
  -webkit-transform: rotate(56.25deg);
  transform: rotate(56.25deg);
}
.month-text .char35 {
  -moz-transform: rotate(61.875deg);
  -o-transform: rotate(61.875deg);
  -ms-transform: rotate(61.875deg);
  -webkit-transform: rotate(61.875deg);
  transform: rotate(61.875deg);
}
.month-text .char36 {
  -moz-transform: rotate(67.5deg);
  -o-transform: rotate(67.5deg);
  -ms-transform: rotate(67.5deg);
  -webkit-transform: rotate(67.5deg);
  transform: rotate(67.5deg);
}
.month-text .char37 {
  -moz-transform: rotate(73.125deg);
  -o-transform: rotate(73.125deg);
  -ms-transform: rotate(73.125deg);
  -webkit-transform: rotate(73.125deg);
  transform: rotate(73.125deg);
}
.month-text .char38 {
  -moz-transform: rotate(78.75deg);
  -o-transform: rotate(78.75deg);
  -ms-transform: rotate(78.75deg);
  -webkit-transform: rotate(78.75deg);
  transform: rotate(78.75deg);
}
.month-text .char39 {
  -moz-transform: rotate(84.375deg);
  -o-transform: rotate(84.375deg);
  -ms-transform: rotate(84.375deg);
  -webkit-transform: rotate(84.375deg);
  transform: rotate(84.375deg);
}
.month-text .char40 {
  -moz-transform: rotate(90deg);
  -o-transform: rotate(90deg);
  -ms-transform: rotate(90deg);
  -webkit-transform: rotate(90deg);
  transform: rotate(90deg);
}
.month-text .char41 {
  -moz-transform: rotate(95.625deg);
  -o-transform: rotate(95.625deg);
  -ms-transform: rotate(95.625deg);
  -webkit-transform: rotate(95.625deg);
  transform: rotate(95.625deg);
}
.month-text .char42 {
  -moz-transform: rotate(101.25deg);
  -o-transform: rotate(101.25deg);
  -ms-transform: rotate(101.25deg);
  -webkit-transform: rotate(101.25deg);
  transform: rotate(101.25deg);
}
.month-text .char43 {
  -moz-transform: rotate(106.875deg);
  -o-transform: rotate(106.875deg);
  -ms-transform: rotate(106.875deg);
  -webkit-transform: rotate(106.875deg);
  transform: rotate(106.875deg);
}
.month-text .char44 {
  -moz-transform: rotate(112.5deg);
  -o-transform: rotate(112.5deg);
  -ms-transform: rotate(112.5deg);
  -webkit-transform: rotate(112.5deg);
  transform: rotate(112.5deg);
}
.month-text .char45 {
  -moz-transform: rotate(118.125deg);
  -o-transform: rotate(118.125deg);
  -ms-transform: rotate(118.125deg);
  -webkit-transform: rotate(118.125deg);
  transform: rotate(118.125deg);
}
.month-text .char46 {
  -moz-transform: rotate(123.75deg);
  -o-transform: rotate(123.75deg);
  -ms-transform: rotate(123.75deg);
  -webkit-transform: rotate(123.75deg);
  transform: rotate(123.75deg);
}
.month-text .char47 {
  -moz-transform: rotate(129.375deg);
  -o-transform: rotate(129.375deg);
  -ms-transform: rotate(129.375deg);
  -webkit-transform: rotate(129.375deg);
  transform: rotate(129.375deg);
}
.month-text .char48 {
  -moz-transform: rotate(135deg);
  -o-transform: rotate(135deg);
  -ms-transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
  transform: rotate(135deg);
}

.day-dial {
  width: 450px;
  height: 450px;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
}

.day-preview span {
  position: absolute;
  top: calc(-25% + 45px);
  left: calc(50% - 12.5px);
  height: 450px;
  width: 25px;
}

.day-preview {
  opacity: 0;
  filter: alpha(opacity=0);
}
.day-preview .char1 {
  -moz-transform: rotate(-22.5deg);
  -o-transform: rotate(-22.5deg);
  -ms-transform: rotate(-22.5deg);
  -webkit-transform: rotate(-22.5deg);
  transform: rotate(-22.5deg);
}
.day-preview .char2 {
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}
.day-preview .char3 {
  -moz-transform: rotate(22.5deg);
  -o-transform: rotate(22.5deg);
  -ms-transform: rotate(22.5deg);
  -webkit-transform: rotate(22.5deg);
  transform: rotate(22.5deg);
}
.day-preview .char4 {
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}

.day-text span {
  position: absolute;
  top: calc(-25% + 55px);
  left: calc(50% - 6px);
  height: 432px;
  width: 12px;
}

.day-text {
  opacity: 0;
  filter: alpha(opacity=0);
}
.day-text .char1 {
  -moz-transform: rotate(-132.0967741935deg);
  -o-transform: rotate(-132.0967741935deg);
  -ms-transform: rotate(-132.0967741935deg);
  -webkit-transform: rotate(-132.0967741935deg);
  transform: rotate(-132.0967741935deg);
}
.day-text .char2 {
  -moz-transform: rotate(-129.1935483871deg);
  -o-transform: rotate(-129.1935483871deg);
  -ms-transform: rotate(-129.1935483871deg);
  -webkit-transform: rotate(-129.1935483871deg);
  transform: rotate(-129.1935483871deg);
}
.day-text .char3 {
  -moz-transform: rotate(-126.2903225806deg);
  -o-transform: rotate(-126.2903225806deg);
  -ms-transform: rotate(-126.2903225806deg);
  -webkit-transform: rotate(-126.2903225806deg);
  transform: rotate(-126.2903225806deg);
}
.day-text .char4 {
  -moz-transform: rotate(-123.3870967742deg);
  -o-transform: rotate(-123.3870967742deg);
  -ms-transform: rotate(-123.3870967742deg);
  -webkit-transform: rotate(-123.3870967742deg);
  transform: rotate(-123.3870967742deg);
}
.day-text .char5 {
  -moz-transform: rotate(-120.4838709677deg);
  -o-transform: rotate(-120.4838709677deg);
  -ms-transform: rotate(-120.4838709677deg);
  -webkit-transform: rotate(-120.4838709677deg);
  transform: rotate(-120.4838709677deg);
}
.day-text .char6 {
  -moz-transform: rotate(-117.5806451613deg);
  -o-transform: rotate(-117.5806451613deg);
  -ms-transform: rotate(-117.5806451613deg);
  -webkit-transform: rotate(-117.5806451613deg);
  transform: rotate(-117.5806451613deg);
}
.day-text .char7 {
  -moz-transform: rotate(-114.6774193548deg);
  -o-transform: rotate(-114.6774193548deg);
  -ms-transform: rotate(-114.6774193548deg);
  -webkit-transform: rotate(-114.6774193548deg);
  transform: rotate(-114.6774193548deg);
}
.day-text .char8 {
  -moz-transform: rotate(-111.7741935484deg);
  -o-transform: rotate(-111.7741935484deg);
  -ms-transform: rotate(-111.7741935484deg);
  -webkit-transform: rotate(-111.7741935484deg);
  transform: rotate(-111.7741935484deg);
}
.day-text .char9 {
  -moz-transform: rotate(-108.8709677419deg);
  -o-transform: rotate(-108.8709677419deg);
  -ms-transform: rotate(-108.8709677419deg);
  -webkit-transform: rotate(-108.8709677419deg);
  transform: rotate(-108.8709677419deg);
}
.day-text .char10 {
  -moz-transform: rotate(-105.9677419355deg);
  -o-transform: rotate(-105.9677419355deg);
  -ms-transform: rotate(-105.9677419355deg);
  -webkit-transform: rotate(-105.9677419355deg);
  transform: rotate(-105.9677419355deg);
}
.day-text .char11 {
  -moz-transform: rotate(-103.064516129deg);
  -o-transform: rotate(-103.064516129deg);
  -ms-transform: rotate(-103.064516129deg);
  -webkit-transform: rotate(-103.064516129deg);
  transform: rotate(-103.064516129deg);
}
.day-text .char12 {
  -moz-transform: rotate(-100.1612903226deg);
  -o-transform: rotate(-100.1612903226deg);
  -ms-transform: rotate(-100.1612903226deg);
  -webkit-transform: rotate(-100.1612903226deg);
  transform: rotate(-100.1612903226deg);
}
.day-text .char13 {
  -moz-transform: rotate(-97.2580645161deg);
  -o-transform: rotate(-97.2580645161deg);
  -ms-transform: rotate(-97.2580645161deg);
  -webkit-transform: rotate(-97.2580645161deg);
  transform: rotate(-97.2580645161deg);
}
.day-text .char14 {
  -moz-transform: rotate(-94.3548387097deg);
  -o-transform: rotate(-94.3548387097deg);
  -ms-transform: rotate(-94.3548387097deg);
  -webkit-transform: rotate(-94.3548387097deg);
  transform: rotate(-94.3548387097deg);
}
.day-text .char15 {
  -moz-transform: rotate(-91.4516129032deg);
  -o-transform: rotate(-91.4516129032deg);
  -ms-transform: rotate(-91.4516129032deg);
  -webkit-transform: rotate(-91.4516129032deg);
  transform: rotate(-91.4516129032deg);
}
.day-text .char16 {
  -moz-transform: rotate(-88.5483870968deg);
  -o-transform: rotate(-88.5483870968deg);
  -ms-transform: rotate(-88.5483870968deg);
  -webkit-transform: rotate(-88.5483870968deg);
  transform: rotate(-88.5483870968deg);
}
.day-text .char17 {
  -moz-transform: rotate(-85.6451612903deg);
  -o-transform: rotate(-85.6451612903deg);
  -ms-transform: rotate(-85.6451612903deg);
  -webkit-transform: rotate(-85.6451612903deg);
  transform: rotate(-85.6451612903deg);
}
.day-text .char18 {
  -moz-transform: rotate(-82.7419354839deg);
  -o-transform: rotate(-82.7419354839deg);
  -ms-transform: rotate(-82.7419354839deg);
  -webkit-transform: rotate(-82.7419354839deg);
  transform: rotate(-82.7419354839deg);
}
.day-text .char19 {
  -moz-transform: rotate(-79.8387096774deg);
  -o-transform: rotate(-79.8387096774deg);
  -ms-transform: rotate(-79.8387096774deg);
  -webkit-transform: rotate(-79.8387096774deg);
  transform: rotate(-79.8387096774deg);
}
.day-text .char20 {
  -moz-transform: rotate(-76.935483871deg);
  -o-transform: rotate(-76.935483871deg);
  -ms-transform: rotate(-76.935483871deg);
  -webkit-transform: rotate(-76.935483871deg);
  transform: rotate(-76.935483871deg);
}
.day-text .char21 {
  -moz-transform: rotate(-74.0322580645deg);
  -o-transform: rotate(-74.0322580645deg);
  -ms-transform: rotate(-74.0322580645deg);
  -webkit-transform: rotate(-74.0322580645deg);
  transform: rotate(-74.0322580645deg);
}
.day-text .char22 {
  -moz-transform: rotate(-71.1290322581deg);
  -o-transform: rotate(-71.1290322581deg);
  -ms-transform: rotate(-71.1290322581deg);
  -webkit-transform: rotate(-71.1290322581deg);
  transform: rotate(-71.1290322581deg);
}
.day-text .char23 {
  -moz-transform: rotate(-68.2258064516deg);
  -o-transform: rotate(-68.2258064516deg);
  -ms-transform: rotate(-68.2258064516deg);
  -webkit-transform: rotate(-68.2258064516deg);
  transform: rotate(-68.2258064516deg);
}
.day-text .char24 {
  -moz-transform: rotate(-65.3225806452deg);
  -o-transform: rotate(-65.3225806452deg);
  -ms-transform: rotate(-65.3225806452deg);
  -webkit-transform: rotate(-65.3225806452deg);
  transform: rotate(-65.3225806452deg);
}
.day-text .char25 {
  -moz-transform: rotate(-62.4193548387deg);
  -o-transform: rotate(-62.4193548387deg);
  -ms-transform: rotate(-62.4193548387deg);
  -webkit-transform: rotate(-62.4193548387deg);
  transform: rotate(-62.4193548387deg);
}
.day-text .char26 {
  -moz-transform: rotate(-59.5161290323deg);
  -o-transform: rotate(-59.5161290323deg);
  -ms-transform: rotate(-59.5161290323deg);
  -webkit-transform: rotate(-59.5161290323deg);
  transform: rotate(-59.5161290323deg);
}
.day-text .char27 {
  -moz-transform: rotate(-56.6129032258deg);
  -o-transform: rotate(-56.6129032258deg);
  -ms-transform: rotate(-56.6129032258deg);
  -webkit-transform: rotate(-56.6129032258deg);
  transform: rotate(-56.6129032258deg);
}
.day-text .char28 {
  -moz-transform: rotate(-53.7096774194deg);
  -o-transform: rotate(-53.7096774194deg);
  -ms-transform: rotate(-53.7096774194deg);
  -webkit-transform: rotate(-53.7096774194deg);
  transform: rotate(-53.7096774194deg);
}
.day-text .char29 {
  -moz-transform: rotate(-50.8064516129deg);
  -o-transform: rotate(-50.8064516129deg);
  -ms-transform: rotate(-50.8064516129deg);
  -webkit-transform: rotate(-50.8064516129deg);
  transform: rotate(-50.8064516129deg);
}
.day-text .char30 {
  -moz-transform: rotate(-47.9032258065deg);
  -o-transform: rotate(-47.9032258065deg);
  -ms-transform: rotate(-47.9032258065deg);
  -webkit-transform: rotate(-47.9032258065deg);
  transform: rotate(-47.9032258065deg);
}
.day-text .char31 {
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
  transform: rotate(-45deg);
}
.day-text .char32 {
  -moz-transform: rotate(-42.0967741935deg);
  -o-transform: rotate(-42.0967741935deg);
  -ms-transform: rotate(-42.0967741935deg);
  -webkit-transform: rotate(-42.0967741935deg);
  transform: rotate(-42.0967741935deg);
}
.day-text .char33 {
  -moz-transform: rotate(-39.1935483871deg);
  -o-transform: rotate(-39.1935483871deg);
  -ms-transform: rotate(-39.1935483871deg);
  -webkit-transform: rotate(-39.1935483871deg);
  transform: rotate(-39.1935483871deg);
}
.day-text .char34 {
  -moz-transform: rotate(-36.2903225806deg);
  -o-transform: rotate(-36.2903225806deg);
  -ms-transform: rotate(-36.2903225806deg);
  -webkit-transform: rotate(-36.2903225806deg);
  transform: rotate(-36.2903225806deg);
}
.day-text .char35 {
  -moz-transform: rotate(-33.3870967742deg);
  -o-transform: rotate(-33.3870967742deg);
  -ms-transform: rotate(-33.3870967742deg);
  -webkit-transform: rotate(-33.3870967742deg);
  transform: rotate(-33.3870967742deg);
}
.day-text .char36 {
  -moz-transform: rotate(-30.4838709677deg);
  -o-transform: rotate(-30.4838709677deg);
  -ms-transform: rotate(-30.4838709677deg);
  -webkit-transform: rotate(-30.4838709677deg);
  transform: rotate(-30.4838709677deg);
}
.day-text .char37 {
  -moz-transform: rotate(-27.5806451613deg);
  -o-transform: rotate(-27.5806451613deg);
  -ms-transform: rotate(-27.5806451613deg);
  -webkit-transform: rotate(-27.5806451613deg);
  transform: rotate(-27.5806451613deg);
}
.day-text .char38 {
  -moz-transform: rotate(-24.6774193548deg);
  -o-transform: rotate(-24.6774193548deg);
  -ms-transform: rotate(-24.6774193548deg);
  -webkit-transform: rotate(-24.6774193548deg);
  transform: rotate(-24.6774193548deg);
}
.day-text .char39 {
  -moz-transform: rotate(-21.7741935484deg);
  -o-transform: rotate(-21.7741935484deg);
  -ms-transform: rotate(-21.7741935484deg);
  -webkit-transform: rotate(-21.7741935484deg);
  transform: rotate(-21.7741935484deg);
}
.day-text .char40 {
  -moz-transform: rotate(-18.8709677419deg);
  -o-transform: rotate(-18.8709677419deg);
  -ms-transform: rotate(-18.8709677419deg);
  -webkit-transform: rotate(-18.8709677419deg);
  transform: rotate(-18.8709677419deg);
}
.day-text .char41 {
  -moz-transform: rotate(-15.9677419355deg);
  -o-transform: rotate(-15.9677419355deg);
  -ms-transform: rotate(-15.9677419355deg);
  -webkit-transform: rotate(-15.9677419355deg);
  transform: rotate(-15.9677419355deg);
}
.day-text .char42 {
  -moz-transform: rotate(-13.064516129deg);
  -o-transform: rotate(-13.064516129deg);
  -ms-transform: rotate(-13.064516129deg);
  -webkit-transform: rotate(-13.064516129deg);
  transform: rotate(-13.064516129deg);
}
.day-text .char43 {
  -moz-transform: rotate(-10.1612903226deg);
  -o-transform: rotate(-10.1612903226deg);
  -ms-transform: rotate(-10.1612903226deg);
  -webkit-transform: rotate(-10.1612903226deg);
  transform: rotate(-10.1612903226deg);
}
.day-text .char44 {
  -moz-transform: rotate(-7.2580645161deg);
  -o-transform: rotate(-7.2580645161deg);
  -ms-transform: rotate(-7.2580645161deg);
  -webkit-transform: rotate(-7.2580645161deg);
  transform: rotate(-7.2580645161deg);
}
.day-text .char45 {
  -moz-transform: rotate(-4.3548387097deg);
  -o-transform: rotate(-4.3548387097deg);
  -ms-transform: rotate(-4.3548387097deg);
  -webkit-transform: rotate(-4.3548387097deg);
  transform: rotate(-4.3548387097deg);
}
.day-text .char46 {
  -moz-transform: rotate(-1.4516129032deg);
  -o-transform: rotate(-1.4516129032deg);
  -ms-transform: rotate(-1.4516129032deg);
  -webkit-transform: rotate(-1.4516129032deg);
  transform: rotate(-1.4516129032deg);
}
.day-text .char47 {
  -moz-transform: rotate(1.4516129032deg);
  -o-transform: rotate(1.4516129032deg);
  -ms-transform: rotate(1.4516129032deg);
  -webkit-transform: rotate(1.4516129032deg);
  transform: rotate(1.4516129032deg);
}
.day-text .char48 {
  -moz-transform: rotate(4.3548387097deg);
  -o-transform: rotate(4.3548387097deg);
  -ms-transform: rotate(4.3548387097deg);
  -webkit-transform: rotate(4.3548387097deg);
  transform: rotate(4.3548387097deg);
}
.day-text .char49 {
  -moz-transform: rotate(7.2580645161deg);
  -o-transform: rotate(7.2580645161deg);
  -ms-transform: rotate(7.2580645161deg);
  -webkit-transform: rotate(7.2580645161deg);
  transform: rotate(7.2580645161deg);
}
.day-text .char50 {
  -moz-transform: rotate(10.1612903226deg);
  -o-transform: rotate(10.1612903226deg);
  -ms-transform: rotate(10.1612903226deg);
  -webkit-transform: rotate(10.1612903226deg);
  transform: rotate(10.1612903226deg);
}
.day-text .char51 {
  -moz-transform: rotate(13.064516129deg);
  -o-transform: rotate(13.064516129deg);
  -ms-transform: rotate(13.064516129deg);
  -webkit-transform: rotate(13.064516129deg);
  transform: rotate(13.064516129deg);
}
.day-text .char52 {
  -moz-transform: rotate(15.9677419355deg);
  -o-transform: rotate(15.9677419355deg);
  -ms-transform: rotate(15.9677419355deg);
  -webkit-transform: rotate(15.9677419355deg);
  transform: rotate(15.9677419355deg);
}
.day-text .char53 {
  -moz-transform: rotate(18.8709677419deg);
  -o-transform: rotate(18.8709677419deg);
  -ms-transform: rotate(18.8709677419deg);
  -webkit-transform: rotate(18.8709677419deg);
  transform: rotate(18.8709677419deg);
}
.day-text .char54 {
  -moz-transform: rotate(21.7741935484deg);
  -o-transform: rotate(21.7741935484deg);
  -ms-transform: rotate(21.7741935484deg);
  -webkit-transform: rotate(21.7741935484deg);
  transform: rotate(21.7741935484deg);
}
.day-text .char55 {
  -moz-transform: rotate(24.6774193548deg);
  -o-transform: rotate(24.6774193548deg);
  -ms-transform: rotate(24.6774193548deg);
  -webkit-transform: rotate(24.6774193548deg);
  transform: rotate(24.6774193548deg);
}
.day-text .char56 {
  -moz-transform: rotate(27.5806451613deg);
  -o-transform: rotate(27.5806451613deg);
  -ms-transform: rotate(27.5806451613deg);
  -webkit-transform: rotate(27.5806451613deg);
  transform: rotate(27.5806451613deg);
}
.day-text .char57 {
  -moz-transform: rotate(30.4838709677deg);
  -o-transform: rotate(30.4838709677deg);
  -ms-transform: rotate(30.4838709677deg);
  -webkit-transform: rotate(30.4838709677deg);
  transform: rotate(30.4838709677deg);
}
.day-text .char58 {
  -moz-transform: rotate(33.3870967742deg);
  -o-transform: rotate(33.3870967742deg);
  -ms-transform: rotate(33.3870967742deg);
  -webkit-transform: rotate(33.3870967742deg);
  transform: rotate(33.3870967742deg);
}
.day-text .char59 {
  -moz-transform: rotate(36.2903225806deg);
  -o-transform: rotate(36.2903225806deg);
  -ms-transform: rotate(36.2903225806deg);
  -webkit-transform: rotate(36.2903225806deg);
  transform: rotate(36.2903225806deg);
}
.day-text .char60 {
  -moz-transform: rotate(39.1935483871deg);
  -o-transform: rotate(39.1935483871deg);
  -ms-transform: rotate(39.1935483871deg);
  -webkit-transform: rotate(39.1935483871deg);
  transform: rotate(39.1935483871deg);
}
.day-text .char61 {
  -moz-transform: rotate(42.0967741935deg);
  -o-transform: rotate(42.0967741935deg);
  -ms-transform: rotate(42.0967741935deg);
  -webkit-transform: rotate(42.0967741935deg);
  transform: rotate(42.0967741935deg);
}
.day-text .char62 {
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}
.day-text .char63 {
  -moz-transform: rotate(47.9032258065deg);
  -o-transform: rotate(47.9032258065deg);
  -ms-transform: rotate(47.9032258065deg);
  -webkit-transform: rotate(47.9032258065deg);
  transform: rotate(47.9032258065deg);
}
.day-text .char64 {
  -moz-transform: rotate(50.8064516129deg);
  -o-transform: rotate(50.8064516129deg);
  -ms-transform: rotate(50.8064516129deg);
  -webkit-transform: rotate(50.8064516129deg);
  transform: rotate(50.8064516129deg);
}
.day-text .char65 {
  -moz-transform: rotate(53.7096774194deg);
  -o-transform: rotate(53.7096774194deg);
  -ms-transform: rotate(53.7096774194deg);
  -webkit-transform: rotate(53.7096774194deg);
  transform: rotate(53.7096774194deg);
}
.day-text .char66 {
  -moz-transform: rotate(56.6129032258deg);
  -o-transform: rotate(56.6129032258deg);
  -ms-transform: rotate(56.6129032258deg);
  -webkit-transform: rotate(56.6129032258deg);
  transform: rotate(56.6129032258deg);
}
.day-text .char67 {
  -moz-transform: rotate(59.5161290323deg);
  -o-transform: rotate(59.5161290323deg);
  -ms-transform: rotate(59.5161290323deg);
  -webkit-transform: rotate(59.5161290323deg);
  transform: rotate(59.5161290323deg);
}
.day-text .char68 {
  -moz-transform: rotate(62.4193548387deg);
  -o-transform: rotate(62.4193548387deg);
  -ms-transform: rotate(62.4193548387deg);
  -webkit-transform: rotate(62.4193548387deg);
  transform: rotate(62.4193548387deg);
}
.day-text .char69 {
  -moz-transform: rotate(65.3225806452deg);
  -o-transform: rotate(65.3225806452deg);
  -ms-transform: rotate(65.3225806452deg);
  -webkit-transform: rotate(65.3225806452deg);
  transform: rotate(65.3225806452deg);
}
.day-text .char70 {
  -moz-transform: rotate(68.2258064516deg);
  -o-transform: rotate(68.2258064516deg);
  -ms-transform: rotate(68.2258064516deg);
  -webkit-transform: rotate(68.2258064516deg);
  transform: rotate(68.2258064516deg);
}
.day-text .char71 {
  -moz-transform: rotate(71.1290322581deg);
  -o-transform: rotate(71.1290322581deg);
  -ms-transform: rotate(71.1290322581deg);
  -webkit-transform: rotate(71.1290322581deg);
  transform: rotate(71.1290322581deg);
}
.day-text .char72 {
  -moz-transform: rotate(74.0322580645deg);
  -o-transform: rotate(74.0322580645deg);
  -ms-transform: rotate(74.0322580645deg);
  -webkit-transform: rotate(74.0322580645deg);
  transform: rotate(74.0322580645deg);
}
.day-text .char73 {
  -moz-transform: rotate(76.935483871deg);
  -o-transform: rotate(76.935483871deg);
  -ms-transform: rotate(76.935483871deg);
  -webkit-transform: rotate(76.935483871deg);
  transform: rotate(76.935483871deg);
}
.day-text .char74 {
  -moz-transform: rotate(79.8387096774deg);
  -o-transform: rotate(79.8387096774deg);
  -ms-transform: rotate(79.8387096774deg);
  -webkit-transform: rotate(79.8387096774deg);
  transform: rotate(79.8387096774deg);
}
.day-text .char75 {
  -moz-transform: rotate(82.7419354839deg);
  -o-transform: rotate(82.7419354839deg);
  -ms-transform: rotate(82.7419354839deg);
  -webkit-transform: rotate(82.7419354839deg);
  transform: rotate(82.7419354839deg);
}
.day-text .char76 {
  -moz-transform: rotate(85.6451612903deg);
  -o-transform: rotate(85.6451612903deg);
  -ms-transform: rotate(85.6451612903deg);
  -webkit-transform: rotate(85.6451612903deg);
  transform: rotate(85.6451612903deg);
}
.day-text .char77 {
  -moz-transform: rotate(88.5483870968deg);
  -o-transform: rotate(88.5483870968deg);
  -ms-transform: rotate(88.5483870968deg);
  -webkit-transform: rotate(88.5483870968deg);
  transform: rotate(88.5483870968deg);
}
.day-text .char78 {
  -moz-transform: rotate(91.4516129032deg);
  -o-transform: rotate(91.4516129032deg);
  -ms-transform: rotate(91.4516129032deg);
  -webkit-transform: rotate(91.4516129032deg);
  transform: rotate(91.4516129032deg);
}
.day-text .char79 {
  -moz-transform: rotate(94.3548387097deg);
  -o-transform: rotate(94.3548387097deg);
  -ms-transform: rotate(94.3548387097deg);
  -webkit-transform: rotate(94.3548387097deg);
  transform: rotate(94.3548387097deg);
}
.day-text .char80 {
  -moz-transform: rotate(97.2580645161deg);
  -o-transform: rotate(97.2580645161deg);
  -ms-transform: rotate(97.2580645161deg);
  -webkit-transform: rotate(97.2580645161deg);
  transform: rotate(97.2580645161deg);
}
.day-text .char81 {
  -moz-transform: rotate(100.1612903226deg);
  -o-transform: rotate(100.1612903226deg);
  -ms-transform: rotate(100.1612903226deg);
  -webkit-transform: rotate(100.1612903226deg);
  transform: rotate(100.1612903226deg);
}
.day-text .char82 {
  -moz-transform: rotate(103.064516129deg);
  -o-transform: rotate(103.064516129deg);
  -ms-transform: rotate(103.064516129deg);
  -webkit-transform: rotate(103.064516129deg);
  transform: rotate(103.064516129deg);
}
.day-text .char83 {
  -moz-transform: rotate(105.9677419355deg);
  -o-transform: rotate(105.9677419355deg);
  -ms-transform: rotate(105.9677419355deg);
  -webkit-transform: rotate(105.9677419355deg);
  transform: rotate(105.9677419355deg);
}
.day-text .char84 {
  -moz-transform: rotate(108.8709677419deg);
  -o-transform: rotate(108.8709677419deg);
  -ms-transform: rotate(108.8709677419deg);
  -webkit-transform: rotate(108.8709677419deg);
  transform: rotate(108.8709677419deg);
}
.day-text .char85 {
  -moz-transform: rotate(111.7741935484deg);
  -o-transform: rotate(111.7741935484deg);
  -ms-transform: rotate(111.7741935484deg);
  -webkit-transform: rotate(111.7741935484deg);
  transform: rotate(111.7741935484deg);
}
.day-text .char86 {
  -moz-transform: rotate(114.6774193548deg);
  -o-transform: rotate(114.6774193548deg);
  -ms-transform: rotate(114.6774193548deg);
  -webkit-transform: rotate(114.6774193548deg);
  transform: rotate(114.6774193548deg);
}
.day-text .char87 {
  -moz-transform: rotate(117.5806451613deg);
  -o-transform: rotate(117.5806451613deg);
  -ms-transform: rotate(117.5806451613deg);
  -webkit-transform: rotate(117.5806451613deg);
  transform: rotate(117.5806451613deg);
}
.day-text .char88 {
  -moz-transform: rotate(120.4838709677deg);
  -o-transform: rotate(120.4838709677deg);
  -ms-transform: rotate(120.4838709677deg);
  -webkit-transform: rotate(120.4838709677deg);
  transform: rotate(120.4838709677deg);
}
.day-text .char89 {
  -moz-transform: rotate(123.3870967742deg);
  -o-transform: rotate(123.3870967742deg);
  -ms-transform: rotate(123.3870967742deg);
  -webkit-transform: rotate(123.3870967742deg);
  transform: rotate(123.3870967742deg);
}
.day-text .char90 {
  -moz-transform: rotate(126.2903225806deg);
  -o-transform: rotate(126.2903225806deg);
  -ms-transform: rotate(126.2903225806deg);
  -webkit-transform: rotate(126.2903225806deg);
  transform: rotate(126.2903225806deg);
}
.day-text .char91 {
  -moz-transform: rotate(129.1935483871deg);
  -o-transform: rotate(129.1935483871deg);
  -ms-transform: rotate(129.1935483871deg);
  -webkit-transform: rotate(129.1935483871deg);
  transform: rotate(129.1935483871deg);
}
.day-text .char92 {
  -moz-transform: rotate(132.0967741935deg);
  -o-transform: rotate(132.0967741935deg);
  -ms-transform: rotate(132.0967741935deg);
  -webkit-transform: rotate(132.0967741935deg);
  transform: rotate(132.0967741935deg);
}
.day-text .char93 {
  -moz-transform: rotate(135deg);
  -o-transform: rotate(135deg);
  -ms-transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
  transform: rotate(135deg);
}

.ring-back {
  opacity: 0.1;
  filter: alpha(opacity=10);
  width: 100%;
  height: 100%;
  border: solid 10px transparent;
  border-radius: 50%;
}
.ring-back:before {
  position: absolute;
  top: 5px;
  right: 5px;
  bottom: 5px;
  left: 5px;
  border-radius: 50%;
  border: solid 35px #FFFFFF;
  content: " ";
}

.ring {
  position: relative;
  top: -100%;
  width: 100%;
  height: 100%;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
  border: solid 45px #202020;
  border-radius: 50%;
  border-bottom-color: transparent;
  box-shadow: 0px -2px 2px #000;
}

.side-ring {
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
  width: 200px;
  height: 200px;
  background-color: #202020;
  border-radius: 50%;
  box-shadow: 0px 2px 2px #000;
  color: #000;
  overflow: hidden;
}

#weather {
  position: absolute;
  top: calc(50% - 100px);
  left: calc(20% - 100px);
}

#steps {
  position: absolute;
  top: calc(50% - 100px);
  left: calc(80% - 100px);
}

.fa-user {
  opacity: 0;
  filter: alpha(opacity=0);
  position: absolute;
  top: calc(50% - 40px);
  left: calc(50% - 40px);
  color: #555;
  font-size: 80px;
}

.temperature {
  opacity: 0;
  filter: alpha(opacity=0);
  position: absolute;
  top: 10%;
  left: 20%;
  color: #FFCC00;
  font-size: 10px;
}

.bars {
  opacity: 0;
  filter: alpha(opacity=0);
  position: relative;
  top: calc(50% - 70px);
  left: calc(50% - 65px);
  width: 140px;
  height: 140px;
}

.bar {
  width: 18px;
  height: 140px;
  margin: 0px -4px;
}

.day-letter {
  position: relative;
  top: 110px;
  color: #555;
  font-size: 18px;
  text-align: center;
}

.x {
  position: absolute;
  bottom: 30px;
  left: 1px;
  width: 16px;
  height: 2px;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
  -ms-transition: all 0.5s;
  -o-transition: all 0.5s;
  transition: all 0.5s;
}
</style>

  <script>
  window.console = window.console || function(t) {};
</script>

  
  
  <script>
  if (document.location.search.match(/type=embed/gi)) {
    window.parent.postMessage("resize", "*");
  }
</script>


</head>

<body translate="no">
  <div class="center-dial">
  <h1 class="center-preview" style="opacity: 0;"><span class="char1">H</span><span class="char2">E</span><span class="char3">L</span><span class="char4">L</span><span class="char5">O</span></h1>
  <div class="head" style="opacity: 0;"></div>
  <div class="torso" style="opacity: 0;"></div>
  <div class="hand-container" id="minutes" style="transform: rotate(210deg); opacity: 1;">
    <div class="minute-hand"></div>
  </div>
  <div class="hand-container" id="hours" style="transform: rotate(647.5deg); opacity: 1;">
    <div class="hour-hand"></div>
  </div>
  <div class="hand-container" id="seconds" style="transform: rotate(102deg); opacity: 1;">
    <div class="second-hand"></div>
  </div>
</div>
<div class="day-name-dial">
  <div class="ring-back"></div>
  <div class="ring" id="r1" style="transform: rotate(-115.714deg);">
    <h1 class="day-name-preview" style="opacity: 0;"><span class="char1">D</span><span class="char2">A</span><span class="char3">Y</span><span class="char4"> </span><span class="char5">N</span><span class="char6">A</span><span class="char7">M</span><span class="char8">E</span></h1>
    <h2 class="day-name-text" style="opacity: 1;"><span class="char1">M</span><span class="char2">O</span><span class="char3">N</span><span class="char4"> </span><span class="char5">T</span><span class="char6">U</span><span class="char7">E</span><span class="char8"> </span><span class="char9">W</span><span class="char10">E</span><span class="char11">D</span><span class="char12"> </span><span class="char13">T</span><span class="char14">H</span><span class="char15">U</span><span class="char16"> </span><span class="char17">F</span><span class="char18">R</span><span class="char19">I</span><span class="char20"> </span><span class="char21">S</span><span class="char22">A</span><span class="char23">T</span><span class="char24"> </span><span class="char25" style="color: rgb(76, 217, 100);">S</span><span class="char26" style="color: rgb(76, 217, 100);">U</span><span class="char27" style="color: rgb(76, 217, 100);">N</span></h2>
  </div>
</div>
<div class="month-dial">
  <div class="ring-back"></div>
  <div class="ring" id="r2" style="transform: rotate(-56.25deg);">
    <h1 class="month-preview" style="opacity: 0;"><span class="char1">M</span><span class="char2">O</span><span class="char3">N</span><span class="char4">T</span><span class="char5">H</span></h1>
    <h2 class="month-text" style="opacity: 1;"><span class="char1">J</span><span class="char2">A</span><span class="char3">N</span><span class="char4"> </span><span class="char5">F</span><span class="char6">E</span><span class="char7">B</span><span class="char8"> </span><span class="char9">M</span><span class="char10">A</span><span class="char11">R</span><span class="char12"> </span><span class="char13">A</span><span class="char14">P</span><span class="char15">R</span><span class="char16"> </span><span class="char17">M</span><span class="char18">A</span><span class="char19">Y</span><span class="char20"> </span><span class="char21">J</span><span class="char22">U</span><span class="char23">N</span><span class="char24"> </span><span class="char25">J</span><span class="char26">U</span><span class="char27">L</span><span class="char28"> </span><span class="char29">A</span><span class="char30">U</span><span class="char31">G</span><span class="char32"> </span><span class="char33" style="color: rgb(0, 122, 255);">S</span><span class="char34" style="color: rgb(0, 122, 255);">E</span><span class="char35" style="color: rgb(0, 122, 255);">P</span><span class="char36"> </span><span class="char37">O</span><span class="char38">C</span><span class="char39">T</span><span class="char40"> </span><span class="char41">N</span><span class="char42">O</span><span class="char43">V</span><span class="char44"> </span><span class="char45">D</span><span class="char46">E</span><span class="char47">C</span></h2>
  </div>
</div>
<div class="day-dial">
  <div class="ring-back"></div>
  <div class="ring" id="r3" style="transform: rotate(-17.4194deg);">
    <h1 class="day-preview" style="opacity: 0;"><span class="char1">D</span><span class="char2">A</span><span class="char3">Y</span></h1>
    <h2 class="day-text" style="opacity: 1;"><span class="char1">0</span><span class="char2">1</span><span class="char3"> </span><span class="char4">0</span><span class="char5">2</span><span class="char6"> </span><span class="char7">0</span><span class="char8">3</span><span class="char9"> </span><span class="char10">0</span><span class="char11">4</span><span class="char12"> </span><span class="char13">0</span><span class="char14">5</span><span class="char15"> </span><span class="char16">0</span><span class="char17">6</span><span class="char18"> </span><span class="char19">0</span><span class="char20">7</span><span class="char21"> </span><span class="char22">0</span><span class="char23">8</span><span class="char24"> </span><span class="char25">0</span><span class="char26">9</span><span class="char27"> </span><span class="char28">1</span><span class="char29">0</span><span class="char30"> </span><span class="char31">1</span><span class="char32">1</span><span class="char33"> </span><span class="char34">1</span><span class="char35">2</span><span class="char36"> </span><span class="char37">1</span><span class="char38">3</span><span class="char39"> </span><span class="char40">1</span><span class="char41">4</span><span class="char42"> </span><span class="char43">1</span><span class="char44">5</span><span class="char45"> </span><span class="char46">1</span><span class="char47">6</span><span class="char48"> </span><span class="char49">1</span><span class="char50">7</span><span class="char51"> </span><span class="char52" style="color: rgb(255, 45, 85);">1</span><span class="char53" style="color: rgb(255, 45, 85);">8</span><span class="char54"> </span><span class="char55">1</span><span class="char56">9</span><span class="char57"> </span><span class="char58">2</span><span class="char59">0</span><span class="char60"> </span><span class="char61">2</span><span class="char62">1</span><span class="char63"> </span><span class="char64">2</span><span class="char65">2</span><span class="char66"> </span><span class="char67">2</span><span class="char68">3</span><span class="char69"> </span><span class="char70">2</span><span class="char71">4</span><span class="char72"> </span><span class="char73">2</span><span class="char74">5</span><span class="char75"> </span><span class="char76">2</span><span class="char77">6</span><span class="char78"> </span><span class="char79">2</span><span class="char80">7</span><span class="char81"> </span><span class="char82">2</span><span class="char83">8</span><span class="char84"> </span><span class="char85">2</span><span class="char86">9</span><span class="char87"> </span><span class="char88">3</span><span class="char89">0</span><span class="char90"> </span><span class="char91">3</span><span class="char92">1</span></h2>
  </div>
</div>
<div class="side-ring" id="weather">
  <div class="fa fa-user" style="opacity: 1;"></div>
  <p class="temperature" style="opacity: 1;"> """

    cal3 = """
  </p>
</div>
<div class="side-ring" id="steps">
  <div class="bars" style="opacity: 1;">
    <div class="bar">
      <div class="day-letter">M</div>
      <div class="x" id="x1" style="height:0 px;"></div>
    </div>
    <div class="bar">
      <div class="day-letter">T</div>
      <div class="x" id="x2" style="height:0 px;"></div>
    </div>
    <div class="bar">
      <div class="day-letter">W</div>
      <div class="x" id="x3" style="height: 76px;"></div>
    </div>
    <div class="bar">
      <div class="day-letter">T</div>
      <div class="x" id="x4" style="height: 40px;"></div>
    </div>
    <div class="bar">
      <div class="day-letter">F</div>
      <div class="x" id="x5" style="height: 21px;"></div>
    </div>
    <div class="bar">
      <div class="day-letter">S</div>
      <div class="x" id="x6" style="height: 58px;"></div>
    </div>
    <div class="bar">
      <div class="day-letter">S</div>
      <div class="x" id="x7" style="height: 40px;"></div>
    </div>
  </div>
</div>
    <script src="https://cpwebassets.codepen.io/assets/common/stopExecutionOnTimeout-1b93190375e9ccc259df3a57c1abc0e64599724ae30d7ea4c6877eb615f89387.js"></script>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/lettering.js/0.6.1/jquery.lettering.min.js"></script>
      <script id="rendered-js">
/*
 * Cirulcar Calendar Display.js
 */

$(function () {

  var date, dayName, day, month, year;
  var range = 270,
  sectionsDayName = 7,
  sectionsDay = 31,
  sectionsMonth = 12,
  charactersDayName = 3,
  charactersDay = 2,
  charactersMonth = 3,
  dayColor = '#FF2D55',
  monthColor = '#007AFF',
  dayNameColor = '#4CD964';


  // Rotate the selected ring the correct amount and illuminate the correct characters of the ring text
  function rotateRing(input, sections, characters, ring, text, color) {
    var sectionWidth = range / sections;
    var initialRotation = 135 - sectionWidth / 2;
    var rotateAmount = initialRotation - sectionWidth * (input - 1);
    var start = characters * (input - 1) + (input - 1) + 1;

    $(ring).css({
      '-webkit-transform': 'rotate(' + rotateAmount + 'deg)',
      '-moz-transform': 'rotate(' + rotateAmount + 'deg)',
      '-ms-transform': 'rotate(' + rotateAmount + 'deg)',
      'transform': 'rotate(' + rotateAmount + 'deg)' });


    for (var i = start; i < start + characters; i++) {
      $(text).children('.char' + i).css({
        'color': color });

    }
  }

  // Get a new date object every second and update the rotation of the clock handles
  function clockRotation() {
    setInterval(function () {
      var date = new Date();
      var seconds = date.getSeconds();
      var minutes = date.getMinutes();
      var hours = date.getHours();
      var secondsRotation = seconds * 6;
      var minutesRotation = minutes * 6;
      var hoursRotation = hours * 30 + minutes / 2;
      $("#seconds").css({
        '-webkit-transform': 'rotate(' + secondsRotation + 'deg)',
        '-moz-transform': 'rotate(' + secondsRotation + 'deg)',
        '-ms-transform': 'rotate(' + secondsRotation + 'deg)',
        'transform': 'rotate(' + secondsRotation + 'deg)' });

      $("#minutes").css({
        '-webkit-transform': 'rotate(' + minutesRotation + 'deg)',
        '-moz-transform': 'rotate(' + minutesRotation + 'deg)',
        '-ms-transform': 'rotate(' + minutesRotation + 'deg)',
        'transform': 'rotate(' + minutesRotation + 'deg)' });

      $("#hours").css({
        '-webkit-transform': 'rotate(' + hoursRotation + 'deg)',
        '-moz-transform': 'rotate(' + hoursRotation + 'deg)',
        '-ms-transform': 'rotate(' + hoursRotation + 'deg)',
        'transform': 'rotate(' + hoursRotation + 'deg)' });

    }, 1000);
  }

  // Give column representing passed days and the current day this week a height
  function loadBars() {
    for (var i = 1; i <= dayName; i++) {
      var newHeight = Math.floor(Math.random() * 85) + 5;
      var newTop = 110 - newHeight;
      $("#x" + 1).css({
        'height': """
    bar1=      5
    cal4=       """+ 'px' });
      $("#x" + 2).css({
        'height':""" 
    bar2=       0 
    cal5=       """+ 'px' });
      $("#x" + 3).css({
        'height': """
    bar3=     10 
    cal6=       """+ 'px' });
      $("#x" + 4).css({
        'height':""" 
    bar4=     10 
    cal7=        """+ 'px' });
      $("#x" + 5).css({
        'height': """
    bar5=      5 
    cal8=        """+ 'px' });
      $("#x" + 6).css({
        'height': """
    bar6=     10 
    cal9=       """+ 'px' });
      $("#x" + 7).css({
        'height':""" 
    bar7=      0 
    cal10=       """+ 'px' });

    }
  }

  function init() {
    $(".center-preview").lettering();
    $(".day-name-preview").lettering();
    $(".day-name-text").lettering();
    $(".day-preview").lettering();
    $(".day-text").lettering();
    $(".month-preview").lettering();
    $(".month-text").lettering();
    $('.day-preview').fadeTo(10, 1);
    $('.month-preview').fadeTo(10, 1);
    $('.day-name-preview').fadeTo(10, 1);
    $('.center-preview').fadeTo(10, 1);

    // Get date variables
    date = new Date();
    dayName = date.getDay(); // Day of week (1-7)
    day = date.getDate(); // Get current date (1-31)
    month = date.getMonth() + 1; // Current month (1-12)
    if (dayName == 0) {
      dayName = 7;
    }
    // Fade in/out second dial and rotate. Also fade in and animate side elements.
    setTimeout(function () {
      $('.day-preview').fadeTo(500, 0);
      $('.day-text').fadeTo(500, 1, function () {
        rotateRing(day, sectionsDay, charactersDay, '#r3', '.day-text', dayColor);
      });
    }, 500);

    // Fade in/out second dial and rotate. Also fade in and animate side elements.
    setTimeout(function () {
      $('.month-preview').fadeTo(500, 0);
      $('.fa-user').fadeTo(500, 1);
      $('.temperature').fadeTo(500, 1);
      $('.bars').fadeTo(500, 1);
      $('.month-text').fadeTo(500, 1, function () {
        rotateRing(month, sectionsMonth, charactersMonth, '#r2', '.month-text', monthColor);
        loadBars();
      });
    }, 1000);

    // Fade in/out first dial and rotate
    setTimeout(function () {
      $('.day-name-preview').fadeTo(500, 0);
      $('.day-name-text').fadeTo(500, 1, function () {
        rotateRing(dayName, sectionsDayName, charactersDayName, '#r1', '.day-name-text', dayNameColor);
      });
    }, 1500);

    // Fade in/out center dial
    setTimeout(function () {
      $('.center-preview').fadeTo(500, 0);
      $('.head').fadeTo(500, 0);
      $('.torso').fadeTo(500, 0);
      $(".hand-container").fadeTo(500, 1, function () {
        //console.log("Clock faded in");
      });
    }, 2000);

    // Begin clock rotation now it is visible
    clockRotation();
  }

  init();
});
//# sourceURL=pen.js
    </script>

  




 
</body></html>

    """
    try:
        wodf = wo_db.fetch().items
        wodf1 = pd.DataFrame(wodf)
        wodf1 = wodf1[wodf1['name'] == st.session_state.user_name]
        wodf1['date'] = pd.to_datetime(wodf1['date'], errors = 'coerce')
        wodf1['dayname'] = wodf1['date'].dt.day_name()
        monday = len(wodf1[wodf1['dayname']=='Monday']) * 2
        tuesday = len(wodf1[wodf1['dayname']=='Tuesday']) * 2
        wednesday = len(wodf1[wodf1['dayname']=='Wednesday']) * 2
        thursday = len(wodf1[wodf1['dayname']=='Thursday']) * 2
        friday = len(wodf1[wodf1['dayname']=='Friday']) * 2
        saturday = len(wodf1[wodf1['dayname']=='Saturday']) * 2
        sunday = len(wodf1[wodf1['dayname']=='Sunday']) * 2
    except:
        monday = 0
        tuesday = 0
        wednesday = 0
        thursday = 0
        friday = 0
        saturday = 0
        sunday = 0
    

    cals = cal_html + HWOD + cal3 + str(monday) + cal4 + str(tuesday) + cal5 + str(wednesday) + cal6 + str(thursday) + cal7 + str(friday) + cal8 + str(saturday) + cal9 + str(sunday) + cal10
 
    column1, column2 = st.columns(2)
    with column2:
        components.html(cals, height=550)
       
        components.iframe('https://asl--learn.glitch.me/', height = 500)

    with column1:
        colored_header("Workout of the Day")
        components.html(full_html, height=290)
        if 'auth_status' in st.session_state:
            try:
                wodf = wo_db.fetch().items
                wodf1 = pd.DataFrame(wodf)
                wodf1 = wodf1[wodf1['name'] == st.session_state.user_name]
                wodf1['date'] = pd.to_datetime(wodf1['date'], errors = 'coerce')
                lastwo = wodf1[wodf1['date'] == wodf1['date'].max()]
                
                
                maxdf = wo_db.fetch().items
                maxdf1 = pd.DataFrame(maxdf)
                maxdf1 = maxdf1[maxdf1['name'] == st.session_state.user_name]
                maxdf1['weight'] = maxdf1['weight'].astype(float)
                maxdf1 = maxdf1[maxdf1['weight'] > 0.00]
                lastmax = maxdf1['date'].max()
                maxdf2 = maxdf1[maxdf1['date'] == lastmax]
                
                maxdf2 = maxdf2.reset_index()
                repmax_lift = maxdf2['lift'].iloc[0]
                maxdf22 = maxdf2[maxdf2['lift'] == repmax_lift]
                repmax_min = min(maxdf22['weight'])
                repmax_weight = max(maxdf22['weight'])
                metric_string = "Last Max: " + str(repmax_lift)
                repmax_diff = int(repmax_weight) - int(repmax_min)

                st.metric(metric_string, value = repmax_weight, delta = repmax_diff)
                lastwo = lastwo.reset_index()
                lastwo = lastwo[lastwo['Movements'].str.len() > 1]
                st.write("Last Workout: ", lastwo['Workout'].iloc[0], " | Performance: ", lastwo['Performance'].iloc[0], " | Date: ", lastwo['date'].iloc[0])
            except:
                pass

        



    
if menu == 'Workouts':
    colored_header("Workouts")
    
    ms = st.selectbox("Search through workouts", options = wods['Workout'].unique())
    ns = wods[wods['Workout'] == ms]
    list_html1 = ""
    for cs in ns.columns.unique():
        ns[cs] = ns[cs].astype(str)
    for d in ns.columns.unique():
        if d == 'Workout':
            continue
        if ns[d].iloc[0]  == 'None':
            continue
        list_html1 += f"<div style='width: fit-content; " \
                     f"background: linear-gradient(246.65deg, #BDCDFF -17.53%, #D2F4D8 83.84%, #E0FFE7 104.88%); " \
                     f"color: #555D9D; letter-spacing: 0.2em; border-radius: 2rem; " \
                     f"padding: 0 1.5rem; margin-bottom: 0.5rem';>" \
                     f"{d}: {ns[d].iloc[0]} </div>" 
    
        
    full_html1 = f"""
                 <script>
                        document.head.innerHTML += 
                        '<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">'
                    </script>
                 <div style="font-family: 'Open Sans';">
                    <div style="color: white; margin-bottom: 1rem;"> 
                    </div>
                    <div style="display: flex; flex-direction: column;">{list_html1}</div>
                </div>"""
    side1, side2 = st.columns(2)
    with side1:
        components.html(full_html1, height = 300)
    with side2:
        if 'auth_status' in st.session_state:
            with st.expander("Log This Workout"):
                rxscale = st.radio("", options=['RX', 'Scaled'], horizontal = True)
                perf = st.text_input("Time or Reps")
                log = st.button("Log")
                if log:
                    st.balloons() 
                    wo_db.put({"name": st.session_state.user_name,"date": str(date), "Workout": ns['Workout'].iloc[0], "Rounds": ns['Rounds'].iloc[0], "Reps": ns['Reps'].iloc[0], "Max Time": ns['Max Time'].iloc[0], "Movements": ns['Movement'].iloc[0], "Performance": perf, "RX/Scaled": rxscale})
            with st.expander("Add Workout"):
                wkt = st.text_input("Enter Workout Name")
                rds = st.number_input("Rounds")
                reps = st.text_input("Reps")
                mxtime = st.number_input("Max Time")
                mvmts = st.text_input("Movements")
                rxscale = st.radio("_", options=['RX', 'Scaled'], horizontal = True)
                perf1 = st.text_input("Time/Reps")
    
                log1 = st.button("Add")
                if log1:
                    st.balloons()
                    wo_db.put({"name": st.session_state.user_name, "date": str(date), "Workout": wkt, "Rounds": rds, "Reps": reps, "Max Time": mxtime, "Movements": mvmts, "Performance": perf1, "RX/Scaled": rxscale})
            

if menu == 'Max':
    if 'auth_status' in st.session_state:
        with st.expander("Log Max Weight"):
            lift = st.selectbox('Select Lift',('Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts', 'Front Box Squat', 'Front Pause Squat', 'Overhead Squat', 'Push Jerk', 'Split Jerk', 'Squat Jerk', 'Hang Power Snatch', 'Hang Squat Snatch', 'Power Snatch', 'Snatch', 'Squat Snatch', 'Romainian Deadlift', 'Sumo Deadlift', 'Clean and Jerk', 'Power Clean and Jerk'))
            weight = st.number_input("Enter Weight", step = 0.5)
            if st.button("➕"):
                wo_db.put({"name": st.session_state.user_name, "date": str(date), "lift": lift, "weight": weight})
                st.success("SUCCESSFULLY ADDED: {}".format(lift))
        maxdf = wo_db.fetch().items
        maxdf1 = pd.DataFrame(maxdf)
        maxdf1 = maxdf1[maxdf1['name'] == st.session_state.user_name]
        maxdf1['weight'] = maxdf1['weight'].astype(float)
        maxdf1 = maxdf1[maxdf1['weight'] > 0.00]
        
        maxtable = pd.DataFrame()
        maxtable['Lifts'] = maxdf1['lift'].unique()
        ind = 0
        maxtable['100%'] = 'na'
        maxtable['95%'] = 'na'
        maxtable['90%'] = 'na'
        maxtable['85%'] = 'na'
        maxtable['80%'] = 'na'
        maxtable['75%'] = 'na'
        maxtable['70%'] = 'na'
        maxtable['65%'] = 'na'
        maxtable['60%'] = 'na'
        maxtable['55%'] = 'na'
        maxtable['50%'] = 'na'
        maxtable['45%'] = 'na'
        maxtable['40%'] = 'na'
        maxtable['35%'] = 'na'
        maxtable['30%'] = 'na'
        maxtable['25%'] = 'na'
        maxtable['20%'] = 'na'
        maxtable['15%'] = 'na'
        maxtable['10%'] = 'na'
        maxtable['5%'] = 'na'
        for lft in maxdf1['lift'].unique():
            print(lft)
            liftdf = maxdf1[maxdf1['lift'] == lft]
            print(liftdf)
    
            for i in range(len(maxtable)):
                maxlft = liftdf['weight'].max()
                maxtable['100%'].iloc[ind] = maxlft
                maxtable['95%'].iloc[ind] = int(maxlft) * 0.95
                maxtable['90%'].iloc[ind] = int(maxlft) * 0.90
                maxtable['85%'].iloc[ind] = int(maxlft) * 0.85
                maxtable['80%'].iloc[ind] = int(maxlft) * 0.80
                maxtable['75%'].iloc[ind] = int(maxlft) * 0.75
                maxtable['70%'].iloc[ind] = int(maxlft) * 0.70
                maxtable['65%'].iloc[ind] = int(maxlft) * 0.65
                maxtable['60%'].iloc[ind] = int(maxlft) * 0.60
                maxtable['55%'].iloc[ind] = int(maxlft) * 0.55
                maxtable['50%'].iloc[ind] = int(maxlft) * 0.50
                maxtable['45%'].iloc[ind] = int(maxlft) * 0.45
                maxtable['40%'].iloc[ind] = int(maxlft) * 0.40
                maxtable['35%'].iloc[ind] = int(maxlft) * 0.35
                maxtable['30%'].iloc[ind] = int(maxlft) * 0.30
                maxtable['25%'].iloc[ind] = int(maxlft) * 0.25
                maxtable['20%'].iloc[ind] = int(maxlft) * 0.20
                maxtable['15%'].iloc[ind] = int(maxlft) * 0.15
                maxtable['10%'].iloc[ind] = int(maxlft) * 0.10
                maxtable['5%'].iloc[ind]= int(maxlft) * 0.05
            ind = ind + 1

        maxsid1, maxsid2 = st.columns(2)
        with maxsid2:
          colored_header("Your Table")
          st.dataframe(maxtable.astype(str).replace('.0', ' ').style.background_gradient())
        with maxsid1:
          colored_header("Reference Table")
          mtab = pd.read_csv('maxtable.csv')
          if 'vl' not in st.session_state:
            st.session_state.vl = 55
          st.session_state.vl = st.slider("Weight", min_value= 55, max_value = 455, value = st.session_state.vl, step = 5)
          mtab1 = mtab[mtab['1 Rep Max'] == st.session_state.vl]
          st.dataframe(mtab1.style.background_gradient())

    else:
      mtab = pd.read_csv('maxtable.csv')
      colored_header("Max Table")
      st.dataframe(mtab.style.background_gradient(), height = 500)


                
