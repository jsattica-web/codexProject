<script setup>
import { onMounted, ref } from "vue";

const loading = ref(true);
const error = ref("");
const apiMessage = ref("");
const serverTime = ref("");

onMounted(async () => {
  try {
    const response = await fetch("/api/hello");
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }
    const data = await response.json();
    apiMessage.value = data.message;
    serverTime.value = new Date(data.serverTime).toLocaleString();
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Unknown API error";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <main class="shell">
    <section class="panel">
      <p class="eyebrow">Spring Boot 2.7 + Vue 3</p>
      <h1>Development Environment Ready</h1>
      <div class="api-box">
        <strong>Backend API</strong>
        <p v-if="loading">Waiting for API response...</p>
        <p v-else-if="error" class="error">{{ error }}</p>
        <p v-else>{{ apiMessage }}</p>
      </div>
      <p v-if="serverTime" class="time">Server time: {{ serverTime }}</p>
    </section>
  </main>
</template>

