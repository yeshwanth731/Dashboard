// Azure Cognitive Search Manager - Main JavaScript

let searchManager;

class AzureSearchManager {
    constructor() {
        this.indexConfig = null;
        this.skillsetConfig = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadConfigurations();
    }

    setupEventListeners() {
        document.getElementById('addFieldForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addField();
        });

        document.getElementById('addSkillForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addSkill();
        });

        document.getElementById('uploadForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.uploadConfig();
        });
    }

    async loadConfigurations() {
        this.showLoading(true);
        try {
            const [indexResponse, skillsetResponse] = await Promise.all([
                fetch('/api/index'),
                fetch('/api/skillset')
            ]);

            this.indexConfig = await indexResponse.json();
            this.skillsetConfig = await skillsetResponse.json();

            this.renderIndexFields();
            this.renderSkillsetSkills();
            this.updateJsonViewer();
        } catch (error) {
            this.showError('Failed to load configurations: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    renderIndexFields() {
        const container = document.getElementById('indexFields');
        container.innerHTML = '';

        if (!this.indexConfig || !this.indexConfig.fields) {
            container.innerHTML = '<p class="text-muted">No fields configured</p>';
            return;
        }

        this.indexConfig.fields.forEach(field => {
            const fieldElement = this.createFieldElement(field);
            container.appendChild(fieldElement);
        });
    }

    createFieldElement(field) {
        const div = document.createElement('div');
        div.className = 'field-item fade-in';
        
        const badges = [];
        if (field.key) badges.push('<span class="badge bg-warning">Key</span>');
        if (field.searchable) badges.push('<span class="badge bg-info">Searchable</span>');
        if (field.filterable) badges.push('<span class="badge bg-success">Filterable</span>');
        if (field.sortable) badges.push('<span class="badge bg-primary">Sortable</span>');
        if (field.facetable) badges.push('<span class="badge bg-dark">Facetable</span>');

        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${field.name}</strong>
                    <span class="badge bg-secondary ms-2">${field.type}</span>
                    ${badges.join('')}
                </div>
                <button class="btn btn-outline-danger btn-sm" onclick="searchManager.removeField('${field.name}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return div;
    }

    renderSkillsetSkills() {
        const container = document.getElementById('skillsetSkills');
        container.innerHTML = '';

        if (!this.skillsetConfig || !this.skillsetConfig.skills) {
            container.innerHTML = '<p class="text-muted">No skills configured</p>';
            return;
        }

        this.skillsetConfig.skills.forEach(skill => {
            const skillElement = this.createSkillElement(skill);
            container.appendChild(skillElement);
        });
    }

    createSkillElement(skill) {
        const div = document.createElement('div');
        div.className = 'skill-item fade-in';
        
        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${skill.name}</strong>
                    <p class="mb-1 text-muted">${skill.description}</p>
                    <small class="text-muted">Context: ${skill.context}</small>
                    <br>
                    <small class="text-muted">Type: ${skill.type}</small>
                </div>
                <button class="btn btn-outline-danger btn-sm" onclick="searchManager.removeSkill('${skill.name}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return div;
    }

    updateJsonViewer() {
        if (this.indexConfig) {
            document.getElementById('indexJsonViewer').textContent = JSON.stringify(this.indexConfig, null, 2);
        }
        if (this.skillsetConfig) {
            document.getElementById('skillsetJsonViewer').textContent = JSON.stringify(this.skillsetConfig, null, 2);
        }
    }

    async addField() {
        const formData = new FormData();
        formData.append('field_name', document.getElementById('fieldName').value);
        formData.append('field_type', document.getElementById('fieldType').value);
        formData.append('searchable', document.getElementById('searchable').checked);
        formData.append('filterable', document.getElementById('filterable').checked);
        formData.append('sortable', document.getElementById('sortable').checked);
        formData.append('facetable', document.getElementById('facetable').checked);
        formData.append('is_key', document.getElementById('isKey').checked);

        try {
            const response = await fetch('/api/index/fields', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.showSuccess('Field added successfully');
                this.loadConfigurations();
                this.closeModal('addFieldModal');
                this.resetForm('addFieldForm');
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to add field');
            }
        } catch (error) {
            this.showError('Error adding field: ' + error.message);
        }
    }

    async addSkill() {
        const formData = new FormData();
        formData.append('skill_name', document.getElementById('skillName').value);
        formData.append('skill_description', document.getElementById('skillDescription').value);
        formData.append('skill_context', document.getElementById('skillContext').value);
        formData.append('skill_type', document.getElementById('skillType').value);

        try {
            const response = await fetch('/api/skillset/skills', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.showSuccess('Skill added successfully');
                this.loadConfigurations();
                this.closeModal('addSkillModal');
                this.resetForm('addSkillForm');
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to add skill');
            }
        } catch (error) {
            this.showError('Error adding skill: ' + error.message);
        }
    }

    async removeField(fieldName) {
        if (!confirm(`Are you sure you want to remove field "${fieldName}"?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/index/fields/${fieldName}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Field removed successfully');
                this.loadConfigurations();
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to remove field');
            }
        } catch (error) {
            this.showError('Error removing field: ' + error.message);
        }
    }

    async removeSkill(skillName) {
        if (!confirm(`Are you sure you want to remove skill "${skillName}"?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/skillset/skills/${skillName}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Skill removed successfully');
                this.loadConfigurations();
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to remove skill');
            }
        } catch (error) {
            this.showError('Error removing skill: ' + error.message);
        }
    }

    downloadConfig(type) {
        window.open(`/api/download/${type}`, '_blank');
    }

    uploadConfig(type) {
        const modal = new bootstrap.Modal(document.getElementById('uploadModal'));
        document.getElementById('configType').value = type;
        modal.show();
    }

    async uploadConfig() {
        const fileInput = document.getElementById('configFile');
        const configType = document.getElementById('configType').value;
        const file = fileInput.files[0];

        if (!file) {
            this.showError('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.showSuccess('Configuration uploaded successfully');
                this.loadConfigurations();
                this.closeModal('uploadModal');
                this.resetForm('uploadForm');
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to upload configuration');
            }
        } catch (error) {
            this.showError('Error uploading configuration: ' + error.message);
        }
    }

    refreshData() {
        this.loadConfigurations();
    }

    showHelp() {
        const modal = new bootstrap.Modal(document.getElementById('helpModal'));
        modal.show();
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        spinner.style.display = show ? 'block' : 'none';
    }

    showError(message) {
        const alert = document.getElementById('errorAlert');
        const messageElement = document.getElementById('errorMessage');
        messageElement.textContent = message;
        alert.style.display = 'block';
        alert.classList.add('show');
        
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => {
                alert.style.display = 'none';
            }, 150);
        }, 5000);
    }

    showSuccess(message) {
        const alert = document.getElementById('successAlert');
        const messageElement = document.getElementById('successMessage');
        messageElement.textContent = message;
        alert.style.display = 'block';
        alert.classList.add('show');
        
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => {
                alert.style.display = 'none';
            }, 150);
        }, 3000);
    }

    closeModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) {
            modal.hide();
        }
    }

    resetForm(formId) {
        document.getElementById(formId).reset();
    }
}

// Global functions
function refreshData() {
    searchManager.refreshData();
}

function showHelp() {
    searchManager.showHelp();
}

function downloadConfig(type) {
    searchManager.downloadConfig(type);
}

function uploadConfig(type) {
    searchManager.uploadConfig(type);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    searchManager = new AzureSearchManager();
});
