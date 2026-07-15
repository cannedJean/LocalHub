<script setup>
import { computed, onMounted, ref } from 'vue'
import { fetchWeather } from '../api/weather'

const weather = ref(null)
const loading = ref(true)
const failed = ref(false)

const temperature = computed(() => {
  const value = Number(weather.value?.temperature)
  return Number.isFinite(value) ? `${Math.round(value)}°C` : ''
})

const RECOMMENDATION_LABELS = {
  outdoor: '야외활동 추천',
  indoor: '실내활동 추천',
  mixed: '실내외 모두 좋음',
}

// The API returns an enum (outdoor/indoor/mixed); show the Korean label, or the raw value if unknown.
const recommendationLabel = computed(() => {
  const value = weather.value?.recommendation
  if (!value) return ''
  return RECOMMENDATION_LABELS[value] || value
})

onMounted(async () => {
  try {
    weather.value = await fetchWeather('daejeon')
  } catch {
    // Weather failure must never break the rest of the app.
    failed.value = true
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="weather-widget flex items-center" role="status" aria-live="polite">
    <div
      v-if="loading"
      class="hidden md:flex items-center gap-2 bg-primary-tint rounded-[24px] px-4 py-1.5 border border-selected-border opacity-60"
    >
      <span class="text-[14px] text-primary-strong">대전 날씨 확인 중</span>
    </div>

    <div
      v-else-if="failed"
      class="hidden md:flex items-center gap-2 bg-danger-bg rounded-[24px] px-4 py-1.5 border border-danger-border"
    >
      <span class="text-[14px] text-danger font-medium">날씨 정보를 불러올 수 없습니다.</span>
    </div>

    <div
      v-else-if="weather"
      class="hidden md:flex items-center gap-2 bg-primary-tint rounded-[24px] px-4 py-1.5 border border-selected-border text-primary-strong text-[14px] font-bold"
    >
      <span aria-hidden="true">{{ weather.icon_code || '☀️' }}</span>
      <span>대전 {{ temperature }}</span>
      <span v-if="recommendationLabel">· {{ recommendationLabel }}</span>
    </div>
  </div>
</template>
