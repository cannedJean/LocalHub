export function formatDate(value, includeTime = false) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '-'
  const datePart = new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
    .format(date)
    .replaceAll(' ', '')
    .replace(/\.$/, '')

  if (!includeTime) return datePart
  const timePart = new Intl.DateTimeFormat('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(date)
  return `${datePart} ${timePart}`
}

export function formatNumber(value) {
  return Number(value || 0).toLocaleString('ko-KR')
}
