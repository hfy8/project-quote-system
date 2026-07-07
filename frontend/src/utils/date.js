/**
 * 时间解析工具 - 统一处理后端 UTC 时间字符串
 *
 * 后端所有 datetime 字段都用 datetime.utcnow() 写入, 序列化时调用 .isoformat(),
 * 返回形如 "2026-07-06T01:41:55.356148" 的字符串, 没有时区后缀.
 *
 * JavaScript 的 new Date('2026-07-06T01:41:55.356148') 会按本地时间 (CST = UTC+8) 解析,
 * 导致 diff 偏差 8 小时 (消息显示成 "8 小时前" 但其实刚创建).
 *
 * 解决方法: 如果字符串没有时区后缀 (Z / +HH:MM / -HH:MM), 视为 UTC, 加 'Z' 后再解析.
 *
 * 注意: 已经带时区的字符串 (如前端手动构造的 ISO +00:00) 不需要再加 Z.
 */

/**
 * 把后端 UTC 时间字符串解析为本地时区 Date 对象
 * @param {string|Date|number|null} t - 时间字符串或 Date 对象
 * @returns {Date|null}
 */
export function parseUtcDate(t) {
  if (!t) return null
  if (t instanceof Date) return t
  // 已经是 Date 的合法字符串 (ISO + 时区), 直接解析
  // 形如 2026-07-06T01:41:55.356148 / 2026-07-06T01:41:55 / 2026-07-06 01:41:55
  if (typeof t === 'string') {
    // 检查是否带时区后缀
    const hasTz = /Z$|[+-]\d{2}:?\d{2}$/.test(t.trim())
    if (!hasTz && /^\d{4}-\d{2}-\d{2}/.test(t.trim())) {
      // 后端 UTC 时间, 加 Z 标记
      // 把空格替换为 T (兼容 "2026-07-06 01:41:55")
      const iso = t.trim().replace(' ', 'T')
      return new Date(iso + 'Z')
    }
    return new Date(t)
  }
  return new Date(t)
}

/**
 * 把时间字符串格式化为"X 分钟前 / X 小时前 / X 天前 / 具体日期"
 * @param {string|Date} t - 时间字符串 (后端 UTC)
 * @returns {string}
 */
export function formatRelativeTime(t) {
  if (!t) return ''
  const d = parseUtcDate(t)
  if (!d || isNaN(d.getTime())) return ''
  const now = new Date()
  const diff = (now - d) / 1000
  if (diff < 0) return '刚刚'  // 未来 (服务器/客户端时钟偏差)
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`
  if (diff < 604800) return `${Math.floor(diff / 86400)} 天前`
  return `${d.getMonth() + 1}-${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}