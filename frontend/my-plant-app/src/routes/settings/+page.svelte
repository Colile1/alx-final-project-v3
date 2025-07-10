<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '$lib/stores/auth';
  import { get } from 'svelte/store';
  let user = get(auth);
  let profile: any = null;
  let error = '';
  let simFreq = 60;
  let moistureThreshold = 30;
  let tempMin = 15;
  let tempMax = 30;
  let lightMin = 200;
  let success = '';

  async function fetchProfile() {
    const res = await fetch('/api/profile', { credentials: 'include' });
    if (res.ok) {
      profile = await res.json();
      simFreq = profile.preferences.simulation_frequency;
      moistureThreshold = profile.preferences.moisture_threshold;
      tempMin = profile.preferences.temperature_min;
      tempMax = profile.preferences.temperature_max;
      lightMin = profile.preferences.light_min;
    } else {
      error = 'Failed to load profile.';
    }
  }

  async function saveProfile() {
    error = '';
    success = '';
    const res = await fetch('/api/profile', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        preferences: {
          simulation_frequency: simFreq,
          moisture_threshold: moistureThreshold,
          temperature_min: tempMin,
          temperature_max: tempMax,
          light_min: lightMin
        }
      })
    });
    if (res.ok) {
      success = 'Settings saved!';
    } else {
      error = 'Failed to save settings.';
    }
  }

  onMount(() => {
    user = get(auth);
    if (!user.isAuthenticated) return;
    fetchProfile();
  });
</script>

<main class="max-w-2xl mx-auto mt-10">
  <h1 class="text-2xl font-bold mb-6">Settings</h1>
  {#if error}
    <div class="text-red-500 mb-4">{error}</div>
  {/if}
  {#if profile}
    <form on:submit|preventDefault={saveProfile} class="mb-8 p-4 border rounded">
      <h2 class="font-semibold mb-2">Data Preferences</h2>
      <label>Simulation Frequency (seconds):</label>
      <input type="number" bind:value={simFreq} min="10" class="input mb-2" />
      <label>Moisture Threshold (%):</label>
      <input type="number" bind:value={moistureThreshold} min="0" class="input mb-2" />
      <label>Temperature Min (°C):</label>
      <input type="number" bind:value={tempMin} class="input mb-2" />
      <label>Temperature Max (°C):</label>
      <input type="number" bind:value={tempMax} class="input mb-2" />
      <label>Light Min (lux):</label>
      <input type="number" bind:value={lightMin} class="input mb-2" />
      <button type="submit" class="btn">Save</button>
      {#if success}
        <span class="text-green-600 ml-4">{success}</span>
      {/if}
    </form>
    <div class="mb-4">
      <h2 class="font-semibold mb-2">Profile</h2>
      <div>Username: {profile.username}</div>
      <div>Member since: {profile.created_at?.slice(0, 10)}</div>
      <div>Last login: {profile.last_login?.slice(0, 19).replace('T', ' ')}</div>
    </div>
  {/if}
</main>
