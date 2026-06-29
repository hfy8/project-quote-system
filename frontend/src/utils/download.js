/**
 * 工具: 给 URL 加 token 参数, 用于 window.open 下载
 *
 * 背景: window.open() 不会自动加 Authorization header,
 *       后端 get_current_user_id 加了 ?token=xxx fallback 兼容
 */
export function withToken(url) {
  const token = localStorage.getItem('token')
  if (!token) return url
  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}token=${encodeURIComponent(token)}`
}

/**
 * 打开下载链接 (新窗口) - 自动带 token
 */
export function openDownload(url) {
  window.open(withToken(url), '_blank')
}
