import apiClient from './client'

// The weather API key lives in the backend .env; the frontend never calls the provider directly.
export function fetchWeather(city = 'daejeon') {
  return apiClient.get('/weather', { params: { city } }).then((res) => res.data)
}
