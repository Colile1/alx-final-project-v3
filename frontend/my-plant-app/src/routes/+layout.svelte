<script lang="ts">
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import { theme } from '$lib/stores/theme';

  let user = get(auth);
  let currentTheme = 'light';

  $: theme.subscribe(value => {
    currentTheme = value;
  });

  function toggleTheme() {
    theme.set(currentTheme === 'light' ? 'dark' : 'light');
  }

  // Check authentication status on mount
  onMount(async () => {
    const res = await fetch('/api/status', { credentials: 'include' });
    const data = await res.json();
    if (data.isAuthenticated) {
      auth.set({
        isAuthenticated: true,
        userId: data.userId,
        username: data.username,
        lastActiveGardenId: data.last_active_garden_id
      });
    } else {
      auth.set({ isAuthenticated: false, userId: null, username: null, lastActiveGardenId: null });
    }
  });

  $: user = $auth;

  function handleLogout() {
    fetch('/api/logout', { method: 'POST', credentials: 'include' })
      .then(() => {
        auth.set({ isAuthenticated: false, userId: null, username: null, lastActiveGardenId: null });
        goto('/login');
      });
  }
</script>

<nav class="w-full bg-gray-100 dark:bg-gray-900 py-4 px-8 flex justify-between items-center shadow">
  <div class="font-bold text-xl">
    <a href="/dashboard">Plant Care Dashboard</a>
  </div>
  <div class="space-x-4 flex items-center">
    {#if user.isAuthenticated}
      <a href="/dashboard">Dashboard</a>
      <a href="/my-gardens">My Gardens</a>
      <a href="/settings">Settings</a>
      <a href="/about">About</a>
      <button on:click={handleLogout} class="text-red-600">Logout</button>
      <span class="ml-2 text-gray-600 dark:text-gray-300">{user.username}</span>
    {:else}
      <a href="/login">Login</a>
      <a href="/register">Register</a>
      <a href="/about">About</a>
    {/if}
    <button on:click={toggleTheme} aria-label="Toggle dark mode" class="ml-4 p-2 rounded bg-gray-200 dark:bg-gray-700">
      {#if currentTheme === 'light'}
        🌞
      {:else}
        🌙
      {/if}
    </button>
  </div>
</nav>

<slot />
