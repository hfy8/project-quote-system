<template>
  <div v-if="summary" class="summary-top-cards">
    <!-- 第一行: 硬件 / 设计重写 / 调试重写 / 差旅(人天) / 认证 -->
    <div class="summary-row-cards">
      <div class="summary-mini-card card-hardware">
        <div class="summary-mini-icon">🔧</div>
        <div class="summary-mini-label">硬件成本</div>
        <div class="summary-mini-value highlight">{{ fmtMoney(summary.material_total_with_rates) }}</div>
      </div>
      <div class="summary-mini-card card-design">
        <div class="summary-mini-icon">📐</div>
        <div class="summary-mini-label">设计成本</div>
        <div class="summary-mini-value">{{ fmtMoney(designLaborCost ?? summary?.design_total) }}</div>
      </div>
      <div class="summary-mini-card card-debug">
        <div class="summary-mini-icon">🔍</div>
        <div class="summary-mini-label">调试成本</div>
        <div class="summary-mini-value">{{ fmtMoney(debugLaborCost ?? summary?.debug_total) }}</div>
      </div>
      <div class="summary-mini-card card-travel">
        <div class="summary-mini-icon">✈️</div>
        <div class="summary-mini-label">差旅成本（人天）</div>
        <div class="summary-mini-value">{{ fmtMoney(summary.travel_person_days_total) }}</div>
      </div>
      <div class="summary-mini-card card-cert">
        <div class="summary-mini-icon">📜</div>
        <div class="summary-mini-label">认证费用成本</div>
        <div class="summary-mini-value">{{ fmtMoney(certificationFeeCost) }}</div>
      </div>
    </div>

    <!-- 第二行: 机票签证 / 项目管理 / 项目利润重写 / 包装运输 / 最终报价 -->
    <div class="summary-row-cards">
      <div class="summary-mini-card card-travel-trips">
        <div class="summary-mini-icon">🚄</div>
        <div class="summary-mini-label">机票签证成本</div>
        <div class="summary-mini-value">{{ fmtMoney(summary.travel_person_trips_total) }}</div>
      </div>
      <div class="summary-mini-card card-mgmt">
        <div class="summary-mini-icon">📋</div>
        <div class="summary-mini-label">项目管理费</div>
        <div class="summary-mini-value">{{ fmtMoney(managementFeeTotal) }}</div>
      </div>
      <div class="summary-mini-card card-profit">
        <div class="summary-mini-icon">💰</div>
        <div class="summary-mini-label">项目利润</div>
        <div class="summary-mini-value">{{ fmtMoney(profitAmount ?? summary?.profit_total) }}</div>
      </div>
      <div class="summary-mini-card card-packing">
        <div class="summary-mini-icon">📦</div>
        <div class="summary-mini-label">包装运输成本</div>
        <div class="summary-mini-value">{{ fmtMoney(summary.packing_total) }}</div>
      </div>
      <div class="summary-mini-card card-final">
        <div class="summary-mini-icon">💵</div>
        <div class="summary-mini-label">最终报价</div>
        <div class="summary-mini-value huge">{{ fmtMoney(summary.grand_total) }}</div>
        <div class="summary-mini-sub">含税 ¥{{ taxAmount?.toFixed(2) || '0.00' }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  summary: { type: Object, default: null },
  // 可选重写: 各卡片的值, 不传则从 summary 取
  designLaborCost: { type: Number, default: null },
  debugLaborCost: { type: Number, default: null },
  profitAmount: { type: Number, default: null },
  managementFeeTotal: { type: Number, default: 0 },
  certificationFeeCost: { type: Number, default: 0 },
  selectedCurrency: { type: String, default: 'CNY' },
  fmtMoney: { type: Function, required: true },
  taxAmount: { type: Number, default: 0 },
})
</script>

<style scoped>
.summary-top-cards { margin-bottom: 16px; }
.summary-row-cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 10px; }
.summary-mini-card {
  background: var(--color-bg-secondary, #f8fafc);
  border: 1px solid var(--color-border, #e2e8f0);
  border-radius: var(--radius-md, 8px);
  padding: 12px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.summary-mini-card.card-final {
  background: linear-gradient(135deg, #e0f2fe, #dbeafe);
  border-color: #93c5fd;
  border-left: 6px solid #2563eb;
}
.summary-mini-card.card-hardware { border-left: 4px solid #3b82f6; }
.summary-mini-card.card-design { border-left: 4px solid #8b5cf6; }
.summary-mini-card.card-debug { border-left: 4px solid #f59e0b; }
.summary-mini-card.card-travel { border-left: 4px solid #10b981; }
.summary-mini-card.card-cert { border-left: 4px solid #06b6d4; }
.summary-mini-card.card-travel-trips { border-left: 4px solid #14b8a6; }
.summary-mini-card.card-mgmt { border-left: 4px solid #6366f1; }
.summary-mini-card.card-profit { border-left: 4px solid #ef4444; }
.summary-mini-card.card-packing { border-left: 4px solid #f97316; }
.summary-mini-icon { font-size: 20px; margin-bottom: 4px; }
.summary-mini-label { font-size: 11px; color: var(--color-text-muted, #64748b); margin-bottom: 4px; white-space: nowrap; }
.summary-mini-value { font-size: 18px; font-weight: 700; color: var(--color-text-primary, #1e293b); }
.summary-mini-value.huge { font-size: 22px; color: #1d4ed8; }
.summary-mini-value.highlight { color: #2563eb; }
.summary-mini-sub { font-size: 11px; color: #6b7280; margin-top: 2px; }
</style>
