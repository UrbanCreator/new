import streamlit as st
from Colorize import ImageColorizationGUI
from BgRemove import BgRemmoveGUI
from Sketch import ImageToSketchGUI

# Define your specific functions
def ImageColorizationGUI():
    st.success("ImageColorizationGUI function called")

def BgRemmoveGUI():
    st.info("Function 2 called: Background Remover")

def ImageToSketchGUI():
    st.warning("Function 3 called")

def function4():
    st.error("Function 4 called")

def function5():
    st.error("Function 5 called", icon="🔔")

# Create the Streamlit app with a grid layout
def main():
    st.title("Digital Images Processing")
    # Improving the space by adding visual space elements
    st.write('\n' * 3)  # Add more effective space after the title

    # Create a 2x2 grid for images and buttons, customized for better spacing
    col1, col2 = st.columns([1, 1])  # Two columns for the first row

    # Adding images and buttons with enlarged images and better spacing
    with col1:  # First column
        st.image("https://via.placeholder.com/300x200", caption="Colorization")
        if st.button("Activate raw_heart", key='1'):
            draw_heart()  # Call raw_heart function on button click

    with col2:  # Second column
        st.image("https://via.placeholder.com/300x200", caption="Background Remover")
        if st.button("Function 2", key='2'):
            function2()

    # Using a single column in the middle to align the third function button with an image
    col3 = st.columns([1])
    with col3[0]:  # Center column
        st.image("https://via.placeholder.com/300x200", caption="Image Enhancement")
        if st.button("Function 3", key='3'):
            function3()

    # Second row of buttons with images
    col4, col5 = st.columns([1, 1])  # Two columns for the second row

    with col4:
        st.image("https://via.placeholder.com/300x200", caption="Image for Function 4")
        if st.button("Function 4", key='4'):
            function4()

    with col5:
        st.image("https://via.placeholder.com/300x200", caption="Image for Function 5")
        if st.button("Function 5", key='5'):
            function5()

if __name__ == "__main__":
    main()
