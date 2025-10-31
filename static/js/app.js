async function loadVideos() {
  try {
    const resp = await fetch('/api/videos/');
    if (!resp.ok) throw new Error('Erro na API');
    const data = await resp.json();

    const list = document.getElementById('videos');
    list.innerHTML = '';
    data.forEach(v => {
      const li = document.createElement('li');
      const title = document.createElement('h3');
      title.textContent = v.title;

      const desc = document.createElement('p');
      desc.textContent = v.description || '';

      li.appendChild(title);
      li.appendChild(desc);

      if (v.file) {
        const video = document.createElement('video');
        video.controls = true;
        video.src = v.file; // já vem como /media/videos/...
        video.width = 480;
        li.appendChild(video);
      } else if (v.url) {
        const a = document.createElement('a');
        a.href = v.url;
        a.target = '_blank';
        a.textContent = 'Ver vídeo externo';
        li.appendChild(a);
      }

      list.appendChild(li);
    });
  } catch (e) {
    console.error(e);
  }
}

document.addEventListener('DOMContentLoaded', loadVideos);
