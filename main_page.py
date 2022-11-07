import streamlit as st
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
import plotly.graph_objects as go
import google_auth_httplib2
import httplib2

st.markdown("# PNR_1000 🎈")
st.sidebar.markdown("# PNR_1000 🎈")


SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1FFUb5e9ZwiLxh1qUKuuxwbRqUgExxj4Cz14Zb6iMeAs"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"


@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:F",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:F",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()




st.title("🐞 Bug report!")

gsheet_connector = connect_to_gsheet()

# Using object notation


form = st.form(key="annotation")

with form:
    cols = st.columns((1, 1))
    author = cols[0].text_input("Report author:")
    bug_type = cols[1].selectbox(
        "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
    )
    comment = st.text_area("Comment:")
    cols = st.columns(2)
    date = cols[0].date_input("Bug date occurrence:")
    bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
    solution = st.text_area("Solution")
    submitted = st.form_submit_button(label="Submit")

if submitted:
    add_row_to_gsheet(
        gsheet_connector,
        [[author, bug_type, comment, str(date), bug_severity, solution]],
    )
    st.success("Thanks! Your bug was recorded.")
    st.balloons()

expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))

# Data Set
bugs = ['404', 'Data related',
        'Back-end ', 'front-end'
        ]

pre_values = get_data(gsheet_connector)
values = pre_values['bug type']
final_values = values.value_counts()
print(values.values)
# The plot
fig = go.Figure(
    go.Pie(
        labels=bugs,
        values=final_values,
        hoverinfo="label+percent",
        textinfo="value"
    ))

with st.container():
    st.header("Distribution of Bugs")
    st.plotly_chart(fig)