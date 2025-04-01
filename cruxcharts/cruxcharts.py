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
        try:
            df = pd.read_excel(BytesIO(data))
        except:
            raise ValueError("Unable to load file. Are you sure its XLSX?")
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


def help_dialog():
    return rx.dialog.root(
        rx.vstack(
            rx.dialog.trigger(
                rx.icon("circle-help", size=20)
            ),
            rx.dialog.content(
                rx.flex(
                    rx.center(
                        rx.dialog.title("Downloading your UKC logbook")
                    ),
                    rx.dialog.close(
                        rx.button(
                            "x",
                            variant="soft",
                            color_scheme="gray"),
                    ),
                spacing="3",
                justify="center",
                ),
                rx.flex(
                    rx.text(
                        "Log in to UKC, navigate to your logbook, and click the 'Download' button in the upper right",
                        as_="p"),
                    rx.center(
                        rx.image(src="./ukc_download.png", width=400, height="auto")
                    ),
                spacing="2",
                direction="column",
                ),
            ),
        ),
        max_width="450px",
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
                rx.flex(
                    rx.flex(
                        rx.center(
                            rx.dialog.title("Upload your logbook"),
                        ),
                        help_dialog(),
                        spacing="9",
                        direction="row",
                    ),
                    rx.flex(
                        rx.upload(
                            rx.button("Select file"),
                            id="logbook_upload",
                            border="0px",
                            padding="0em",
                        ),
                        rx.center(
                            rx.selected_files("logbook_upload"),
                        ),
                        direction="column",
                        spacing="2",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                on_click=rx.clear_selected_files("logbook_upload"),
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Upload",
                                on_click=State.handle_upload(
                                    rx.upload_files(upload_id="logbook_upload")
                                ),
                            ),
                        ),
                    spacing="2",
                    justify="center",
                    ),
                spacing="3",
                direction="column",
                ),
            max_width="350px",
            ),
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
