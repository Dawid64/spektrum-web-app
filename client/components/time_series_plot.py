import streamlit as st
import pandas as pd
import altair as alt
from client.logic import SESSION, Measurements


def time_series():
    col1, col2 = st.columns([1, 3])
    with col1:
        chamber_names = st.multiselect(
            "Chambers", ["Chamber-1", "Chamber-2"], default=["Chamber-1"]
        )
        parameters = st.multiselect(
            "Parameters",
            ["temperature", "humidity", "light_intensity"],
            default=["temperature", "humidity", "light_intensity"],
        )
    with SESSION() as session:
        query = session.query(Measurements).filter(
            Measurements.chamber_name.in_(chamber_names)
        )
        df = pd.read_sql(query.statement, query.session.bind)
    # st.dataframe(df, hide_index=True)

    df_long = df.melt(
        id_vars=["date", "chamber_name"],
        value_vars=parameters,  # from your multiselect
        var_name="parameter",
        value_name="value",
    )
    with col2:
        chart = (
            alt.Chart(df_long)
            .mark_line()
            .encode(
                x="date:T",
                y="value:Q",
                color=alt.Color("chamber_name:N", title="Chamber"),
                strokeDash=alt.StrokeDash("parameter:N", title="Parameter"),
                tooltip=["date:T", "chamber_name:N", "parameter:N", "value:Q"],
            )
            .properties(height=350)
        )

        st.altair_chart(chart, use_container_width=True)
