import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats


st.title('Ranking players')

uploaded_file = st.sidebar.file_uploader("Choose a file")
pdi = []
if uploaded_file is not None:
    df = pd.read_excel(io=uploaded_file)
    df = df.fillna(0)
    df["KPI"]=0
    age_max = st.sidebar.slider("Max Age", 16, 40, 24)
    minute_min = st.sidebar.slider("Minimum Minutes",0,max(df["Minutes played"]),0)
    unique_list_pos = ["Keeper","Central Defender","Fullback","Midfielders","Wingers","Forwards"]
    dictionnaire_position ={
        "Keeper":["General keeper","Line keeper","Ball playing keeper"], 
        "Central Defender":["General Central Defender","Ball playing defender","Ball winning defender"],
        "Fullback" :["General fullback","Defensive minded fullback","Wingback"], 
        "Midfielders":["General Midfielder","Holding midfielder","Box to box midfielder","Deep lying playmaker"],
        "Wingers" : ["General Winger","Classic winger","Wide playmaker"], 
        "Forwards":["General Forward","Target Man","Mobile striker","Complete striker"]}
    position = st.sidebar.selectbox("Position",unique_list_pos)
    list_profil = dictionnaire_position[position]
    i= 0
    choice_var = st.sidebar.selectbox("Player's Profile",list_profil)
    dictionnaire_variables = {
        "General keeper": ["Conceded goals","Conceded goals per 90","Shots against","Shots against per 90","Clean sheets","Save rate, %","xG against","xG against per 90","Prevented goals","Prevented goals per 90","Back passes received as GK per 90","Exits per 90","Aerial duels per 90","Interceptions per 90","Offensive duels per 90","Progressive passes per 90","Average pass length, m"],
        "Line keeper" :["Prevented goals per 90","Save rate, %","Exits per 90"],
        "Ball playing keeper":["Prevented goals per 90","Save rate, %","Interceptions per 90","Offensive duels per 90","Progressive passes per 90","Average pass length, m"],
        "Ball playing defender":["Defensive duels per 90", "Defensive duels won, %", "PAdj Interceptions", "Progressive passes per 90", "Progressive runs per 90", "Passes to final third per 90", "Accurate passes to final third, %", "Third assists per 90", "Through passes per 90","Forward passes per 90", "Accurate forward passes, %"],
        "Ball winning defender" :["Successful defensive actions per 90", "Defensive duels per 90","Defensive duels won, %", "PAdj Interceptions", "PAdj Sliding tackles", "Aerial duels per 90", "Aerial duels won, %"],
        "Defensive minded fullback" : ["Successful defensive actions per 90", "Defensive duels per 90","Defensive duels won, %", "PAdj Interceptions", "Aerial duels per 90", "Aerial duels won, %", "Crosses per 90", "xA per 90", "Assists per 90", "Forward passes per 90", "Accurate forward passes, %"],
        "Wingback" : ["PAdj Interceptions", "Successful attacking actions per 90", "Progressive runs per 90", "Dribbles per 90", "xG per 90", "xA per 90", "Assists per 90", "Crosses per 90", "Forward passes per 90", "Accurate forward passes, %", "Passes to penalty area per 90", "Key passes per 90", "Second assists per 90", "Progressive passes per 90"],
        "Holding midfielder" : ["Successful defensive actions per 90", "Defensive duels per 90","Defensive duels won, %", "PAdj Interceptions", "Shots blocked per 90", "Forward passes per 90", "Accurate forward passes, %"],
        "Box to box midfielder": ["Successful defensive actions per 90", "Defensive duels per 90","Defensive duels won, %", "PAdj Interceptions", "Shots blocked per 90", "Passes per 90", "Accurate passes, %", "Forward passes per 90", "Accurate forward passes, %", "Progressive passes per 90", "Passes to final third per 90", "Passes to penalty area per 90"],
        "Deep lying playmaker" : ["Progressive passes per 90", "Passes to final third per 90", "Passes to penalty area per 90","Second assists per 90", "Assists per 90", "xA per 90", "Shot assists per 90", "Key passes per 90", "Through passes per 90", "Deep completions per 90", "Dribbles per 90"],
        "Classic winger" : ["xG per 90", "Goals per 90", "Shots per 90", "Assists per 90", "xA per 90", "Crosses per 90", "Dribbles per 90", "Successful dribbles, %", "Progressive runs per 90", "Accelerations per 90"],
        "Wide playmaker" : ["xG per 90", "Goals per 90", "Shots per 90", "Assists per 90", "xA per 90", "Crosses per 90", "Shot assists per 90", "Key passes per 90", "Passes to penalty area per 90", "Through passes per 90", "Deep completions per 90"],
        "Target Man" : ["Goals per 90", "xG per 90","Head goals per 90", "Shots per 90", "Aerial duels per 90", "Aerial duels won, %", "Touches in box per 90", "Received long passes per 90"],
        "Mobile striker" : ["Goals per 90", "xG per 90", "Shots per 90", "PAdj Interceptions", "Defensive duels per 90", "Dribbles per 90", "Progressive runs per 90", "Accelerations per 90"],
        "Complete striker" : ["Goals per 90", "xG per 90", "Shots per 90", "Aerial duels per 90", "Aerial duels won, %", "Touches in box per 90", "Goal conversion, %", "Shots on target, %"]
    }
    general_result = []
    general_key = dictionnaire_position[position][0]
    for element in dictionnaire_position[position][1:]:
        general_result.extend(dictionnaire_variables[element])
    general_result = list(set(general_result))
    dictionnaire_variables[general_key]=general_result
    choice_variable_off = dictionnaire_variables[choice_var]
    if len(choice_variable_off)>0:
        age_mask = df["Age"] <= age_max
        min_mask = df["Minutes played"] >= minute_min
        #pos_mask = df["Position"].apply(lambda x: any(pos in x for pos in positions))
        final_mask = age_mask & min_mask
        df = df[final_mask]
        st.sidebar.title("Influence of each parameter")
        for variable in choice_variable_off:
            var = st.sidebar.slider(variable, 0, 100, 100)
            df[variable] = stats.zscore(df[variable])
            #st.write(df[[variable,'Joueur']])
            df["KPI"] += df[variable]*(var/100)
            

        df = df.sort_values(by='KPI', ascending=False)
        df.reset_index(drop=True, inplace=True)
        st.header(choice_var)
        #st.write(df[['Player', 'Team within selected timeframe',"Minutes played","Position", "Age","Market value","Contract expires","Accurate forward passes, %","Accurate progressive passes, %","Accurate passes to final third, %","Key passes per 90","Accurate smart passes, %","Goals","xG","Passes per 90","Long passes per 90","Free kicks per 90","KPI"]].head(50))
        st.write(df[['Player', 'Team within selected timeframe',"Matches played","Minutes played","Position", "Age","Height","Foot","Passport country","Market value","Contract expires","KPI"]])
