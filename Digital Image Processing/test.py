import streamlit as st

# Define functions for button clicks
def function1():
    st.write("Function 1 called")

def function2():
    st.write("Function 2 called")

def function3():
    st.write("Function 3 called")

# Create the Streamlit app
def main():
    st.title("Button Functions Demo")

    # Add buttons to call functions
    if st.button("Function 1"):
        function1()

    if st.button("Function 2"):
        function2()

    if st.button("Function 3"):
        function3()

if __name__ == "_main_":
    main()