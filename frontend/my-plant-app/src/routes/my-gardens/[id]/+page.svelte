<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { auth } from '$lib/stores/auth';
  import { get } from 'svelte/store';
  import GardenCharts from '$lib/components/GardenCharts.svelte';
  import CsvImportExport from '$lib/components/CsvImportExport.svelte';

  let user = get(auth);
  let garden: any = null;
  let readings = [];
  let error = '';
  let moisture_level = '';
  let temperature = '';
  let light_intensity = '';
  let humidity = '';
  let ph_level = '';
  let notes = '';
  let weather: any = null;
  let prediction = '';

  let editMode = false;
  let editName = '';
  let editLocation = '';
  let editSensorType = '';
  let editPlantType = '';
  let editWateringFrequency = 3;

  $: gardenId = $page.params.id;

  async function fetchGarden() {
    const res = await fetch(`/api/gardens/${gardenId}`, { credentials: 'include' });
    if (res.ok) {
      garden = await res.json();
    } else {
      error = 'Failed to load garden.';
    }
  }

  async function fetchReadings() {
    const res = await fetch(`/api/gardens/${gardenId}/readings`, { credentials: 'include' });
    if (res.ok) {
      readings = await res.json();
    } else {
      error = 'Failed to load readings.';
    }
  }

  async function fetchWeather() {
    if (!garden?.location) return;
    const res = await fetch(`/api/weather?location=${encodeURIComponent(garden.location)}`, { credentials: 'include' });
    if (res.ok) {
      weather = await res.json();
    } else {
      weather = null;
    }
  }

  async function fetchPrediction() {
    const res = await fetch(`/api/gardens/${gardenId}/prediction`, { credentials: 'include' });
    if (res.ok) {
      const data = await res.json();
      prediction = data.next_watering_estimate;
    } else {
      prediction = 'Unavailable';
    }
  }

  onMount(() => {
    user = get(auth);
    if (!user.isAuthenticated) {
      goto('/login');
      return;
    }
    fetchGarden();
    fetchReadings();
    fetchWeather();
    fetchPrediction();
  });

  async function addReading() {
    error = '';
    const res = await fetch(`/api/gardens/${gardenId}/readings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        moisture_level,
        temperature,
        light_intensity,
        humidity,
        ph_level,
        notes,
        is_manual: true
      })
    });
    if (res.ok) {
      moisture_level = '';
      temperature = '';
      light_intensity = '';
      humidity = '';
      ph_level = '';
      notes = '';
      await fetchReadings();
    } else {
      const data = await res.json();
      error = data.error || 'Failed to add reading.';
    }
  }

  function startEdit() {
    editMode = true;
    editName = garden.name;
    editLocation = garden.location;
    editSensorType = garden.sensor_type;
    editPlantType = garden.plant_type;
    editWateringFrequency = garden.watering_frequency;
  }

  async function saveEdit() {
    const res = await fetch(`/api/gardens/${gardenId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        name: editName,
        location: editLocation,
        sensor_type: editSensorType,
        plant_type: editPlantType,
        watering_frequency: editWateringFrequency
      })
    });
    if (res.ok) {
      editMode = false;
      await fetchGarden();
    } else {
      error = 'Failed to update garden.';
    }
  }

  async function pairSensor(type: string) {
    const res = await fetch(`/api/gardens/${gardenId}/pair_sensor`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ sensor_type: type })
    });
    if (res.ok) {
      await fetchGarden();
    } else {
      error = 'Failed to pair sensor.';
    }
  }

  async function unpairSensor() {
    const res = await fetch(`/api/gardens/${gardenId}/unpair_sensor`, {
      method: 'DELETE',
      credentials: 'include'
    });
    if (res.ok) {
      await fetchGarden();
    } else {
      error = 'Failed to unpair sensor.';
    }
  }
</script>

<main class="max-w-3xl mx-auto mt-10">
  {#if error}
    <div class="text-red-500 mb-4">{error}</div>
  {/if}
  {#if garden}
    <CsvImportExport gardenId={gardenId} />
    <div class="mb-4">
      <span class="font-semibold">Next Watering Prediction:</span>
      <span class="ml-2">{prediction}</span>
    </div>
    <h1 class="text-2xl font-bold mb-2">{garden.name}</h1>
    <button on:click={startEdit} class="btn mb-2">Edit Garden</button>
    {#if editMode}
      <form on:submit|preventDefault={saveEdit} class="mb-4 p-4 border rounded bg-gray-50">
        <input bind:value={editName} placeholder="Name" class="input mb-2" required />
        <input bind:value={editLocation} placeholder="Location" class="input mb-2" />
        <input bind:value={editPlantType} placeholder="Plant Type" class="input mb-2" />
        <input type="number" bind:value={editWateringFrequency} min="1" placeholder="Watering Frequency (days)" class="input mb-2" />
        <select bind:value={editSensorType} class="input mb-2">
          <option value="simulated_basic">Simulated Basic</option>
          <option value="moisture_only">Moisture Only</option>
          <option value="full_environment">Full Environment</option>
        </select>
        <button type="submit" class="btn">Save</button>
        <button type="button" on:click={() => editMode = false} class="btn ml-2">Cancel</button>
      </form>
    {/if}
    <div class="mb-4">
      <span class="font-semibold">Sensor Pairing:</span>
      <button on:click={() => pairSensor('simulated_basic')} class="btn mx-1">Simulated Basic</button>
      <button on:click={() => pairSensor('moisture_only')} class="btn mx-1">Moisture Only</button>
      <button on:click={() => pairSensor('full_environment')} class="btn mx-1">Full Environment</button>
      <button on:click={unpairSensor} class="btn mx-1 text-red-600">Unpair</button>
      <span class="ml-2 text-gray-600">Current: {garden.sensor_type}</span>
    </div>
    <div class="mb-6">Sensor: {garden.sensor_type} | Plant: {garden.plant_type} | Watering: every {garden.watering_frequency} days</div>
    {#if weather}
      <div class="mb-6 p-4 border rounded bg-blue-50">
        <div class="font-semibold">Weather: {weather.location?.name}</div>
        <div>Temp: {weather.current?.temp_c}°C, {weather.current?.condition?.text}</div>
        <div>Humidity: {weather.current?.humidity}%</div>
        <div>Wind: {weather.current?.wind_kph} kph</div>
      </div>
    {/if}
    <GardenCharts {readings} />
    <h2 class="font-semibold mb-2 mt-8">Add Manual Reading</h2>
    <form on:submit|preventDefault={addReading} class="mb-8 p-4 border rounded">
      <input bind:value={moisture_level} type="number" placeholder="Moisture Level (%)" class="input mb-2" required />
      <input bind:value={temperature} type="number" placeholder="Temperature (°C)" class="input mb-2" required />
      <input bind:value={light_intensity} type="number" placeholder="Light Intensity (lux)" class="input mb-2" required />
      <input bind:value={humidity} type="number" placeholder="Humidity (%)" class="input mb-2" />
      <input bind:value={ph_level} type="number" placeholder="pH Level" class="input mb-2" />
      <input bind:value={notes} placeholder="Notes" class="input mb-2" />
      <button type="submit" class="btn">Add Reading</button>
    </form>
    <h2 class="font-semibold mb-2">Recent Readings</h2>
    {#if readings.length === 0}
      <div>No readings found.</div>
    {:else}
      <table class="w-full border">
        <thead>
          <tr class="bg-gray-100">
            <th class="p-2">Time</th>
            <th class="p-2">Moisture</th>
            <th class="p-2">Temp</th>
            <th class="p-2">Light</th>
            <th class="p-2">Humidity</th>
            <th class="p-2">pH</th>
            <th class="p-2">Notes</th>
          </tr>
        </thead>
        <tbody>
          {#each readings as r}
            <tr>
              <td class="p-2">{r.timestamp?.slice(0, 19).replace('T', ' ')}</td>
              <td class="p-2">{r.moisture_level}</td>
              <td class="p-2">{r.temperature}</td>
              <td class="p-2">{r.light_intensity}</td>
              <td class="p-2">{r.humidity}</td>
              <td class="p-2">{r.ph_level}</td>
              <td class="p-2">{r.notes}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  {/if}
</main>
