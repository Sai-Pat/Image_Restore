// Particle System Generation
document.addEventListener('DOMContentLoaded', () => {
    const particleContainer = document.querySelector('.particles');
    if (particleContainer) {
        for (let i = 0; i < 20; i++) {
            createParticle(particleContainer);
        }
    }
});

function createParticle(container) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    // Randomize properties
    const size = Math.random() * 15 + 5;
    const left = Math.random() * 100;
    const animationDuration = Math.random() * 10 + 10;
    const animationDelay = Math.random() * 5;
    
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${left}vw`;
    particle.style.animationDuration = `${animationDuration}s`;
    particle.style.animationDelay = `${animationDelay}s`;
    
    container.appendChild(particle);
}

// Drag and Drop Logic
function setupDragAndDrop(dropZoneId, fileInputId, previewId) {
    const dropZone = document.getElementById(dropZoneId);
    const fileInput = document.getElementById(fileInputId);
    const preview = document.getElementById(previewId);

    if (!dropZone || !fileInput) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0 && preview) {
            const file = files[0];
            const uploadIcon = dropZone.querySelector('.upload-icon');
            
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.classList.remove('hidden');
                    if (uploadIcon) uploadIcon.classList.add('hidden');
                }
                reader.readAsDataURL(file);
            } else if (file.type.startsWith('video/')) {
                // For videos, just show a generic video icon and filename
                preview.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ffb7b2"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>';
                preview.classList.remove('hidden');
                preview.style.width = '64px';
                if (uploadIcon) {
                    uploadIcon.innerHTML = `<h3 class="text-xl font-semibold text-gray-600 mb-2 mt-4">${file.name}</h3>`;
                }
            }
        }
    }
}
