// static/js/progress-bars.js - Versión mejorada
class ProgressBarManager {
    constructor() {
        this.bars = [];
        this.init();
    }
    
    init() {
        this.loadBars();
        this.setupEventListeners();
    }
    
    loadBars() {
        const progressBars = document.querySelectorAll('.tarea-progreso');
        
        progressBars.forEach((bar, index) => {
            const progress = parseInt(bar.getAttribute('data-progreso')) || 0;
            this.animateBar(bar, progress);
            this.bars.push({ element: bar, progress: progress });
        });
    }
    
    animateBar(bar, progress) {
        // Reset y animación
        bar.style.width = '0%';
        bar.classList.remove('bg-success', 'bg-warning', 'bg-info');
        
        setTimeout(() => {
            bar.style.width = progress + '%';
            this.setBarColor(bar, progress);
        }, 100);
    }
    
    setBarColor(bar, progress) {
        if (progress === 100) {
            bar.classList.add('bg-success');
        } else if (progress >= 50) {
            bar.classList.add('bg-warning');
        } else {
            bar.classList.add('bg-info');
        }
    }
    
    setupEventListeners() {
        // Para futuras funcionalidades dinámicas
        document.addEventListener('progressBarUpdate', (event) => {
            this.updateBar(event.detail.barId, event.detail.progress);
        });
    }
    
    updateBar(barId, newProgress) {
        const bar = document.getElementById(barId);
        if (bar) {
            this.animateBar(bar, newProgress);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ProgressBarManager();
});