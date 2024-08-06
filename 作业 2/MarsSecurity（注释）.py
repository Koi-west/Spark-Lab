import requests
import gradio as gr

# 函数：获取火星车照片,并由三个参数决定
def fetch_mars_rover_photos(api_key, sol=1000, page=1):
    # 设置API的基础URL,这是要请求照片 api 的地址
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    
    # 设置请求参数
    """
    在 HTTP 请求中,请求参数（reaqust parameter）是用来传递给服务器信息,以便服务器能根据信息处理请求。
    在 Python 的 requests 库中,可以通过 params 参数来指定这些请求参数。
    """
    params = {
        'api_key': api_key,
        'sol': sol,
        'page': page
    }
    """
    params 是一个字典,包含了三个键值对：
        'api_key': API密钥,通常用于验证身份。
        'sol': 表示火星车工作的“天数”,即火星上的太阳日数。
        'page': 请求数据的页数,用于分页获取大量数据时。
    """
    """
    定义了一个名为params的字典,用于存储HTTP请求中的查询参数。
    这些参数会被附加到请求URL上,以告诉服务器如何处理请求。
    例如,在这个例子中,服务器会根据提供的api_key、sol和page参数返回相应的火星车照片数据。
    """
    print(params)  # 打印参数,用于调试
    
    # 发送GET请求
    """
    GET 请求是一种从服务器获取信息的方法,它通过 URL 传递参数,并且这些请求应该是安全的、可缓存的,并且不应该改变服务器上的数据。
    发送GET请求,其中 base_url 是 API 地址, params 是请求参数。
    """
    response = requests.get(base_url, params=params)
    
    
    if response.status_code == 200: # 检查响应状态
        return response.json()  # 如果状态码是 200 ,表示请求成功,返回JSON数据
    else:
        return None  # 否则失败,返回 None

# Gradio接口函数
def mars_rover_photo_interface(sol, page): # 接受两个参数 sol 和 page
    api_key = "KKDMzTTxJzgLJBkaMqw0ZfMAyTBtLdKUmneFbPD8"  # API密钥
    data = fetch_mars_rover_photos(api_key, sol=sol, page=page) # 使用fetch_mars_rover_photos函数获取照片数据,传入api_key、sol和page作为参数。
    print(data)  # 打印返回的数据,用于调试
    """如果请求成功, data 将包含从 API 返回的 JSON 数据。如果请求失败, data 将是 None 。"""
    if data:
        photos = data.get('photos', [])  # 如果data存在，则从返回的数据中提取照片列表photos。
        photo_urls = [photo['img_src'] for photo in photos]  # 提取每张照片的URL
        print(photo_urls)  # 打印URL列表,用于调试
        """从其元数据中提取URL，并将其添加到 photo_urls 列表中"""
        return photo_urls
    else:
        return []
    """函数返回photo_urls列表。如果没有数据，则返回空列表。"""

# 定义Gradio输入组件
"""
    sol_input 和 page_input 分别定义了两个 Gradio 组件，用于接收用户的输入。
    sol_input 是一个数字输入框，其标签为" Martian Sol "，默认值为1000。
    page_input 同样是一个数字输入框，其标签为" Page "，默认值为1。
"""
sol_input = gr.Number(label="Martian Sol", value=1000)
page_input = gr.Number(label="Page", value=1)

# 创建Gradio接口
gr.Interface(fn=mars_rover_photo_interface, 
        inputs=[sol_input,  page_input], 
        outputs=gr.Gallery(label="Mars Rover Photos")).launch()
"""
gr.Interface 是 Gradio 的核心类，用于定义用户界面。

fn 参数指定了一个函数，该函数将根据用户输入生成输出。
inputs 参数是一个列表，包含了所有输入组件。
outputs 参数指定了输出组件。在这个例子中，使用 gr.Gallery 来展示一组图片。
launch() 方法启动 Gradio 应用程序，使得用户可以通过 Web 浏览器与之交互。
"""