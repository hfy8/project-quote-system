"""
.env loader for backend_fastapi
用法: from utils.env_loader import load_env; load_env()

优先级 (后启动的覆盖先启动的):
    1. .env 文件 (如果存在, 自动 export)
    2. shell 已有环境变量 (优先级最高)
"""
import os
import sys
from pathlib import Path


def load_env(env_file=None):
    """加载 .env 文件到环境变量"""
    if env_file is None:
        env_file = Path(__file__).resolve().parent.parent / '.env'
    else:
        env_file = Path(env_file)

    loaded = {}
    if not env_file.exists():
        print(f"⚠️  .env 不存在: {env_file} (使用环境变量或代码默认值)")
        return loaded

    print(f"📝 加载 .env: {env_file}")
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key not in os.environ:
                os.environ[key] = value
                loaded[key] = value

    print(f"   已加载 {len(loaded)} 个变量")
    return loaded


if __name__ == '__main__':
    """直接运行: python3 -m utils.env_loader [path/to/.env]"""
    path = sys.argv[1] if len(sys.argv) > 1 else None
    loaded = load_env(path)
    # 打印非敏感的 URL/路径类
    print("\n当前生效的配置:")
    for k in ['DATABASE_URL', 'REDIS_URL']:
        v = os.environ.get(k, '<未设置>')
        print(f"   {k} = {v}")
    # 敏感 KEY 只显示长度
    print("\n敏感 KEY (只显示长度):")
    for k in os.environ:
        if 'KEY' in k or 'SECRET' in k or 'PASSWORD' in k or 'TOKEN' in k:
            v = os.environ[k]
            if len(v) > 8:
                print(f"   {k} = {v[:4]}***{v[-4:]} (len={len(v)})")
            else:
                print(f"   {k} = *** (len={len(v)})")
