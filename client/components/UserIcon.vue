<script setup lang="ts">
import { toSvg } from 'jdenticon'
import { computed } from 'vue'
import { APIUser, TelegramUserData } from '~/utils/auth';

const props = defineProps<{ user: APIUser | TelegramUserData }>()

const jdenticon = computed(() => {
  if (props.user.photo_url) return null
  return toSvg(props.user.id, 128).replace('width="128"', 'width="100%"').replace('height="128"', 'height="100%"')
})
</script>

<template>
  <img
    v-if="user.photo_url"
    :src="user.photo_url"
    alt=""
    class="userAvatar"
  />
  <div v-else v-html="jdenticon" class="userAvatar jdenticon-wrapper"></div>
</template>

<style scoped>
.jdenticon-wrapper {
  background-color: rgb(47, 47, 47);
}
</style>