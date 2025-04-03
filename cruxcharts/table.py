import reflex as rx

from .common import State, Ascent


def table_section():
    return rx.cond(
        State.ascents.length() > 0,
        rx.vstack(
            rx.heading(State.logbook_file),
            rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Grade"),
                            rx.table.column_header_cell("Style"),
                            rx.table.column_header_cell("Date"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.get_current_page,
                            show_ascent
                        ),
                    ),
                    variant="surface",
                    size="3",
                    width="50em",
            ),
            rx.hstack(
                _num_rows_view(),
                _pagination_view(),
            ),
        ),
    )


def show_ascent(ascent: Ascent):
    return rx.table.row(
            rx.table.cell(ascent.name,
                          min_width="13em",
                          max_width="13em"),
            rx.table.cell(ascent.grade,
                          min_width="7em",
                          max_width="7em"),
            rx.table.cell(ascent.style,
                          min_width="10em",
                          max_width="10em"),
            rx.table.cell(ascent.date,
                          min_width="20em",
                          max_width="20em"),
        )


def _num_rows_view() -> rx.Component:
    return rx.form.root(
        rx.hstack(
            rx.input(
                name="limit",
                type="number",
                placeholder="Num rows",
            ),
            rx.button("Set", type="submit"),
            margin_top="1em",
            margin_left="1em",
        ),
        on_submit=State.handle_set_limit,
    )


def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(State.page_number),
                f" of {State.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=State.first_page,
                    opacity=rx.cond(State.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(State.page_number == 1,
                                         "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=State.prev_page,
                    opacity=rx.cond(State.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(State.page_number == 1,
                                         "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=State.next_page,
                    opacity=rx.cond(State.page_number == State.total_pages,
                                    0.6, 1),
                    color_scheme=rx.cond(
                        State.page_number == State.total_pages,
                        "gray", "accent"
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=State.last_page,
                    opacity=rx.cond(State.page_number == State.total_pages,
                                    0.6, 1),
                    color_scheme=rx.cond(
                        State.page_number == State.total_pages,
                        "gray", "accent"
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="30em",
            justify="end",
        ),
    )
