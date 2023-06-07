import base64
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs
import streamlit as st
from streamlit import session_state as state


st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
    body {
          background-image: url("bg.png");
          background-repeat: no-repeat;
          background-size: cover;
         }
         }
</style>

<div class="css-1629p8f e16nr0p31"><h1 id="flipkart-scraper" style="display: flex; justify-content: center; background-color: rgb(243, 243, 221); color: rgb(4, 123, 213); text-align: center; padding: 20px;"><div class="css-zt5igj e16nr0p33"><a href="#flipkart-scraper" class="css-eczf16 e16nr0p32"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a><span class="css-10trblm e16nr0p30">
<img src="https://www.freepnglogos.com/uploads/flipkart-logo-png/flipkart-inventory-management-system-zap-inventory-1.png" style="width: 40px; height: 40px; margin-right: 10px;"> Flipkart Scraper
</span></div></h1></div></div></div></div><div data-stale="false" width="362" class="element-container css-15qwjnv e1tzin5v3"><div class="stNumberInput" style="width: 362px;"><label aria-hidden="true" class="css-81oif8 effi0qh3"><div data-testid="stMarkdownContainer" class="css-184tjsw e16nr0p34"><p><strong>Enter the number of URLs:</strong></p></div></label><div class=" css-1rvyln1 e1jwn65y3"><div data-baseweb="input" class="st-bd st-b3 st-be st-b8 st-bf st-bg st-bh st-bi st-bj st-bk st-bl st-bm st-bn st-b1 st-bo st-au st-ax st-bp st-bq st-ae st-af st-ag st-ah st-ai st-aj st-br st-bs st-bt st-bu st-bv st-bw st-bx"><div data-baseweb="base-input" class="st-b3 st-b8 st-by st-b1 st-bo st-ae st-af st-ag st-ah st-ai st-aj st-bz st-bv st-bp st-bq"><input aria-label="**Enter the number of URLs:**" aria-invalid="false" aria-required="false" autocomplete="on" inputmode="text" name="" placeholder="" type="number" min="1" max="Infinity" step="1" class="st-bd st-c0 st-bf st-bg st-bh st-bi st-c1 st-c2 st-c3 st-c4 st-c5 st-b8 st-c6 st-c7 st-c8 st-c9 st-ca st-cb st-cc st-cd st-ae st-af st-ag st-ce st-ai st-aj st-bz st-cf st-cg" value="1"></div></div><div class="css-76z9jo e1jwn65y2"><button class="step-down css-1r8izn3 e1jwn65y1" disabled=""><svg viewBox="0 0 8 8" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="disabled" class="e1fb0mya1 css-1i8bqbz ex0cdmw0"><path d="M0 3v2h8V3H0z"></path></svg></button><button class="step-up css-1r8izn3 e1jwn65y1"><svg viewBox="0 0 8 8" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="e1fb0mya1 css-bubqsq ex0cdmw0"><path d="M3 0v3H0v2h3v3h2V5h3V3H5V0H3z"></path></svg></button></div></div><div class="css-uapcc7 e1jwn65y0"><div class="input-instructions css-1li7dat effi0qh1"></div></div></div></div><div data-stale="false" width="362" class="element-container css-15qwjnv e1tzin5v3"><div class="row-widget stTextInput css-1nsugzs edfmue0" width="362"><label aria-hidden="true" class="css-81oif8 effi0qh3"><div data-testid="stMarkdownContainer" class="css-184tjsw e16nr0p34"><p><strong>Enter URL 1:</strong></p></div></label><div data-baseweb="input" class="st-bd st-b3 st-be st-b8 st-ch st-ci st-cj st-ck st-bj st-bk st-bl st-bm st-bn st-b1 st-bo st-au st-ax st-av st-aw st-ae st-af st-ag st-ah st-ai st-aj st-br st-bs st-bt st-bu st-bv st-bw st-bx"><div data-baseweb="base-input" class="st-b3 st-b8 st-by st-b1 st-bo st-ae st-af st-ag st-ah st-ai st-aj st-bz st-bv"><input aria-label="**Enter URL 1:**" aria-invalid="false" aria-required="false" autocomplete="" inputmode="text" name="" placeholder="" type="text" class="st-bd st-c0 st-bf st-bg st-bh st-bi st-c1 st-c2 st-c3 st-c4 st-c5 st-b8 st-c6 st-c7 st-c8 st-c9 st-ca st-cb st-cc st-cd st-ae st-af st-ag st-ce st-ai st-aj st-bz st-cf st-cg st-cl" value=""></div></div><div class="css-1li7dat effi0qh1"></div></div></div><div data-stale="false" width="362" class="element-container css-15qwjnv e1tzin5v3"><div class="row-widget stButton" style="width: 362px;"><button kind="secondary" class="css-1x8cf1d edgvbvh10"><div data-testid="stMarkdownContainer" class="css-1offfwp e16nr0p34"><p>Add URL 1</p></div></button></div></div><div data-stale="false" width="362" class="element-container css-15qwjnv e1tzin5v3"><div class="stMarkdown" style="width: 362px;"><div data-testid="stMarkdownContainer" class="css-1offfwp e16nr0p34"><p><strong>URL List:</strong></p></div></div></div><div data-stale="false" width="362" class="element-container css-15qwjnv e1tzin5v3"><div data-testid="stJson" style="width: 362px;"><div class="react-json-view" style="font-family: &quot;Source Code Pro&quot;, monospace; cursor: default; background-color: rgb(255, 255, 255); position: relative; font-size: 14px;"><div class="pretty-json-container object-container"><div class="object-content"><div class="object-key-val"><span><span style="display: inline-block; cursor: pointer;"><div class="icon-container" style="display: inline-block; width: 17px;"><span class="collapsed-icon"><svg viewBox="0 0 15 15" fill="currentColor" style="vertical-align: top; color: rgb(42, 161, 152); height: 1em; width: 1em; padding-left: 2px;"><path d="M0 14l6-6-6-6z"></path></svg></span></div><span></span><span style="display: inline-block; cursor: pointer; font-weight: bold; color: rgb(0, 43, 54);">[</span></span></span><span class="brace-row"><span style="display: inline-block; cursor: pointer; font-weight: bold; color: rgb(0, 43, 54); padding-left: 0px;">]</span><div class="object-meta-data" style="display: inline-block; padding: 0px 0px 0px 10px;"><span class="copy-to-clipboard-container" title="Copy to clipboard" style="vertical-align: top; display: none;"><span style="cursor: pointer; display: inline;"><span class="copy-icon"><svg viewBox="0 0 40 40" fill="currentColor" preserveAspectRatio="xMidYMid meet" style="vertical-align: top; color: rgb(38, 139, 210); font-size: 15px; margin-right: 3px; height: 1em; width: 1em;"><g><path d="m30 35h-25v-22.5h25v7.5h2.5v-12.5c0-1.4-1.1-2.5-2.5-2.5h-7.5c0-2.8-2.2-5-5-5s-5 2.2-5 5h-7.5c-1.4 0-2.5 1.1-2.5 2.5v27.5c0 1.4 1.1 2.5 2.5 2.5h25c1.4 0 2.5-1.1 2.5-2.5v-5h-2.5v5z m-20-27.5h2.5s2.5-1.1 2.5-2.5 1.1-2.5 2.5-2.5 2.5 1.1 2.5 2.5 1.3 2.5 2.5 2.5h2.5s2.5 1.1 2.5 2.5h-20c0-1.5 1.1-2.5 2.5-2.5z m-2.5 20h5v-2.5h-5v2.5z m17.5-5v-5l-10 7.5 10 7.5v-5h12.5v-5h-12.5z m-17.5 10h7.5v-2.5h-7.5v2.5z m12.5-17.5h-12.5v2.5h12.5v-2.5z m-7.5 5h-5v2.5h5v-2.5z"></path></g></svg></span></span></span></div></span></div></div></div></div></div></div><div data-stale="false" width="362" class="element-container css-15qwjnv e1tzin5v3"><div class="stMarkdown" style="width: 362px;"><div data-testid="stMarkdownContainer" class="css-1offfwp e16nr0p34"><p>No data available.</p></div></div></div></div></div><div class="resize-triggers"><div class="expand-trigger"><div style="width: 395px; height: 670px;"></div></div><div class="contract-trigger"></div></div></div>
    body {
          background-image: url("bg.png");
          background-repeat: no-repeat;
          background-size: cover;
         }
</style>
    
<h1 style="display: flex; align-tems: center; justify-content: center; background-color: #F3F3DD; color: #047bd5; text-align: center; padding: 20px;">
<img src="https://www.freepnglogos.com/uploads/flipkart-logo-png/flipkart-inventory-management-system-zap-inventory-1.png" style="width: 40px; height:40px; margin-right:10px;"> Flipkart Scraper
</h1>
""", unsafe_allow_html=True)

# Initialize session state
if 'urls' not in state:
    state.urls = []
num_urls = st.number_input("**Enter the number of URLs:**", value=len(state.urls) + 1, min_value=1, step=1)
for i in range(num_urls):
    url = st.text_input(f"**Enter URL {i+1}:**", key=f"url_{i}")
    if st.button(f"Add URL {i+1}", key=f"add_{i}"):
        if url and url not in state.urls:
            state.urls.append(url)
            st.success("URL added successfully.")
        elif url in state.urls:
            st.warning("URL already exists. Skipping...")
        else:
            st.warning("Please enter a valid URL.")

#st.write("URLs entered:")
#for url in state.urls:
#    st.write(url)
# Create a list of the entered URLs
url_list = state.urls
st.write("**URL List:**")
st.write(url_list)

def get_product_info(url):
    # Send an HTTP GET request and retrieve the webpage content
    response = requests.get(url)
    content = response.content

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Extract the name of product
    prod_name = soup.find('div', {'class': 'aMaAEs'})
    name = prod_name.text.strip() if prod_name else 'N/A'
    
    # Extract the category of product
    a_tag = soup.find('a',{'class': '_2whKao'})
    parent_div = a_tag.find_parent('div',{'class':'_3GIHBu'})
    sibling_div = parent_div.find_next_sibling('div', {'class':'_3GIHBu'})
    category = sibling_div.find('a',{'class':'_2whKao'}).text
    
    # Extract the Star out of 5
    prod_star = soup.find('div', {'class': '_3LWZlK'})
    star = prod_star.text.strip() if prod_star else 'N/A'
    
    # Ratings and Reviews
    span_tag = soup.find('span', {'class' : '_2_R_DZ'})
    ratings = span_tag.find('span').text.strip().split()[0]
    
    reviews_span = span_tag.find_all('span')[-1] 
    reviews = reviews_span.text.strip() if reviews_span else "NA"

    # Extract the product cost
    cost_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
    cost = cost_element.text.strip() if cost_element else 'N/A'

    # Extract the seller information
    seller_element = soup.find('div', {'class': '_1RLviY'})
    seller = seller_element.text.strip() if seller_element else 'N/A'

    # Extract other sellers
    other_sellers = []
    element = soup.find('a', string='See other sellers')

    # Parse the href link to a variable
    href_link = None  
    if element:
      href_link = element['href']
      other_sellers.append('https://www.flipkart.com'+href_link)

    # Extract Flipkart Serial Number
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    serial_number = query_params.get('pid', [''])[0]

    # Return the extracted information
    return {
        'Flipkart Serial Number': serial_number,
        'Product URL': url,
        'Product Name': name,
        'Product Category': category,
        'Star Rating': star,
        'Count of Ratings': ratings,
        'Reviews': reviews,
        'Cost of product': cost,
        'Seller': seller,
        'Other Sellers': ', '.join(other_sellers)
    }

# Create an empty DataFrame
data = []

# Extract information from each product URL
for url in state.urls:
    product_info = get_product_info(url)
    data.append(product_info) 

if data:
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    df['Seller'] = df['Seller'].str[:-3]
    st.dataframe(df)

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    button_label = "Download Data"
    button_text = f'<a href="data:file/csv;base64,{b64}" download="data.csv"><button style="background-color: white; color: #035689; border: 2px solid #035689;">{button_label}</button></a>'
    st.markdown(button_text, unsafe_allow_html=True)
else:
    st.write("No data available.")
