<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  let user = get(auth);
  let gardens = [];
  let error = '';
  let name = '';
  let location = '';
  let sensor_type = 'simulated_basic';
  let plant_type = 'General';
  let watering_frequency = 3;

  async function fetchGardens() {
    const res = await fetch('/api/gardens', { credentials: 'include' });
    if (res.ok) {
      gardens = await res.json();
    } else {
      error = 'Failed to load gardens.';
    }
  }

  onMount(() => {
    user = get(auth);
    if (!user.isAuthenticated) {
      goto('/login');
      return;
    }
    fetchGardens();
  });

  async function addGarden() {
    error = '';
    const res = await fetch('/api/gardens', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ name, location, sensor_type, plant_type, watering_frequency })
    });
    if (res.ok) {
      name = '';
      location = '';
      sensor_type = 'simulated_basic';
      plant_type = 'General';
      watering_frequency = 3;
      await fetchGardens();
    } else {
      const data = await res.json();
      error = data.error || 'Failed to add garden.';
    }
  }

  async function deleteGarden(id: number) {
    if (!confirm('Delete this garden?')) return;
    const res = await fetch(`/api/gardens/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    });
    if (res.ok) {
      await fetchGardens();
    } else {
      error = 'Failed to delete garden.';
    }
  }
</script>

<main class="max-w-3xl mx-auto mt-10">
  <h1 class="text-2xl font-bold mb-6">My Gardens</h1>
  {#if error}
    <div class="text-red-500 mb-4">{error}</div>
  {/if}
  <form on:submit|preventDefault={addGarden} class="mb-8 p-4 border rounded">
    <h2 class="font-semibold mb-2">Add New Garden</h2>
    <input bind:value={name} placeholder="Garden Name" class="input mb-2" required />
    <input bind:value={location} placeholder="Location (city or address)" class="input mb-2" />
    <input bind:value={plant_type} placeholder="Plant Type" class="input mb-2" />
    <input type="number" bind:value={watering_frequency} min="1" placeholder="Watering Frequency (days)" class="input mb-2" />
    <select bind:value={sensor_type} class="input mb-2">
      <option value="simulated_basic">Simulated Basic</option>
      <option value="moisture_only">Moisture Only</option>
      <option value="full_environment">Full Environment</option>
    </select>
    <button type="submit" class="btn">Add Garden</button>
  </form>
  {#if gardens.length === 0}
    <div>No gardens found.</div>
  {:else}
    <ul>
      {#each gardens as garden}
        <li class="mb-4 p-4 border rounded shadow flex justify-between items-center">
          <div>
            <div class="font-semibold">{garden.name}</div>
            <div class="text-sm text-gray-600">Location: {garden.location}</div>
            <div class="text-sm">Sensor: {garden.sensor_type}</div>
            <div class="text-sm">Plant: {garden.plant_type}</div>
            <div class="text-sm">Watering: every {garden.watering_frequency} days</div>
          </div>
          <button on:click={() => deleteGarden(garden.id)} class="text-red-600">Delete</button>
        </li>
      {/each}
    </ul>
  {/if}
</main>
