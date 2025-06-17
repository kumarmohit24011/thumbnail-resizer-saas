document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById('fileInput');
  const platform = document.getElementById('platform').value;
  const status = document.getElementById('status');

  if (!fileInput.files.length) {
    alert('Please select a file.');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  status.classList.remove('hidden');
  status.innerText = 'Resizing...';

  try {
    const res = await fetch(`https://thumbnail-resizer-saas.onrender.com/resize?platform=${platform}`, {
  method: 'POST',
  body: formData,
});


    if (!res.ok) throw new Error('Resize failed');

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resized_${platform}.jpg`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    status.innerText = '✅ Done!';
  } catch (err) {
    status.innerText = '❌ Error resizing image.';
    console.error(err);
  }
});
