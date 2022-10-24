import streamlit as st

def col_displayer(list, wcol=4):
    ncol = len(list)
    cols = st.columns(ncol)

    for i in range(ncol):
        col = cols[i%wcol]
        col.write(f"{list[i]}")

    return cols