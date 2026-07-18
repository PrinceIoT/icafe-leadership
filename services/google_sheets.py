import os
import json
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------------------------------------
# Google API Scopes
# ---------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ---------------------------------------------------------
# Load Credentials
# Local PC -> credentials.json
# Render -> GOOGLE_CREDENTIALS Environment Variable
# ---------------------------------------------------------

if "GOOGLE_CREDENTIALS" in os.environ:

    credentials = json.loads(
        os.environ["GOOGLE_CREDENTIALS"]
    )

    creds = Credentials.from_service_account_info(
        credentials,
        scopes=SCOPES
    )

else:

    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

client = gspread.authorize(creds)

# ---------------------------------------------------------
# Open Spreadsheet
# Local -> Spreadsheet Name
# Render -> Spreadsheet ID
# ---------------------------------------------------------

if "SPREADSHEET_ID" in os.environ:

    spreadsheet = client.open_by_key(
        os.environ["SPREADSHEET_ID"]
    )

else:

    spreadsheet = client.open("iCafe Leadership")

events_sheet = spreadsheet.worksheet("Events")
leaders_sheet = spreadsheet.worksheet("Leaders")
volunteers_sheet = spreadsheet.worksheet("Form Responses 1")


# ---------------------------------------------------------
# Get All Events
# ---------------------------------------------------------

def get_events():

    event_rows = events_sheet.get_all_records()

    volunteer_rows = volunteers_sheet.get_all_records()

    events = []

    for event in event_rows:

        helpers = []

        for volunteer in volunteer_rows:

            volunteer_event = volunteer.get(
                "Which event would you like to help with?",
                ""
            ).strip()

            if volunteer_event == event["Event"]:

                helper_name = volunteer.get(
                    "Full Name",
                    ""
                ).strip()

                helper_role = volunteer.get(
                    "Which role would you like?",
                    ""
                ).strip()

                helpers.append(
                    f"{helper_name} - {helper_role}"
                )

        events.append({

            "id": event["ID"],

            "date": event["Date"],

            "name": event["Event"],

            
            "mc": event["MC"],

            

            "devotion": event["Devotion"],

            "food": event["Food"],

            "helpers": helpers

        })

    return events


# ---------------------------------------------------------
# Get Leader Names
# ---------------------------------------------------------

def get_leaders():

    rows = leaders_sheet.get_all_records()

    leaders = []

    for row in rows:

        leaders.append(row["Name"])

    return leaders


# ---------------------------------------------------------
# Get Volunteer Responses
# ---------------------------------------------------------

def get_helpers():

    rows = volunteers_sheet.get_all_records()

    return rows


# ---------------------------------------------------------
# Get One Event
# ---------------------------------------------------------

def get_event(event_id):

    rows = events_sheet.get_all_records()

    for row in rows:

        if str(row["ID"]) == str(event_id):

            return row

    return None


# ---------------------------------------------------------
# Update Event Assignments
# ---------------------------------------------------------

def update_event(event_id, mc,  devotion, food):

    cell = events_sheet.find(str(event_id))

    row = cell.row

    events_sheet.update(f"D{row}", [[mc]])
    
    events_sheet.update(f"F{row}", [[devotion]])
    events_sheet.update(f"G{row}", [[food]])