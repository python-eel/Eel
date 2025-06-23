<template>
  <div>
    <h1>VueEel</h1>
    <h1>Call Python Function</h1>
    <button @click="callPythonFunction">Say Hello</button>
    <p>{{ response }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
const response = ref('')
async function callPythonFunction () {
  console.log("window.eel:", window.eel); // Log window.eel
  const result = await window.eel.say_hello("Vue User")();
  response.value = result; // Display the Python response in the UI
}

</script>
