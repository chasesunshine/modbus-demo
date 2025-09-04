from flask import Flask, jsonify, request

import os

from src.database.SQLiteDatabase import SQLiteDatabase
from src.util.ModbusClient import ModbusClient
from werkzeug.utils import secure_filename  # 用于安全处理文件名

# 创建Flask应用实例
app = Flask(__name__)

# 模拟一些数据
books = [{"id": 1, "title": "《Python编程：从入门到实践》", "author": "Eric Matthes"},{"id": 2, "title": "《流畅的Python》", "author": "Luciano Ramalho"}]

# 定义一个简单的GET请求API接口，获取所有书籍
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)


# 定义一个按ID获取特定书籍的GET接口
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


# 定义一个添加新书籍的POST接口
@app.route('/api/books', methods=['POST'])
def add_book():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    new_id = max(b['id'] for b in books) + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": data.get('title'),
        "author": data.get('author')
    }
    books.append(new_book)
    return jsonify(new_book), 201  # 201 Created status code


# modbus连接
@app.route('/api/connet', methods=['POST'])
def modbus_connect():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    modbusType = data.get("modbusType");
    # serial = data.get("serial");
    # ip = data.get("ip");
    # port = data.get("port");
    # baudRate = data.get("baudRate");
    # parityCheck = data.get("parityCheck");
    # stopBits = data.get("stopBits");
    # dataBits = data.get("dataBits");
    # gatewayType = data.get("gatewayType");

    # 初始化 modbus
    ModbusClient.__init__(modbusType,modbusType)
    # 连接 modbus
    result = ModbusClient.connect();

    return result


# 初次文件配置
@app.route('/file/config', methods=['POST'])
def upload_file():
    """
    处理POST请求的文件上传接口
    """
    # 检查请求中是否包含文件部分
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # 如果用户没有选择文件，浏览器可能会提交一个没有文件名的空部分
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # 获取参数
    gatewayType = request.form.get('gatewayType')

    # 如果数据表不存在就创建数据表
    sQLiteDatabase = SQLiteDatabase()
    sQLiteDatabase.connect()
    result = sQLiteDatabase.table_exists_method1("orders")
    if result :
        # 如果不存在就要创建表
        sQLiteDatabase.create_tables()

    # 插入数据
    # sQLiteDatabase.insertSql();
    # return jsonify({
    #     'message': 'File successfully uploaded',
    #     'filename': filename,
    #     'saved_path': file_path
    # }), 200

    # 如果文件存在且扩展名被允许
    if file and allowed_file(filename=file.filename):
        # 使用secure_filename确保文件名安全
        filename = secure_filename(file.filename)
        # 确保上传目录存在
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        # 保存文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({
            'message': 'File successfully uploaded',
            'filename': filename,
            'saved_path': file_path
        }), 200
    else:
        return jsonify({'error': 'File type not allowed or upload failed'}), 400

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件后缀

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 文件配置回显（展示）
@app.route('/file/detail', methods=['POST'])
def file_detail():
    # 查询数据表
    sQLiteDatabase = SQLiteDatabase()
    with sQLiteDatabase.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return users



# 运行应用
if __name__ == '__main__':
    app.run(debug=True)  # debug模式适合开发，生产环境应关闭