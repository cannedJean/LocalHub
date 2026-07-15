<script setup>
import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import L from 'leaflet'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import StateView from '../components/StateView.vue'
import Pagination from '../components/Pagination.vue'
import ImagePlaceholder from '../components/ImagePlaceholder.vue'
import { fetchLocations } from '../api/locations'
import { normalizeLocation, normalizePage } from '../utils/normalizers'
import { CITIES, PLACE_FILTER_TYPES } from '../utils/constants'

defineProps({
  mapFirst: { type: Boolean, default: false },
})

// Fix Leaflet's default marker icons under a bundler (otherwise images 404).
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const route = useRoute()
const router = useRouter()

const locationTypesList = PLACE_FILTER_TYPES
const cities = CITIES

const filterKeyword = ref(route.query.keyword || '')
const filterType = ref(route.query.type || null)
const filterCity = ref(route.query.city || null)
const parsePage = (value) => Math.max(1, Number.parseInt(value, 10) || 1)
const page = ref(parsePage(route.query.page))

const items = ref([])
const totalItems = ref(0)
const totalPages = ref(1)
const loading = ref(true)
const error = ref(false)
const selected = ref(null)

const DAEJEON_CENTER = [36.3504, 127.3845]

let mapInstance = null
let markersGroup = null
const markerById = new Map()

const selectedIcon = L.divIcon({
  className: 'custom-selected-marker',
  html: '<div style="background-color:#2563eb;width:24px;height:24px;border-radius:50%;border:3px solid white;box-shadow:0 0 10px rgba(0,0,0,0.5);"></div>',
  iconSize: [24, 24],
  iconAnchor: [12, 12],
})

function initMap() {
  const el = document.getElementById('map')
  if (!el || mapInstance) return
  mapInstance = L.map('map').setView(DAEJEON_CENTER, 10)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      'Leaflet | © OpenStreetMap contributors · 한국관광공사 TourAPI 4.0',
  }).addTo(mapInstance)
  markersGroup = L.layerGroup().addTo(mapInstance)
}

// Build the popup as DOM nodes (textContent) so place data can never inject HTML/XSS.
function buildSafePopup(item) {
  const wrap = document.createElement('div')
  wrap.className = 'w-[300px] p-4 flex flex-col gap-2'

  const imgBox = document.createElement('div')
  imgBox.className =
    'w-full h-[140px] bg-[#e2edff] rounded-lg overflow-hidden relative mb-1 flex items-center justify-center text-5xl'
  if (item.image) {
    const img = document.createElement('img')
    img.src = item.image
    img.alt = ''
    img.className = 'w-full h-full object-cover relative z-10'
    img.onerror = () => {
      img.style.display = 'none'
    }
    imgBox.appendChild(img)
  }
  const emoji = document.createElement('span')
  emoji.className = 'absolute inset-0 flex items-center justify-center z-0'
  emoji.textContent = item.emoji
  imgBox.appendChild(emoji)
  wrap.appendChild(imgBox)

  const title = document.createElement('div')
  title.className = 'font-extrabold text-[17px] text-heading leading-tight'
  title.textContent = item.title
  wrap.appendChild(title)

  const type = document.createElement('div')
  type.className = 'text-[13px] text-primary font-bold'
  type.textContent = `${item.typeLabel} (contentTypeId ${item.typeId})`
  wrap.appendChild(type)

  const addr = document.createElement('div')
  addr.className = 'text-[13px] text-muted leading-tight mt-1 whitespace-pre-wrap'
  const tel = item.telephone ? ` · ☎ ${item.telephone}` : ''
  addr.textContent = `📍 ${item.address}${tel}`
  wrap.appendChild(addr)

  return wrap
}

function renderMarkers() {
  if (!markersGroup || !mapInstance) return
  markersGroup.clearLayers()
  markerById.clear()

  const bounds = []
  items.value.forEach((item) => {
    if (!item.hasValidCoordinates) return
    const marker = L.marker([item.latitude, item.longitude]).addTo(markersGroup)
    marker.bindPopup(() => buildSafePopup(item))
    marker.on('click', () => selectItem(item))
    markerById.set(item.contentId, marker)
    bounds.push([item.latitude, item.longitude])
  })

  if (bounds.length > 0) {
    mapInstance.fitBounds(bounds, { padding: [30, 30], maxZoom: 14 })
  } else {
    mapInstance.setView(DAEJEON_CENTER, 10)
  }
}

function selectItem(item) {
  selected.value = item.contentId
  markerById.forEach((m) => m.setIcon(new L.Icon.Default()))
  const marker = markerById.get(item.contentId)
  if (marker && mapInstance && item.hasValidCoordinates) {
    marker.setIcon(selectedIcon)
    mapInstance.setView([item.latitude, item.longitude], 15)
    marker.openPopup()
  }
}

async function loadData() {
  loading.value = true
  error.value = false
  try {
    const params = { page: page.value, size: 20 }
    if (filterKeyword.value) params.keyword = filterKeyword.value
    if (filterType.value) params.type_id = filterType.value
    if (filterCity.value) params.city = filterCity.value

    const data = await fetchLocations(params)
    const normalized = normalizePage(data, normalizeLocation)
    items.value = normalized.items
    totalItems.value = normalized.total
    totalPages.value = normalized.totalPages
    selected.value = null
    renderMarkers()
  } catch {
    error.value = true
    items.value = []
    if (markersGroup) markersGroup.clearLayers()
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  const query = {}
  if (filterKeyword.value) query.keyword = filterKeyword.value
  if (filterType.value) query.type = filterType.value
  if (filterCity.value) query.city = filterCity.value
  if (page.value > 1) query.page = page.value
  router.push({ path: route.path, query })
}

function submitFilters() {
  page.value = 1
  applyFilters()
}

function setFilterType(id) {
  filterType.value = id
  page.value = 1
  applyFilters()
}

function setFilterCity(id) {
  filterCity.value = id
  page.value = 1
  applyFilters()
}

function changePage(p) {
  page.value = p
  applyFilters()
}

watch(
  () => route.query,
  (q) => {
    filterKeyword.value = q.keyword || ''
    filterType.value = q.type || null
    filterCity.value = q.city || null
    page.value = parsePage(q.page)
    loadData()
  },
)

onMounted(() => {
  nextTick(() => {
    initMap()
    loadData()
  })
})

onUnmounted(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
    markersGroup = null
    markerById.clear()
  }
})
</script>

<template>
  <div class="max-w-[1360px] mx-auto px-6 py-6 md:h-[calc(100vh-72px)] flex flex-col md:flex-row gap-6">
    <!-- List side -->
    <div class="w-full md:w-[480px] flex flex-col gap-4 h-[60vh] md:h-full shrink-0">
      <div class="bg-white rounded-[14px] p-5 shadow-sm border border-border flex flex-col gap-4 shrink-0">
        <h1 class="text-[26px] font-extrabold text-heading">지역정보 찾아보기</h1>
        <div class="relative">
          <label for="place-search" class="sr-only">장소 검색</label>
          <input
            id="place-search"
            v-model="filterKeyword"
            placeholder="🔍  장소명 또는 주소로 검색  (예: 유성, 둘레길, 국밥)"
            class="w-full bg-page border border-border-input rounded-[10px] pl-4 pr-16 py-2.5 outline-none text-[15px] focus:border-primary focus:ring-1 focus:ring-primary"
            @keyup.enter="submitFilters"
          />
          <button
            type="button"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-primary font-bold text-sm px-2 focus:outline-none"
            @click="submitFilters"
          >
            검색
          </button>
        </div>

        <div class="flex flex-col gap-3">
          <div>
            <div class="text-[13px] font-bold text-muted mb-1.5">콘텐츠 유형</div>
            <div class="flex flex-wrap gap-1.5">
              <button
                type="button"
                class="border px-3 py-1.5 rounded-[18px] text-[13px] font-medium transition-colors focus:outline-none"
                :class="!filterType ? 'bg-primary text-white border-primary' : 'bg-white text-nav border-border-input'"
                @click="setFilterType(null)"
              >
                전체
              </button>
              <button
                v-for="t in locationTypesList"
                :key="t.id"
                type="button"
                class="border px-3 py-1.5 rounded-[18px] text-[13px] font-medium transition-colors focus:outline-none"
                :class="filterType === t.id ? 'bg-primary text-white border-primary' : 'bg-white text-nav border-border-input'"
                @click="setFilterType(t.id)"
              >
                {{ t.label }}
              </button>
            </div>
          </div>
          <div>
            <div class="text-[13px] font-bold text-muted mb-1.5">지역</div>
            <div class="flex flex-wrap gap-1.5">
              <button
                type="button"
                class="border px-3 py-1.5 rounded-[17px] text-[13px] font-medium transition-colors focus:outline-none"
                :class="!filterCity ? 'bg-primary text-white border-primary' : 'bg-white text-nav border-border-input'"
                @click="setFilterCity(null)"
              >
                전체
              </button>
              <button
                v-for="c in cities"
                :key="c.id"
                type="button"
                class="border px-3 py-1.5 rounded-[17px] text-[13px] font-medium transition-colors focus:outline-none"
                :class="filterCity === c.id ? 'bg-primary text-white border-primary' : 'bg-white text-nav border-border-input'"
                @click="setFilterCity(c.id)"
              >
                {{ c.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-[14px] shadow-sm border border-border flex-1 flex flex-col overflow-hidden min-h-[200px]">
        <div class="px-5 py-3 border-b border-border flex justify-between items-center bg-subtle shrink-0">
          <span class="font-bold text-strong text-[15px]">검색 결과</span>
          <span class="text-[13px] text-primary font-bold">총 {{ totalItems }}건</span>
        </div>
        <div class="overflow-y-auto flex-1 p-3 flex flex-col gap-2">
          <StateView
            :loading="loading"
            :error="error"
            :empty="items.length === 0"
            empty-message="검색 조건에 맞는 장소가 없습니다."
            @retry="loadData"
          >
            <button
              v-for="item in items"
              :key="item.contentId"
              type="button"
              class="p-3 w-full text-left rounded-[12px] flex gap-4 hover:bg-page transition-colors border border-transparent h-[92px] focus:outline-none"
              :class="{ '!border-selected-border bg-primary-tint': selected === item.contentId }"
              @click="selectItem(item)"
            >
              <div class="w-[64px] h-[64px] rounded-[10px] shrink-0 overflow-hidden">
                <ImagePlaceholder :src="item.image" :emoji="item.emoji" :tint-index="item.tintIndex" />
              </div>
              <div class="flex flex-col justify-center flex-1 overflow-hidden">
                <div class="font-bold text-[16px] text-heading leading-tight mb-1 truncate">
                  {{ item.title }}
                </div>
                <div class="text-[13px] text-muted truncate">
                  {{ item.typeLabel }} · 📍 {{ item.address }}
                </div>
              </div>
            </button>
            <Pagination :page="page" :total-pages="totalPages" class="pb-2" @update:page="changePage" />
          </StateView>
        </div>
      </div>
    </div>

    <!-- Map side -->
    <div
      class="flex-1 bg-white rounded-[14px] shadow-sm border border-border overflow-hidden relative h-[50vh] md:h-full shrink-0 flex flex-col"
      :class="{ 'order-first md:order-none': mapFirst }"
    >
      <div id="map" class="w-full flex-1 z-10"></div>
      <div
        class="absolute bottom-2 right-2 z-[400] bg-white/90 px-2 py-1 text-[11px] text-muted rounded pointer-events-none shadow-sm"
      >
        유효한 좌표가 있는 장소만 지도에 표시됩니다.
      </div>
    </div>
  </div>
</template>
