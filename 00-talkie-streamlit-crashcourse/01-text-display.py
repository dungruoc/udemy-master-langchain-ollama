import streamlit as st

st.title("Streamlit text display")
st.header("This is a header")
st.subheader("this is a subheader")
st.text("Text data")
st.write("Write with default font")

# Markdown

st.markdown("""
# This is a markdown heading
## This is a makrdown subheading
### This is a makrdown subsubheading

This is a **bold markdown**

This is an *italic markdown*
            
> block quote
            
1. List first item
2. List second item
            
- Some bullet points
- etc.
""")

st.markdown("[Markdown cheat sheet](https://www.markdownguide.org/cheat-sheet/)")

# Emojies

st.markdown("[Emojies](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)")
st.markdown(":100: :streamlit: :smiley:")

# HTML

st.markdown("# HTML")

html_content = '''
<h1 style="color:orange;">A blue html heading</h1>
<p style="color:aqua;">A read paragraph</p>
'''

st.markdown(html_content, unsafe_allow_html=True)
st.markdown("---")

# Latex
st.markdown("# Latex")
st.latex(r"( x^2 + y^2 ) = z^2")
st.latex(r"f(x) = \frac{1}{\sqrt{1 + x^2}}")
st.divider()