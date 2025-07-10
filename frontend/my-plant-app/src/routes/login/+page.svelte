<script lang="ts">
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';

  let username = '';
  let password = '';
  let error = '';

  async function handleLogin() {
    error = '';
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      auth.set({
        isAuthenticated: true,
        userId: data.user_id,
        username: data.username,
        lastActiveGardenId: data.last_active_garden_id
      });
      goto('/dashboard');
    } else {
      error = data.error || 'Login failed';
    }
  }
</script>

<form on:submit|preventDefault={handleLogin} class="max-w-md mx-auto mt-10">
  <h1 class="text-2xl font-bold mb-4">Login</h1>
  <input bind:value={username} placeholder="Username" class="input" required />
  <input type="password" bind:value={password} placeholder="Password" class="input" required />
  {#if error}
    <div class="text-red-500 mt-2">{error}</div>
  {/if}
  <button type="submit" class="btn mt-4">Login</button>
</form>
