from fsystem_backend.database import db
import datetime

# Database Models
class RegisteredObject(db.Model):
    """
    SQLAlchemy model for ma_registered_object table.
    Maps to the company/organization registration information.
    """
    __tablename__ = 'ma_registered_object'

    # Primary Key
    registered_objectno = db.Column(db.String(6), primary_key=True, comment='註冊者代號(固定5碼)')
    
    # Required fields (NOT NULL)
    registered_objectnam = db.Column(db.String(10), nullable=False, comment='註冊者簡稱')
    
    # Optional fields
    object_full_name = db.Column(db.String(30), nullable=True, comment='註冊者全稱')
    object_eng_full_name = db.Column(db.String(30), nullable=True, comment='註冊者英全稱')
    object_eng_brief_name = db.Column(db.String(6), nullable=True, comment='註冊者英簡稱(6碼)')
    object_typeno = db.Column(db.String(6), nullable=True, comment='註冊者種類(對象種類)')
    registered_objectid = db.Column(db.String(20), nullable=True, comment='註冊者證號')
    unit_currencyno = db.Column(db.String(6), nullable=True, comment='共幣別')
    in_cityno = db.Column(db.String(6), nullable=True, comment='所在都市')
    in_econo = db.Column(db.String(6), nullable=True, comment='所在經濟體')
    applicant = db.Column(db.Integer, nullable=True, comment='申請人(empid)')
    applicanted_date = db.Column(db.DateTime, nullable=True, comment='申請日期')
    want_login_date = db.Column(db.Date, nullable=True, comment='希望登錄日期')
    menuno = db.Column(db.String(6), nullable=True, comment='選單別')
    agreeed_login_date = db.Column(db.Date, nullable=True, comment='核可日期')
    administratora_nam = db.Column(db.String(20), nullable=True, comment='管理員A姓名')
    administratora_no = db.Column(db.String(10), nullable=True, comment='管理員A代號')
    administratora_password = db.Column(db.String(16), nullable=True, comment='管理員A密碼')
    administratora_mobile = db.Column(db.String(16), nullable=True, comment='管理員A手機')
    administratora_birthday = db.Column(db.String(20), nullable=True, comment='管理員A生日')
    approve_empid = db.Column(db.Integer, nullable=True, comment='平台核可員工ID')
    cancel_date = db.Column(db.Date, nullable=True, comment='取消日期')
    status = db.Column(db.SmallInteger, nullable=True, comment='狀態')
    
    # Audit fields
    created_by = db.Column(db.Integer, nullable=True, comment='創建人(empid)')
    created_date = db.Column(db.DateTime, nullable=True, comment='創建日期')
    last_update_by = db.Column(db.Integer, nullable=True, comment='最後修改人(empid)')
    last_update = db.Column(db.DateTime, nullable=True, comment='最後修改日期')
    remark = db.Column(db.String(100), nullable=True, comment='備註')

    def __init__(self, **kwargs):
        super(RegisteredObject, self).__init__(**kwargs)
        if not self.created_date:
            self.created_date = datetime.utcnow()
        self.last_update = datetime.utcnow()

    def __repr__(self):
        return f'<RegisteredObject {self.registered_objectno}: {self.registered_objectnam}>'

    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'registered_objectno': self.registered_objectno,
            'registered_objectnam': self.registered_objectnam,
            'object_full_name': self.object_full_name,
            'object_eng_full_name': self.object_eng_full_name,
            'object_eng_brief_name': self.object_eng_brief_name,
            'object_typeno': self.object_typeno,
            'registered_objectid': self.registered_objectid,
            'unit_currencyno': self.unit_currencyno,
            'in_cityno': self.in_cityno,
            'in_econo': self.in_econo,
            'applicant': self.applicant,
            'applicanted_date': self.applicanted_date.isoformat() if self.applicanted_date else None,
            'want_login_date': self.want_login_date.isoformat() if self.want_login_date else None,
            'menuno': self.menuno,
            'agreeed_login_date': self.agreeed_login_date.isoformat() if self.agreeed_login_date else None,
            'administratora_nam': self.administratora_nam,
            'administratora_no': self.administratora_no,
            'administratora_mobile': self.administratora_mobile,
            'administratora_birthday': self.administratora_birthday,
            'approve_empid': self.approve_empid,
            'cancel_date': self.cancel_date.isoformat() if self.cancel_date else None,
            'status': self.status,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_update_by': self.last_update_by,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'remark': self.remark
        }

    @staticmethod
    def from_dict(data):
        """Create object from dictionary"""
        return RegisteredObject(
            registered_objectno=data.get('registered_objectno'),
            registered_objectnam=data.get('registered_objectnam'),
            object_full_name=data.get('object_full_name'),
            object_eng_full_name=data.get('object_eng_full_name'),
            object_eng_brief_name=data.get('object_eng_brief_name'),
            object_typeno=data.get('object_typeno'),
            registered_objectid=data.get('registered_objectid'),
            unit_currencyno=data.get('unit_currencyno'),
            in_cityno=data.get('in_cityno'),
            in_econo=data.get('in_econo'),
            applicant=data.get('applicant'),
            menuno=data.get('menuno'),
            administratora_nam=data.get('administratora_nam'),
            administratora_no=data.get('administratora_no'),
            administratora_mobile=data.get('administratora_mobile'),
            administratora_birthday=data.get('administratora_birthday'),
            approve_empid=data.get('approve_empid'),
            status=data.get('status'),
            created_by=data.get('created_by'),
            last_update_by=data.get('last_update_by'),
            remark=data.get('remark')
        )




class LoginUser(db.Model):
    """User login information"""
    id = db.Column(db.Integer, primary_key=True)
    registed_objectno = db.Column(db.String(6), nullable=False)
    userno = db.Column(db.String(10), nullable=False)
    usernam = db.Column(db.String(20))
    # ... other fields as per ma_login_user table
