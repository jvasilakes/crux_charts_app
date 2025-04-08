from io import BytesIO
from typing import List

import reflex as rx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


ASCENT2COLOR = {
    "Solo": "#ffffb3",
    "O/S": "#8dd3c7",
    "β": "#80b1d3",
    "Redpoint": "#fb8072",
    "Repeat": "#b3b3b3"
}


DIFFICULTY2COLOR = {
    'EASY': '#66c2a5',
    'MODERATE': '#ff9933',
    'HARD': '#b30000',
    'VERYHARD': '#66ccff',
    'ELITE': '#e6e6e6'}


HUECO2FONT = {
    "VB": ["f2", "f2+", "f3"],
    "V0": ["f3+", "f4", "f4+"],
    "V1": ["f5"],
    "V2": ["f5+"],
    "V3": ["f6A", "f6A+"],
    "V4": ["f6B", "f6B+"],
    "V5": ["f6C", "f6C+"],
    "V6": ["f7A"],
    "V7": ["f7A+"],
    "V8": ["f7B", "f7B+"],
    "V9": ["f7C"],
    "V10": ["f7C+"],
    "V11": ["f8A"]
}


GRADE2DIFFICULTY = {}
for (i, (hueco, fonts)) in enumerate(HUECO2FONT.items()):
    if i < 2:
        diff = "EASY"
    elif i < 4:
        diff = "MODERATE"
    elif i < 7:
        diff = "HARD"
    elif i < 11:
        diff = "VERYHARD"
    else:
        diff = "ELITE"
    GRADE2DIFFICULTY[hueco] = diff
    for font in fonts:
        GRADE2DIFFICULTY[font] = diff


FONT2HUECO = {}
for (hueco, fonts) in HUECO2FONT.items():
    for f in fonts:
        FONT2HUECO[f] = hueco


class Ascent(rx.Base):
    name: str
    grade: str
    stars: int
    date: str
    style: str
    _type: str
    crag: str

    @classmethod
    def from_row(cls, row):
        return cls(
            name=row["Climb name"],
            grade=row["Grade"],
            stars=row["Stars"],
            date=row["Date"],
            style=cls.format_style(row["Style"]),
            _type=row["Grade Type"],
            crag=row["Crag name"],
        )

    @classmethod
    def format_style(cls, style_str):
        if "Solo" in style_str:
            style = "Solo"
        else:
            style = style_str.split()[-1]
            if style in ["Sent", '-', "rpt"]:
                style = 'Redpoint'
            if style == 'x':
                style = "Redpoint"
        return style


class LogbookState(rx.State):
    logbook_file: str  # The name of the file
    logbook_df: pd.DataFrame = None  # The raw DataFrame
    ascents: list[Ascent] = []  # Ascent instances
    visible_ascents: list[int] = []  # Indices of Ascents to show
    ascent_type: str = "All"
    total_items: int = 0
    offset: int = 0  # Current row in full table
    limit: int = 12  # Number of rows visible at a time
    figure: go.Figure = go.Figure()

    @rx.event
    def create_figure(self):
        if self.logbook_df is not None:
            df = self.logbook_df.loc[self.visible_ascents]
            self.figure = px.histogram(
                df,
                y="Grade",
                color="Style",
                width=600,
                height=740,
            )
            self.figure.update_layout(yaxis_title=None, xaxis_title=None)

    @rx.event
    async def handle_upload(self, upload_files: list[rx.UploadFile]):
        data = await upload_files[0].read()
        try:
            df = pd.read_excel(BytesIO(data))
        except:
            raise ValueError("Unable to load file. Are you sure its XLSX?")

        all_grades = []
        all_stars = []
        for (grade, stars) in df["Grade"].apply(self.get_grade_and_stars):
            all_grades.append(grade)
            all_stars.append(stars)
        df["Grade"] = all_grades
        df["Stars"] = all_stars
        self.logbook_file = upload_files[0].name
        self.logbook_df = df
        self.get_ascents(df)
        self.filter_logbook()

    @staticmethod
    def get_grade_and_stars(grade):
        splitted = grade.rsplit(maxsplit=1)
        if len(splitted) == 1:
            return grade.strip(), 0
        elif '*' not in splitted[-1]:
            return grade.strip(), 0
        return splitted[0].strip(), len(splitted[1])

    @rx.event
    def get_ascents(self, logbook_df: pd.DataFrame):
        self.ascents = [Ascent.from_row(row)
                        for (_, row) in logbook_df.iterrows()]

    @rx.event
    def filter_logbook(self):
        if self.ascent_type == "All":
            idxs = list(range(len(self.ascents)))
        else:
            filtered = self.logbook_df[self.logbook_df["Grade Type"] == self.ascent_type]  # noqa
            idxs = filtered.index
        self.visible_ascents = list(idxs)
        self.total_items = len(self.visible_ascents)
        self.create_figure()

    @rx.event
    def set_ascent_type(self, value: str):
        self.ascent_type = value
        if self.logbook_df is not None:
            self.filter_logbook()
            self.offset = 0  # reset the page number

    @rx.event
    def handle_set_limit(self, form_data: dict):
        i = int(form_data["limit"])
        self.limit = i

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> List[Ascent]:
        start_index = self.offset
        end_index = start_index + self.limit
        ascents_to_show = [a for (i, a) in enumerate(self.ascents)
                           if i in self.visible_ascents]
        return ascents_to_show[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit
