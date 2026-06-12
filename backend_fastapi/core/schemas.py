"""Pydantic schemas - 请求/响应数据模型"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime


# ============== 通用 ==============
class ApiResponse(BaseModel):
    """通用响应"""
    model_config = ConfigDict(extra="allow")
    code: int = 0
    data: Any = None
    error: Optional[str] = None


# ============== Auth ==============
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=1, max_length=100)


# ============== Quotation ==============
class QuotationCreate(BaseModel):
    """创建报价单请求"""
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field("single", pattern="^(single|line)$")
    scheme_no: Optional[str] = Field(None, max_length=50)
    business_owner_id: Optional[int] = None
    tax_rate: float = Field(0.13, ge=0, le=1)
    profit_rate: float = Field(0.0, ge=-1, le=10)
    currency: str = Field("CNY", max_length=10)
    parent_id: Optional[int] = None
    coefficients: Optional[Dict[str, float]] = None


class QuotationUpdate(BaseModel):
    """更新报价单请求（所有字段可选）"""
    name: Optional[str] = Field(None, max_length=100)
    scheme_no: Optional[str] = None
    business_owner_id: Optional[int] = None
    tax_rate: Optional[float] = Field(None, ge=0, le=1)
    profit_rate: Optional[float] = Field(None, ge=-1, le=10)
    currency: Optional[str] = None
    parent_id: Optional[int] = None
    coefficients: Optional[Dict[str, float]] = None


class QuotationStatusUpdate(BaseModel):
    """更新状态请求"""
    status: str = Field(..., pattern="^(draft|approved)$")


class ParticipantAddRequest(BaseModel):
    """添加参与人请求"""
    user_id: int
    participant_type: str = Field("project", pattern="^(project|agency|electrical)$")


class ParticipantTypeUpdate(BaseModel):
    """更新参与人类型"""
    participant_type: str = Field(..., pattern="^(project|agency|electrical)$")


# ============== Module ==============
class ModuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class ModuleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    name_en: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class ModuleMaterialAdd(BaseModel):
    """加物料到模块"""
    material_id: int
    quantity: int = Field(1, ge=1)
    is_other: bool = False
    unit_price_override: Optional[float] = None


class ModuleMaterialUpdate(BaseModel):
    """改物料数量/单价"""
    quantity: Optional[int] = Field(None, ge=1)
    unit_price_override: Optional[float] = None


# ============== Fee ==============
class FeeCreate(BaseModel):
    fee_type: str = Field(..., min_length=1, max_length=50)
    location: Optional[str] = Field(None, pattern="^(inside|outside|厂内|厂外)$")
    amount: float = Field(..., ge=0)
    module_id: Optional[int] = None
    description: Optional[str] = None


class FeeUpdate(BaseModel):
    fee_type: Optional[str] = None
    location: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)
    module_id: Optional[int] = None
    description: Optional[str] = None


class FeeTypeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    name_en: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True


# ============== Labor ==============
class LaborHourCreate(BaseModel):
    name: str = Field(..., min_length=1)
    hours: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)


# ============== Travel ==============
class PackingEntryCreate(BaseModel):
    quotation_id: int
    packing_type_id: int
    quantity: int = Field(..., ge=1)
    unit_price: Optional[float] = None
    remark: Optional[str] = None


class PackingEntryUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    unit_price: Optional[float] = None
    remark: Optional[str] = None


class TravelPersonDaysCreate(BaseModel):
    quotation_id: int
    travel_category_id: int
    person_days: float = Field(..., gt=0)
    unit_price: Optional[float] = None
    remark: Optional[str] = None


class TravelPersonDaysUpdate(BaseModel):
    person_days: Optional[float] = Field(None, gt=0)
    unit_price: Optional[float] = None
    remark: Optional[str] = None


class TravelPersonTripCreate(BaseModel):
    quotation_id: int
    travel_category_id: int
    travel_mode_id: int
    person_count: int = Field(..., ge=1)
    unit_price: Optional[float] = None
    visa_fee: Optional[float] = None
    remark: Optional[str] = None


class TravelPersonTripUpdate(BaseModel):
    person_count: Optional[int] = Field(None, ge=1)
    unit_price: Optional[float] = None
    visa_fee: Optional[float] = None
    remark: Optional[str] = None


# ============== Material ==============
class MaterialCreate(BaseModel):
    name: str = Field(..., min_length=1)
    spec: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    unit_price: float = Field(..., ge=0)
    category: str = Field("standard", pattern="^(large|standard|other|大件|普通件|其他件)$")
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    status: str = Field("active", pattern="^(active|inactive)$")


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    spec: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = Field(None, ge=0)
    category: Optional[str] = None
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    status: Optional[str] = None


# ============== Version ==============
class VersionCreate(BaseModel):
    remark: Optional[str] = None


# ============== User / Role / System ==============
class UserUpdate(BaseModel):
    username: Optional[str] = None
    real_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    is_active: Optional[bool] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


# ============== ExchangeRate ==============
class ExchangeRateCreate(BaseModel):
    currency: str = Field(..., min_length=2, max_length=10)
    rate: float = Field(..., gt=0)
    is_base: bool = False
    description: Optional[str] = None


class ExchangeRateUpdate(BaseModel):
    rate: Optional[float] = Field(None, gt=0)
    is_base: Optional[bool] = None
    description: Optional[str] = None


# ============== Travel Fee ==============
class PackingTypeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    name_en: Optional[str] = None
    unit_price: float = Field(0, ge=0)
    description: Optional[str] = None
    is_active: bool = True


class TravelCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1)
    code: Optional[str] = None
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class TravelDayRateCreate(BaseModel):
    travel_category_id: int
    unit_price: float = Field(0, ge=0)
    currency: str = "CNY"
    description: Optional[str] = None
    is_active: bool = True


class TravelModeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    name_en: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class TravelPersonTripFeeCreate(BaseModel):
    travel_category_id: int
    travel_mode_id: int
    unit_price: float = Field(0, ge=0)
    visa_fee: float = Field(0, ge=0)
    currency: str = "CNY"
    description: Optional[str] = None
    is_active: bool = True


# ============== ChangeRequest ==============
class ChangeRequestCreate(BaseModel):
    quotation_id: int
    changes: List[Dict[str, Any]]
    remark: Optional[str] = None


class ChangeRequestReview(BaseModel):
    reason: Optional[str] = None