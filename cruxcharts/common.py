from io import BytesIO
from typing import List

import reflex as rx
import pandas as pd


class Ascent(rx.Base):
    name: str
    grade: str
    date: str
    style: str
    _type: str

    @classmethod
    def from_row(cls, row):
        return cls(
            name=row["Climb name"],
            grade=row["Grade"],
            date=row["Date"],
            style=row["Style"],
            _type=row["Grade Type"],
        )


class State(rx.State):
    logbook_file: str  # The name of the file
    logbook_df: pd.DataFrame = None  # The raw DataFrame
    ascents: list[Ascent] = []  # Ascent instances
    visible_ascents: list[Ascent] = []  # What to actually show
    ascent_type: str = "Bouldering"
    total_items: int = 0
    offset: int = 0  # Current row in full table
    limit: int = 12  # Number of rows visible at a time

    @rx.event
    async def handle_upload(self, upload_files: list[rx.UploadFile]):
        data = await upload_files[0].read()
        try:
            df = pd.read_excel(BytesIO(data))
        except:
            raise ValueError("Unable to load file. Are you sure its XLSX?")
        self.logbook_file = upload_files[0].name
        self.logbook_df = df
        self.get_ascents(df)
        self.filter_logbook()

    @rx.event
    def get_ascents(self, logbook_df: pd.DataFrame):
        self.ascents = [Ascent.from_row(row)
                        for (_, row) in logbook_df.iterrows()]

    @rx.event
    def filter_logbook(self):
        filtered = self.logbook_df[self.logbook_df["Grade Type"] == self.ascent_type]  # noqa
        visible_ascents = [ascent for (i, ascent) in enumerate(self.ascents)
                           if i in filtered.index]
        self.visible_ascents = visible_ascents
        self.total_items = len(self.visible_ascents)

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
        return self.visible_ascents[start_index:end_index]

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
