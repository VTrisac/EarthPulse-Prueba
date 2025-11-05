<script>
  import { renameFile } from '../stores/files.js';

  export let file = null;
  export let onClose;

  let newName = '';
  let saving = false;
  let errorMessage = '';

  $: if (file) {
    newName = file.name;
    errorMessage = '';
  }

  async function handleSave() {
    if (!newName.trim()) {
      errorMessage = 'File name cannot be empty';
      return;
    }

    if (newName === file.name) {
      onClose();
      return;
    }

    saving = true;
    errorMessage = '';

    try {
      await renameFile(file.id, newName.trim());
      onClose();
    } catch (err) {
      errorMessage = err.message;
    } finally {
      saving = false;
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'Enter') {
      handleSave();
    }
  }

  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) {
      onClose();
    }
  }
</script>

{#if file}
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in"
    on:click={handleBackdropClick}
    on:keydown={handleKeydown}
  >
    <div class="glass-effect rounded-3xl shadow-2xl max-w-md w-full p-8 transform transition-all duration-300 scale-100 animate-slide-up border-2 border-white/30">
      <div class="flex items-center space-x-3 mb-6">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
          <span class="text-2xl">✏️</span>
        </div>
        <h2 class="text-2xl font-bold text-gradient">Rename File</h2>
      </div>

      <div class="mb-6">
        <label for="filename" class="block text-sm font-bold text-purple-700 mb-3">
          New File Name
        </label>
        <input
          id="filename"
          type="text"
          bind:value={newName}
          class="input w-full text-lg"
          disabled={saving}
          autofocus
        />
      </div>

      {#if errorMessage}
        <div class="mb-6 p-4 bg-red-500/20 backdrop-blur-xl text-red-900 rounded-xl text-sm border-2 border-red-400/50 font-semibold">
          ⚠️ {errorMessage}
        </div>
      {/if}

      <div class="flex space-x-3">
        <button
          on:click={onClose}
          class="btn btn-secondary flex-1"
          disabled={saving}
        >
          ❌ Cancel
        </button>
        <button
          on:click={handleSave}
          class="btn btn-primary flex-1"
          disabled={saving}
        >
          {saving ? '⏳ Saving...' : '✅ Save'}
        </button>
      </div>
    </div>
  </div>
{/if}
