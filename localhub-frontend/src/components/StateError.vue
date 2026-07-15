<script setup>
defineProps({
  message: { type: String, default: '정보를 불러오지 못했습니다.' },
})

defineEmits(['retry'])
</script>

<template>
  <div class="state" role="alert">
    <span class="icon" aria-hidden="true">⚠️</span>
    <p>{{ message }}</p>
    <button type="button" class="button button-primary" @click="$emit('retry')">다시 시도</button>
  </div>
</template>

<style scoped>
.state {
  display: flex;
  min-height: 180px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 28px;
  color: var(--text-muted);
  text-align: center;
}

.icon {
  font-size: 30px;
}
</style>
