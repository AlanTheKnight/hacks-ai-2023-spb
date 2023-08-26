<script setup lang="ts">
import { useAuthStore } from "./stores/auth";
import { usePresentStore } from "./stores/presentation";

const authStore = useAuthStore();
const presentStore = usePresentStore();

onMounted(() => {
  if (authStore.user === null && authStore.access_token) {
    authStore.getCurrentUserAction();
  }
});
</script>

<template>
  <MainNavbar />
  <div class="rt-wp view-wrapper">
    <NuxtPage />
  </div>
  <MainFooter />
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

.view-wrapper {
  min-height: 1vh;
}

/* @media (min-width: 768px) {
  .view-wrapper {
    margin-bottom: 320px;
  }
} */
</style>
