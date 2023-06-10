import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io
import seaborn as sns

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))
def subset_df(df: pd.DataFrame, column_name: str) -> pd.Series:
    subset_col = df[column_name]
    return subset_col

web_apps = "Exploratory Data Analysis"  # Example web_apps value for testing

if web_apps == "Exploratory Data Analysis":
    uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
      df = pd.read_csv(uploaded_file)
      # Display the number of rows and columns
      num_rows = len(df)
      num_cols = len(df.columns)
      st.write(f"Number of Rows: {num_rows}")
      st.write(f"Number of Columns: {num_cols}")

      # Count the number of categorical, numerical, and boolean variables
      categorical_cols = df.select_dtypes(include="object").columns
      numerical_cols = df.select_dtypes(include=["int", "float"]).columns
      boolean_cols = df.select_dtypes(include="bool").columns
      num_categorical = len(categorical_cols)
      num_numerical = len(numerical_cols)
      num_boolean = len(boolean_cols)
      st.write(f"Number of Categorical Variables: {num_categorical}")
      st.write(f"Number of Numerical Variables: {num_numerical}")
      st.write(f"Number of Boolean Variables: {num_boolean}")

      show_df = st.checkbox("Show Data Frame", key="disabled")

      if 'df' in locals() and show_df:
            st.write(df)

      if 'df' in locals():
            selected_column = st.selectbox("Select a column", df.columns)

            if selected_column in df.columns:
              subset_column = subset_df(df, selected_column)
                  
              if isinstance(subset_column[1], (int, float)):
                summary_table = subset_column.describe()
                st.table(summary_table)

                fig = plt.figure()
                sns.kdeplot(subset_column)
                st.pyplot(fig)
              else:
                proportions = subset_column.value_counts(normalize=True)
                st.table(proportions.to_frame(name="Proportion"))    

                fig, ax = plt.subplots()
                sns.barplot(x=proportions.index, y=proportions.values, ax=ax)
                ax.set_xlabel(selected_column)
                ax.set_ylabel("Proportion")
                ax.set_title("Bar Plot of Proportions")
                st.pyplot(fig)

            else:
              st.error("Invalid column selected")

      if show_df:
          st.write(df)

      column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

      if column_type == "Numerical":
         numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 0.5)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )