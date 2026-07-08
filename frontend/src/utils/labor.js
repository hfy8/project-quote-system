// 8 工时 = 1 人天 (标准 1 天 8 小时)
export const HOURS_PER_DAY = 8

// 7 个固定工时名称 (选择后自动匹配工时类型)
export const LABOR_NAME_CHOICES = [
  { name: '机械设计',                     labor_type: 'design' },
  { name: '电控编程设计（PLC&HMI）',         labor_type: 'design' },
  { name: '软件编程设计（C#&Vision&robot）', labor_type: 'design' },
  { name: '生产装配',                     labor_type: 'assembly' },
  { name: '机械厂外调试',                 labor_type: 'debug' },
  { name: '电控编程厂外调试（PLC&HMI）',      labor_type: 'debug' },
  { name: '软件编程厂外调试（C#&Vision&robot）', labor_type: 'debug' },
]

export const LABOR_TYPE_CHOICES = [
  { value: 'design', label: '设计', color: '#3b82f6' },
  { value: 'debug', label: '调试', color: '#f59e0b' },
  { value: 'assembly', label: '装配', color: '#10b981' },
]

// 人天 ↔ 工时 双向换算
export function formatPersonDays(hours) {
  if (!hours) return '0.00'
  return (hours / HOURS_PER_DAY).toFixed(2)
}

export function hoursToPersonDays(hours) {
  if (hours == null) hours = 0
  return +(hours / HOURS_PER_DAY).toFixed(2)
}

export function personDaysToHours(days) {
  if (days == null) days = 0
  return +(days * HOURS_PER_DAY).toFixed(1)
}