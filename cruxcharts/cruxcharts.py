from io import BytesIO

import pandas as pd
import reflex as rx


class Ascent(rx.Base):
    name: str
    grade: str
    date: str


class State(rx.State):
    logbook: str
    ascents: list[Ascent] = []

    @rx.event
    async def handle_upload(self, upload_files: list[rx.UploadFile]):
        data = await upload_files[0].read()
        df = pd.read_excel(BytesIO(data))
        self.logbook = upload_files[0].name
        self.load_logbook(df)

    @rx.event
    def load_logbook(self, logbook_df: pd.DataFrame):
        self.ascents = [Ascent(name=row["Climb name"], grade=row["Grade"], date=row["Date"])
                        for (i, row) in logbook_df.iterrows()]



def show_ascent(ascent: Ascent):
    return rx.table.row(
            rx.table.cell(ascent.name),
            rx.table.cell(ascent.grade),
            rx.table.cell(ascent.date),
        )


def upload_section():
    return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    rx.icon("arrow-up-from-line", size=26),
                    rx.text("Upload Logbook", size="4"),
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Upload your logbook"),
                rx.vstack(
                    rx.upload(
                        rx.button("Select file"),
                        id="logbook_upload",
                        border="0px",
                        padding="0em",
                        ),
                    rx.selected_files("logbook_upload"),
                ),
                rx.dialog.close(
                    rx.button(
                        "Upload",
                        on_click=State.handle_upload(
                            rx.upload_files(upload_id="logbook_upload")
                        ),
                    ),
                )
            )
        )


def table_section():
    return rx.cond(
        State.ascents.length() > 0,
        rx.vstack(
            rx.heading(State.logbook),
            rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Grade"),
                            rx.table.column_header_cell("Date"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(State.ascents, show_ascent)
                    ),
            variant="surface",
            size="3",
            )
        )
    )


def index() -> rx.Component:
    return rx.vstack(
            rx.heading("CruxCharts", size="9"),
            upload_section(),
            table_section()
           )


app = rx.App()
app.add_page(index)
