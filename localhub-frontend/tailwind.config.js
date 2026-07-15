/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',
        'primary-strong': '#1d4ed8',
        'primary-tint': '#eff6ff',
        'link-chip-bg': '#eff3fe',
        'selected-border': '#c6d9fe',
        heading: '#111827',
        body: '#374151',
        strong: '#1f2937',
        muted: '#6b7280',
        faint: '#9ca3af',
        nav: '#4a5568',
        page: '#f8fafd',
        card: '#ffffff',
        subtle: '#f3f4f6',
        chat: '#f6f8fb',
        border: '#e5e7eb',
        'border-input': '#d9dde5',
        'border-list': '#edeff2',
        danger: '#dc2626',
        'danger-bg': '#fff2f2',
        'danger-border': '#f9b5b5',
      },
      fontFamily: {
        sans: ['Inter', 'Pretendard', 'Apple SD Gothic Neo', 'Noto Sans KR', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
