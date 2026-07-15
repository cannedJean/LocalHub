<script setup>
defineProps({
  items: { type: Array, required: true },
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, required: true },
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="chips" role="group" :aria-label="label">
    <button
      v-for="item in items"
      :key="String(item.id)"
      type="button"
      class="chip"
      :class="{ active: String(modelValue) === String(item.id) }"
      :aria-pressed="String(modelValue) === String(item.id)"
      @click="$emit('update:modelValue', item.id)"
    >
      {{ item.label }}
    </button>
  </div>
</template>

<style scoped>
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  min-height: 38px;
  border: 1px solid var(--border-input);
  border-radius: 999px;
  padding: 0 15px;
  color: var(--text-nav);
  background: white;
  font-size: 14px;
  font-weight: 600;
}

.chip:hover {
  border-color: var(--selected-border);
  color: var(--primary-strong);
}

.chip.active {
  border-color: var(--primary);
  color: white;
  background: var(--primary);
}
</style>
