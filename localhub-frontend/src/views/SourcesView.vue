<script setup>
import { LOCATION_TYPE_COUNTS, TOTAL_LOCATION_COUNT } from '../utils/constants'
</script>

<template>
  <div class="max-w-[800px] mx-auto px-6 py-12 min-h-[calc(100vh-260px)]">
    <h1 class="text-[26px] font-extrabold text-heading mb-8">데이터 출처 및 라이선스</h1>

    <div class="bg-white border border-border rounded-[14px] p-8 flex flex-col gap-8 text-[15px] text-body shadow-sm">
      <div class="border-l-4 border-primary pl-4">
        <h2 class="font-extrabold text-strong text-[18px] mb-2">데이터 제공</h2>
        <p class="mb-1"><span class="font-bold text-heading">제공 기관:</span> 한국관광공사</p>
        <p><span class="font-bold text-heading">데이터명:</span> TourAPI 4.0 국문 관광정보</p>
      </div>

      <div class="border-l-4 border-primary pl-4">
        <h2 class="font-extrabold text-strong text-[18px] mb-2">활용 범위</h2>
        <p class="mb-1"><span class="font-bold text-heading">대상 권역:</span> 대전·충청권</p>
        <p class="mb-1">
          <span class="font-bold text-heading">포함 지역:</span> 대전, 세종, 계룡, 공주, 논산, 옥천
        </p>
        <p>
          <span class="font-bold text-heading">총 건수:</span>
          {{ TOTAL_LOCATION_COUNT.toLocaleString() }}건
        </p>
      </div>

      <div class="border-l-4 border-primary pl-4">
        <h2 class="font-extrabold text-strong text-[18px] mb-3">콘텐츠 유형별 건수</h2>
        <table class="w-full max-w-[400px] text-left border-collapse border border-border">
          <thead>
            <tr class="bg-subtle text-muted text-[13px]">
              <th class="p-2 border border-border">유형</th>
              <th class="p-2 border border-border">건수</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in LOCATION_TYPE_COUNTS" :key="row.label">
              <td class="p-2 border border-border text-[14px]">{{ row.label }}</td>
              <td class="p-2 border border-border text-[14px]">{{ row.count.toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="border-l-4 border-primary pl-4">
        <h2 class="font-extrabold text-strong text-[18px] mb-2">라이선스 표기</h2>
        <p class="font-bold text-primary text-[16px]">공공누리 제3유형 (출처표시-변경금지)</p>
        <p class="mt-2 text-muted text-[14px] leading-relaxed">
          출처: 한국관광공사 | 데이터: TourAPI 4.0 국문 관광정보 | 라이선스: 공공누리 제3유형
          (출처표시-변경금지)<br />
          원본 데이터의 수정·변형은 금지되며, 본 서비스는 비상업·교육용으로 구현되었습니다. 지도는
          OpenStreetMap을 사용합니다.
        </p>
      </div>
    </div>
  </div>
</template>
