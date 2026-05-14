from flask import Blueprint

# 创建各模块蓝图
auth_bp = Blueprint('auth', __name__)
quotation_bp = Blueprint('quotations', __name__)
module_bp = Blueprint('modules', __name__)
material_bp = Blueprint('materials', __name__)
fee_bp = Blueprint('fees', __name__)
version_bp = Blueprint('versions', __name__)
user_bp = Blueprint('users', __name__)
export_bp = Blueprint('exports', __name__)
logs_bp = Blueprint('logs', __name__)
roles_bp = Blueprint('roles', __name__)
fee_rate_bp = Blueprint('fee_rates', __name__)
exchange_rate_bp = Blueprint('exchange_rates', __name__)
module_participant_bp = Blueprint('module_participants', __name__)
sync_bp = Blueprint('sync', __name__)
change_request_bp = Blueprint('change_requests', __name__)
messages_bp = Blueprint('messages', __name__)

# 导入各模块路由
from app.routes.auth import auth_bp
from app.routes.quotations import quotation_bp
from app.routes.modules import module_bp
from app.routes.materials import material_bp
from app.routes.fees import fee_bp
from app.routes.versions import version_bp
from app.routes.users import user_bp
from app.routes.exports import export_bp
from app.routes.logs import logs_bp
from app.routes.roles import roles_bp
from app.routes.fee_rates import fee_rate_bp
from app.routes.exchange_rates import exchange_rate_bp
from app.routes.module_participants import module_participant_bp
from app.routes.sync import sync_bp
from app.routes.change_requests import change_request_bp
from app.routes.messages import messages_bp