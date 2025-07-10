<script lang="ts">
  import { goto } from '$app/navigation';
  let username = '';
  let password = '';
  let error = '';
  let success = '';

  async function handleRegister() {
    error = '';
    success = '';
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      success = 'Registration successful! You can now log in.';
      setTimeout(() => goto('/login'), 1000);
    } else {
      error = data.error || 'Registration failed';
    }
  }
</script>

<form on:submit|preventDefault={handleRegister} class="max-w-md mx-auto mt-10">
  <h1 class="text-2xl font-bold mb-4">Register</h1>
  <input bind:value={username} placeholder="Username" class="input" required />
  <input type="password" bind:value={password} placeholder="Password" class="input" required />
  {#if error}
    <div class="text-red-500 mt-2">{error}</div>
  {/if}
  {#if success}
    <div class="text-green-500 mt-2">{success}</div>
  {/if}
  <button type="submit" class="btn mt-4">Register</button>
</form>
