<template>
  <MainNavbar />
  <div class="rt-wp view-wrapper">
    <NuxtPage />
  </div>
</template>

<style>
.rt-wp {
  padding-top: 60px;
}

html {
  position: relative;
  min-height: 100%;
  scroll-behavior: smooth;
}

/* @media (min-width: 768px) {
  .view-wrapper {
    margin-bottom: 320px;
  }
} */
</style>
