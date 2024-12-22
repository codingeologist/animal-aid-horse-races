import json
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="horsedeathwatch.com - statistics",
    page_icon="🐴",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items=None
)

st.set_option("client.toolbarMode", "viewer")

with st.sidebar:
    st.image(image="images/animal_aid.png", caption="Animal Aid")
    st.page_link(page="https://www.animalaid.org.uk/donate/", label="Donate to Animal Aid 🎗️")
    st.page_link(page="https://www.horsedeathwatch.com/", label="horsedeathwatch.com")
    st.write("© www.horsedeathwatch.com, Animal Aid's Race Horse Deathwatch website")
    st.write("© codingeologist")
    st.page_link(page="https://codingeologist.github.io/", label="My website")
    st.page_link(page="https://github.com/codingeologist", label="My Github")


@st.cache_data
def get_data(filename: str):

    with open(f"data/{filename}.json", "r") as file:
        items = json.load(file)

    if "year" in filename:
        data = {item["year"]: item["count"] for item in items}
        data = pd.DataFrame.from_dict(data, orient="index").reset_index()
        data.columns = ["year", "count"]
    elif "month" in filename:
        data = {item["month"]: item["count"] for item in items}
        data = pd.DataFrame.from_dict(data, orient="index").reset_index()
        data.columns = ["month", "count"]
    elif "course" in filename:
        data = {item["racecourse"]: item["count"] for item in items}
        data = pd.DataFrame.from_dict(data, orient="index").reset_index()
        data.columns = ["racecourse", "count"]
    elif "horse" in filename:
        data = pd.DataFrame.from_dict(items, orient="columns")
    return data


@st.cache_data
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")


if __name__ == "__main__":

    yearly_casualties = get_data(filename="year_agg")
    monthly_casualties = get_data(filename="month_agg")
    course_casualties = get_data(filename="course_agg")
    horses = get_data(filename="horse_stats")

    highest_course_index = course_casualties["count"].idxmax()
    highest_year_index = yearly_casualties["count"].idxmax()
    highest_month_index = monthly_casualties["count"].idxmax()
    months = {
        0: "January",
        1: "February",
        2: "March",
        3: "April",
        4: "May",
        5: "June",
        6: "July",
        7: "August",
        8: "September",
        9: "October",
        10: "November",
        11: "December"
    }
    highest_month_text = months[highest_month_index]

    euth_count = len(horses.loc[horses["euthanised"]])
    gbr_count = len(horses.loc[horses["country"] == "GBR"])
    ire_count = len(horses.loc[horses["country"] == "IRE"])
    country_count = len(horses)

    st.write("Animal Aid started collecting horse racing casualty data since 2007. 📈")
    st.write(f"{country_count} horses have suffered from fatal and non-fatal racing injuries. 😭")
    st.write(f"{euth_count} horses were killed due to them suffering from their wounds caused by accidents on the track. 🏁")
    st.write(f"🇬🇧 {gbr_count} British horses have died so far...")
    st.write(f"🇮🇪 {ire_count} Irish horses have suffered the cruelties of racing...")
    st.write("🛑 This has to stop! 🛑")

    st.download_button(
        label="Download Full Dataset",
        data=convert_df(horses),
        file_name="horse_statistics.csv"
    )

    st.write("Yearly Horse Casualties")
    st.write("The deadliest year for horse races was {} with {} casualties.".format(yearly_casualties.loc[highest_year_index]["year"], yearly_casualties.loc[highest_year_index]["count"]))
    st.bar_chart(data=yearly_casualties, x="year", y="count")
    st.download_button(
        label="Download Yearly Statistics",
        data=convert_df(yearly_casualties),
        file_name="yearly_statistics.csv"
    )

    st.write("Monthly Horse Casualties")
    st.write("The deadliest month for horse racing is {} with {} casualties since 2007.".format(highest_month_text, monthly_casualties.loc[highest_month_index]["count"]))
    st.bar_chart(data=monthly_casualties, x="month", y="count")
    st.download_button(
        label="Download Monthly Statistics",
        data=convert_df(monthly_casualties),
        file_name="monthly_statistics.csv"
    )

    st.write("Horse Casualties by Racecourse")
    st.write("The deadliest racecourse for horse races is {} with {} casualties so far.".format(course_casualties.loc[highest_course_index]["racecourse"], course_casualties.loc[highest_course_index]["count"]))
    st.bar_chart(data=course_casualties, x="racecourse", y="count")
    st.download_button(
        label="Download Racecourse Statistics",
        data=convert_df(course_casualties),
        file_name="racecourse_statistics.csv"
    )
    