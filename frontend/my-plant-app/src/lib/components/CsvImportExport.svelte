<script lang="ts">
  export let gardenId: string;
  let importError = '';
  let importSuccess = '';
  let fileInput: HTMLInputElement;

  async function handleImport() {
    importError = '';
    importSuccess = '';
    const file = fileInput.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`/api/gardens/${gardenId}/import_data`, {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });
    if (res.ok) {
      importSuccess = 'Import successful!';
    } else {
      const data = await res.json();
      importError = data.error || 'Import failed.';
    }
  }
</script>

<div class="mb-4">
  <label class="block font-semibold mb-1">Import CSV</label>
  <input type="file" bind:this={fileInput} accept=".csv" class="mb-2" />
  <button on:click={handleImport} class="btn">Import</button>
  {#if importError}
    <div class="text-red-500">{importError}</div>
  {/if}
  {#if importSuccess}
    <div class="text-green-500">{importSuccess}</div>
  {/if}
</div>
<div class="mb-4">
  <label class="block font-semibold mb-1">Export CSV</label>
  <a class="btn" href={`/api/gardens/${gardenId}/export_data`} target="_blank" download>Export</a>
</div>
