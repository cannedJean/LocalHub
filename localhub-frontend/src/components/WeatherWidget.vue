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

const weatherIcon = computed(() => {
  const code = String(weather.value?.icon_code || '').trim()
  if (!code) return '☀️'
  if (!/^[0-9]/.test(code)) return code

  const icons = {
    '01': '☀️',
    '02': '🌤️',
    '03': '☁️',
    '04': '☁️',
    '09': '🌧️',
    '10': '🌧️',
    '11': '⛈️',
    '13': '🌨️',
    '50': '🌫️',
  }
  return icons[code.slice(0, 2)] || '🌤️'
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
      class="flex items-center gap-2 bg-primary-tint rounded-[24px] px-3 md:px-4 py-1.5 border border-selected-border opacity-60"
    >
      <span class="text-[14px] text-primary-strong md:hidden">날씨…</span>
      <span class="hidden md:inline text-[14px] text-primary-strong">대전 날씨 확인 중</span>
    </div>

    <div
      v-else-if="failed"
      class="flex items-center gap-2 bg-danger-bg rounded-[24px] px-3 md:px-4 py-1.5 border border-danger-border"
    >
      <span class="text-[13px] text-danger font-medium md:hidden">날씨 오류</span>
      <span class="sr-only md:hidden">날씨 정보를 불러올 수 없습니다.</span>
      <span class="hidden md:inline text-[14px] text-danger font-medium">
        날씨 정보를 불러올 수 없습니다.
      </span>
    </div>

    <div
      v-else-if="weather"
      class="flex items-center gap-1.5 md:gap-2 bg-primary-tint rounded-[24px] px-3 md:px-4 py-1.5 border border-selected-border text-primary-strong text-[14px] font-bold whitespace-nowrap"
    >
      <span aria-hidden="true">{{ weatherIcon }}</span>
      <span class="md:hidden">{{ temperature || '대전' }}</span>
      <span class="hidden md:inline">대전 {{ temperature }}</span>
      <span v-if="recommendationLabel" class="hidden md:inline">· {{ recommendationLabel }}</span>
    </div>
  </div>
</template>
