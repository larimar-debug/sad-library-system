import streamlit as st
import pandas as pd
import base64
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="SAD Library System", page_icon="📚", layout="wide")

# Function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Try to load background image
img_base64 = get_base64_image("static/LIBRARY ROOM.jpg")

# Custom CSS for background
if img_base64:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: -1;
        }}
        
        h1, h2, h3, p, label, .stMarkdown {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
        }}
        
        .stButton>button {{
            background-color: rgba(139, 92, 46, 0.9);
            color: white;
            font-weight: bold;
        }}
        
        .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {{
            background-color: rgba(255, 255, 255, 0.9);
        }}
        </style>
    """, unsafe_allow_html=True)

# Initialize session state for storing books
if 'books' not in st.session_state:
    st.session_state.books = pd.DataFrame({
        'Book ID': ['B001', 'B002', 'B003'],
        'Title': ['Python Programming', 'Data Science Handbook', 'Web Development Guide'],
        'Author': ['John Smith', 'Jane Doe', 'Mike Johnson'],
        'ISBN': ['978-1234567890', '978-0987654321', '978-1122334455'],
        'Category': ['Programming', 'Data Science', 'Web Development'],
        'Quantity': [5, 3, 7],
        'Available': [5, 3, 7],
        'Status': ['Available', 'Available', 'Available']
    })

if 'borrowed_books' not in st.session_state:
    st.session_state.borrowed_books = pd.DataFrame(columns=['Book ID', 'Title', 'Borrower Name', 'Borrower ID', 'Borrow Date', 'Due Date', 'Status'])

# Title
st.title("📚 SAD Library Inventory Management System")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Add Book", "Search Books", "Borrow Book", "Return Book", "Borrowed Books", "View All Books"])

# Dashboard
if menu == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #f0ad4e; margin: 0;'>Total Books</h3>
                <h1 style='color: white; margin: 10px 0;'>{}</h1>
            </div>
        """.format(len(st.session_state.books)), unsafe_allow_html=True)
    
    with col2:
        total_quantity = st.session_state.books['Quantity'].sum()
        st.markdown("""
            <div style='background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #5bc0de; margin: 0;'>Total Copies</h3>
                <h1 style='color: white; margin: 10px 0;'>{}</h1>
            </div>
        """.format(total_quantity), unsafe_allow_html=True)
    
    with col3:
        available_books = st.session_state.books['Available'].sum()
        st.markdown("""
            <div style='background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #5cb85c; margin: 0;'>Available Copies</h3>
                <h1 style='color: white; margin: 10px 0;'>{}</h1>
            </div>
        """.format(available_books), unsafe_allow_html=True)
    
    with col4:
        borrowed = total_quantity - available_books
        st.markdown("""
            <div style='background: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #d9534f; margin: 0;'>Books Borrowed</h3>
                <h1 style='color: white; margin: 10px 0;'>{}</h1>
            </div>
        """.format(borrowed), unsafe_allow_html=True)
    
    st.subheader("📖 Recent Books")
    st.dataframe(st.session_state.books.head(5), use_container_width=True)
    
    st.subheader("📂 Books by Category")
    if not st.session_state.books.empty:
        category_counts = st.session_state.books['Category'].value_counts()
        st.bar_chart(category_counts)

# Add Book
elif menu == "Add Book":
    st.header("➕ Add New Book")
    
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            book_id = st.text_input("Book ID *", placeholder="e.g., B004")
            title = st.text_input("Book Title *", placeholder="e.g., Machine Learning Basics")
            author = st.text_input("Author *", placeholder="e.g., Sarah Williams")
            isbn = st.text_input("ISBN", placeholder="e.g., 978-1234567890")
        
        with col2:
            category = st.selectbox("Category *", ["Programming", "Data Science", "Web Development", "Database", "Networking", "Other"])
            quantity = st.number_input("Quantity *", min_value=1, value=1)
            available = st.number_input("Available Copies *", min_value=1, value=1)
            status = st.selectbox("Status", ["Available", "Out of Stock"])
        
        submit = st.form_submit_button("Add Book")
        
        if submit:
            if book_id and title and author and category:
                # Check if book ID already exists
                if book_id in st.session_state.books['Book ID'].values:
                    st.error("❌ Book ID already exists!")
                else:
                    new_book = pd.DataFrame({
                        'Book ID': [book_id],
                        'Title': [title],
                        'Author': [author],
                        'ISBN': [isbn],
                        'Category': [category],
                        'Quantity': [quantity],
                        'Available': [available],
                        'Status': [status]
                    })
                    st.session_state.books = pd.concat([st.session_state.books, new_book], ignore_index=True)
                    st.success(f"✅ Book '{title}' added successfully!")
            else:
                st.error("❌ Please fill all required fields (*)")

# Search Books
elif menu == "Search Books":
    st.header("🔍 Search Books")
    
    search_option = st.radio("Search by:", ["Title", "Author", "Category", "Book ID"])
    search_query = st.text_input(f"Enter {search_option}")
    
    if search_query:
        if search_option == "Title":
            results = st.session_state.books[st.session_state.books['Title'].str.contains(search_query, case=False, na=False)]
        elif search_option == "Author":
            results = st.session_state.books[st.session_state.books['Author'].str.contains(search_query, case=False, na=False)]
        elif search_option == "Category":
            results = st.session_state.books[st.session_state.books['Category'].str.contains(search_query, case=False, na=False)]
        else:
            results = st.session_state.books[st.session_state.books['Book ID'].str.contains(search_query, case=False, na=False)]
        
        if not results.empty:
            st.success(f"Found {len(results)} result(s)")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("No books found matching your search.")

# Borrow Book
elif menu == "Borrow Book":
    st.header("📤 Borrow Book")
    
    available_books = st.session_state.books[st.session_state.books['Available'] > 0]
    
    if available_books.empty:
        st.warning("No books available for borrowing at the moment.")
    else:
        with st.form("borrow_form"):
            book_id = st.selectbox("Select Book ID", available_books['Book ID'].tolist())
            
            if book_id:
                selected_book = st.session_state.books[st.session_state.books['Book ID'] == book_id].iloc[0]
                st.info(f"**Title:** {selected_book['Title']}\n\n**Author:** {selected_book['Author']}\n\n**Available:** {selected_book['Available']}")
            
            borrower_name = st.text_input("Borrower Name *")
            borrower_id = st.text_input("Borrower ID *", placeholder="e.g., STU001")
            
            borrow_date = st.date_input("Borrow Date", value=datetime.now())
            due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=14))
            
            submit = st.form_submit_button("Borrow Book")
            
            if submit:
                if borrower_name and borrower_id:
                    # Update book availability
                    idx = st.session_state.books[st.session_state.books['Book ID'] == book_id].index[0]
                    st.session_state.books.at[idx, 'Available'] -= 1
                    
                    if st.session_state.books.at[idx, 'Available'] == 0:
                        st.session_state.books.at[idx, 'Status'] = 'Out of Stock'
                    
                    # Add to borrowed books
                    new_borrow = pd.DataFrame({
                        'Book ID': [book_id],
                        'Title': [selected_book['Title']],
                        'Borrower Name': [borrower_name],
                        'Borrower ID': [borrower_id],
                        'Borrow Date': [borrow_date],
                        'Due Date': [due_date],
                        'Status': ['Borrowed']
                    })
                    st.session_state.borrowed_books = pd.concat([st.session_state.borrowed_books, new_borrow], ignore_index=True)
                    
                    st.success(f"✅ Book borrowed successfully by {borrower_name}!")
                else:
                    st.error("❌ Please fill all required fields!")

# Return Book
elif menu == "Return Book":
    st.header("📥 Return Book")
    
    if st.session_state.borrowed_books.empty:
        st.warning("No borrowed books to return.")
    else:
        borrowed_books = st.session_state.borrowed_books[st.session_state.borrowed_books['Status'] == 'Borrowed']
        
        if borrowed_books.empty:
            st.warning("No books currently borrowed.")
        else:
            with st.form("return_form"):
                borrower_id = st.selectbox("Select Borrower ID", borrowed_books['Borrower ID'].unique().tolist())
                
                if borrower_id:
                    borrower_books = borrowed_books[borrowed_books['Borrower ID'] == borrower_id]
                    book_id = st.selectbox("Select Book to Return", borrower_books['Book ID'].tolist())
                    
                    submit = st.form_submit_button("Return Book")
                    
                    if submit:
                        # Update book availability
                        idx = st.session_state.books[st.session_state.books['Book ID'] == book_id].index[0]
                        st.session_state.books.at[idx, 'Available'] += 1
                        st.session_state.books.at[idx, 'Status'] = 'Available'
                        
                        # Update borrowed books status
                        borrow_idx = st.session_state.borrowed_books[
                            (st.session_state.borrowed_books['Book ID'] == book_id) & 
                            (st.session_state.borrowed_books['Borrower ID'] == borrower_id) &
                            (st.session_state.borrowed_books['Status'] == 'Borrowed')
                        ].index[0]
                        st.session_state.borrowed_books.at[borrow_idx, 'Status'] = 'Returned'
                        
                        st.success(f"✅ Book returned successfully!")

# Borrowed Books
elif menu == "Borrowed Books":
    st.header("📋 Currently Borrowed Books")
    
    borrowed = st.session_state.borrowed_books[st.session_state.borrowed_books['Status'] == 'Borrowed']
    
    if borrowed.empty:
        st.info("No books are currently borrowed.")
    else:
        st.dataframe(borrowed, use_container_width=True)
        
        # Check for overdue books
        today = pd.to_datetime(datetime.now().date())
        borrowed['Due Date'] = pd.to_datetime(borrowed['Due Date'])
        overdue = borrowed[borrowed['Due Date'] < today]
        
        if not overdue.empty:
            st.warning(f"⚠️ {len(overdue)} overdue book(s)!")
            st.dataframe(overdue, use_container_width=True)

# View All Books
elif menu == "View All Books":
    st.header("📚 All Books in Library")
    
    if st.session_state.books.empty:
        st.info("No books in the library yet.")
    else:
        st.dataframe(st.session_state.books, use_container_width=True)
        
        # Download as CSV
        csv = st.session_state.books.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="library_inventory.csv",
            mime="text/csv"
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.info("📚 SAD Library System v1.0")