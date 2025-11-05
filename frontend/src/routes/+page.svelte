<script>
  import { onMount } from 'svelte';
  import UploadDropzone from '$lib/components/UploadDropzone.svelte';
  import FileList from '$lib/components/FileList.svelte';
  import EditNameModal from '$lib/components/EditNameModal.svelte';
  import { fetchFiles, loading, error } from '$lib/stores/files.js';

  let searchQuery = '';
  let fileToRename = null;

  onMount(() => {
    loadFiles();
  });

  async function loadFiles() {
    try {
      await fetchFiles(searchQuery);
    } catch (err) {
      console.error('Error loading files:', err);
    }
  }

  function handleSearch() {
    loadFiles();
  }

  function handleRename(file) {
    fileToRename = file;
  }

  function closeRenameModal() {
    fileToRename = null;
  }
</script>

<svelte:head>
  <title>EarthPulse - Cloud Storage</title>
</svelte:head>

<div class="container mx-auto px-4 py-12 max-w-7xl">
  <!-- Header -->
  <header class="mb-12 text-center">
    <h1 class="text-6xl font-extrabold mb-4 text-gradient drop-shadow-lg">
      EarthPulse
    </h1>
    <p class="text-xl text-white/90 font-medium drop-shadow-md">
      Your files, reimagined in the cloud
    </p>
  </header>

  <!-- Upload Section -->
  <section class="mb-8">
    <UploadDropzone />
  </section>

  <!-- Search Bar -->
  <section class="mb-6">
    <div class="flex space-x-2">
      <input
        type="text"
        bind:value={searchQuery}
        on:keydown={(e) => e.key === 'Enter' && handleSearch()}
        placeholder="Search files..."
        class="input flex-1"
      />
      <button on:click={handleSearch} class="btn btn-primary">
        Search
      </button>
      {#if searchQuery}
        <button
          on:click={() => {
            searchQuery = '';
            loadFiles();
          }}
          class="btn btn-secondary"
        >
          Clear
        </button>
      {/if}
    </div>
  </section>

  <!-- Error Message -->
  {#if $error}
    <div class="mb-6 p-5 glass-effect rounded-2xl text-red-900 border-red-300/50">
      <div class="flex items-center space-x-2">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        <span class="font-semibold">Error: {$error}</span>
      </div>
    </div>
  {/if}

  <!-- Loading State -->
  {#if $loading}
    <div class="text-center py-16">
      <div class="inline-block relative">
        <svg
          class="animate-spin h-16 w-16 mx-auto text-white drop-shadow-2xl"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      </div>
      <p class="mt-6 text-white text-lg font-semibold drop-shadow-md">Loading your files...</p>
    </div>
  {:else}
    <!-- Files List -->
    <section class="card">
      <h2 class="text-3xl font-bold mb-6 text-gradient">Your Files</h2>
      <FileList onRename={handleRename} />
    </section>
  {/if}
</div>

<!-- Rename Modal -->
<EditNameModal file={fileToRename} onClose={closeRenameModal} />
