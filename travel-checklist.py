import streamlit as st
import pandas as pd

# Load data from Excel
def load_data():
    return pd.read_excel('travel_packing_list.xlsx')

def save_data(df):
    df.to_excel('travel_packing_list.xlsx', index=False)

def main():
    st.title("Interactive Checklist")

    # Load data
    df = load_data()

    # Initialize session state for edit inputs
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {}

    # Filter options
    filter_option = st.radio("Filter items:", ("All", "Ticked", "Unticked"))

    # Display categories
    categories = df['Category'].unique()
    for category in categories:
        st.header(category)
        category_items = df[df['Category'] == category]

        # Apply filter
        if filter_option == "Ticked":
            category_items = category_items[category_items['Status'] == 1]
        elif filter_option == "Unticked":
            category_items = category_items[category_items['Status'] == 0]

        # Display items with interactive buttons
        for idx, row in category_items.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                if st.session_state.edit_mode.get(idx, False):
                    new_name = st.text_input("Edit Item Name", value=row['Item Name'], key=f"edit_input_{idx}")
                else:
                    st.write(row['Item Name'])
            with col2:
                if st.button("Tick" if row['Status'] == 0 else "Untick", key=f"tick_{idx}"):
                    df.loc[idx, 'Status'] = 1 if row['Status'] == 0 else 0
                    save_data(df)
                    st.rerun()
            with col3:
                button_label = "Save" if st.session_state.edit_mode.get(idx, False) else "Edit"
                if st.button(button_label, key=f"edit_save_{idx}"):
                    if st.session_state.edit_mode.get(idx, False):
                        if f"edit_input_{idx}" in st.session_state:
                            df.loc[idx, 'Item Name'] = st.session_state[f"edit_input_{idx}"]
                            save_data(df)
                        st.session_state.edit_mode[idx] = False
                    else:
                        st.session_state.edit_mode[idx] = True
                    st.rerun()
            with col4:
                if st.button("Delete", key=f"delete_{idx}"):
                    df = df.drop(idx)
                    save_data(df)
                    st.rerun()

    # Add new category and item
    st.sidebar.header("Add New Category")
    new_category = st.sidebar.text_input("Category Name")
    new_category_item = st.sidebar.text_input("Item Name for New Category")
    if st.sidebar.button("Add Category"):
        if new_category and new_category_item and new_category not in categories:
            new_row = pd.DataFrame({"Category": [new_category], "Item Name": [new_category_item], "Status": [0]})
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.rerun()

    # Add new item
    st.sidebar.header("Add New Item")
    selected_category = st.sidebar.selectbox("Select Category", categories)
    new_item = st.sidebar.text_input("Item Name")
    if st.sidebar.button("Add Item"):
        if selected_category and new_item:
            new_row = pd.DataFrame({"Category": [selected_category], "Item Name": [new_item], "Status": [0]})
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.rerun()

if __name__ == "__main__":
    main()
