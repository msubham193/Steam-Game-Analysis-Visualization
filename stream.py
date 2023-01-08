import streamlit as st
import hydralit_components as hc
import plotly.express as px
import pandas as pd
from streamlit_card import card


# Using object notation
st.set_page_config(page_title="Sales Dashboard", layout="wide")


menu_data = [
    {'icon': "far fa-copy", 'label': "Left End"},
    {'id': 'Copy', 'icon': "🐙", 'label': "Copy"},
    {'icon': "fa-solid fa-radar", 'label': "Dropdown1", 'submenu': [{'id': ' subid11', 'icon': "fa fa-paperclip", 'label': "Sub-item 1"}, {
        'id': 'subid12', 'icon': "💀", 'label': "Sub-item 2"}, {'id': 'subid13', 'icon': "fa fa-database", 'label': "Sub-item 3"}]},
    {'icon': "far fa-chart-bar", 'label': "Chart"},  # no tooltip message
    {'id': ' Crazy return value 💀', 'icon': "💀", 'label': "Calendar"},
    {'icon': "fas fa-tachometer-alt", 'label': "Dashboard",
        'ttip': "I'm the Dashboard tooltip!"},  # can add a tooltip message
    {'icon': "far fa-copy", 'label': "Right End"},
    {'icon': "fa-solid fa-radar", 'label': "Dropdown2",
        'submenu': [{'label': "Sub-item 1", 'icon': "fa fa-meh"}, {'label': "Sub-item 2"}, {'icon': '🙉', 'label': "Sub-item 3", }]},
]

over_theme = {'txc_inactive': '#FFFFFF'}

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    # will show the st hamburger as well as the navbar now!
    hide_streamlit_markers=True,
    sticky_nav=True,  # at the top or not
    sticky_mode='pinned',  # jumpy or not-jumpy, but sticky or pinned
)


st.title(":bar_chart: Steam Game Analysis Dashboard")
st.markdown("##")


def cleaning():
    data = pd.read_csv("steam.csv")
    data = data.head(2000)
    data = data.drop(['appid', 'english', 'average_playtime',
                     'median_playtime', 'owners', 'steamspy_tags', 'categories'], axis=1)
    for i, val in data['genres'].iteritems():
        data['genres'][i] = val.split(';')[0]
    return data


st.header("Dataset")
s = cleaning()
st.dataframe(s.head(3))


col1, col2, col3 = st.columns(3)

with col1:
    st.header("No. of Games")
    st.subheader(s["name"].nunique())
with col2:
    st.header("No. of Genres")
    st.subheader(s["genres"].nunique())
with col3:
    st.header("Highest Rating")
    st.subheader("1200")


d = s.groupby(by=["genres"]).size().reset_index(name="counts")
fig2 = px.bar(data_frame=d, x="genres", y="counts",text_auto='.2s',)


fig1 = px.scatter(s.head(40), x="name", y="price", color="name",
                  size="price", title="Highest price of the game")

d = s.groupby(by=["platforms"]).size().reset_index(name="counts")
fig3 = px.bar(data_frame=d, x="platforms", y="counts", color="platforms",text_auto='.2s',
              title="Platform Based Games")


# devloper = data['developer'].value_counts()
d = s.groupby(by=["developer"]).size().reset_index(name="counts")
fig4 = px.bar(data_frame=d.head(30), x="developer", y="counts", color="developer",text_auto='.2s',
              title="Top 20 developer")

fig5 = px.box(s, y="price", title="Boxplot Price")


free, not_free = s[s['price'] ==
                   0].shape[0], s[s['price'] != 0].shape[0]
label = ['Free Games', 'Paid Games']
fig6 = px.pie(values=[free, not_free], names=label)

fig8 = px.pie(s.head(20),values='positive_ratings',names='name',title="Postive ratings per games")

fig7 = px.line(s.head(30), x="name", y="price", markers=True)

fig9 = px.pie(s.head(30),values='achievements',names='name',title="Achivements of games")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Scatterplot", "Barchart", "Boxplot", "Piechart", "Lineplot"])


with tab1:
    st.subheader("Bubble chart Price vs Name")
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)


with tab2:

    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

with tab3:

    st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

with tab4:
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)
    st.plotly_chart(fig8, theme="streamlit", use_container_width=True)
    st.plotly_chart(fig9, theme="streamlit", use_container_width=True)

with tab5:
    st.plotly_chart(fig7, theme="streamlit", use_container_width=True)
