import { CONTENT_TYPES } from '../data/constants'

const typeMap = new Map(CONTENT_TYPES.map((type) => [String(type.id), type]))
const tints = ['var(--tint-blue)', 'var(--tint-green)', 'var(--tint-orange)', 'var(--tint-purple)']

function parseCoordinate(value, min, max) {
  if (value === null || value === undefined || value === '') return null
  const parsed = Number.parseFloat(value)
  return Number.isFinite(parsed) && parsed >= min && parsed <= max ? parsed : null
}

export function normalizeLocation(source = {}, index = 0) {
  const id = String(source.contentid ?? source.content_id ?? source.id ?? '')
  const typeId = String(source.contenttypeid ?? source.content_type_id ?? source.type_id ?? '')
  const type = typeMap.get(typeId) || { label: source.type_label || '기타', emoji: '📍' }
  const longitude = parseCoordinate(source.mapx ?? source.longitude, -180, 180)
  const latitude = parseCoordinate(source.mapy ?? source.latitude, -90, 90)
  const addr1 = source.addr1 ?? source.address ?? source.full_address ?? ''
  const addr2 = source.addr2 ?? ''

  return {
    id,
    typeId,
    typeLabel: source.type_label || type.label,
    emoji: type.emoji,
    title: source.title || '이름 없는 장소',
    address: [addr1, addr2].filter(Boolean).join(' ') || '주소 정보 없음',
    tel: source.tel || '전화번호 정보 없음',
    city: source.city || '',
    cityLabel: source.city_label || '',
    image: String(source.firstimage || source.firstimage2 || source.thumbnail_url || '').replace(
      /^http:/,
      'https:',
    ),
    latitude,
    longitude,
    hasValidCoordinates: latitude !== null && longitude !== null,
    tint: tints[index % tints.length],
    raw: source,
  }
}

export function normalizeLocationResponse(payload = {}) {
  const envelope = payload?.data && !Array.isArray(payload) ? payload.data : payload
  const sourceItems = Array.isArray(envelope) ? envelope : envelope?.items || envelope?.results || []
  const items = sourceItems.map(normalizeLocation)
  return {
    items,
    total: Number(envelope?.total ?? items.length),
    page: Number(envelope?.page ?? 1),
    size: Number(envelope?.size ?? items.length),
    totalPages: Number(envelope?.totalPages ?? envelope?.total_pages ?? 1),
  }
}
