from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'calculator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CalcRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(256), nullable=False)
    result = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    if not os.path.exists(os.path.join(basedir, "instance")):
        os.mkdir("instance")
    db.create_all()

# ===== 计算接口 只保留这一个！包含计算+入库 =====
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get("expression", "")
    try:
        raw_result = eval(expr)
        rounded_result = round(float(raw_result), 6)
        # 存入数据库
        new_record = CalcRecord(expression=expr, result=str(rounded_result))
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"code":200, "result": rounded_result})
    except Exception as e:
        return jsonify({"code":400, "msg":"表达式错误"})

# 分页查询历史，带搜索 + 北京时间转换
@app.route('/api/history', methods=['GET'])
def get_history():
    page = request.args.get("page",1,type=int)
    size = request.args.get("size",5,type=int)
    keyword = request.args.get("keyword","")
    query = CalcRecord.query.order_by(CalcRecord.create_time.desc())
    if keyword:
        query = query.filter(CalcRecord.expression.contains(keyword))
    paginate = query.paginate(page=page, per_page=size, error_out=False)
    records = paginate.items
    res_list = []
    for r in records:
        bj_time = r.create_time + timedelta(hours=8)
        res_list.append({
            "id": r.id,
            "expr": r.expression,
            "result": r.result,
            "time": bj_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({
        "code":200,
        "data": res_list,
        "page": page,
        "size": size,
        "total": paginate.total,
        "totalPage": paginate.pages
    })

# 删除单条历史
@app.route('/api/history/<int:rid>', methods=['DELETE'])
def del_one(rid):
    rec = CalcRecord.query.get(rid)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return jsonify({"code":200})

# 清空全部历史
@app.route('/api/history', methods=['DELETE'])
def del_all():
    CalcRecord.query.delete()
    db.session.commit()
    return jsonify({"code":200})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
