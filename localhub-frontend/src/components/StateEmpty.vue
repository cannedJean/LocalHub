<script setup>
defineProps({
  message: { type: String, default: '표시할 정보가 없습니다.' },
  description: { type: String, default: '' },
})
</script>

<template>
  <div class="state">
    <span class="icon" aria-hidden="true">🗂️</span>
    <p class="message">{{ message }}</p>
    <p v-if="description" class="description">{{ description }}</p>
    <slot />
  </div>
</template>

<style scoped>
.state {
  display: flex;
  min-height: 180px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 28px;
  text-align: center;
}

.icon {
  font-size: 30px;
}

.message {
  color: var(--text-strong);
  font-size: 16px;
  font-weight: 700;
}

.description {
  color: var(--text-muted);
  font-size: 14px;
}
</style>
