from datetime import datetime

from sqlalchemy import Column, Integer, JSON, Sequence, String

from app.db import Base, db_query, db_update


class Workflow(Base):
    """
    工作流表
    """
    # ID
    id = Column(Integer, Sequence('id'), primary_key=True, index=True)
    # 名称
    name = Column(String, index=True, nullable=False)
    # 描述
    description = Column(String)
    # 定时器
    timer = Column(String)
    # 状态：W-等待 R-运行中 P-暂停 S-成功 F-失败
    state = Column(String, nullable=False, index=True, default='W')
    # 当前执行动作
    current_action = Column(String)
    # 任务执行结果
    result = Column(String)
    # 已执行次数
    run_count = Column(Integer, default=0)
    # 任务列表
    actions = Column(JSON, default=list)
    # 执行上下文
    context = Column(JSON, default=dict)
    # 创建时间
    add_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 最后执行时间
    last_time = Column(String)

    @staticmethod
    @db_query
    def get_enabled_workflows(db):
        return db.query(Workflow).filter(Workflow.state != 'P').all()

    @staticmethod
    @db_query
    def get_by_name(db, name: str):
        return db.query(Workflow).filter(Workflow.name == name).first()

    @staticmethod
    @db_update
    def update_state(db, wid: int, state: str):
        db.query(Workflow).filter(Workflow.id == wid).update({"state": state})
        return True

    @staticmethod
    @db_update
    def start(db, wid: int):
        db.query(Workflow).filter(Workflow.id == wid).update({
            "state": 'R'
        })
        return True

    @staticmethod
    @db_update
    def fail(db, wid: int, result: str):
        db.query(Workflow).filter(Workflow.id == wid).update({
            "state": 'F',
            "result": result,
            "run_count": Workflow.run_count + 1,
            "last_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return True

    @staticmethod
    @db_update
    def success(db, wid: int, result: str = None):
        db.query(Workflow).filter(Workflow.id == wid).update({
            "state": 'S',
            "result": result,
            "run_count": Workflow.run_count + 1,
            "last_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return True

    @staticmethod
    @db_update
    def update_current_action(db, wid: int, action: str, context: dict):
        db.query(Workflow).filter(Workflow.id == wid).update({"current_action": action, "context": context})
        return True
