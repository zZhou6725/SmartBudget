"""插入初始测试数据"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal
from app.models import Department, User, Budget, Expense, Notification
from app.core.security import hash_password

db = SessionLocal()

# 清空旧数据（开发用，生产勿跑）
db.query(Notification).delete()
db.query(Expense).delete()
db.query(Budget).delete()
db.query(User).delete()
db.query(Department).delete()
db.commit()

# 部门
depts = [
    Department(name="技术部", manager="张三"),
    Department(name="财务部", manager="李四"),
    Department(name="市场部", manager="王五"),
    Department(name="人事部", manager="赵六"),
]
db.add_all(depts)
db.flush()

# 用户
users = [
    User(id=1, username="admin", real_name="管理员", dept_id=depts[0].id, role="admin", status="active", password=hash_password("admin123")),
    User(id=2, username="zhangsan", real_name="张三", dept_id=depts[0].id, role="manager", status="active", password=hash_password("123456")),
    User(id=3, username="lisi", real_name="李四", dept_id=depts[1].id, role="finance", status="active", password=hash_password("123456")),
]
db.add_all(users)
db.flush()

# 预算
budgets = [
    Budget(dept_name="技术部", year=2026, total_amount=500000),
    Budget(dept_name="财务部", year=2026, total_amount=300000),
    Budget(dept_name="市场部", year=2026, total_amount=400000),
    Budget(dept_name="人事部", year=2026, total_amount=200000),
]
db.add_all(budgets)
db.flush()

# 支出
expenses = [
    Expense(expense_no="E20260601001", dept_name="技术部", budget_id=budgets[0].id,
            title="服务器采购", category="office", amount=85000, status="approved",
            applicant="张三", apply_date="2026-06-01"),
    Expense(expense_no="E20260602001", dept_name="技术部", budget_id=budgets[0].id,
            title="差旅费报销", category="travel", amount=3200, status="pending",
            applicant="张三", apply_date="2026-06-10"),
    Expense(expense_no="E20260603001", dept_name="财务部", budget_id=budgets[1].id,
            title="财务软件年费", category="office", amount=12000, status="approved",
            applicant="李四", apply_date="2026-06-05"),
    Expense(expense_no="E20260604001", dept_name="市场部", budget_id=budgets[2].id,
            title="广告投放", category="entertainment", amount=50000, status="pending",
            applicant="王五", apply_date="2026-06-12"),
    Expense(expense_no="E20260605001", dept_name="技术部", budget_id=budgets[0].id,
            title="加班餐费", category="transport", amount=800, status="rejected",
            applicant="张三", apply_date="2026-06-15"),
    Expense(expense_no="E20260606001", dept_name="技术部", budget_id=budgets[0].id,
            title="办公桌椅", category="office", amount=15000, status="pending",
            applicant="张三", apply_date="2026-06-20"),
]
db.add_all(expenses)
db.flush()

# 消息
notifications = [
    Notification(type="alert", title="技术部预算使用超过50%", summary="技术部2026年度预算已使用 ¥104,000，使用率20.8%", content="详细预警内容...", status="unread", user_id=1),
    Notification(type="notice", title="系统上线通知", summary="FinBalance财衡中台已正式上线运行", content="详细通知内容...", status="read", user_id=1, read_at=None),
    Notification(type="approval", title="差旅费报销待审批", summary="张三提交差旅费报销 ¥3,200 待您审批", content="详细审批内容...", status="unread", user_id=1),
]
db.add_all(notifications)

db.commit()
db.close()
print("种子数据插入完成")