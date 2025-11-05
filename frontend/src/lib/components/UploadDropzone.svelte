<script>
  import { uploadFile, uploading } from '../stores/files.js';

  let dragOver = false;
  let fileInput;
  let uploadStatus = '';

  function handleDragOver(e) {
    e.preventDefault();
    dragOver = true;
  }

  function handleDragLeave() {
    dragOver = false;
  }

  async function handleDrop(e) {
    e.preventDefault();
    dragOver = false;

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      await handleUpload(files[0]);
    }
  }

  async function handleFileInput(e) {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      await handleUpload(files[0]);
    }
    // Reset input
    e.target.value = '';
  }

  async function handleUpload(file) {
    try {
      uploadStatus = `Uploading ${file.name}...`;
      await uploadFile(file);
      uploadStatus = `✓ ${file.name} uploaded successfully!`;
      setTimeout(() => {
        uploadStatus = '';
      }, 3000);
    } catch (err) {
      uploadStatus = `✗ Error: ${err.message}`;
      setTimeout(() => {
        uploadStatus = '';
      }, 5000);
    }
  }

  function openFileDialog() {
    fileInput.click();
  }
</script>

<div class="w-full">
  <input
    type="file"
    bind:this={fileInput}
    on:change={handleFileInput}
    class="hidden"
  />

  <div
    on:dragover={handleDragOver}
    on:dragleave={handleDragLeave}
    on:drop={handleDrop}
    on:click={openFileDialog}
    class="border-3 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-300 transform hover:scale-[1.02] {dragOver
      ? 'border-purple-500 bg-purple-100/50 glass-effect scale-[1.02]'
      : 'border-white/40 glass-effect hover:border-purple-300'} {$uploading ? 'opacity-50 cursor-not-allowed' : ''}"
  >
    {#if $uploading}
      <div class="text-white">
        <div class="inline-block relative">
          <svg
            class="animate-spin h-16 w-16 mx-auto mb-4 text-white drop-shadow-2xl"
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
        <p class="text-xl font-bold drop-shadow-md">Uploading your file...</p>
      </div>
    {:else}
      <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 mb-6 shadow-2xl animate-float">
        <svg
          class="h-12 w-12 text-white"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
      <p class="mt-6 text-xl font-bold text-white drop-shadow-md">
        <span class="text-gradient bg-white px-3 py-1 rounded-lg shadow-lg">Click to upload</span>
      </p>
      <p class="mt-4 text-lg text-white/90 font-medium drop-shadow-md">
        or drag and drop your files here
      </p>
      <p class="mt-3 text-sm text-white/70">
        📄 PDF • 🖼️ Images • 📝 Documents (Max 200MB)
      </p>
    {/if}
  </div>

  {#if uploadStatus}
    <div
      class="mt-6 p-5 rounded-2xl backdrop-blur-xl shadow-xl border-2 {uploadStatus.startsWith('✓')
        ? 'bg-green-500/30 text-white border-green-400/50'
        : uploadStatus.startsWith('✗')
          ? 'bg-red-500/30 text-white border-red-400/50'
          : 'bg-blue-500/30 text-white border-blue-400/50'}"
    >
      <p class="font-bold text-lg drop-shadow-md">{uploadStatus}</p>
    </div>
  {/if}
</div>
