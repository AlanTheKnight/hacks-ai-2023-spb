<script lang="ts" setup>
import { scrollToSection } from "@/utils/scrolling";
import { useAuthStore } from "~/stores/auth";

const authStore = useAuthStore();

const isScrolled = ref(false);

const onScroll = () => {
  isScrolled.value = window.scrollY > 0;
};

onMounted(() => {
  window.addEventListener("scroll", onScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", onScroll);
});
</script>

<template>
  <nav
    id="mainNavbar"
    class="navbar navbar-expand-md fixed-top bg-dark"
    :class="{
      scrolled: isScrolled,
    }">
    <div class="container position-relative">
      <NuxtLink
        @click.prevent="scrollToSection('#home')"
        to="/"
        class="navbar-brand d-flex align-items-center start-0 ms-3 fw-bold">
        <img src="@/assets/images/logo.svg" alt="" height="38" class="me-2" />
        NeoPitch
      </NuxtLink>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        id="mainNavbarToggler"
        data-bs-target="#mainNavbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="mainNavbarContent">
        <ul class="navbar-nav mt-1 mx-auto">
          <!-- <li class="nav-item">
            <a
              class="nav-link"
              href="#about-us-section"
              @click.prevent="scrollToSection('#about-us-section')"
              >О нас</a
            >
          </li> -->
        </ul>

        <!-- <button
          class="btn btn-outline-primary end-0 me-3"
          id="callToActionButton"
          @click.prevent="scrollToSection('#contacts-section')"
        >
          <i class="bi-telephone-fill me-2"></i>Связаться с нами
        </button> -->

        <div v-if="!authStore.user">
          <TelegramLoginWidget />
        </div>
        <div v-else class="d-flex align-items-center">
          <div class="dropdown">
            <div data-bs-toggle="dropdown" class="d-flex flex-row align-items-center">
              <div class="me-2 fw-bold">{{ authStore.user.username }}</div>
              <UserIcon :user="authStore.user" />
            </div>

            <ul class="dropdown-menu">
              <li>
                <a class="dropdown-item" href="#" @click.prevent="authStore.logoutAction">
                  <i class="bi-box-arrow-right me-2"></i>
                  <span>Log out</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
#mainNavbar {
  transition: background-color 0.2s ease-in-out;
  background-color: #ffffff;
}

#mainNavbar.scrolled {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  transition: box-shadow 0.2s ease-in-out;
}

#brandName {
  line-height: 30px !important;
  text-align: center;
}

/* @media (min-width: 767.98px) {
  .navbar-brand {
    position: absolute;
  }
} */

.userAvatar {
  border-radius: 0.375rem;
  width: 40px;
  height: 40px;
}
</style>
