// Custom Dialog System
class Dialog {
    constructor() {
        this.dialog = null;
        this.overlay = null;
    }

    show(options = {}) {
        const {
            title = 'Dialog',
            message = '',
            type = 'info', // info, success, error, warning
            showCancel = false,
            confirmText = 'OK',
            cancelText = 'Cancel',
            onConfirm = null,
            onCancel = null
        } = options;

        // Remove existing dialog if any
        this.hide();

        // Create overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'dialog-overlay';
        this.overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        `;

        // Create dialog
        this.dialog = document.createElement('div');
        this.dialog.className = 'dialog';
        this.dialog.style.cssText = `
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            animation: slideIn 0.3s ease;
        `;

        // Dialog content
        this.dialog.innerHTML = `
            <div class="dialog-header" style="padding: 20px 20px 0 20px;">
                <h3 style="margin: 0; color: #0f766e; font-size: 18px; font-weight: 600;">
                    ${title}
                </h3>
            </div>
            <div class="dialog-body" style="padding: 20px;">
                <div class="dialog-icon" style="text-align: center; margin-bottom: 16px;">
                    ${this.getIcon(type)}
                </div>
                <p style="margin: 0; color: #374151; line-height: 1.5; text-align: center;">
                    ${message}
                </p>
            </div>
            <div class="dialog-footer" style="padding: 0 20px 20px 20px; display: flex; gap: 12px; justify-content: flex-end;">
                ${showCancel ? `<button class="dialog-btn dialog-cancel" style="padding: 8px 16px; border: 1px solid #d1d5db; background: white; color: #374151; border-radius: 6px; cursor: pointer; font-weight: 500;">${cancelText}</button>` : ''}
                <button class="dialog-btn dialog-confirm" style="padding: 8px 16px; border: none; background: #14b8a6; color: white; border-radius: 6px; cursor: pointer; font-weight: 500;">
                    ${confirmText}
                </button>
            </div>
        `;

        // Add styles
        this.addStyles();

        // Append to body
        this.overlay.appendChild(this.dialog);
        document.body.appendChild(this.overlay);

        // Add event listeners
        this.dialog.querySelector('.dialog-confirm').addEventListener('click', () => {
            if (onConfirm) onConfirm();
            this.hide();
        });

        if (showCancel) {
            this.dialog.querySelector('.dialog-cancel').addEventListener('click', () => {
                if (onCancel) onCancel();
                this.hide();
            });
        }

        // Close on overlay click
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                if (onCancel) onCancel();
                this.hide();
            }
        });

        // Close on escape key
        this.handleEscape = (e) => {
            if (e.key === 'Escape') {
                if (onCancel) onCancel();
                this.hide();
            }
        };
        document.addEventListener('keydown', this.handleEscape);
    }

    hide() {
        if (this.dialog) {
            this.dialog.style.animation = 'slideOut 0.3s ease';
            this.overlay.style.animation = 'fadeOut 0.3s ease';
            
            setTimeout(() => {
                if (this.overlay && this.overlay.parentNode) {
                    this.overlay.parentNode.removeChild(this.overlay);
                }
                this.dialog = null;
                this.overlay = null;
            }, 300);
        }
        
        if (this.handleEscape) {
            document.removeEventListener('keydown', this.handleEscape);
        }
    }

    getIcon(type) {
        const icons = {
            info: '<div style="width: 48px; height: 48px; background: #dbeafe; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 24px;">ℹ️</div>',
            success: '<div style="width: 48px; height: 48px; background: #d1fae5; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 24px;">✅</div>',
            error: '<div style="width: 48px; height: 48px; background: #fee2e2; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 24px;">❌</div>',
            warning: '<div style="width: 48px; height: 48px; background: #fef3c7; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 24px;">⚠️</div>'
        };
        return icons[type] || icons.info;
    }

    addStyles() {
        if (document.getElementById('dialog-styles')) return;

        const style = document.createElement('style');
        style.id = 'dialog-styles';
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            
            @keyframes slideIn {
                from { transform: translateY(-20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes slideOut {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(-20px); opacity: 0; }
            }
            
            .dialog-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            
            .dialog-btn:active {
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }
}

// Global dialog instance
window.dialog = new Dialog();

// Convenience functions
window.showDialog = (options) => window.dialog.show(options);
window.showAlert = (message, title = 'Alert') => window.dialog.show({ title, message, type: 'info' });
window.showSuccess = (message, title = 'Success') => window.dialog.show({ title, message, type: 'success' });
window.showError = (message, title = 'Error') => window.dialog.show({ title, message, type: 'error' });
window.showWarning = (message, title = 'Warning') => window.dialog.show({ title, message, type: 'warning' });
window.showConfirm = (message, title = 'Confirm', onConfirm = null, onCancel = null) => 
    window.dialog.show({ 
        title, 
        message, 
        type: 'warning', 
        showCancel: true, 
        confirmText: 'Yes', 
        cancelText: 'No',
        onConfirm,
        onCancel
    });
