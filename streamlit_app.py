import streamlit as st
import pandas as pd
import altair as alt

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

df = pd.read_csv('https://raw.githubusercontent.com/dravenbc/gym/refs/heads/main/strong5875123372966107080.csv', delimiter=';', on_bad_lines='skip')
df.columns = df.columns.str.strip()
df = df.sort_values("Date")



df["Pounds"] = (df["Weight (kg)"] * 2.20462).round(1)

df["Volume"] = df["Pounds"] * df["Reps"]




df["Date"] = pd.to_datetime(df["Date"])


st.dataframe(df, use_container_width=True)

# Check if 'Exercise Name' exists
if "Exercise Name" in df.columns:
    # Create a filter dropdown
    exercise_list = sorted(df["Exercise Name"].dropna().unique())
    selected_exercise = st.selectbox("Select an Exercise:", ["All"] + list(exercise_list))

    # Filter data based on selection
    if selected_exercise != "All":
        df = df[df["Exercise Name"] == selected_exercise]

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="Date:T",
        y="Reps:Q",
        tooltip=["Date", "Reps"]
    )
    .properties(title="Line Chart Example")
)

# Display Chart in Streamlit
st.altair_chart(chart, use_container_width=True)

# Group by Workout # and sum Volume
if "Date" in df.columns:
    volume_summary = df.groupby("Date")["Volume"].sum().reset_index()

    # Create Altair Chart for Volume per Workout
    volume_chart = (
        alt.Chart(volume_summary)
        .mark_bar()
        .encode(
            x="Date:T",  # Treat Date as time
            y="Volume:Q",
            tooltip=["Date", "Volume"]
        )
        .properties(title=f"Total Volume per Workout for {selected_exercise}")
    )

    # Display Chart
    st.altair_chart(volume_chart, use_container_width=True)
else:
    st.error("The dataset does not contain the 'Date' column.")
