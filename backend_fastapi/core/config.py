import os


# 生产环境 fail-fast: 必须设置密钥
_ENV = os.environ.get('FLASK_ENV', os.environ.get('APP_ENV', 'production'))
_IS_PROD = _ENV in ('production', 'prod')


def _require_secret(env_var: str, fallback: str) -> str:
    """生产环境强制要求密钥, 开发环境可 fallback"""
    val = os.environ.get(env_var)
    if val:
        return val
    if _IS_PROD:
        raise RuntimeError(
            f'🚨 [{env_var}] 未设置! 生产环境必须设置. '
            f'生成密钥: python -c "import secrets; print(secrets.token_hex(32))"'
        )
    print(f'⚠️  [{env_var}] 使用代码默认值 (仅开发环境!)', file=__import__('sys').stderr)
    return fallback


class Config:
    """应用配置"""
    SECRET_KEY = _require_secret('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = _require_secret('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:***@localhost:5432/quotation_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    JSON_AS_ASCII = False
