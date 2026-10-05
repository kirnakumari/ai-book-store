import streamlit as st
from google import genai

# Gemini AI
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


# ---------------- BOOK DATABASE ----------------

books = [
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "Programming",
        "price": 499,
        "description": "A beginner-friendly book for learning Python."
    },
    {
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "category": "Programming",
        "price": 399,
        "description": "Learn Python through practical automation projects."
    },
    {
        "title": "Computer Networking",
        "author": "Andrew S. Tanenbaum",
        "category": "Networking",
        "price": 699,
        "description": "Learn computer networking concepts and protocols."
    },
    {
        "title": "Linux Basics for Hackers",
        "author": "OccupyTheWeb",
        "category": "Cybersecurity",
        "price": 599,
        "description": "Learn Linux fundamentals with a cybersecurity focus."
    },
    {
        "title": "The Web Application Hacker's Handbook",
        "author": "Dafydd Stuttard",
        "category": "Cybersecurity",
        "price": 799,
        "description": "Learn web application security concepts."
    },
    {
        "title": "Hands-On Machine Learning",
        "author": "Aurélien Géron",
        "category": "AI & ML",
        "price": 899,
        "description": "Practical introduction to machine learning."
    },
    {
        "title": "Artificial Intelligence",
        "author": "Stuart Russell",
        "category": "AI & ML",
        "price": 999,
        "description": "Introduction to artificial intelligence."
    },
    {
        "title": "IoT Fundamentals",
        "author": "David Hanes",
        "category": "IoT",
        "price": 749,
        "description": "Learn IoT architecture, devices and protocols."
    }
]


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="AI Book Store",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Book Store")
st.caption("AI-powered book discovery and shopping")

st.divider()


# ---------------- SESSION CART ----------------

if "cart" not in st.session_state:
    st.session_state.cart = []


# ---------------- SIDEBAR ----------------

st.sidebar.header("🔎 Search & Filter")

search = st.sidebar.text_input(
    "Search books"
)

category = st.sidebar.selectbox(
    "Category",
    [
        "All",
        "Programming",
        "AI & ML",
        "Cybersecurity",
        "Networking",
        "IoT"
    ]
)

st.sidebar.divider()
   
st.sidebar.caption("Made by")
st.sidebar.markdown("**Kirna Kumari**")
st.sidebar.caption("B.Tech CSE (IoT)")


# ---------------- AI RECOMMENDER ----------------

st.header("🤖 AI Book Recommendation")

user_query = st.text_input(
    "What type of book are you looking for?",
    placeholder="Example: I want to learn cybersecurity as a beginner"
)

if st.button("✨ Recommend Books"):

    if not user_query:
        st.warning("Please enter what you want to learn.")

    elif not client:
        st.error("Gemini API key not found.")

    else:

        book_data = "\n".join(
            [
                f"{b['title']} | {b['author']} | "
                f"{b['category']} | ₹{b['price']} | "
                f"{b['description']}"
                for b in books
            ]
        )

        prompt = f"""
You are an AI book recommendation assistant.

User request:
{user_query}

Available books:
{book_data}

Recommend the 3 most suitable books.

IMPORTANT:
Only recommend books from the available list.
Do not invent any books.

For every recommendation explain why it matches the user's request.
"""

        with st.spinner("AI is finding the best books..."):

            response = client.models.generate_content(
             model="gemini-3.5-flash-lite", 
                contents=prompt
            )

        st.success("AI Recommendations")
        st.write(response.text)


st.divider()


# ---------------- BOOK STORE ----------------

st.header("📖 Explore Books")

filtered_books = books.copy()


if category != "All":

    filtered_books = [
        book for book in filtered_books
        if book["category"] == category
    ]


if search:

    filtered_books = [
        book for book in filtered_books
        if search.lower() in (
            book["title"]
            + " "
            + book["author"]
            + " "
            + book["category"]
            + " "
            + book["description"]
        ).lower()
    ]


# ---------------- DISPLAY BOOKS ----------------

columns = st.columns(4)

for i, book in enumerate(filtered_books):

    with columns[i % 4]:

        st.subheader("📕 " + book["title"])

        st.write("**Author:**", book["author"])

        st.write("**Category:**", book["category"])

        st.write("**Price:** ₹", book["price"])

        st.caption(book["description"])

        if st.button(
            "🛒 Add to Cart",
            key=f"add_{i}"
        ):

            st.session_state.cart.append(book)

            st.success("Added to cart!")


# ---------------- CART ----------------

st.divider()

st.header("🛒 Shopping Cart")

if not st.session_state.cart:

    st.info("Your cart is empty.")

else:

    total = 0

    for book in st.session_state.cart:

        st.write(
            f"📕 **{book['title']}** — ₹{book['price']}"
        )

        total += book["price"]

    st.subheader(f"Total: ₹{total}")

    if st.button("💳 Place Order"):

        st.success(
            "🎉 Order placed successfully! "
            "This is a demo checkout."
        )