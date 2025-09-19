- crawl data
- tìm thư viện: cách crawl dùng chrome engine hay dùng selinum phân tích so sánh lợi hại.
- dữ liệu cần lấy: title, image, tags, meta
  - meta cần nghiên cứu dùng gì.
- thiết kế cấu trúc json để có thể đọc ở nhiều website dùng selector của css hoặc gì đó ()
- Lấy dữ liệu json từ database

main(){
    url = ''
    json = {};
    // todo: Call database
    json = database.json;
    url = database.url;
    crawData(url, json); -> title
    // insert tĩnh vào 1 file json, csv
    // test thành công 
    // tạo cấu trúc bảng mới insert vào bảng đó hoặc bảng content.

}

input json: {
    {
        value: 'title 1',
        field: 'title',
        selector: '#content ~ #title'
    }
}

output: {
    title: 'title 1',
    author:"",
    catgory:"",
    tags:[],
    excerpt:""
}