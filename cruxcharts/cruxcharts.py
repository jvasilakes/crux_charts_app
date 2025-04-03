import reflex as rx

from .common import State
from .table import table_section


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
                        "Log in to UKC, navigate to your logbook, and click the 'Download' button in the upper right",  # noqa
                        as_="p"),
                    rx.center(
                        rx.image(src="./ukc_download.png",
                                 width=400, height="auto")
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
                                on_click=rx.clear_selected_files("logbook_upload"),  # noqa
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


def ascent_type_section():
    return rx.select(
        ["Bouldering", "Trad", "Sport"],
        value=State.ascent_type,
        on_change=State.set_ascent_type
    )


def index() -> rx.Component:
    return rx.vstack(
            rx.heading("CruxCharts", size="9"),
            rx.hstack(
                upload_section(),
                ascent_type_section(),
                spacing="3",
            ),
            table_section()
           )


app = rx.App()
app.add_page(index)
