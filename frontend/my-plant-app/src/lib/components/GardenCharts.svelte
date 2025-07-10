<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  export let readings = [];
  let chartEl: HTMLCanvasElement;
  let chart: Chart;

  $: labels = readings.map(r => r.timestamp?.slice(0, 19).replace('T', ' '));
  $: moisture = readings.map(r => r.moisture_level);
  $: temperature = readings.map(r => r.temperature);
  $: light = readings.map(r => r.light_intensity);

  onMount(() => {
    if (chart) chart.destroy();
    chart = new Chart(chartEl, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'Moisture (%)', data: moisture, borderColor: '#22c55e', fill: false },
          { label: 'Temperature (°C)', data: temperature, borderColor: '#f59e42', fill: false },
          { label: 'Light (lux)', data: light, borderColor: '#3b82f6', fill: false }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'top' } },
        scales: { x: { display: true }, y: { display: true } }
      }
    });
    return () => chart?.destroy();
  });
</script>

<canvas bind:this={chartEl} class="w-full h-64"></canvas>
