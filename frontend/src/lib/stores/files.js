import { writable } from 'svelte/store';

const API_BASE_URL = '/api/files';

// Create writable stores
export const files = writable([]);
export const loading = writable(false);
export const error = writable(null);
export const uploading = writable(false);

// API functions
export async function fetchFiles(search = '', page = 1, limit = 20) {
  loading.set(true);
  error.set(null);

  try {
    const params = new URLSearchParams({ page, limit });
    if (search) params.append('search', search);

    const response = await fetch(`${API_BASE_URL}?${params}`);
    if (!response.ok) throw new Error('Failed to fetch files');

    const data = await response.json();
    files.set(data.files);
    return data;
  } catch (err) {
    error.set(err.message);
    throw err;
  } finally {
    loading.set(false);
  }
}

export async function uploadFile(file) {
  uploading.set(true);
  error.set(null);

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Upload failed');
    }

    const newFile = await response.json();

    // Add new file to the beginning of the list
    files.update(currentFiles => [newFile, ...currentFiles]);

    return newFile;
  } catch (err) {
    error.set(err.message);
    throw err;
  } finally {
    uploading.set(false);
  }
}

export async function renameFile(fileId, newName) {
  error.set(null);

  try {
    const response = await fetch(`${API_BASE_URL}/${fileId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: newName })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Rename failed');
    }

    const updatedFile = await response.json();

    // Update file in the list
    files.update(currentFiles =>
      currentFiles.map(f => (f.id === fileId ? updatedFile : f))
    );

    return updatedFile;
  } catch (err) {
    error.set(err.message);
    throw err;
  }
}

export async function deleteFile(fileId) {
  error.set(null);

  try {
    const response = await fetch(`${API_BASE_URL}/${fileId}`, {
      method: 'DELETE'
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Delete failed');
    }

    // Remove file from the list
    files.update(currentFiles =>
      currentFiles.filter(f => f.id !== fileId)
    );
  } catch (err) {
    error.set(err.message);
    throw err;
  }
}

export function downloadFile(fileId, fileName) {
  const url = `${API_BASE_URL}/${fileId}/download`;
  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
