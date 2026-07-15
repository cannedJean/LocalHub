<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import StateView from '../components/StateView.vue'
import ImagePlaceholder from '../components/ImagePlaceholder.vue'
import { fetchLocations } from '../api/locations'
import { fetchPosts } from '../api/posts'
import { normalizeLocation, normalizePage } from '../utils/normalizers'
import { HOME_CATEGORIES, getCategoryColor, getCategoryLabel, formatDateShort } from '../utils/constants'

const router = useRouter()
const searchKeyword = ref('')

const categories = HOME_CATEGORIES

const locations = ref([])
const loadingLoc = ref(true)
const errorLoc = ref(false)

const posts = ref([])
const loadingPosts = ref(true)
const errorPosts = ref(false)

async function loadLocations() {
  loadingLoc.value = true
  errorLoc.value = false
  try {
    const data = await fetchLocations({ size: 3 })
    locations.value = normalizePage(data, normalizeLocation).items
  } catch {
    errorLoc.value = true
  } finally {
    loadingLoc.value = false
  }
}

async function loadPosts() {
  loadingPosts.value = true
  errorPosts.value = false
  try {
    const data = await fetchPosts({ size: 4 })
    posts.value = normalizePage(data).items
  } catch {
    errorPosts.value = true
  } finally {
    loadingPosts.value = false
  }
}

function goSearch() {
  const keyword = searchKeyword.value.trim()
  if (keyword) router.push({ path: '/places', query: { keyword } })
}

onMounted(() => {
  loadLocations()
  loadPosts()
})
</script>

<template>
  <div class="pb-16">
    <!-- Hero -->
    <section class="bg-primary text-white text-center py-16 px-6">
      <p class="text-[16px] font-semibold text-[#d9e5ff] mb-3">대전 · 세종 · 충청권</p>
      <h1 class="text-[32px] md:text-[44px] font-extrabold mb-5 leading-tight">
        지역의 모든 정보를 한 곳에서,<br class="md:hidden" /> LocalHub
      </h1>
      <p class="text-[15px] md:text-[17px] text-[#e5edff] mb-10 max-w-2xl mx-auto">
        관광지 · 맛집 · 축제 정보부터 이웃 주민과의 이야기까지.<br class="md:hidden" /> 회원가입
        없이 지금 바로 이용하세요.
      </p>
      <div class="max-w-[620px] mx-auto flex items-center bg-white rounded-[12px] p-2 shadow-lg">
        <label for="hero-search" class="sr-only">장소 검색</label>
        <input
          id="hero-search"
          v-model="searchKeyword"
          type="text"
          placeholder="🔍  지역, 장소, 키워드를 검색해 보세요"
          class="flex-1 px-4 py-3 outline-none text-body text-[15px] bg-transparent"
          @keyup.enter="goSearch"
        />
        <button
          type="button"
          class="bg-primary hover:bg-primary-strong text-white px-6 py-3 rounded-lg font-bold text-[15px] transition-colors"
          @click="goSearch"
        >
          검색
        </button>
      </div>
    </section>

    <div class="max-w-[1200px] mx-auto px-6 py-12 flex flex-col gap-16">
      <!-- Categories -->
      <section>
        <h2 class="text-[22px] font-extrabold text-heading mb-6">카테고리 바로가기</h2>
        <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
          <button
            v-for="c in categories"
            :key="c.id"
            type="button"
            class="bg-page border border-border rounded-[14px] p-6 flex flex-col items-center justify-center hover:border-primary hover:shadow-sm transition-all gap-2 h-[116px] focus:outline-none focus:ring-2 focus:ring-primary"
            @click="router.push({ path: '/places', query: { type: c.id } })"
          >
            <span class="text-3xl" aria-hidden="true">{{ c.emoji }}</span>
            <span class="text-[15px] font-bold text-strong">{{ c.label }}</span>
          </button>
        </div>
      </section>

      <!-- Recommended places -->
      <section>
        <h2 class="text-[22px] font-extrabold text-heading mb-6">대전·충청 추천 장소</h2>
        <StateView
          :loading="loadingLoc"
          :error="errorLoc"
          :empty="locations.length === 0"
          empty-message="추천할 장소가 없습니다."
          @retry="loadLocations"
        >
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <button
              v-for="loc in locations"
              :key="loc.contentId"
              type="button"
              class="bg-white border border-border rounded-[14px] overflow-hidden hover:shadow-md transition-shadow text-left w-full flex flex-col focus:outline-none focus:ring-2 focus:ring-primary"
              @click="router.push({ path: '/places', query: { keyword: loc.title } })"
            >
              <div class="h-[150px] w-full shrink-0">
                <ImagePlaceholder :src="loc.image" :emoji="loc.emoji" :tint-index="loc.tintIndex" />
              </div>
              <div class="p-5 flex flex-col gap-1 flex-1">
                <div class="text-[17px] font-bold text-strong truncate">
                  {{ loc.typeLabel }} · {{ loc.title }}
                </div>
                <div class="text-[14px] text-muted truncate">📍 {{ loc.address }}</div>
              </div>
            </button>
          </div>
        </StateView>
      </section>

      <!-- Recent posts -->
      <section>
        <div class="flex justify-between items-end mb-6">
          <h2 class="text-[22px] font-extrabold text-heading">커뮤니티 최근 게시글</h2>
          <router-link to="/boards" class="text-primary font-bold text-[15px] hover:underline">
            전체보기 ›
          </router-link>
        </div>
        <StateView
          :loading="loadingPosts"
          :error="errorPosts"
          :empty="posts.length === 0"
          empty-message="아직 게시글이 없습니다."
          @retry="loadPosts"
        >
          <div class="bg-white border border-border rounded-[14px] overflow-hidden">
            <router-link
              v-for="p in posts"
              :key="p.id"
              :to="`/boards/${p.id}`"
              class="flex flex-col md:flex-row md:items-center justify-between p-4 border-b border-border-list hover:bg-page transition-colors last:border-0 gap-2 md:h-[60px] focus:outline-none focus:bg-page"
            >
              <div class="flex items-center gap-3 overflow-hidden">
                <span :class="['cat-badge shrink-0', getCategoryColor(p.category)]">
                  {{ getCategoryLabel(p.category) }}
                </span>
                <span class="text-[15px] font-medium text-strong truncate">{{ p.title }}</span>
              </div>
              <div class="text-[13px] text-faint flex gap-2 shrink-0">
                <span>{{ formatDateShort(p.created_at) }}</span>
                <span v-if="p.views !== undefined && p.views !== null">· 조회 {{ p.views }}</span>
              </div>
            </router-link>
          </div>
        </StateView>
      </section>
    </div>
  </div>
</template>
