import reflex as rx
import plotly.express as px

from .common import LogbookState


def plot_section():
    return (
        rx.cond(
            LogbookState.logbook_df != None,
            rx.plotly(
                data=LogbookState.figure,
                on_mount=LogbookState.create_figure(),
            ),
        ),
    )
