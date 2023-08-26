<script setup lang="ts">
import { usePresentStore } from "~/stores/presentation";

const presentStore = usePresentStore();

const fetchData = () => {
  presentStore.fetchCurrentPres();
};

onMounted(() => {
  setInterval(fetchData, 4000);
});
</script>

<template>
  <div>
    Loading...
    {{ presentStore.currentPresentation }}
  </div>
</template>
