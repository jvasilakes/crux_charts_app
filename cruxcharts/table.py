import reflex as rx

from .common import LogbookState, Ascent


def table_section():
    return rx.cond(
        LogbookState.ascents.length() > 0,
        rx.vstack(
            rx.heading(LogbookState.logbook_file),
            rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Grade"),
                            rx.table.column_header_cell(rx.icon("star")),
                            rx.table.column_header_cell("Style"),
                            rx.table.column_header_cell("Date"),
                            rx.table.column_header_cell("Crag"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            LogbookState.get_current_page,
                            show_ascent
                        ),
                    ),
                    variant="surface",
                    size="3",
                    width="40em",
            ),
            rx.flex(
                _num_rows_view(),
                _pagination_view(),
            ),
        ),
    )


def show_ascent(ascent: Ascent):
    stars = rx.match(
        ascent.stars,
        (1, rx.center(rx.icon("star", size=15))),
        (2, rx.hstack(rx.icon("star", size=15),
                      rx.icon("star", size=15),
                      spacing="0")
         ),
        (3, rx.fragment(
                rx.center(rx.icon("star", size=12)),
                rx.center(
                    rx.hstack(rx.icon("star", size=12),
                              rx.icon("star", size=12),
                              spacing="0"),
                ),
                spacing="0",
            )
         )
    )
    ukc_search = "https://www.ukclimbing.com/logbook/search/?sort=score&query="
    search_str = f'"{ascent.name}" {ascent.crag}'
    search_url = ukc_search + search_str
    name_and_search = rx.hstack(rx.text(ascent.name),
                                rx.hover_card.root(
                                    rx.hover_card.trigger(
                                        rx.link(
                                            rx.icon("external-link", size=15),
                                            href=search_url, is_external=True
                                        ),
                                    ),
                                    rx.hover_card.content(
                                        rx.text("View on UKC"),
                                    ),
                                ),
                                spacing="1"
                            )
    return rx.table.row(
            rx.table.cell(name_and_search,
                          min_width="18em",
                          max_width="18em"),
            rx.table.cell(ascent.grade,
                          min_width="6em",
                          max_width="6em"),
            rx.table.cell(stars,
                          min_width="3em",
                          max_width="3em"),
            rx.table.cell(ascent.style,
                          min_width="7em",
                          max_width="7em"),
            rx.table.cell(ascent.date,
                          min_width="7em",
                          max_width="7em"),
            rx.table.cell(ascent.crag,
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
                width="6em",
            ),
            rx.button("Set",
                      type="submit",
                      variant="soft",
                      ),
            margin_top="1em",
            margin_left="1em",
        ),
        on_submit=LogbookState.handle_set_limit,
    )


def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(LogbookState.page_number),
                f" of {LogbookState.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=LogbookState.first_page,
                    opacity=rx.cond(LogbookState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(LogbookState.page_number == 1,
                                         "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=LogbookState.prev_page,
                    opacity=rx.cond(LogbookState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(LogbookState.page_number == 1,
                                         "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=LogbookState.next_page,
                    opacity=rx.cond(LogbookState.page_number == LogbookState.total_pages,
                                    0.6, 1),
                    color_scheme=rx.cond(
                        LogbookState.page_number == LogbookState.total_pages,
                        "gray", "accent"
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=LogbookState.last_page,
                    opacity=rx.cond(LogbookState.page_number == LogbookState.total_pages,
                                    0.6, 1),
                    color_scheme=rx.cond(
                        LogbookState.page_number == LogbookState.total_pages,
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
            justify="start",
        ),
    )
