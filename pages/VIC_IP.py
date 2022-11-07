import streamlit as st
import plotly.graph_objects as go
import sqlite3

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown("# VIC_IP")
st.markdown(hide_st_style, unsafe_allow_html=True)
st.sidebar.markdown("# VIC_IP")

st.title("🐞 Bug report!")

# Using object notation


form = st.form(key="annotation")

with form:
    cols = st.columns((1, 1))
    author = cols[0].text_input("Report author:")
    bug_type = cols[1].selectbox(
        "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
    )
    description = st.text_area("Comment:")
    cols = st.columns(2)
    date = cols[0].date_input("Bug date occurrence:")
    bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
    solution = st.text_area("Solution")
    submitted = st.form_submit_button(label="Submit")

if submitted:
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS vic_bugs (id INTEGER PRIMARY kEY AUTOINCREMENT, author TEXT, bug_type TEXT, description TEXT, date TEXT, bug_severity INT, solution TEXT)')
        cur.execute("""INSERT INTO vic_bugs (author,bug_type,description,date,bug_severity,solution)
                            VALUES(?, ?, ?, ?, ?, ?)""",
                    (author, bug_type, description, date, bug_severity, solution))
        con.commit()
        st.success("Thanks! Your bug was recorded.")
        st.balloons()

expander = st.expander("See all records")
with expander:
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("select * from vic_bugs")

    rows = cur.fetchall()
    st.dataframe(rows)


# Data Set
bugs = ['404', 'Back-end',
        'Data related ', 'front-end'
        ]

with sqlite3.connect("database.db") as con:
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM vic_bugs GROUP BY bug_type')
    values = cur.fetchall()
    newVal = list(zip(*values))[0]

# The plot
fig = go.Figure(
    go.Pie(
        labels=bugs,
        values=newVal,
        hoverinfo="label+percent",
        textinfo="value"
    ))

with st.container():
    st.header("Distribution of Bugs")
    st.plotly_chart(fig)

