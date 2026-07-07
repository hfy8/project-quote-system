from .user import User
from .quotation import Quotation, QuotationParticipant
from .module import Module, ModuleParticipant
from .material import Material, ModuleMaterial
# 延迟初始化 Module.material_total（material 模块此时才可用）
from .module import _init_module_material_total
_init_module_material_total()
from .fee import OtherFee, FeeType
from .version import VersionSnapshot
from .fee_rate import FeeRate
from .labor_hour import LaborHour
from .exchange_rate import ExchangeRate
from .landing_project import LandingProject
from .department import Department
from .position import Position
from .organization import Organization
from .employee import Employee
from .operation_log import OperationLog
from .change_request import ChangeRequest
from .message import Message
from .participant_type_permission import ParticipantTypePermission
from .permission import Role, Permission
from .ai_conversation import AiConversation, AiMessage
from .packing import PackingType
from .travel import TravelCategory, TravelDayRate, TravelMode, TravelPersonTripFee
from .travel_entry import PackingEntry, TravelPersonDays, TravelPersonTrip

__all__ = [
    'User',
    'Quotation',
    'QuotationParticipant',
    'Module',
    'ModuleParticipant',
    'Material',
    'ModuleMaterial',
    'OtherFee',
    'FeeType',
    'VersionSnapshot',
    'FeeRate',
    'LaborHour',
    'ExchangeRate',
    'LandingProject',
    'Department',
    'Position',
    'Organization',
    'Employee',
    'OperationLog',
    'ChangeRequest',
    'Message',
    'ParticipantTypePermission',
    'Role',
    'Permission',
    'AiConversation',
    'AiMessage',
    'PackingType',
    'TravelCategory',
    'TravelDayRate',
    'TravelMode',
    'TravelPersonTripFee',
    'PackingEntry',
    'TravelPersonDays',
    'TravelPersonTrip',
]
