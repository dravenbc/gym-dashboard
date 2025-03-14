import streamlit as st
import pandas as pd
import altair as alt

st.title("DBC Gym Dashboard")

#pull data from raw CSV link on github, clean, and sort it
df = pd.read_csv('https://raw.githubusercontent.com/dravenbc/gym-dashboard/refs/heads/main/data/strong.csv', delimiter=';', on_bad_lines='skip')
df.columns = df.columns.str.strip()
df = df.sort_values("Date")

# create a field converting weight from kg to pounds:
df["Pounds"] = (df["Weight (kg)"] * 2.20462).round(1)

# create a field that calculates volume:
df["Volume"] = df["Pounds"] * df["Reps"]

df["Date"] = pd.to_datetime(df["Date"])

#show the raw table data:
with st.expander("Show Data Table"):
    st.dataframe(df, use_container_width=True)

# Check if 'Exercise Name' exists
if "Exercise Name" in df.columns:
    # Create a filter dropdown
    exercise_list = sorted(df["Exercise Name"].dropna().unique())
    selected_exercise = st.selectbox("Select an Exercise:", list(exercise_list))

    # Filter data based on selection
    df = df[df["Exercise Name"] == selected_exercise]

# Group by Workout # and sum Volume
if "Date" in df.columns:
    volume_summary = df.groupby("Date")["Volume"].sum().reset_index()

    # Create Altair Chart for Volume per Workout
    volume_chart = (
        alt.Chart(volume_summary)
        .mark_line()
        .encode(
            x=alt.X("Date:T", axis=alt.Axis(
                format = "%b %Y",
                tickCount = 'week',
                labelAngle = 45
            )),
            y="Volume:Q",
            tooltip=["Date", "Volume"]
        )
        
    ).properties(
        title=alt.TitleParams(
            text = "Total Volume per Workout",
            anchor = 'middle',
            fontSize = 20
        )

        )

    # Display Chart
    st.altair_chart(volume_chart, use_container_width=True)
else:
    st.error("The dataset does not contain the 'Date' column.")

# find the max weight for each exercise in each workout:
max_weight_summary = df.groupby("Date")['Pounds'].max().reset_index()

#plot the max weights on a line chart:
# Create Altair Chart for max weight per Workout
max_weight_chart = (
    alt.Chart(max_weight_summary)
    .mark_line()
    .encode(
        x="Date:T",  # Treat Date as time
        y="Pounds:Q",
        tooltip=["Date", "Pounds"]
    )
    .properties(
        title=alt.TitleParams(
            text = "Max Weight per Workout",
            anchor = 'middle',
            fontSize = 20
        )
    )
)

# Display Chart
st.altair_chart(max_weight_chart, use_container_width=True)

# Find the latest workout number for the selected exercise
latest_workout_number = df[df['Exercise Name'] == selected_exercise]['Workout #'].max()
# Filter for only that exercise and its latest workout number
latest_summary = df[(df['Exercise Name'] == selected_exercise) & (df['Workout #'] == latest_workout_number)]
latest_summary = latest_summary.sort_values(by="Set Order", ascending=True)
st.subheader(f"Latest Workout Summary for {selected_exercise}")
st.dataframe(latest_summary, use_container_width=True, column_order=("Set Order", "Pounds", "Reps"))