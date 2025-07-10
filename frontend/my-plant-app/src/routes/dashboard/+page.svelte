<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  let user = get(auth);
  let gardens = [];
  let error = '';

  onMount(async () => {
    user = get(auth);
    if (!user.isAuthenticated) {
      goto('/login');
      return;
    }
    // Fetch user's gardens
    const res = await fetch('/api/gardens', { credentials: 'include' });
    if (res.ok) {
      gardens = await res.json();
    } else {
      error = 'Failed to load gardens.';
    }
  });
</script>

<main class="max-w-4xl mx-auto mt-10">
  <h1 class="text-3xl font-bold mb-6">Dashboard</h1>
  {#if error}
    <div class="text-red-500 mb-4">{error}</div>
  {/if}
  {#if gardens.length === 0}
    <div>No gardens found. <a href="/my-gardens" class="text-blue-600 underline">Add a garden</a>.</div>
  {:else}
    <ul>
      {#each gardens as garden}
        <li class="mb-4 p-4 border rounded shadow">
          <div class="font-semibold">{garden.name}</div>
          <div class="text-sm text-gray-600">Location: {garden.location}</div>
          <div class="text-sm">Sensor: {garden.sensor_type}</div>
          <a href="/my-gardens" class="text-blue-600 underline">View Details</a>
        </li>
      {/each}
    </ul>
  {/if}
</main>
