from bs4 import BeautifulSoup

def extract_by_class(html: str, class_name: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all(class_=class_name)

def extract_by_selectors(html: str, selectors: dict):
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    for key, selector in selectors.items():
        elem = soup.select_one(selector)
        data[key] = elem.get_text(strip=True) if elem else None
    return data

def extract_multiple_items(html: str, container_selector: str, item_selectors: dict):
    """
    Trích xuất nhiều item từ HTML dựa trên container và item selectors
    
    Args:
        html (str): HTML cần trích xuất
        container_selector (str): CSS selector cho container chứa các item
        item_selectors (dict): Dictionary chứa các selector cho từng trường dữ liệu
        
    Returns:
        list: Danh sách các item đã trích xuất
    """
    soup = BeautifulSoup(html, "html.parser")
    containers = soup.select(container_selector)
    results = []
    
    for container in containers:
        item_data = {}
        # print(item_selectors.items())
        for key, selector in item_selectors.items():
            elem = container.select_one(selector)
            item_data[key] = elem.get_text(strip=True) if elem else None
            
            # Lấy thêm href cho các link nếu có
            if elem and elem.name == 'a' and 'href' in elem.attrs:
                item_data[f"{key}_link"] = elem['href']
                
        results.append(item_data)
    
    return results

# # Dữ liệu HTML mẫu để test
# example_html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Example Page</title>
# </head>
# <body>
#     <div class="container">
#         <div class="postsmod1-details">
#             <h3 class="entry-title"><a href="https://example.com/post1">Bài viết số 1</a></h3>
#             <span class="postsmod1-author-name"><a href="https://example.com/author1">Tác giả 1</a></span>
#             <span class="postsmod1-date">01/01/2023</span>
#             <div class="postsmod1-excerpt">Đây là nội dung tóm tắt của bài viết số 1</div>
#         </div>
        
#         <div class="postsmod1-details">
#             <h3 class="entry-title"><a href="https://example.com/post2">Bài viết số 2</a></h3>
#             <span class="postsmod1-author-name"><a href="https://example.com/author2">Tác giả 2</a></span>
#             <span class="postsmod1-date">02/01/2023</span>
#             <div class="postsmod1-excerpt">Đây là nội dung tóm tắt của bài viết số 2</div>
#         </div>
        
#         <div class="postsmod1-details">
#             <h3 class="entry-title"><a href="https://example.com/post3">Bài viết số 3</a></h3>
#             <span class="postsmod1-author-name"><a href="https://example.com/author3">Tác giả 3</a></span>
#             <span class="postsmod1-date">03/01/2023</span>
#             <div class="postsmod1-excerpt">Đây là nội dung tóm tắt của bài viết số 3</div>
#         </div>
#     </div>
# </body>
# </html>
# """

# # Thiết lập selectors
# container_selector = ".postsmod1-details"
# item_selectors = {
#     "title": "h3.entry-title a",
#     "author": "span.postsmod1-author-name a",
#     "date": "span.postsmod1-date",
#     "excerpt": "div.postsmod1-excerpt"
# }

# # Gọi hàm extract_multiple_items với dữ liệu mẫu
# results = extract_multiple_items(example_html, container_selector, item_selectors)

# # # In kết quả để debug
# # print(f"Tìm thấy {len(results)} items:")
# # for i, item in enumerate(results, 1):
# #     print(f"\nItem {i}:")
# #     for key, value in item.items():
# #         print(f"  {key}: {value}")