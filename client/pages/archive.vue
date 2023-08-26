<script setup lang="ts">
import { usePresentStore } from "~/stores/presentation";

const presentStore = usePresentStore();

onMounted(() => {
  presentStore.fetchPresentations();
  setInterval(presentStore.fetchPresentations, 4000);
});
</script>

<template>
  <div class="container mt-5">
    <div v-if="presentStore.presentations?.length" v-for="pres in presentStore.presentations">
      <PresentationCard :obj="pres" />
    </div>
    <div v-else>
      <div class="text-light">
        <div class="text-center fs-5 mb-4">У вас ещё нет ни одной презентации</div>
        <div class="text-center">
          <NuxtLink to="/generate" class="btn btn-outline-light">Сгенерировать</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  margin-bottom: 320px;
}
</style>
