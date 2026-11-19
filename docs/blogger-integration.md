# Blogger integration

Enable GitHub Pages and wait for the first successful Actions deployment. Public endpoints:

- Gallery: https://nanlingemperor-droid.github.io/nanling-illustration-engine/
- Catalog JSON: https://nanlingemperor-droid.github.io/nanling-illustration-engine/catalog.json

Add a dedicated gallery block only to the Wanxiang/Nanling Daozang Blogger template. Keep it isolated from existing blog styles. Do not replace the main blog template.

\`\`\`html
<div id="nanling-illustrations"></div>
<script>
(async function () {
  const catalogUrl = 'https://nanlingemperor-droid.github.io/nanling-illustration-engine/catalog.json';
  const root = document.getElementById('nanling-illustrations');
  try {
    const data = await (await fetch(catalogUrl)).json();
    const grid = document.createElement('div');
    grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px';
    for (const item of data.illustrations || []) {
      const card = document.createElement('article');
      const img = document.createElement('img');
      img.src = new URL('assets/' + encodeURIComponent(item.thumbnail), catalogUrl).href;
      img.alt = item.alt || item.title || 'Nanling illustration';
      img.loading = 'lazy';
      img.style.cssText = 'display:block;width:100%;height:auto;object-fit:contain;border:0';
      const title = document.createElement('p');
      title.textContent = item.title || '';
      card.append(img, title);
      grid.append(card);
    }
    root.replaceChildren(grid);
  } catch (_) { root.textContent = 'Galeri ilustrasi belum tersedia.'; }
})();
</script>
\`\`\`

Never expose GitHub tokens, Cloudflare secrets, or private data in this public repository.
