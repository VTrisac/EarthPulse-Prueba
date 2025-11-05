<script>
  import { files, deleteFile, downloadFile } from '../stores/files.js';

  export let onRename;

  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  }

  function getFileIcon(contentType) {
    if (contentType.startsWith('image/')) return '🖼️';
    if (contentType.includes('pdf')) return '📄';
    if (contentType.includes('word') || contentType.includes('document')) return '📝';
    if (contentType.includes('sheet') || contentType.includes('excel')) return '📊';
    if (contentType.includes('presentation') || contentType.includes('powerpoint')) return '📊';
    if (contentType.includes('video')) return '🎥';
    if (contentType.includes('audio')) return '🎵';
    if (contentType.includes('zip') || contentType.includes('rar')) return '📦';
    return '📎';
  }

  async function handleDelete(fileId, fileName) {
    if (confirm(`Are you sure you want to delete "${fileName}"?`)) {
      try {
        await deleteFile(fileId);
      } catch (err) {
        alert(`Failed to delete file: ${err.message}`);
      }
    }
  }

  function handleDownload(fileId, fileName) {
    downloadFile(fileId, fileName);
  }
</script>

<div class="overflow-x-auto">
  {#if $files.length === 0}
    <div class="text-center py-16">
      <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 mb-6 animate-float">
        <svg
          class="h-12 w-12 text-white"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
          />
        </svg>
      </div>
      <p class="mt-4 text-2xl font-bold text-gradient">No files uploaded yet</p>
      <p class="mt-3 text-lg text-white/80">Upload your first file to get started</p>
    </div>
  {:else}
    <!-- Mobile view -->
    <div class="block md:hidden space-y-4">
      {#each $files as file (file.id)}
        <div class="card card-hover">
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-start space-x-4 flex-1 min-w-0">
              <div class="text-4xl bg-gradient-to-br from-purple-500 to-pink-500 p-3 rounded-xl shadow-lg">
                {getFileIcon(file.content_type)}
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-bold text-gray-900 truncate text-lg">{file.name}</p>
                <p class="text-sm text-purple-600 font-semibold mt-1">{formatFileSize(file.size)}</p>
                <p class="text-xs text-gray-600 mt-1">
                  {formatDate(file.upload_date)}
                </p>
              </div>
            </div>
          </div>
          <div class="flex space-x-2">
            <button
              on:click={() => handleDownload(file.id, file.name)}
              class="btn btn-primary flex-1 text-sm"
            >
              📥 Download
            </button>
            <button
              on:click={() => onRename(file)}
              class="btn btn-secondary flex-1 text-sm"
            >
              ✏️ Rename
            </button>
            <button
              on:click={() => handleDelete(file.id, file.name)}
              class="btn btn-danger flex-1 text-sm"
            >
              🗑️ Delete
            </button>
          </div>
        </div>
      {/each}
    </div>

    <!-- Desktop view -->
    <table class="hidden md:table min-w-full">
      <thead>
        <tr class="border-b border-white/20">
          <th class="px-6 py-4 text-left text-sm font-bold text-purple-700 uppercase tracking-wider">
            Name
          </th>
          <th class="px-6 py-4 text-left text-sm font-bold text-purple-700 uppercase tracking-wider">
            Size
          </th>
          <th class="px-6 py-4 text-left text-sm font-bold text-purple-700 uppercase tracking-wider">
            Type
          </th>
          <th class="px-6 py-4 text-left text-sm font-bold text-purple-700 uppercase tracking-wider">
            Upload Date
          </th>
          <th class="px-6 py-4 text-right text-sm font-bold text-purple-700 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-white/10">
        {#each $files as file (file.id)}
          <tr class="hover:bg-white/30 transition-all duration-200 group">
            <td class="px-6 py-5 whitespace-nowrap">
              <div class="flex items-center">
                <div class="text-3xl bg-gradient-to-br from-purple-500 to-pink-500 p-2 rounded-lg mr-4 shadow-md group-hover:scale-110 transition-transform duration-200">
                  {getFileIcon(file.content_type)}
                </div>
                <div class="text-base font-bold text-gray-900">{file.name}</div>
              </div>
            </td>
            <td class="px-6 py-5 whitespace-nowrap text-sm font-semibold text-purple-700">
              {formatFileSize(file.size)}
            </td>
            <td class="px-6 py-5 whitespace-nowrap text-sm text-gray-700">
              {file.content_type}
            </td>
            <td class="px-6 py-5 whitespace-nowrap text-sm text-gray-700">
              {formatDate(file.upload_date)}
            </td>
            <td class="px-6 py-5 whitespace-nowrap text-right text-sm font-medium space-x-3">
              <button
                on:click={() => handleDownload(file.id, file.name)}
                class="text-purple-600 hover:text-purple-900 font-semibold hover:scale-110 transition-transform inline-block"
              >
                📥 Download
              </button>
              <button
                on:click={() => onRename(file)}
                class="text-blue-600 hover:text-blue-900 font-semibold hover:scale-110 transition-transform inline-block"
              >
                ✏️ Rename
              </button>
              <button
                on:click={() => handleDelete(file.id, file.name)}
                class="text-red-600 hover:text-red-900 font-semibold hover:scale-110 transition-transform inline-block"
              >
                🗑️ Delete
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>
