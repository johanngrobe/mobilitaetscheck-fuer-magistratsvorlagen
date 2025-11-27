<template>
  <div class="main-content min-h-screen flex flex-col justify-between">
    <footer class="footer w-full bg-blue text-white py-4 text-center mt-auto">
      <div class="footer-content mt-4 max-w-screen-lg mx-auto">
        <div class="grid grid-cols-2 items-center justify-center gap-4">
          <div class="grid grid-cols-1 items-center justify-center gap-2">
            <div class="bg-white flex w-fit p-2 rounded justify-center items-center">
              <img src="../assets/logos/pimoo_3logos.png" class="h-8 sm:h-8" alt="pimoo Logos" />
            </div>
            <div class="bg-white flex w-fit p-2 rounded justify-center items-center">
              <img src="../assets/logos/BMFTR.jpg" class="h-14 sm:h-14" alt="pimoo Logos" />
            </div>
            <div class="bg-white flex w-fit p-2 rounded justify-center items-center">
              <img src="../assets/logos/FONA.jpg" class="h-10 sm:h-10" alt="pimoo Logos" />
            </div>
          </div>
          <div>
            <span class="font-bold">Mobilitätscheck für Magistratsvorlagen</span>
            <div class="mt-2">
              <router-link :to="{ name: 'ueber-das-tool' }" class="hover:underline"
                >Über das Tool</router-link
              >
            </div>
          </div>
        </div>
        <div></div>
        <p class="mt-4">&copy; 2025 Hochschule RheinMain</p>
      </div>
    </footer>
  </div>
</template>

<script setup></script>

<style scoped>
/* Tailwind CSS is used, no additional styles needed */
</style>
