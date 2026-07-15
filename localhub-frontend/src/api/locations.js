import apiClient from './client'

export function fetchLocationTypes() {
  return apiClient.get('/location-types').then((res) => res.data)
}

export function fetchLocations(params = {}) {
  return apiClient.get('/locations', { params }).then((res) => res.data)
}

export function fetchLocation(contentId) {
  return apiClient.get(`/locations/${contentId}`).then((res) => res.data)
}
