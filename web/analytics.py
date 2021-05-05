import plotly.graph_objects as go
import plotly.express as px

def plot_gender_stroke(df):
    len_df = len(df)
    len_female = len(df[df["gender"]=="Female"])
    len_male = len_df - len_female
    male_stroke = len(df.loc[(df["gender"]=="Male")&(df["stroke"]==1)])
    female_stroke = len(df.loc[(df["gender"]=="Female") & (df["stroke"]==1)])
    male_healthy = len_male - male_stroke
    female_healthy = len_female - female_stroke
    print(male_stroke, female_stroke, female_healthy, male_healthy)

    values = [female_healthy, female_stroke, male_healthy, male_stroke]
    labels = ["Healthy Womans", "Female Stroke", "Healthy Mans", "Male Stroke"]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    return fig

def plot_scatter_bmi_glu(data, target_feature):
    fig = px.scatter(data, x="bmi", y="avg_glucose_level", color=target_feature, hover_name=target_feature,
                     log_x=True, size_max=15
                     )

    fig.update_layout(width=1000)
    return fig