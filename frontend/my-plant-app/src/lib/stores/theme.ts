import { writable } from 'svelte/store';

// Check localStorage for persisted theme, default to 'light'
const initialTheme = typeof localStorage !== 'undefined' && localStorage.getItem('theme')
  ? localStorage.getItem('theme')
  : 'light';

export const theme = writable(initialTheme);

theme.subscribe((value) => {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('theme', value ?? 'light');
  }
  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme', value ?? 'light');
  }
});
