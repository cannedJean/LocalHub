<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import WeatherWidget from './WeatherWidget.vue'

const route = useRoute()
const mobileMenuOpen = ref(false)

function closeMenu() {
  mobileMenuOpen.value = false
}
</script>

<template>
  <header
    class="sticky top-0 z-[60] h-[72px] bg-white border-b border-border shadow-sm flex items-center justify-between px-6 md:px-8"
  >
    <div class="flex items-center gap-8">
      <router-link
        to="/"
        class="text-[22px] font-extrabold text-primary tracking-tight focus:outline-none"
        @click="closeMenu"
      >
        ◉ LocalHub
      </router-link>
      <nav class="hidden md:flex gap-6">
        <router-link
          to="/"
          class="text-nav font-medium text-[15px] hover:text-primary transition-colors focus:outline-none"
          active-class="!text-primary !font-bold"
          exact-active-class="!text-primary !font-bold"
        >
          홈
        </router-link>
        <router-link
          to="/places"
          class="text-nav font-medium text-[15px] hover:text-primary transition-colors focus:outline-none"
          :class="{ '!text-primary !font-bold': route.path === '/places' || route.path === '/map' }"
        >
          지역정보·지도
        </router-link>
        <router-link
          to="/boards"
          class="text-nav font-medium text-[15px] hover:text-primary transition-colors focus:outline-none"
          :class="{ '!text-primary !font-bold': route.path.startsWith('/boards') }"
        >
          커뮤니티
        </router-link>
      </nav>
    </div>

    <div class="flex items-center gap-4">
      <WeatherWidget />
      <button
        type="button"
        class="md:hidden text-2xl text-strong w-10 h-10 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-primary rounded"
        :aria-expanded="mobileMenuOpen"
        aria-label="메뉴 열기"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        ☰
      </button>
    </div>
  </header>

  <div
    v-if="mobileMenuOpen"
    class="md:hidden fixed top-[72px] left-0 right-0 bg-white border-b border-border shadow-lg z-[50] flex flex-col p-4 gap-2"
  >
    <router-link
      to="/"
      class="text-[16px] font-bold text-heading p-3 bg-page rounded-lg focus:outline-none"
      @click="closeMenu"
    >
      홈
    </router-link>
    <router-link
      to="/places"
      class="text-[16px] font-bold text-heading p-3 bg-page rounded-lg focus:outline-none"
      @click="closeMenu"
    >
      지역정보
    </router-link>
    <router-link
      to="/map"
      class="text-[16px] font-bold text-heading p-3 bg-page rounded-lg focus:outline-none"
      @click="closeMenu"
    >
      지도 보기
    </router-link>
    <router-link
      to="/boards"
      class="text-[16px] font-bold text-heading p-3 bg-page rounded-lg focus:outline-none"
      @click="closeMenu"
    >
      커뮤니티
    </router-link>
  </div>
</template>
