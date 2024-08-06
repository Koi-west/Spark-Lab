"""
API文档: https://developers.thecatapi.com/view-account/ylX4blBYT9FaoVd6OhvR?report=bOoHBz-8t

申请API KEY: https://thecatapi.com/signup
"""
import requests
import gradio as gr

# Function to fetch cat images
def fetch_cat_images(api_key, limit=10, page=0):
    base_url = "https://api.thecatapi.com/v1/images/search"
    
    headers = {
        'x-api-key': api_key
    }
    
    params = {
        'limit': limit,
        'page': page
    }
    print(params)
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Gradio interface setup
def cat_image_interface(limit, page):
    """
    本函数主要调用API请求函数, 并处理API请求得到的JSON数据, 提取出图片的URL并返回
    
    The Cat API返回的是一个包含多个对象的列表，每个对象代表一张猫咪图片
    我们需要遍历这个列表，提取每个对象中的'url'字段
    """
    
    api_key = "live_YOUR_API_KEY_HERE"  # 请替换为你自己的API KEY
    data = fetch_cat_images(api_key, limit=int(limit), page=int(page))
    print(data)
    if data:
        photo_urls = [photo['url'] for photo in data]
        print(photo_urls)
        return photo_urls
    else:
        return []

# Define the input components for the Gradio interface
limit_input = gr.Number(label="Number of Images", value=10, minimum=1, maximum=100)
page_input = gr.Number(label="Page", value=0, minimum=0)

# Create the Gradio interface
gr.Interface(fn=cat_image_interface, 
        inputs=[limit_input, page_input], 
        outputs=gr.Gallery(label="Cat Images")).launch()