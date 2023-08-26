<template>
  <footer class="border-top footer w-100" id="footer">
    <div class="container pb-3 pt-3">
      <div class="row d-flex justify-content-between align-items-center">
        <img class="col-6 col-md-3 mb-3 mb-md-0" src="@/assets/images/team-logo.svg" height="40" alt="" />
        <img class="col-6 col-md-3 mb-3 mb-md-0" src="@/assets/images/hacks-ai-logo.svg" height="60" alt="" />
        <img class="col-6 col-md-3" src="@/assets/images/rsv-logo.svg" height="60" alt="" />
        <img class="col-6 col-md-3" src="@/assets/images/minecom-logo.svg" height="60" alt="" />
      </div>
    </div>
    <div class="border-top">
      <div class="container py-2">
        <div class="text-muted text-center">
          Данный сервис является решением одного из кейсов хакатона «Цифровой Прорыв: Сезон
          Искусственный Интеллект» в ЗСФО 25.08 — 27.08.2023
        </div>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup></script>

<style scoped>
.footer {
  position: absolute;
  left: 0;
  bottom: 0;
}

.footer-darker {
  background-color: #cadbfb;
  line-height: 40px;
}

@media (max-width: 768px) {
  .mb-10 {
    margin-bottom: 4.5rem;
  }
}

#version {
  white-space: nowrap;
}

#diaryx-info {
  flex-wrap: wrap;
}
</style>
