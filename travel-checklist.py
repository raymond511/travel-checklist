import streamlit as st
import pandas as pd

# Load data from Excel
def load_data():
    return pd.read_excel('travel_packing_list.xlsx')

def save_data(df):
    print(df)
    print('saved')
    df.to_excel('travel_packing_list.xlsx', index=False)

def main():
    print('loaded')
    st.title("Interactive Checklist")

    # Load data
    df = load_data()

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
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(row['Item Name'])
            with col2:
                print(df)
                if st.button("Tick" if row['Status'] == 0 else "Untick", key=idx):
                    print('clicked')
                    print(row)

                    #df.at[idx, 'Status'] = 1 if row['Status'] == 0 else 0
                    df.loc[idx, 'Status'] = 1 if row['Status'] == 0 else 0
                    print(df)
                    print('end')
                    save_data(df)
                    st.experimental_rerun()

    # Add new category and item
    st.sidebar.header("Add New Category")
    new_category = st.sidebar.text_input("Category Name")
    new_category_item = st.sidebar.text_input("Item Name for New Category")
    if st.sidebar.button("Add Category"):
        if new_category and new_category_item and new_category not in categories:
            new_row = pd.DataFrame({"Category": [new_category], "Item Name": [new_category_item], "Status": [0]})
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.experimental_rerun()

    # Add new item
    st.sidebar.header("Add New Item")
    selected_category = st.sidebar.selectbox("Select Category", categories)
    new_item = st.sidebar.text_input("Item Name")
    if st.sidebar.button("Add Item"):
        if selected_category and new_item:
            new_row = pd.DataFrame({"Category": [selected_category], "Item Name": [new_item], "Status": [0]})
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.experimental_rerun()

    # Delete item
    st.sidebar.header("Delete Item")
    item_to_delete = st.sidebar.selectbox("Select Item to Delete", df['Item Name'])
    if st.sidebar.button("Delete Item"):
        if item_to_delete:
            df = df[df['Item Name'] != item_to_delete]
            save_data(df)
            st.experimental_rerun()

if __name__ == "__main__":
    main()

