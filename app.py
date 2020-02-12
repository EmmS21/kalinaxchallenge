import dash
import dash_table
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import os
import numpy as np
path = 'C://Users//User//Downloads//finaldataset2.csv'
path_two = 'C://Users//User//Downloads//limitedsupervisor.csv'
#reading the data
performance_data = pd.read_csv(path)
supervisor = pd.read_csv(path_two)
#employment span in months
performance_data['Month'] = pd.to_datetime(performance_data['Month'])
#cost to company to span of team ratio
supervisor['Pay to team size ratio'] = supervisor['Cost to Company']/supervisor['span']
#correlation dataframe
correlation_df = supervisor[['Características (D)', 'Características (I)',
       'Características (S)', 'Características (C)', 'Motivación (D)',
       'Motivación (I)', 'Motivación (S)', 'Motivación (C)', 'Bajo Stress (D)',
       'Bajo Stress (I)', 'Bajo Stress (S)', 'Bajo Stress (C)','span','Mean Team Performance','employment span','Pay to team size ratio']]
correlation_df  = correlation_df.corr()
#supervisor data characteristics
fig = go.Figure()
category_dict = {'Características (D)': 'markers',
                 'Características (I)': 'markers',
                 'Características (S)': 'markers',
                 'Características (C)': 'markers'}
for category in category_dict.keys():
    fig.add_trace(go.Scatter(
        x=supervisor[category],
        y=supervisor['Mean Team Performance'],
        mode=category_dict[category],
        name=category
    ))
fig.update_layout(title="Relationship between characteristic profiles and average team performance",
                  yaxis={"title": 'Mean Team Performance', "range": [0, max(supervisor['Mean Team Performance'])+1]},
                  xaxis={"title": 'Characteristic scores',"tickangle": 45}, )
#supervisor data motivation
fig_one = go.Figure()
category_dict = {'Motivación (D)': 'markers',
                 'Motivación (I)': 'markers',
                 'Motivación (S)': 'markers',
                 'Motivación (C)': 'markers'}
for category in category_dict.keys():
    fig_one.add_trace(go.Scatter(
        x=supervisor[category],
        y=supervisor['Mean Team Performance'],
        mode=category_dict[category],
        name=category,
    ))
fig_one.update_layout(title="Relationship between Motivation profiles and average team performance",
                  yaxis={"title": 'Mean Team Performance', "range": [0, max(supervisor['Mean Team Performance'])+1]},
                  xaxis={"title": 'Motivation scores',"tickangle": 45}, )
#working under stress
fig_two = go.Figure()
category_dict = {'Bajo Stress (D)': 'markers',
                 'Bajo Stress (I)': 'markers',
                 'Bajo Stress (S)': 'markers',
                 'Bajo Stress (C)': 'markers'}
for category in category_dict.keys():
    fig_two.add_trace(go.Scatter(
        x=supervisor[category],
        y=supervisor['Mean Team Performance'],
        mode=category_dict[category],
        name=category,
    ))
fig_two.update_layout(title="Relationship between ability to work under stress and average team performance",
                  yaxis={"title": 'Mean Team Performance', "range": [0, max(supervisor['Mean Team Performance'])+1]},
                  xaxis={"title": 'Scores for working under stress',"tickangle": 45}, )
#length of employment
fig_three = go.Figure()
fig_three.add_trace(go.Scatter(
    x=supervisor['employment span'],
    y=supervisor['Mean Team Performance'],
    mode='markers',
    name='Length of Employment'
))
fig_three.update_layout(title="Relationship between supervisor length of employment and average team performance",
                  yaxis={"title": 'Mean Team Performance', "range": [0, max(supervisor['Mean Team Performance'])+1]},
                  xaxis={"title": 'Days of Employment',"tickangle": 45}, )
#span of team
fig_four = go.Figure()
fig_four.add_trace(go.Scatter(
    x=supervisor['span'],
    y=supervisor['Mean Team Performance'],
    mode='markers',
    name='Size of team'
))
fig_four.update_layout(title="Relationship between team size and average team performance",
                  yaxis={"title": 'Mean Team Performance', "range": [0, max(supervisor['Mean Team Performance'])+1]},
                  xaxis={"title": 'Size of team',"tickangle": 45}, )
#cost to company to team ratio
fig_five = go.Figure()
fig_five.add_trace(go.Scatter(
    x=supervisor['Pay to team size ratio'],
    y=supervisor['Mean Team Performance'],
    mode='markers',
    name='Pay to team size'
))
fig_five.update_layout(title="Relationship between total pay divided by the size of a supervisor's team and average team performance",
                  yaxis={"title": 'Mean Team Performance', "range": [0, max(supervisor['Mean Team Performance'])+1]},
                  xaxis={"title": 'Total Pay/Team Size',"tickangle": 45}, )
#correlation heatmap
corr_fig = go.Figure()
corr_fig.add_trace(go.Heatmap(
    z= correlation_df.values,
    x= ['Características (D)', 'Características (I)',
       'Características (S)', 'Características (C)', 'Motivación (D)',
       'Motivación (I)', 'Motivación (S)', 'Motivación (C)', 'Bajo Stress (D)',
       'Bajo Stress (I)', 'Bajo Stress (S)', 'Bajo Stress (C)','span','Mean Team Performance','employment span','Pay to team size ratio'],
    y= ['Características (D)', 'Características (I)',
       'Características (S)', 'Características (C)', 'Motivación (D)',
       'Motivación (I)', 'Motivación (S)', 'Motivación (C)', 'Bajo Stress (D)',
       'Bajo Stress (I)', 'Bajo Stress (S)', 'Bajo Stress (C)','span','Mean Team Performance','employment span','Pay to team size ratio'],
    hoverongaps=False
))
corr_fig.update_layout(title="Correlation heatmap",
                  yaxis={"title": 'Traits'},
                  width=1000,
                  height=700,
                  xaxis={"title": 'Traits',"tickangle": 45}, )


#css stylesheet
app = dash.Dash()
#html layout
app.layout = html.Div(children=[
    html.H1(children='SAC Challenge Level 2 Dashboard', style={
        'textAlign': 'center',
        'height': '10'
    }),
    html.Div(children='''
        Objective: Studying the impact of supervision on the performance of sales executives in Area 1
        '''),
    dcc.DatePickerRange(
        id='year_month',
        start_date=min(performance_data['Month'].dt.date.tolist()),
        end_date=max(performance_data['Month'].dt.date.tolist()),
        calendar_orientation='vertical',
    ),
    dcc.Graph(
        id='performancetable',
        ),
    dcc.Markdown('''
        # The Rationale

        This table is a merger of both the hr and sales tables. The purpose being to allow the end user to filter through different time periods and get a snap shot of the performance of each agent listed in the table.
        I included the most relevant columns, specifically:
        * Month
        * Sales System Code
        * TITULO
        * Supervisor Employee ID
        * Monthly Subscribers - this is the total number of subscriptions associated with a given sales person in the selected time period
        * Churned Subscribers - this is the number of subscriptions lost in a given time period per agent
        * Months of Employment Rounded - this is the rounded off delta between the hire date and the current report month. This does not factor in the Exit Date
        * Exit Date
        * Rental Charge
        * Cost to Company - this is a calculation of what a given agent costs to the company, while factoring the expectations the company has from the individual in question. To get this figure I added the Base pay, car allowance and commission target. I made the assumption that including commission target would allow me to factor in the expectations the company had from a given agent.
        * Revenue Per CtC - this metric divides the rental charges by the cost to company. The purpose being to have a metric that measures the revenue a sales agent bring in per $ spent on the sales 's core salary while factoring in the expected output from the sales person.
    '''),
    dcc.Graph(
        id='supervisor',
        figure=fig.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    I wanted to visualize the characteristic measures to assess whether was a linear relationship between a score in a the characteristics columns and the mean performance of people working under a given sales supervisor. I also included a feature that is mean of the character scores.
    
    From this particular set of characteristics there appears to be no visible linear relationship between a score attained by a supervisor and the mean team terformance.
    
    ### Assumptions: 
    For the purpose of analysing which traits have a higher impact on performance I focused on sales people who had employee ID's that matches supervisorEmployeeIDs. From the information I received I believed that this indicated that the sales person was either currently or at some point a supervisor for a given team. Therefore in order to understand what characterisitcs need to be maximised to improve performance it is important to include everyone who has supervised any sales person.    
    '''),
    dcc.Graph(
        id='motivation',
        figure=fig_one.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    From just eyeballing this chart there doesn't appear to be a strong correlation between any of the motivation scores and mean team performance. However, the mere fact that this trend is not clearly visible to the eye does not mean that there is no correlation.
    '''),
    dcc.Graph(
        id='under-stress',
        figure= fig_two.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    Much like the previous charts there is no clear correlation between the scores pertaining to working under stress and mean team performance.
    '''),
    dcc.Graph(
        id='employmentlength',
        figure=fig_three.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    For this chart I created a custom feature looking at the length of a supervisor's employment in months. From eyeballing this chart there appears to be a positive correlation between the length of employment and mean team performance. However, this will need to be investigated further.
    '''),
    dcc.Graph(
        id='span',
        figure=fig_four.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    This chart compares the size of a person's team and the mean performance of sales people under particular supervisor. Aside from a single outlier, there is very little evidence from the data to indicate a relationship between the size of one's team and the team's performance.
    '''),
    dcc.Graph(
        id='ctcteamratio',
        figure=fig_five.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    In creating this feature I had the assumption that total compensation that is not commensurate to the number of people a supervisor has under them may be a demotivating factor lowering the supervisor's productivity (or ability to mentor and manage sales executives) thus reducing their performance in the long run. This seems to indicate that the more pay is scaled as a supervisor manages more executives, the better the performance of executives under said supervisor.
    
    '''),
    dcc.Graph(
        id='heatmap',
        figure=corr_fig.to_dict()
    ),
    dcc.Markdown('''
    ## Explanation
    
    The purpose of creating a heatmap to visualize correlations was to specifically try and find out which features appear to be more associated with higher mean team performance. Looking at this heatmap in conjunction with the visualizations created helps us understand if there is a relationship between a feature and the performance.
    
    If we zoom in specifically on mean team performance we see the highest correlation between performance, Bajo Stress(S), Motivacion (D) and Características (D) scores. When we filter the relevant visualizations for these scores, leaving aside the outliers, we can see the existence of what appears to be a linear relationship between the supervisors scores and their team's performance.
    
    This may indicate a need to get a better understanding of what these specific scores reflect and what they are associated with and trying to get a better understanding of how to either; 
    
    i.) better select leaders based on what traits these scores reflect or 
    
    ii.) identify inhouse training techniques that can help potential leaders better develop these traits.
    
    We can also observe a strong positive relationship between the employment span of the supervisor in question and the pay to team size ratio. From this we can assume that the more experienced the supervisor the better they become at possibly mentoring sales executives and as the team and presumably responsibilities of a supervisor grows, there is a need to review their total compentation to match their growing responsibility. To see further improvement in team performance it may be worthwhile looking into incentivizing either overall team performance (assuming this is not already happening) or offering more regular salary reviews as a supervisor's team grows. 
    
    In order to improve team performance it may also be worthwhile investing in supervisor mentoring program were less experienced supervisors leverage the expertise of more experienced supervisors to learn how to be lead their teams. 
        
    It is important to note however that the analysis carried out shows potential associations and possible causal links to team performance, more context is required to fully understand the true nature of the relationships between the features listed here and team performance. We would for example need to have more clarity on how these scores are made, how the tests are drafted, what the purpose of each test is and the accuracy of these tests.
    
    ''')
    ])
@app.callback(dash.dependencies.Output('performancetable','figure'),
             [dash.dependencies.Input('year_month', 'start_date'),
              dash.dependencies.Input('year_month', 'end_date')])
def update_table(start_date,end_date):
    performance = performance_data[(performance_data['Month'] > start_date) & (performance_data['Month'] < end_date)]
    performance = performance.drop(columns ='Unnamed: 0')
    columns = ['Month','SalesSystemCode','TITULO','SupervisorEmployeeID','Monthly Subscribers','Churned Subscribers',
               'MonthsofEmploymentRounded','Exit Date','Rental Charge','Cost to Company','Rev per CtC']
    return {
        'data': [
            go.Table(
                header=dict(values=columns,fill_color='paleturquoise',align='left'),
                cells=dict(values=[performance['Month'],performance['SalesSystemCode'],performance['TITULO'],
                                   performance['SupervisorEmployeeID'],performance['Monthly Subscribers'],
                                   performance['Churned Subscribers'],performance['MonthsofEmploymentRounded'],performance['Exit Date'],
                                   performance['Rental Charge'],performance['Cost to Company'],performance['Revenue Per CtC']],
                           fill_color='lavender', align='left'),
                )],
        'layout': go.Layout(
            title='Sales Team Performance',
            )
        }

if __name__ == '__main__':
        app.run_server(debug=True)
