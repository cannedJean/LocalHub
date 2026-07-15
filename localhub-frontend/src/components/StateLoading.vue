<script setup>
defineProps({
  label: { type: String, default: '정보를 불러오는 중입니다.' },
})
</script>

<template>
  <div class="state" role="status" aria-live="polite">
    <span class="spinner" aria-hidden="true"></span>
    <span>{{ label }}</span>
  </div>
</template>

<style scoped>
.state {
  display: flex;
  min-height: 180px;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--text-muted);
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--selected-border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 700ms linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
  }
}
</style>
