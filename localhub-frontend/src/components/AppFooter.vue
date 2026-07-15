<script setup>
// Static footer with the mandatory data-source attribution (공공누리 제3유형).
</script>

<template>
  <footer class="bg-[var(--footer-bg)] text-[var(--footer-text)] py-12 px-6 md:px-8 mt-auto relative z-10">
    <div class="max-w-[1200px] mx-auto flex flex-col gap-4">
      <div class="text-[20px] font-extrabold text-white">◉ LocalHub</div>
      <p class="text-[14px] text-[var(--footer-text)] leading-relaxed">
        본 서비스는 한국관광공사 TourAPI 4.0 국문 관광정보 데이터를 활용하였습니다.
      </p>
      <p class="text-[13px] text-[var(--footer-text)]">
        출처: 한국관광공사 | 데이터: TourAPI 4.0 국문 관광정보 | 라이선스: 공공누리 제3유형
        (출처표시-변경금지)
      </p>
      <p class="text-[13px] text-[var(--footer-faint)]">
        대전·세종·계룡·공주·논산·옥천 | 총 1,365건 |
        <router-link to="/sources" class="underline underline-offset-2 hover:text-white">
          데이터 출처 자세히 보기
        </router-link>
        | © 2026 LocalHub. 비상업·교육용 프로젝트
      </p>
    </div>
  </footer>
</template>
