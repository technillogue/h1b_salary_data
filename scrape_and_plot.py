import requests
import pandas as pd
import seaborn
from bs4 import BeautifulSoup as Soup

base_url = "https://h1bdata.info/index.php?em=&job=Software+Engineer&"


def get_data(city: str = "BOSTON") -> pd.DataFrame:
    print("sending requests")
    pages = [
        requests.get(base_url + f"city={city}&year={year}").text
        for year in range(2012, 2021)
    ]
    print("got data")
    tables = [str(Soup(page, "lxml").find("table")) for page in pages]
    salaries = [
        df["BASE SALARY"].to_frame(name="salary")
        for df in pd.read_html("\n".join(tables))
    ]
    for i, salary in enumerate(salaries):
        salary["year"] = i + 2012
    all_salaries = pd.concat(salaries)
    return all_salaries


def plot(salaries: pd.DataFrame) -> None:
    boxplot = seaborn.boxplot(x="year", y="salary", data=salaries).set_title("H1B software engineer base salaries in Boston")
    boxplot.get_figure().savefig("boxplot.png")
    last_year = salaries[salaries["year"] == 2020]
    displot = seaborn.displot(last_year, x="salary", kind="kde")
    #displot.axvline(last_year.mean())
    displot.fig.savefig("2020_distribution.png")


if __name__ == "__main__":
    try:
        data = pd.read_csv("salaries.csv")
    except FileNotFoundError:
        data = get_data()
        data.to_csv("salaries.csv")
    plot(data)
